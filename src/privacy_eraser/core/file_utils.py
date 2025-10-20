"""File utilities adapted from BleachBit FileUtilities.py

Core file operations including:
- Safe file deletion
- Secure wiping (optional)
- Whitelist checking
- Size calculation
"""

from __future__ import annotations

import glob
import logging
import os
import shutil
import stat
from pathlib import Path
from typing import Iterator

logger = logging.getLogger(__name__)

# Whitelist patterns - files that should never be deleted
WHITELIST_PATTERNS = [
    # System critical
    "C:\\Windows\\System32\\*",
    "C:\\Windows\\SysWOW64\\*",
    "C:\\Windows\\WinSxS\\*",
    # Bootloader
    "C:\\Boot\\*",
    "C:\\bootmgr",
    "/boot/*",
    "/usr/bin/*",
    "/usr/sbin/*",
    "/bin/*",
    "/sbin/*",
]


def is_whitelisted(path: str) -> bool:
    """Check if path matches whitelist patterns."""
    try:
        normalized = os.path.normpath(os.path.abspath(path))
        for pattern in WHITELIST_PATTERNS:
            if glob.fnmatch.fnmatch(normalized.lower(), pattern.lower()):
                logger.warning(f"Whitelisted path skipped: {path}")
                return True
        return False
    except Exception as e:
        logger.error(f"Error checking whitelist for {path}: {e}")
        return True  # Err on side of caution


def get_file_size(path: str) -> int:
    """Get size of file or directory in bytes."""
    try:
        if os.path.isfile(path):
            return os.path.getsize(path)
        elif os.path.isdir(path):
            total = 0
            for dirpath, _dirnames, filenames in os.walk(path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        total += os.path.getsize(filepath)
                    except (OSError, FileNotFoundError):
                        continue
            return total
        return 0
    except Exception:
        return 0


def delete_file_simple(path: str) -> tuple[bool, int]:
    """Delete a single file.
    
    Returns: (success: bool, bytes_deleted: int)
    """
    if is_whitelisted(path):
        return False, 0
        
    try:
        if not os.path.lexists(path):
            return False, 0
            
        size = get_file_size(path)
        
        # Handle read-only files
        if os.path.isfile(path):
            try:
                os.chmod(path, stat.S_IWRITE | stat.S_IREAD)
            except Exception:
                pass
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path, ignore_errors=False)
        else:
            # Symlink or special file
            os.remove(path)
            
        logger.debug(f"Deleted: {path} ({size} bytes)")
        return True, size
        
    except PermissionError as e:
        logger.warning(f"Permission denied deleting {path}: {e}")
        return False, 0
    except Exception as e:
        logger.error(f"Error deleting {path}: {e}")
        return False, 0


def expand_glob_pattern(pattern: str) -> Iterator[str]:
    """Expand glob pattern to matching paths."""
    expanded = os.path.expanduser(os.path.expandvars(pattern))
    if os.name == "nt":
        expanded = os.path.normpath(expanded)
    
    # If pattern has glob chars, expand it
    if any(c in expanded for c in "*?[]"):
        yield from glob.iglob(expanded, recursive=True)
    else:
        # Direct path
        if os.path.lexists(expanded):
            yield expanded


def walk_directory_files(directory: str) -> Iterator[str]:
    """Recursively yield all files in directory."""
    try:
        for root, _dirs, files in os.walk(directory):
            for file in files:
                yield os.path.join(root, file)
    except Exception as e:
        logger.error(f"Error walking directory {directory}: {e}")


def walk_directory_all(directory: str) -> Iterator[str]:
    """Recursively yield all files and directories."""
    try:
        for root, dirs, files in os.walk(directory, topdown=False):
            for file in files:
                yield os.path.join(root, file)
            for dir_name in dirs:
                yield os.path.join(root, dir_name)
    except Exception as e:
        logger.error(f"Error walking directory {directory}: {e}")


def format_bytes(size: int) -> str:
    """Format bytes as human-readable string."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} PB"

