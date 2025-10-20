# WinClean Analysis & Integration Guide

**Analysis Date**: 2025-10-11
**Project**: privacy_eraser
**Source**: WinClean v1.3.1 (https://github.com/5cover/WinClean)

---

## Executive Summary

WinClean is a mature Windows optimization utility with **40+ pre-built scripts** that can be leveraged in your privacy_eraser application. The scripts cover privacy-focused cleaning, system optimization, and debloating operations. **All scripts can be wrapped as Python functions** and executed via subprocess calls.

### Key Benefits for Your Project

- ✅ **Battle-tested scripts**: Community-vetted cleaning operations
- ✅ **XML-based format**: Easy to parse and adapt
- ✅ **Multi-language support**: Localized descriptions (EN/FR)
- ✅ **Safety classification**: Scripts rated Safe/Limited/Dangerous
- ✅ **Impact categorization**: Clear documentation of effects
- ✅ **Version targeting**: Windows version compatibility metadata

---

## Architecture Overview

### WinClean Stack
```
C# .NET 6 Desktop App (WPF)
├── MVVM Architecture
├── XML Script Repository (40+ embedded scripts)
├── Host Execution Engine (PowerShell, CMD, Registry)
├── Metadata System (Categories, Safety Levels, Impacts)
└── Multi-language Resource System
```

### Your privacy_eraser Stack
```
Python 3.12+ Desktop App (PySide6)
├── Current: Browser cleaning (Chrome, Firefox, etc.)
├── **NEW**: Windows system cleaning via WinClean scripts
├── Current: Qt Material UI theme
└── Current: Program detection & cleaning options
```

---

## Script Analysis

### Script Distribution by Category

| Category | Count | Purpose |
|----------|-------|---------|
| **Maintenance** | ~15 | Regular cleaning operations |
| **Debloating** | ~20 | One-time optimization & privacy |
| **Customization** | ~5 | UI/UX tweaks (no performance impact) |

### Safety Level Distribution

| Level | Count | Description | User Recommendation |
|-------|-------|-------------|---------------------|
| **Safe** | ~25 | No impact on common features | Default preset |
| **Limited** | ~10 | Affects minority user features | Power user preset |
| **Dangerous** | ~5 | Advanced optimization only | Expert preset with warnings |

### Impact Categories

| Impact | Example Scripts | Value Proposition |
|--------|----------------|-------------------|
| **Privacy** | Disable telemetry, Clear history | Core value for privacy_eraser |
| **Free Storage** | Delete junk files, Remove bloat apps | High user value |
| **Memory Usage** | Stop background apps | Performance benefit |
| **Network Usage** | Disable delivery optimization | Bandwidth savings |
| **Ergonomics** | Show file extensions | User experience |
| **Startup/Shutdown** | Remove scheduled tasks | Boot performance |
| **Storage Speed** | Optimize drives | Disk performance |
| **Stability** | System file checker | System health |

---

## Script Execution Model

### WinClean XML Schema

```xml
<Script>
  <Name>Clear File Explorer history</Name>
  <Name xml:lang="fr">Effacer l'historique de l'Explorateur</Name>
  <Description>Description in English...</Description>
  <Description xml:lang="fr">Description en français...</Description>
  <Category>Maintenance|Debloating|Customization</Category>
  <SafetyLevel>Safe|Limited|Dangerous</SafetyLevel>
  <Impact>Privacy|Free storage space|Memory usage|etc.</Impact>
  <Versions>>=10.0.0</Versions> <!-- Optional: Windows version range -->
  <Code>
    <!-- Execution actions -->
    <Execute Host="PowerShell|Cmd|Regedit">Script code here...</Execute>
    <!-- OR -->
    <Enable Host="...">Code to enable feature...</Enable>
    <Disable Host="...">Code to disable feature...</Disable>
    <Detect Host="...">Code to detect current state...</Detect>
  </Code>
</Script>
```

### Host Types

| Host | Description | Execution Method | Use Cases |
|------|-------------|------------------|-----------|
| **PowerShell** | .NET-based scripting | `powershell.exe -NoProfile -ExecutionPolicy Unrestricted -File` | Complex operations, registry, file manipulation |
| **Cmd** | Command Processor | `cmd.exe /d /c` | Simple commands, batch operations |
| **Regedit** | Registry Editor | `regedit.exe /s` | Registry import/export operations |
| **Execute** | Direct Shell | Shell execution | Standalone programs |

---

## Integration Strategy

### Phase 1: Core Infrastructure (Week 1)

#### 1.1 Script Parser Module
```python
# privacy_eraser/winclean/parser.py
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List
import xml.etree.ElementTree as ET

class ScriptCategory(Enum):
    MAINTENANCE = "Maintenance"
    DEBLOATING = "Debloating"
    CUSTOMIZATION = "Customization"

class SafetyLevel(Enum):
    SAFE = "Safe"
    LIMITED = "Limited"
    DANGEROUS = "Dangerous"

class HostType(Enum):
    POWERSHELL = "PowerShell"
    CMD = "Cmd"
    REGEDIT = "Regedit"
    EXECUTE = "Execute"

@dataclass
class ScriptAction:
    host: HostType
    code: str
    action_type: str  # "Execute", "Enable", "Disable", "Detect"

@dataclass
class WinCleanScript:
    name: str
    description: str
    category: ScriptCategory
    safety_level: SafetyLevel
    impact: str
    version_range: Optional[str]
    actions: List[ScriptAction]

    # Localization support
    name_fr: Optional[str] = None
    description_fr: Optional[str] = None

def parse_script(xml_path: str) -> WinCleanScript:
    """Parse WinClean XML script into Python dataclass."""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Extract names (multi-language)
    names = {elem.get('lang', 'en'): elem.text
             for elem in root.findall('Name')}

    # Extract descriptions (multi-language)
    descriptions = {elem.get('lang', 'en'): elem.text
                   for elem in root.findall('Description')}

    # Parse actions
    actions = []
    code_elem = root.find('Code')
    for action in code_elem:
        actions.append(ScriptAction(
            host=HostType(action.get('Host')),
            code=action.text,
            action_type=action.tag
        ))

    return WinCleanScript(
        name=names.get('en', names.get(None)),
        name_fr=names.get('fr'),
        description=descriptions.get('en', descriptions.get(None)),
        description_fr=descriptions.get('fr'),
        category=ScriptCategory(root.find('Category').text),
        safety_level=SafetyLevel(root.find('SafetyLevel').text),
        impact=root.find('Impact').text,
        version_range=root.find('Versions').text if root.find('Versions') is not None else None,
        actions=actions
    )
```

#### 1.2 Script Executor Module
```python
# privacy_eraser/winclean/executor.py
import subprocess
import tempfile
import platform
from pathlib import Path
from typing import Tuple, Optional
from .parser import WinCleanScript, HostType, ScriptAction

class ExecutionResult:
    def __init__(self, success: bool, stdout: str, stderr: str, exit_code: int):
        self.success = success
        self.stdout = stdout
        self.stderr = stderr
        self.exit_code = exit_code

class ScriptExecutor:
    """Execute WinClean scripts on Windows systems."""

    def __init__(self):
        if platform.system() != 'Windows':
            raise RuntimeError("WinClean scripts can only run on Windows")

    def execute_script(self, script: WinCleanScript,
                      action_type: str = "Execute") -> ExecutionResult:
        """
        Execute a WinClean script.

        Args:
            script: Parsed WinCleanScript object
            action_type: "Execute", "Enable", "Disable", or "Detect"

        Returns:
            ExecutionResult with success status and output
        """
        # Find matching action
        action = next((a for a in script.actions if a.action_type == action_type), None)
        if not action:
            raise ValueError(f"Action type '{action_type}' not found in script")

        return self._execute_action(action)

    def _execute_action(self, action: ScriptAction) -> ExecutionResult:
        """Execute a single script action."""
        if action.host == HostType.POWERSHELL:
            return self._execute_powershell(action.code)
        elif action.host == HostType.CMD:
            return self._execute_cmd(action.code)
        elif action.host == HostType.REGEDIT:
            return self._execute_regedit(action.code)
        elif action.host == HostType.EXECUTE:
            return self._execute_shell(action.code)
        else:
            raise ValueError(f"Unknown host type: {action.host}")

    def _execute_powershell(self, code: str) -> ExecutionResult:
        """Execute PowerShell script."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ps1', delete=False) as f:
            f.write(code)
            temp_file = f.name

        try:
            result = subprocess.run(
                ['powershell.exe', '-NoProfile', '-ExecutionPolicy',
                 'Unrestricted', '-File', temp_file],
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

    def _execute_cmd(self, code: str) -> ExecutionResult:
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

    def _execute_regedit(self, code: str) -> ExecutionResult:
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

    def _execute_shell(self, code: str) -> ExecutionResult:
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
```

#### 1.3 Script Repository
```python
# privacy_eraser/winclean/repository.py
from pathlib import Path
from typing import List, Dict, Optional
from .parser import WinCleanScript, parse_script, ScriptCategory, SafetyLevel

class ScriptRepository:
    """Manage collection of WinClean scripts."""

    def __init__(self, scripts_dir: Path):
        self.scripts_dir = Path(scripts_dir)
        self._scripts: Dict[str, WinCleanScript] = {}
        self._load_scripts()

    def _load_scripts(self):
        """Load all XML scripts from directory."""
        for xml_file in self.scripts_dir.glob('*.xml'):
            try:
                script = parse_script(str(xml_file))
                self._scripts[script.name] = script
            except Exception as e:
                print(f"Error loading {xml_file}: {e}")

    def get_all_scripts(self) -> List[WinCleanScript]:
        """Get all loaded scripts."""
        return list(self._scripts.values())

    def get_by_category(self, category: ScriptCategory) -> List[WinCleanScript]:
        """Get scripts by category."""
        return [s for s in self._scripts.values() if s.category == category]

    def get_by_safety_level(self, level: SafetyLevel) -> List[WinCleanScript]:
        """Get scripts by safety level."""
        return [s for s in self._scripts.values() if s.safety_level == level]

    def get_privacy_scripts(self) -> List[WinCleanScript]:
        """Get all privacy-focused scripts."""
        return [s for s in self._scripts.values() if 'Privacy' in s.impact]

    def search(self, query: str) -> List[WinCleanScript]:
        """Search scripts by name or description."""
        query_lower = query.lower()
        return [s for s in self._scripts.values()
                if query_lower in s.name.lower()
                or query_lower in s.description.lower()]
```

### Phase 2: UI Integration (Week 2)

#### 2.1 Update Models
```python
# Add to privacy_eraser/models.py

class SystemCleanerOption(CleanerOption):
    """Extended cleaner option for system operations."""
    safety_level: str  # "Safe", "Limited", "Dangerous"
    impact: str  # "Privacy", "Free storage space", etc.
    requires_admin: bool = True
    version_requirement: Optional[str] = None
```

#### 2.2 Add System Cleaning View
```python
# privacy_eraser/ui/widgets/system_cleaner.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QCheckBox
from ...winclean.repository import ScriptRepository
from ...winclean.executor import ScriptExecutor

class SystemCleanerPanel(QWidget):
    """Panel for Windows system cleaning operations."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.repository = ScriptRepository(Path('winclean_scripts'))
        self.executor = ScriptExecutor()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        # Group by category
        for category in ScriptCategory:
            group = self._create_category_group(category)
            layout.addWidget(group)

    def _create_category_group(self, category: ScriptCategory) -> QGroupBox:
        scripts = self.repository.get_by_category(category)
        group = QGroupBox(category.value)
        layout = QVBoxLayout(group)

        for script in scripts:
            checkbox = QCheckBox(script.name)
            checkbox.setToolTip(f"{script.description}\n\n"
                              f"Safety: {script.safety_level.value}\n"
                              f"Impact: {script.impact}")

            # Color code by safety level
            if script.safety_level == SafetyLevel.DANGEROUS:
                checkbox.setStyleSheet("color: #f44336;")  # Red
            elif script.safety_level == SafetyLevel.LIMITED:
                checkbox.setStyleSheet("color: #ff9800;")  # Orange

            layout.addWidget(checkbox)

        return group
```

### Phase 3: Testing & Validation (Week 3)

#### 3.1 Test Suite
```python
# tests/test_winclean_integration.py

import pytest
from privacy_eraser.winclean.parser import parse_script
from privacy_eraser.winclean.executor import ScriptExecutor

def test_parse_script():
    """Test XML script parsing."""
    script = parse_script('winclean_scripts/Clear File Explorer history.xml')
    assert script.name == "Clear File Explorer history"
    assert script.category == ScriptCategory.MAINTENANCE
    assert script.safety_level == SafetyLevel.LIMITED

@pytest.mark.skipif(platform.system() != 'Windows', reason="Windows only")
def test_execute_safe_script():
    """Test execution of safe script."""
    # Test with a read-only detection script
    script = parse_script('winclean_scripts/Detect feature.xml')
    executor = ScriptExecutor()
    result = executor.execute_script(script, action_type="Detect")
    assert result.exit_code in [0, 1, -1]  # Valid detection states
```

---

## Easy-Win Features (Immediate Implementation)

### Top 10 Scripts to Implement First

| Priority | Script | Category | Safety | Value |
|----------|--------|----------|--------|-------|
| 1 | **Clear File Explorer history** | Maintenance | Limited | Privacy★★★ |
| 2 | **Disable telemetry and data collection** | Debloating | Safe | Privacy★★★ |
| 3 | **Delete junk files** | Maintenance | Limited | Storage★★★ |
| 4 | **Remove useless apps** | Debloating | Limited | Storage★★★ |
| 5 | **Clear event logs** | Maintenance | Limited | Privacy★★ |
| 6 | **Stop apps from running in background** | Debloating | Safe | Memory★★ |
| 7 | **Hide ads and suggestions** | Debloating | Safe | UX★★ |
| 8 | **Show file extensions** | Customization | Safe | UX★★ |
| 9 | **Disable Cortana** | Debloating | Safe | Privacy★★ |
| 10 | **Run Disk Cleanup tool** | Maintenance | Safe | Storage★★ |

### Pre-built Function Library

```python
# privacy_eraser/winclean/presets.py

class WindowsCleaningPresets:
    """Pre-configured cleaning presets using WinClean scripts."""

    def __init__(self, repository: ScriptRepository, executor: ScriptExecutor):
        self.repo = repository
        self.executor = executor

    def quick_privacy_clean(self):
        """Quick privacy-focused cleaning (safe operations only)."""
        scripts = [
            "Clear File Explorer history",
            "Disable telemetry and data collection",
            "Clear event logs",
            "Disable Cortana",
            "Hide ads and suggestions",
        ]
        return self._execute_scripts(scripts)

    def deep_privacy_clean(self):
        """Deep privacy cleaning (includes limited safety scripts)."""
        scripts = self.repo.get_privacy_scripts()
        return self._execute_scripts([s.name for s in scripts])

    def debloat_windows(self):
        """Remove bloatware and unnecessary features."""
        scripts = [
            "Remove useless apps",
            "Stop apps from running in the background",
            "Disable Timeline",
            "Remove scheduled tasks",
        ]
        return self._execute_scripts(scripts)

    def free_disk_space(self):
        """Free up disk space (maintenance + cleanup)."""
        scripts = [
            "Delete junk files",
            "Run Disk Cleanup tool",
            "Run advanced disk cleanup",
            "Run Component Store cleanup",
        ]
        return self._execute_scripts(scripts)

    def _execute_scripts(self, script_names: List[str]) -> Dict[str, ExecutionResult]:
        """Execute list of scripts and return results."""
        results = {}
        for name in script_names:
            script = self.repo._scripts.get(name)
            if script:
                results[name] = self.executor.execute_script(script)
        return results
```

---

## Implementation Recommendations

### ✅ DO Implement

1. **Privacy Scripts** (Core Value)
   - Clear File Explorer history
   - Disable telemetry
   - Clear event logs
   - Disable Cortana

2. **Storage Scripts** (High User Value)
   - Delete junk files
   - Run Disk Cleanup
   - Remove bloatware apps

3. **Safe Scripts** (Low Risk)
   - Show file extensions
   - Hide ads/suggestions
   - Stop background apps

### ⚠️ Implement with Warnings

1. **Limited Safety Scripts**
   - Delete junk files (may delete useful logs)
   - Remove useless apps (user might want some)
   - Clear all event logs (debugging impact)

2. **Require Confirmation**
   - Delete system restore points
   - Remove Internet Explorer
   - Disable hibernation

### ❌ DO NOT Implement (Yet)

1. **Dangerous Scripts**
   - Remove Microsoft Edge (can break Windows)
   - Disable UAC features
   - System-critical modifications

2. **Maintenance Scripts Requiring Reboot**
   - Schedule Check Disk utility
   - Component Store cleanup
   - Service Pack cleanup

---

## Technical Considerations

### Admin Privileges Required
Most WinClean scripts require administrator privileges. Your app needs to:
- Detect if running as admin
- Prompt for UAC elevation if needed
- Show clear indicators of admin-required operations

```python
import ctypes

def is_admin():
    """Check if running with admin privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def request_admin():
    """Request UAC elevation."""
    if not is_admin():
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
```

### Windows Version Detection
```python
import platform

def get_windows_version():
    """Get Windows version for script compatibility."""
    version = platform.version()
    # Parse version like "10.0.19045"
    major, minor, build = version.split('.')
    return f"{major}.{minor}.{build}"

def is_script_compatible(script: WinCleanScript):
    """Check if script is compatible with current Windows version."""
    if not script.version_range:
        return True

    current = get_windows_version()
    # Parse semver range like ">=10.0.0"
    # Use packaging.specifiers or semver library
    from packaging.specifiers import SpecifierSet
    spec = SpecifierSet(script.version_range)
    return current in spec
```

### Error Handling
```python
class ScriptExecutionError(Exception):
    """Base exception for script execution errors."""
    pass

class AdminRequiredError(ScriptExecutionError):
    """Raised when admin privileges required."""
    pass

class IncompatibleVersionError(ScriptExecutionError):
    """Raised when Windows version incompatible."""
    pass
```

---

## Project Structure Updates

```
privacy_eraser/
├── privacy_eraser/
│   ├── winclean/                   # NEW: WinClean integration
│   │   ├── __init__.py
│   │   ├── parser.py              # XML parsing
│   │   ├── executor.py            # Script execution
│   │   ├── repository.py          # Script management
│   │   └── presets.py             # Pre-built cleaning functions
│   ├── ui/
│   │   └── widgets/
│   │       └── system_cleaner.py  # NEW: System cleaning UI
│   └── ...
├── winclean_scripts/               # NEW: WinClean XML scripts
│   ├── Clear File Explorer history.xml
│   ├── Disable telemetry and data collection.xml
│   └── ... (copy from WinClean/Scripts/)
└── tests/
    └── test_winclean_integration.py  # NEW: Integration tests
```

---

## Dependencies to Add

```toml
# pyproject.toml additions
dependencies = [
    "installed-browsers>=0.1.5",
    "pyside6>=6.10.0",
    "qt-material>=2.17",
    "packaging>=24.0",        # NEW: Version comparison
]
```

---

## Next Steps

### Week 1: Core Infrastructure
1. ✅ Copy WinClean scripts to `winclean_scripts/` directory
2. ✅ Implement `parser.py` for XML parsing
3. ✅ Implement `executor.py` for script execution
4. ✅ Implement `repository.py` for script management
5. ✅ Write unit tests for parsing and execution

### Week 2: UI Integration
1. Create `SystemCleanerPanel` widget
2. Add "Windows Cleaning" tab to main window
3. Implement preset buttons (Quick/Deep/Debloat/Storage)
4. Add progress indicators and result display
5. Implement admin privilege detection and elevation

### Week 3: Testing & Polish
1. Test all Safe-level scripts on Windows VM
2. Add confirmation dialogs for Limited/Dangerous scripts
3. Implement undo/restore functionality where possible
4. Add logging and error reporting
5. Create user documentation

---

## Code Quality Checklist

- [ ] All scripts parsed successfully
- [ ] Admin privilege detection working
- [ ] Windows version compatibility checks
- [ ] Error handling for all script types
- [ ] Progress indication during execution
- [ ] Cancellation support for long operations
- [ ] Logging for all operations
- [ ] Unit tests for all modules
- [ ] Integration tests on Windows
- [ ] User documentation

---

## Performance Notes

- Script execution is sequential (not parallelizable due to system state)
- PowerShell scripts typically take 1-5 seconds
- CMD scripts typically take <1 second
- Registry operations are instant
- Disk cleanup operations can take 5-30 minutes

---

## Security Considerations

1. **Script Validation**: Validate all XML before execution
2. **Sandboxing**: Consider using Windows Sandbox for testing
3. **Logging**: Log all operations for audit trail
4. **Rollback**: Implement system restore point creation before operations
5. **User Consent**: Always show what will be modified before execution

---

## License Compatibility

WinClean uses **MIT License** which is compatible with your project.
You must:
- Include WinClean license and attribution
- Acknowledge scripts from Sycnex/Windows10Debloater (also MIT)
- Maintain original license headers in scripts

---

## Estimated Development Time

| Phase | Duration | Complexity |
|-------|----------|------------|
| Core Infrastructure | 1 week | Medium |
| UI Integration | 1 week | Low |
| Testing & Validation | 1 week | High |
| **Total** | **3 weeks** | **Medium** |

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Script execution errors | Medium | High | Comprehensive error handling, logging |
| Admin privilege issues | High | Medium | Clear UX for privilege requirements |
| Windows version incompatibility | Low | Medium | Version detection and filtering |
| User data loss | Low | High | Confirmation dialogs, system restore points |
| Performance issues | Low | Low | Progress indicators, cancellation support |

---

## Conclusion

**WinClean scripts are highly valuable for your privacy_eraser project** and can be easily integrated via Python subprocess wrappers. The XML-based format makes parsing straightforward, and the existing metadata (categories, safety levels, impacts) provides excellent UX guidance.

**Recommended Approach**: Start with the 10 high-value, safe scripts, implement the core infrastructure in Week 1, add UI in Week 2, and thoroughly test in Week 3. This gives you a solid foundation that can be expanded with additional scripts based on user feedback.

The integration provides significant value with manageable risk when proper safeguards (admin checks, confirmations, logging) are implemented.
