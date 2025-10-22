"""Development Data Generator

Generate dummy browser data files for testing.
"""

import os
import random
from pathlib import Path
from loguru import logger

from privacy_eraser.config import (
    TEST_DATA_DIR,
    DEV_FILE_COUNTS,
    DEV_FILE_SIZE_MIN,
    DEV_FILE_SIZE_MAX,
)


# ═══════════════════════════════════════════════════════════
# Browser Directory Structures
# ═══════════════════════════════════════════════════════════

BROWSER_STRUCTURES = {
    "Chrome": {
        "paths": [
            "Cache/f_{:06d}",
            "Cache/data_{:d}",
            "Code Cache/js/index-dir/the-real-index",
            "GPUCache/data_{:d}",
            "Cookies",
            "History",
            "Login Data",
            "Web Data",
        ]
    },
    "Firefox": {
        "paths": [
            "cache2/entries/{:08X}",
            "cookies.sqlite",
            "places.sqlite",
            "formhistory.sqlite",
            "logins.json",
        ]
    },
    "Edge": {
        "paths": [
            "Cache/f_{:06d}",
            "GPUCache/data_{:d}",
            "Cookies",
            "History",
        ]
    },
    "Brave": {
        "paths": [
            "Cache/f_{:06d}",
            "GPUCache/data_{:d}",
            "Cookies",
            "History",
        ]
    },
    "Opera": {
        "paths": [
            "Cache/f_{:06d}",
            "GPUCache/data_{:d}",
            "Cookies",
            "History",
        ]
    },
    "Whale": {
        "paths": [
            "Cache/f_{:06d}",
            "GPUCache/data_{:d}",
            "Cookies",
            "History",
        ]
    },
    "Safari": {
        "paths": [
            "Cache.db",
            "Cookies/Cookies.binarycookies",
            "History.db",
        ]
    },
}


# ═══════════════════════════════════════════════════════════
# File Generation Functions
# ═══════════════════════════════════════════════════════════


def generate_random_file(file_path: Path, min_size: int, max_size: int):
    """Generate a random binary file"""
    size = random.randint(min_size, max_size)

    # Create parent directory
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Write random data
    with open(file_path, "wb") as f:
        # Write in chunks for large files
        remaining = size
        chunk_size = 8192

        while remaining > 0:
            current_chunk = min(chunk_size, remaining)
            f.write(os.urandom(current_chunk))
            remaining -= current_chunk


def generate_browser_files(browser_name: str, count_range: tuple[int, int]) -> int:
    """Generate dummy files for a specific browser

    Returns:
        Number of files generated
    """

    if browser_name not in BROWSER_STRUCTURES:
        logger.warning(f"Unknown browser: {browser_name}")
        return 0

    browser_dir = TEST_DATA_DIR / browser_name.lower()
    structure = BROWSER_STRUCTURES[browser_name]
    paths = structure["paths"]

    # Determine file count
    min_count, max_count = count_range
    total_files = random.randint(min_count, max_count)

    generated = 0
    while generated < total_files:
        # Pick random path template
        path_template = random.choice(paths)

        # Format with random number if needed
        try:
            if "{" in path_template:
                path_str = path_template.format(generated)
            else:
                # For non-template paths, add suffix if already exists
                path_str = path_template
                if generated > 0:
                    path_str += f".{generated}"
        except Exception as e:
            logger.debug(f"Path format error: {e}")
            continue

        file_path = browser_dir / path_str

        # Generate file
        try:
            generate_random_file(file_path, DEV_FILE_SIZE_MIN, DEV_FILE_SIZE_MAX)
            generated += 1
        except Exception as e:
            logger.warning(f"Failed to generate {file_path}: {e}")

    return generated


def clean_test_data():
    """Remove existing test data"""
    if TEST_DATA_DIR.exists():
        import shutil
        shutil.rmtree(TEST_DATA_DIR, ignore_errors=True)


def check_test_data_exists() -> bool:
    """Check if test data already exists and is not empty"""
    if not TEST_DATA_DIR.exists():
        return False

    # Check if there are any files
    for browser_dir in TEST_DATA_DIR.iterdir():
        if browser_dir.is_dir():
            for file_path in browser_dir.rglob("*"):
                if file_path.is_file():
                    return True  # Found at least one file

    return False


def count_test_files(browser_name: str) -> int:
    """Count test files for a specific browser

    Args:
        browser_name: Browser name (e.g., "Chrome", "Firefox")

    Returns:
        Number of test files for the browser
    """
    browser_dir = TEST_DATA_DIR / browser_name.lower()

    if not browser_dir.exists():
        logger.debug(f"[DEV] Test data directory not found: {browser_dir}")
        return 0

    # Count all files in browser directory
    file_count = 0
    for file_path in browser_dir.rglob("*"):
        if file_path.is_file():
            file_count += 1

    return file_count


def generate_all_test_data(force: bool = False) -> dict:
    """Generate test data for all browsers

    Args:
        force: If True, regenerate even if data exists

    Returns:
        Dictionary with statistics
    """
    # Check if data already exists
    if not force and check_test_data_exists():
        logger.info("[DEV] Test data already exists, skipping generation")
        return {"skipped": True, "total_files": 0, "total_size_mb": 0}

    logger.info("[DEV] Generating test data...")

    # Clean existing data
    if force:
        clean_test_data()

    # Create test data directory
    TEST_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Generate files for each browser
    total_files = 0
    for browser_name, count_range in DEV_FILE_COUNTS.items():
        try:
            count = generate_browser_files(browser_name, count_range)
            total_files += count
            logger.info(f"  [OK] {browser_name}: {count} files")
        except Exception as e:
            logger.error(f"  [ERROR] {browser_name}: {e}")

    # Calculate total size
    total_size = 0
    for browser_dir in TEST_DATA_DIR.iterdir():
        if browser_dir.is_dir():
            for file_path in browser_dir.rglob("*"):
                if file_path.is_file():
                    total_size += file_path.stat().st_size

    total_size_mb = total_size / (1024 * 1024)

    logger.success(f"Generated {total_files} test files ({total_size_mb:.1f} MB)")

    return {
        "skipped": False,
        "total_files": total_files,
        "total_size_mb": total_size_mb,
    }
