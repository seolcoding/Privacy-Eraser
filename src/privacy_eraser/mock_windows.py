"""Mock Windows-specific functionality for macOS/Linux development.

This module provides fake data and stub implementations for Windows-specific
features, allowing GUI development and testing on non-Windows platforms.

Usage:
    Only imported when os.name != "nt"
    Provides mock browser detection, registry operations, and cleaning results
"""

from __future__ import annotations

import os
import random
from typing import Iterator


# Mock browser detection data
MOCK_BROWSERS = [
    {
        "name": "Google Chrome",
        "icon": "C",
        "color": "#4285F4",
        "present": "yes",
        "running": "no",
        "cache_size": "234 MB",
        "cookies": "1,245",
        "user_data_path": "/mock/path/Chrome/User Data/Default",
    },
    {
        "name": "Microsoft Edge",
        "icon": "E",
        "color": "#0078D7",
        "present": "yes",
        "running": "no",
        "cache_size": "156 MB",
        "cookies": "892",
        "user_data_path": "/mock/path/Edge/User Data/Default",
    },
    {
        "name": "Mozilla Firefox",
        "icon": "F",
        "color": "#FF7139",
        "present": "yes",
        "running": "no",
        "cache_size": "89 MB",
        "cookies": "543",
        "user_data_path": "/mock/path/Firefox/Profiles/default",
    },
    {
        "name": "Brave",
        "icon": "B",
        "color": "#FB542B",
        "present": "yes",
        "running": "no",
        "cache_size": "45 MB",
        "cookies": "234",
        "user_data_path": "/mock/path/Brave/User Data/Default",
    },
    {
        "name": "Opera",
        "icon": "O",
        "color": "#FF1B2D",
        "present": "no",
        "running": "no",
        "cache_size": "N/A",
        "cookies": "N/A",
        "user_data_path": "",
    },
    {
        "name": "Naver Whale",
        "icon": "W",
        "color": "#1EC800",
        "present": "yes",
        "running": "no",
        "cache_size": "67 MB",
        "cookies": "456",
        "user_data_path": "/mock/path/Whale/User Data/Default",
    },
]


# Mock cleaner options data
MOCK_CLEANER_OPTIONS = [
    {
        "id": "cache",
        "label": "Cache",
        "description": "Temporary files that speed up browsing but take up space",
        "icon": "🗂️",
        "size": "234 MB",
        "file_count": "3,456",
        "last_cleaned": "Never",
        "warning": None,
    },
    {
        "id": "cookies",
        "label": "Cookies",
        "description": "Small files that websites use to remember your preferences",
        "icon": "🍪",
        "size": "12 MB",
        "file_count": "1,245",
        "last_cleaned": "2 days ago",
        "warning": None,
    },
    {
        "id": "history",
        "label": "History",
        "description": "Record of websites you've visited",
        "icon": "📜",
        "size": "8 MB",
        "file_count": "234",
        "last_cleaned": "1 week ago",
        "warning": None,
    },
    {
        "id": "session",
        "label": "Session & Tabs",
        "description": "Currently open tabs and windows (you'll lose unsaved work)",
        "icon": "📑",
        "size": "2 MB",
        "file_count": "45",
        "last_cleaned": "Never",
        "warning": "⚠️ This will close all open tabs and windows",
    },
    {
        "id": "passwords",
        "label": "Saved Passwords",
        "description": "Stored login credentials (DANGEROUS - cannot be recovered)",
        "icon": "🔑",
        "size": "500 KB",
        "file_count": "12",
        "last_cleaned": "Never",
        "warning": "⚠️ DESTRUCTIVE: Passwords cannot be recovered after deletion",
    },
    {
        "id": "autofill",
        "label": "Autofill Data",
        "description": "Saved form data like addresses and credit cards",
        "icon": "💳",
        "size": "1 MB",
        "file_count": "23",
        "last_cleaned": "Never",
        "warning": "⚠️ This will delete saved addresses and payment methods",
    },
]


class MockWinreg:
    """Mock Windows registry module."""

    HKEY_CURRENT_USER = 0x80000001
    HKEY_LOCAL_MACHINE = 0x80000002
    HKEY_CLASSES_ROOT = 0x80000000
    HKEY_USERS = 0x80000003

    @staticmethod
    def OpenKey(*args, **kwargs):
        """Mock registry key open - always succeeds for mock browsers."""
        return None

    @staticmethod
    def CloseKey(*args, **kwargs):
        """Mock registry key close."""
        pass


def mock_registry_key_exists(full_key: str) -> bool:
    """Mock registry key existence check.

    Returns True for Chrome, Edge, Firefox, Brave, Whale.
    Returns False for Opera (to simulate "not installed").
    """
    key_lower = full_key.lower()

    # Chrome
    if "google\\chrome" in key_lower or "chromium" in key_lower:
        return True

    # Edge
    if "microsoft\\edge" in key_lower:
        return True

    # Firefox
    if "mozilla\\firefox" in key_lower:
        return True

    # Brave
    if "bravesoftware\\brave" in key_lower:
        return True

    # Whale
    if "naver\\whale" in key_lower:
        return True

    # Opera - simulate not installed
    if "opera" in key_lower:
        return False

    # Default: random true/false
    return random.choice([True, False])


def mock_detect_file_glob(path_pattern: str) -> bool:
    """Mock file detection via glob patterns.

    Returns True for known browser paths, False for Opera.
    """
    pattern_lower = path_pattern.lower()

    # Chrome/Chromium-based
    if "chrome" in pattern_lower or "chromium" in pattern_lower:
        return True

    # Edge
    if "edge" in pattern_lower:
        return True

    # Firefox
    if "firefox" in pattern_lower:
        return True

    # Brave
    if "brave" in pattern_lower:
        return True

    # Whale
    if "whale" in pattern_lower:
        return True

    # Opera - simulate not installed
    if "opera" in pattern_lower:
        return False

    return False


def mock_is_process_running(exename: str, same_user: bool = True) -> bool:
    """Mock process detection.

    Always returns False (no browsers running) for UI testing.
    """
    return False


def mock_safe_delete(path: str) -> tuple[bool, int]:
    """Mock file deletion.

    Returns:
        (success: bool, bytes_deleted: int)
    """
    # Simulate random file sizes
    mock_size = random.randint(1024, 1024 * 1024 * 10)  # 1KB to 10MB
    return (True, mock_size)


def mock_get_file_size(path: str) -> int:
    """Mock file size calculation."""
    return random.randint(1024, 1024 * 1024 * 50)  # 1KB to 50MB


def mock_iter_search_files(
    path: str,
    search_type: str = "file",
    recurse: bool = False,
) -> Iterator[str]:
    """Mock file search iterator.

    Yields fake file paths for UI preview testing.
    """
    # Generate 5-20 fake files
    count = random.randint(5, 20)

    for i in range(count):
        # Generate realistic-looking cache/cookie file names
        if "cache" in path.lower():
            yield f"/mock/path/Cache/f_{i:06d}"
        elif "cookie" in path.lower():
            yield f"/mock/path/Cookies/cookie_{i:03d}"
        elif "history" in path.lower():
            yield f"/mock/path/History/history_{i:03d}.db"
        else:
            yield f"/mock/path/data_{i:03d}"


def mock_execute_cleaning(option_id: str, browser_name: str) -> dict:
    """Mock cleaning execution.

    Returns:
        {
            "success": bool,
            "files_deleted": int,
            "bytes_deleted": int,
            "errors": list[str],
        }
    """
    # Simulate realistic cleaning results
    files_deleted = random.randint(10, 500)
    bytes_deleted = random.randint(1024 * 1024, 1024 * 1024 * 200)  # 1MB to 200MB

    # Simulate occasional errors (10% chance)
    errors = []
    if random.random() < 0.1:
        errors.append(f"Permission denied: /mock/path/locked_file.dat")

    return {
        "success": len(errors) == 0,
        "files_deleted": files_deleted,
        "bytes_deleted": bytes_deleted,
        "errors": errors,
    }


def get_mock_browsers() -> list[dict]:
    """Get list of mock browser data for UI testing."""
    return MOCK_BROWSERS.copy()


def get_mock_cleaner_options(browser_name: str) -> list[dict]:
    """Get list of mock cleaner options for a browser."""
    # Add browser-specific variations
    options = MOCK_CLEANER_OPTIONS.copy()

    # Randomize sizes slightly per browser
    for opt in options:
        if opt["size"] != "N/A":
            base_mb = int(opt["size"].split()[0])
            new_mb = base_mb + random.randint(-20, 20)
            opt["size"] = f"{max(1, new_mb)} MB"

    return options


# Export mock data and functions
__all__ = [
    "MockWinreg",
    "mock_registry_key_exists",
    "mock_detect_file_glob",
    "mock_is_process_running",
    "mock_safe_delete",
    "mock_get_file_size",
    "mock_iter_search_files",
    "mock_execute_cleaning",
    "get_mock_browsers",
    "get_mock_cleaner_options",
    "MOCK_BROWSERS",
    "MOCK_CLEANER_OPTIONS",
]
