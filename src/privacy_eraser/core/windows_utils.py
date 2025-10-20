"""Windows-specific utilities adapted from BleachBit Windows.py

Provides Windows-specific operations:
- Registry key operations
- Locked file deletion (reboot-pending)
- Process detection
- Windows path operations
"""

from __future__ import annotations

import logging
import os
import sys
from typing import Any, Iterator

logger = logging.getLogger(__name__)

# Windows-only imports
if sys.platform == "win32":
    import winreg
    import psutil
    try:
        import win32api
        import win32file
        HAS_WIN32 = True
    except ImportError:
        HAS_WIN32 = False
        logger.warning("pywin32 not available - some features disabled")
else:
    winreg = None  # type: ignore
    HAS_WIN32 = False


# Registry hive mapping
REGISTRY_HIVES = {
    "HKCR": winreg.HKEY_CLASSES_ROOT if winreg else None,
    "HKCU": winreg.HKEY_CURRENT_USER if winreg else None,
    "HKLM": winreg.HKEY_LOCAL_MACHINE if winreg else None,
    "HKU": winreg.HKEY_USERS if winreg else None,
}


def parse_registry_key(full_key: str) -> tuple[Any, str]:
    """Parse registry key string like 'HKCU\\Software\\App' into (hive, subkey)."""
    if not winreg:
        raise RuntimeError("Registry operations not available on this platform")
    
    parts = full_key.split("\\\\", 1)
    if len(parts) != 2:
        raise ValueError(f"Invalid registry key format: {full_key}")
    
    hive_name, subkey = parts
    hive = REGISTRY_HIVES.get(hive_name.upper())
    if hive is None:
        raise ValueError(f"Unknown registry hive: {hive_name}")
    
    return hive, subkey


def registry_key_exists(full_key: str) -> bool:
    """Check if registry key exists."""
    if not winreg:
        return False
    
    try:
        hive, subkey = parse_registry_key(full_key)
        key = winreg.OpenKey(hive, subkey, 0, winreg.KEY_READ)
        winreg.CloseKey(key)
        return True
    except FileNotFoundError:
        return False
    except Exception as e:
        logger.debug(f"Error checking registry key {full_key}: {e}")
        return False


def read_registry_value(full_key: str, value_name: str) -> str | None:
    """Read a registry value."""
    if not winreg:
        return None
    
    try:
        hive, subkey = parse_registry_key(full_key)
        key = winreg.OpenKey(hive, subkey, 0, winreg.KEY_READ)
        value, _type = winreg.QueryValueEx(key, value_name)
        winreg.CloseKey(key)
        return str(value) if value else None
    except Exception as e:
        logger.debug(f"Error reading registry {full_key}\\{value_name}: {e}")
        return None


def delete_registry_key(full_key: str) -> bool:
    """Delete a registry key.
    
    Returns True if deleted, False otherwise.
    """
    if not winreg:
        return False
    
    try:
        hive, subkey = parse_registry_key(full_key)
        winreg.DeleteKey(hive, subkey)
        logger.info(f"Deleted registry key: {full_key}")
        return True
    except FileNotFoundError:
        return False
    except PermissionError as e:
        logger.warning(f"Permission denied deleting registry key {full_key}: {e}")
        return False
    except Exception as e:
        logger.error(f"Error deleting registry key {full_key}: {e}")
        return False


def delete_registry_value(full_key: str, value_name: str) -> bool:
    """Delete a registry value.
    
    Returns True if deleted, False otherwise.
    """
    if not winreg:
        return False
    
    try:
        hive, subkey = parse_registry_key(full_key)
        key = winreg.OpenKey(hive, subkey, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, value_name)
        winreg.CloseKey(key)
        logger.info(f"Deleted registry value: {full_key}\\{value_name}")
        return True
    except FileNotFoundError:
        return False
    except PermissionError as e:
        logger.warning(f"Permission denied deleting registry value {full_key}\\{value_name}: {e}")
        return False
    except Exception as e:
        logger.error(f"Error deleting registry value {full_key}\\{value_name}: {e}")
        return False


def is_process_running(process_name: str, same_user: bool = True) -> bool:
    """Check if a process is running.
    
    Args:
        process_name: Name of the executable (e.g., 'chrome.exe')
        same_user: If True, only check processes running as current user
    """
    if not sys.platform == "win32":
        return False
    
    target_name = process_name.lower()
    try:
        current_user = psutil.Process().username().lower() if same_user else None
    except Exception:
        current_user = None
    
    for proc in psutil.process_iter(['name', 'username']):
        try:
            proc_info = proc.info
            if proc_info['name'] and proc_info['name'].lower() == target_name:
                if not same_user:
                    return True
                if current_user and proc_info.get('username', '').lower() == current_user:
                    return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    return False


def delete_locked_file(path: str) -> bool:
    """Mark a locked file for deletion on reboot.
    
    Uses Windows MoveFileEx with MOVEFILE_DELAY_UNTIL_REBOOT flag.
    Returns True if scheduled, False otherwise.
    """
    if not HAS_WIN32:
        logger.warning("pywin32 not available - cannot schedule locked file deletion")
        return False
    
    try:
        # MoveFileEx with NULL destination and MOVEFILE_DELAY_UNTIL_REBOOT
        # schedules file deletion on next reboot
        win32file.MoveFileEx(path, None, win32file.MOVEFILE_DELAY_UNTIL_REBOOT)
        logger.info(f"Scheduled for deletion on reboot: {path}")
        return True
    except Exception as e:
        logger.error(f"Error scheduling locked file deletion {path}: {e}")
        return False


def expand_windows_path_vars(path_pattern: str) -> Iterator[str]:
    """Expand Windows environment variables including W6432 variants.
    
    BleachBit/Winapp2 convention: expand ProgramFiles to both 
    %ProgramFiles% and %ProgramW6432% for 32/64-bit compatibility.
    """
    # Standard expansion
    yield os.path.expandvars(path_pattern)
    
    # W6432 variants for 32-bit compatibility
    if "%ProgramFiles%" in path_pattern:
        yield os.path.expandvars(path_pattern.replace("%ProgramFiles%", "%ProgramW6432%"))
    if "%CommonProgramFiles%" in path_pattern:
        yield os.path.expandvars(path_pattern.replace("%CommonProgramFiles%", "%CommonProgramW6432%"))

