#!/usr/bin/env python3
"""
Privacy Eraser 구현 검증 테스트 스크립트
"""

import sys
import os

# 프로젝트 루트 경로 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """기본 모듈 임포트 테스트"""
    print("Testing basic imports...")

    try:
        from privacy_eraser.daemon import get_daemon
        print("✓ daemon module imported")
    except Exception as e:
        print(f"✗ daemon import failed: {e}")
        return False

    try:
        from privacy_eraser.settings_db import get_database_manager
        print("✓ settings_db module imported")
    except Exception as e:
        print(f"✗ settings_db import failed: {e}")
        return False

    try:
        from privacy_eraser.scheduler import get_scheduler, ScheduleType, ScheduleConfig
        print("✓ scheduler module imported")
    except Exception as e:
        print(f"✗ scheduler import failed: {e}")
        return False

    try:
        from privacy_eraser.app_state import app_state
        print("✓ app_state module imported")
    except Exception as e:
        print(f"✗ app_state import failed: {e}")
        return False

    return True

def test_daemon():
    """데몬 초기화 테스트"""
    print("\nTesting daemon initialization...")

    try:
        from privacy_eraser.daemon import get_daemon
        daemon = get_daemon()
        print("✓ Daemon created successfully")
        return True
    except Exception as e:
        print(f"✗ Daemon creation failed: {e}")
        return False

def test_database():
    """데이터베이스 초기화 테스트"""
    print("\nTesting database initialization...")

    try:
        from privacy_eraser.settings_db import get_database_manager
        db = get_database_manager()

        info = db.get_database_info()
        print(f"✓ Database initialized: {info['database_path']}")
        print(f"  Size: {info['database_size_bytes']} bytes")
        print(f"  Tables: {info['table_counts']}")

        return True
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")
        return False

def test_scheduler():
    """스케줄러 초기화 테스트"""
    print("\nTesting scheduler initialization...")

    try:
        from privacy_eraser.daemon import DaemonSignals
        from privacy_eraser.scheduler import get_scheduler

        signals = DaemonSignals()
        scheduler = get_scheduler(signals)

        # 기본 프리셋 확인
        presets = scheduler.get_builtin_presets()
        print(f"✓ Scheduler initialized with {len(presets)} builtin presets")

        return True
    except Exception as e:
        print(f"✗ Scheduler initialization failed: {e}")
        return False

def test_gui():
    """GUI 모듈 테스트"""
    print("\nTesting GUI modules...")

    try:
        from privacy_eraser.gui import create_main_window
        window = create_main_window()
        print("✓ Main window created successfully")
        return True
    except Exception as e:
        print(f"✗ GUI creation failed: {e}")
        return False

def main():
    """메인 테스트 함수"""
    print("Privacy Eraser Implementation Validation")
    print("=" * 50)

    tests = [
        ("Basic Imports", test_imports),
        ("Daemon System", test_daemon),
        ("Database System", test_database),
        ("Scheduler System", test_scheduler),
        ("GUI System", test_gui),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"PASSED: {test_name}")
            else:
                print(f"FAILED: {test_name}")
        except Exception as e:
            print(f"ERROR: {test_name} - {e}")

    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} passed")

    if passed == total:
        print("SUCCESS: All systems operational!")
        print("Privacy Eraser implementation is complete and ready!")
        return True
    else:
        print("WARNING: Some systems need attention")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
