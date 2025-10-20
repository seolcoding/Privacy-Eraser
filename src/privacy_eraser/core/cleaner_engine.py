"""Cleaner engine adapted from BleachBit Cleaner.py

Orchestrates cleaning operations:
- Load CleanerML files
- Load WinClean XML scripts
- Execute cleaning actions
- Report progress
- Handle errors gracefully
"""

from __future__ import annotations

import logging
import os
import platform
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Iterator

from . import file_utils

logger = logging.getLogger(__name__)


class ActionType(Enum):
    """Type of cleaning action."""
    DELETE = "delete"
    TRUNCATE = "truncate"
    REGISTRY_DELETE_KEY = "registry.delete_key"
    REGISTRY_DELETE_VALUE = "registry.delete_value"
    WINCLEAN_EXECUTE = "winclean.execute"


class SearchType(Enum):
    """Type of file search."""
    FILE = "file"  # Single file
    GLOB = "glob"  # Glob pattern
    WALK_FILES = "walk.files"  # Recursive files only
    WALK_ALL = "walk.all"  # Recursive files and dirs
    WALK_TOP = "walk.top"  # walk.all + parent dir itself


class WinCleanHost(Enum):
    """WinClean script execution host."""
    POWERSHELL = "PowerShell"
    CMD = "Cmd"
    REGEDIT = "Regedit"
    EXECUTE = "Execute"


class WinCleanCategory(Enum):
    """WinClean script category."""
    MAINTENANCE = "Maintenance"
    DEBLOATING = "Debloating"
    CUSTOMIZATION = "Customization"


class WinCleanSafetyLevel(Enum):
    """WinClean script safety level."""
    SAFE = "Safe"
    LIMITED = "Limited"
    DANGEROUS = "Dangerous"


@dataclass
class WinCleanScript:
    """Represents a WinClean XML script."""
    name: str
    description: str
    category: WinCleanCategory
    safety_level: WinCleanSafetyLevel
    impact: str
    version_range: str | None = None
    code: str = ""
    host: WinCleanHost = WinCleanHost.POWERSHELL
    name_fr: str | None = None
    description_fr: str | None = None


@dataclass
class ExecutionResult:
    """Result of script execution."""
    success: bool
    stdout: str
    stderr: str
    exit_code: int


@dataclass
class CleaningAction:
    """Represents a single cleaning action."""
    action_type: ActionType
    search_type: SearchType | None = None
    path: str = ""
    registry_key: str = ""
    registry_value: str = ""
    
    def preview(self) -> list[str]:
        """Preview what would be cleaned (don't actually delete)."""
        items: list[str] = []
        
        if self.action_type == ActionType.DELETE:
            if self.search_type == SearchType.FILE:
                for path in file_utils.expand_glob_pattern(self.path):
                    if os.path.lexists(path):
                        items.append(path)
                        
            elif self.search_type == SearchType.GLOB:
                items.extend(file_utils.expand_glob_pattern(self.path))
                
            elif self.search_type == SearchType.WALK_FILES:
                for path in file_utils.expand_glob_pattern(self.path):
                    if os.path.isdir(path):
                        items.extend(file_utils.walk_directory_files(path))
                    elif os.path.lexists(path):
                        items.append(path)
                        
            elif self.search_type == SearchType.WALK_ALL:
                for path in file_utils.expand_glob_pattern(self.path):
                    if os.path.isdir(path):
                        items.extend(file_utils.walk_directory_all(path))
                    elif os.path.lexists(path):
                        items.append(path)
                        
            elif self.search_type == SearchType.WALK_TOP:
                for path in file_utils.expand_glob_pattern(self.path):
                    if os.path.isdir(path):
                        items.extend(file_utils.walk_directory_all(path))
                        items.append(path)  # Include parent dir
                    elif os.path.lexists(path):
                        items.append(path)
                        
        elif self.action_type == ActionType.REGISTRY_DELETE_KEY:
            # Registry preview - just return the key path
            items.append(f"Registry: {self.registry_key}")
            
        elif self.action_type == ActionType.REGISTRY_DELETE_VALUE:
            items.append(f"Registry: {self.registry_key}\\{self.registry_value}")
        
        return sorted(set(items))
    
    def execute(self) -> tuple[int, int]:
        """Execute the cleaning action.
        
        Returns: (items_deleted, bytes_deleted)
        """
        items_deleted = 0
        bytes_deleted = 0
        
        if self.action_type == ActionType.DELETE:
            for path in self.preview():
                if path.startswith("Registry:"):
                    continue  # Skip registry placeholders
                success, size = file_utils.delete_file_simple(path)
                if success:
                    items_deleted += 1
                    bytes_deleted += size
                    
        elif self.action_type == ActionType.REGISTRY_DELETE_KEY:
            # Import here to avoid Windows dependency on other platforms
            if os.name == "nt":
                from . import windows_utils
                if windows_utils.delete_registry_key(self.registry_key):
                    items_deleted = 1
                    
        elif self.action_type == ActionType.REGISTRY_DELETE_VALUE:
            if os.name == "nt":
                from . import windows_utils
                if windows_utils.delete_registry_value(self.registry_key, self.registry_value):
                    items_deleted = 1
        
        return items_deleted, bytes_deleted


@dataclass
class CleanerOption:
    """Represents a cleaning option (e.g., 'Cache', 'Cookies')."""
    id: str
    label: str
    description: str
    warning: str | None = None
    actions: list[CleaningAction] = field(default_factory=list)
    
    def preview(self) -> list[str]:
        """Preview all items that would be cleaned."""
        all_items: list[str] = []
        for action in self.actions:
            all_items.extend(action.preview())
        return sorted(set(all_items))
    
    def execute(self, progress_callback: Callable[[str, int, int], None] | None = None) -> tuple[int, int]:
        """Execute all cleaning actions.
        
        Args:
            progress_callback: Optional callback(message, items_done, total_items)
            
        Returns: (total_items_deleted, total_bytes_deleted)
        """
        total_items = 0
        total_bytes = 0
        
        for i, action in enumerate(self.actions):
            if progress_callback:
                progress_callback(f"Cleaning {self.label}...", i, len(self.actions))
            
            try:
                items, size = action.execute()
                total_items += items
                total_bytes += size
            except Exception as e:
                logger.error(f"Error executing action in {self.id}: {e}")
                continue
        
        if progress_callback:
            progress_callback(f"Completed {self.label}", len(self.actions), len(self.actions))
        
        return total_items, total_bytes


@dataclass
class Cleaner:
    """Represents a cleaner (e.g., 'Chrome', 'Firefox')."""
    id: str
    name: str
    description: str
    options: dict[str, CleanerOption] = field(default_factory=dict)
    
    def get_option(self, option_id: str) -> CleanerOption | None:
        """Get a specific cleaning option."""
        return self.options.get(option_id)
    
    def preview_all(self) -> dict[str, list[str]]:
        """Preview all options.
        
        Returns: {option_id: [items]}
        """
        result: dict[str, list[str]] = {}
        for option_id, option in self.options.items():
            result[option_id] = option.preview()
        return result
    
    def execute_options(
        self, 
        option_ids: list[str],
        progress_callback: Callable[[str, int, int], None] | None = None
    ) -> tuple[int, int]:
        """Execute selected options.
        
        Returns: (total_items_deleted, total_bytes_deleted)
        """
        total_items = 0
        total_bytes = 0
        
        for option_id in option_ids:
            option = self.get_option(option_id)
            if not option:
                logger.warning(f"Option not found: {option_id}")
                continue
            
            try:
                items, size = option.execute(progress_callback)
                total_items += items
                total_bytes += size
                logger.info(f"Cleaned {option.label}: {items} items, {file_utils.format_bytes(size)}")
            except Exception as e:
                logger.error(f"Error cleaning {option.label}: {e}")
                continue
        
        return total_items, total_bytes


def parse_winclean_script(xml_path: str) -> WinCleanScript:
    """Parse a WinClean XML script into a WinCleanScript object."""
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # Extract names (multi-language)
        names = {}
        for name_elem in root.findall('Name'):
            lang = name_elem.get('xml:lang', 'en')
            names[lang] = name_elem.text or ""
        
        # Extract descriptions (multi-language)
        descriptions = {}
        for desc_elem in root.findall('Description'):
            lang = desc_elem.get('xml:lang', 'en')
            descriptions[lang] = desc_elem.text or ""
        
        # Extract metadata
        category = WinCleanCategory(root.find('Category').text)
        safety_level = WinCleanSafetyLevel(root.find('SafetyLevel').text)
        impact = root.find('Impact').text or ""
        version_range = root.find('Versions').text if root.find('Versions') is not None else None
        
        # Extract code
        code_elem = root.find('Code')
        host = WinCleanHost.POWERSHELL
        code = ""
        
        if code_elem is not None:
            # Find the Execute element
            execute_elem = code_elem.find('Execute')
            if execute_elem is not None:
                host_str = execute_elem.get('Host', 'PowerShell')
                try:
                    host = WinCleanHost(host_str)
                except ValueError:
                    host = WinCleanHost.POWERSHELL
                code = execute_elem.text or ""
        
        return WinCleanScript(
            name=names.get('en', names.get(None, "")),
            description=descriptions.get('en', descriptions.get(None, "")),
            category=category,
            safety_level=safety_level,
            impact=impact,
            version_range=version_range,
            code=code,
            host=host,
            name_fr=names.get('fr'),
            description_fr=descriptions.get('fr')
        )
        
    except Exception as e:
        logger.error(f"Error parsing WinClean script {xml_path}: {e}")
        raise


def load_winclean_scripts(scripts_dir: str | Path) -> list[WinCleanScript]:
    """Load all WinClean scripts from a directory."""
    scripts_dir = Path(scripts_dir)
    scripts = []
    
    if not scripts_dir.exists():
        logger.warning(f"WinClean scripts directory does not exist: {scripts_dir}")
        return scripts
    
    for xml_file in scripts_dir.glob("*.xml"):
        try:
            script = parse_winclean_script(str(xml_file))
            scripts.append(script)
            logger.debug(f"Loaded WinClean script: {script.name}")
        except Exception as e:
            logger.error(f"Failed to load WinClean script {xml_file}: {e}")
            continue
    
    logger.info(f"Loaded {len(scripts)} WinClean scripts from {scripts_dir}")
    return scripts


def execute_winclean_script(script: WinCleanScript) -> ExecutionResult:
    """Execute a WinClean script and return the result."""
    if platform.system() != 'Windows':
        return ExecutionResult(
            success=False,
            stdout="",
            stderr="WinClean scripts can only run on Windows",
            exit_code=-1
        )
    
    try:
        if script.host == WinCleanHost.POWERSHELL:
            return _execute_powershell(script.code)
        elif script.host == WinCleanHost.CMD:
            return _execute_cmd(script.code)
        elif script.host == WinCleanHost.REGEDIT:
            return _execute_regedit(script.code)
        elif script.host == WinCleanHost.EXECUTE:
            return _execute_shell(script.code)
        else:
            return ExecutionResult(
                success=False,
                stdout="",
                stderr=f"Unknown host type: {script.host}",
                exit_code=-1
            )
    except Exception as e:
        logger.error(f"Error executing WinClean script {script.name}: {e}")
        return ExecutionResult(
            success=False,
            stdout="",
            stderr=str(e),
            exit_code=-1
        )


def _execute_powershell(code: str) -> ExecutionResult:
    """Execute PowerShell script."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ps1', delete=False) as f:
        f.write(code)
        temp_file = f.name
    
    try:
        result = subprocess.run(
            ['powershell.exe', '-NoProfile', '-ExecutionPolicy', 'Unrestricted', '-File', temp_file],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        return ExecutionResult(
            success=result.returncode == 0,
            stdout=result.stdout,
            stderr=result.stderr,
            exit_code=result.returncode
        )
    finally:
        Path(temp_file).unlink(missing_ok=True)


def _execute_cmd(code: str) -> ExecutionResult:
    """Execute CMD batch commands."""
    result = subprocess.run(
        ['cmd.exe', '/d', '/c', code],
        capture_output=True,
        text=True,
        timeout=300
    )
    return ExecutionResult(
        success=result.returncode == 0,
        stdout=result.stdout,
        stderr=result.stderr,
        exit_code=result.returncode
    )


def _execute_regedit(code: str) -> ExecutionResult:
    """Execute registry import."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.reg', delete=False) as f:
        f.write(code)
        temp_file = f.name
    
    try:
        result = subprocess.run(
            ['regedit.exe', '/s', temp_file],
            capture_output=True,
            text=True,
            timeout=60
        )
        return ExecutionResult(
            success=result.returncode == 0,
            stdout=result.stdout,
            stderr=result.stderr,
            exit_code=result.returncode
        )
    finally:
        Path(temp_file).unlink(missing_ok=True)


def _execute_shell(code: str) -> ExecutionResult:
    """Execute direct shell command."""
    result = subprocess.run(
        code,
        shell=True,
        capture_output=True,
        text=True,
        timeout=300
    )
    return ExecutionResult(
        success=result.returncode == 0,
        stdout=result.stdout,
        stderr=result.stderr,
        exit_code=result.returncode
    )

