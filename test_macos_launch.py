#!/usr/bin/env python3
"""Quick test script to verify macOS mock data works.

Usage:
    uv run python test_macos_launch.py
"""

import os
import sys

# Ensure we're testing non-Windows mode
print(f"Platform: {sys.platform}")
print(f"os.name: {os.name}")
print(f"Mock mode: {os.name != 'nt'}")
print()

# Test imports
try:
    from src.privacy_eraser import mock_windows
    print("✅ mock_windows imported successfully")
except ImportError as e:
    print(f"❌ Failed to import mock_windows: {e}")
    sys.exit(1)

# Test mock browser data
try:
    browsers = mock_windows.get_mock_browsers()
    print(f"✅ Got {len(browsers)} mock browsers")
    for b in browsers:
        print(f"   - {b['name']}: {b['present']} (Cache: {b['cache_size']})")
except Exception as e:
    print(f"❌ Failed to get mock browsers: {e}")
    sys.exit(1)

print()

# Test mock cleaner options
try:
    options = mock_windows.get_mock_cleaner_options("Google Chrome")
    print(f"✅ Got {len(options)} mock cleaner options for Chrome")
    for opt in options[:3]:  # Show first 3
        print(f"   - {opt['label']}: {opt['size']} ({opt['file_count']} files)")
except Exception as e:
    print(f"❌ Failed to get mock options: {e}")
    sys.exit(1)

print()

# Test detection module with mocks
try:
    from src.privacy_eraser.detect_windows import (
        registry_key_exists,
        detect_file_glob,
        is_process_running_windows,
    )
    print("✅ detect_windows imported successfully")

    # Test mock registry
    chrome_reg = r"HKCU\Software\Google\Chrome"
    exists = registry_key_exists(chrome_reg)
    print(f"✅ Mock registry check: {chrome_reg} = {exists}")

    # Test mock file detection
    chrome_path = r"%LOCALAPPDATA%\Google\Chrome\User Data"
    found = detect_file_glob(chrome_path)
    print(f"✅ Mock file glob: {chrome_path} = {found}")

    # Test mock process detection
    running = is_process_running_windows("chrome.exe")
    print(f"✅ Mock process check: chrome.exe running = {running}")

except Exception as e:
    print(f"❌ Failed to test detection with mocks: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test GUI integration
try:
    from src.privacy_eraser.gui_integration import run_scan, load_cleaner_options
    print("✅ gui_integration imported successfully")

    # Test scan (should use mocks on macOS)
    results = run_scan()
    print(f"✅ Scan returned {len(results)} programs")
    for prog in results[:3]:  # Show first 3
        print(f"   - {prog['name']}: present={prog.get('present', 'N/A')}")

    # Test load cleaner options (should use mocks on macOS)
    opts = load_cleaner_options("Google Chrome", "/fake/path")
    print(f"✅ load_cleaner_options returned {len(opts)} options")

except Exception as e:
    print(f"❌ Failed to test GUI integration: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("=" * 60)
print("✅ All mock functionality tests passed!")
print("=" * 60)
print()
print("You can now run the GUI with:")
print("  uv run privacy_eraser")
print()
print("Expected behavior:")
print("1. GUI launches successfully")
print("2. Click 'Scan Programs' shows 6 mock browsers")
print("3. Select browser shows mock cleaner options")
print("4. All UI interactions work (Easy Mode + Advanced Mode)")
print("5. Preview/Clean operations are simulated")
