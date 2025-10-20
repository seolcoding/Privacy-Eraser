"""Core privacy deletion logic adapted from BleachBit.

This module provides the core cleaning functionality:
- File and directory operations
- Registry operations (Windows)
- Secure deletion
- CleanerML processing
"""

from __future__ import annotations

__all__ = [
    "file_utils",
    "windows_utils",
    "cleaner_engine",
]

