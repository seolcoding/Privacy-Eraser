#!/usr/bin/env python3
"""
Privacy Eraser 체계적 테스팅 플랜
===============================

이 문서는 Privacy Eraser 프로젝트의 모든 테스트를 체계적으로 수행하기 위한 계획입니다.
"""

import os
import sys
import time
import psutil
import platform
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass

# 프로젝트 경로 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

@dataclass
class TestResult:
    """테스트 결과 데이터 클래스"""
    test_name: str
    status: str  # 'PASS', 'FAIL', 'ERROR', 'SKIP'
    duration: float
    message: str = ""
    details: Dict[str, Any] = None

    def __post_init__(self):
        if self.details is None:
            self.details = {}

class TestSuite:
    """테스트 스위트 관리 클래스"""

    def __init__(self, name: str):
        self.name = name
        self.results: List[TestResult] = []
        self.start_time = time.time()

    def add_result(self, result: TestResult):
        """테스트 결과 추가"""
        self.results.append(result)

    def get_summary(self) -> Dict[str, Any]:
        """테스트 요약 반환"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r.status == 'PASS')
        failed = sum(1 for r in self.results if r.status == 'FAIL')
        errors = sum(1 for r in self.results if r.status == 'ERROR')
        skipped = sum(1 for r in self.results if r.status == 'SKIP')

        return {
            'name': self.name,
            'total': total,
            'passed': passed,
            'failed': failed,
            'errors': errors,
            'skipped': skipped,
            'success_rate': (passed / total * 100) if total > 0 else 0,
            'total_duration': sum(r.duration for r in self.results)
        }

    def print_summary(self):
        """테스트 요약 출력"""
        summary = self.get_summary()
        print(f"\n{'='*60}")
        print(f"테스트 스위트: {self.name}")
        print(f"총 테스트 수: {summary['total']}")
        print(f"통과: {summary['passed']} ({summary['success_rate']:.1f}%)")
        print(f"실패: {summary['failed']}")
        print(f"오류: {summary['errors']}")
        print(f"건너뜀: {summary['skipped']}")
        print(f"총 소요 시간: {summary['total_duration']:.2f}초")
        print(f"{'='*60}")

class Tester:
    """메인 테스터 클래스"""

    def __init__(self):
        self.suites: Dict[str, TestSuite] = {}
        self.system_info = self._get_system_info()

    def _get_system_info(self) -> Dict[str, Any]:
        """시스템 정보 수집"""
        return {
            'platform': platform.platform(),
            'python_version': sys.version,
            'cpu_count': os.cpu_count(),
            'memory_gb': round(psutil.virtual_memory().total / (1024**3), 2),
            'project_path': str(project_root)
        }

    def create_suite(self, name: str) -> TestSuite:
        """새 테스트 스위트 생성"""
        suite = TestSuite(name)
        self.suites[name] = suite
        return suite

    def run_test(self, test_func, test_name: str, suite_name: str = "default"):
        """단일 테스트 실행"""
        if suite_name not in self.suites:
            self.create_suite(suite_name)

        suite = self.suites[suite_name]
        start_time = time.time()

        try:
            result = test_func()
            duration = time.time() - start_time

            if result is True:
                suite.add_result(TestResult(test_name, 'PASS', duration))
            elif result is False:
                suite.add_result(TestResult(test_name, 'FAIL', duration, "Test returned False"))
            elif isinstance(result, str):
                suite.add_result(TestResult(test_name, 'FAIL', duration, result))
            else:
                suite.add_result(TestResult(test_name, 'PASS', duration))

        except Exception as e:
            duration = time.time() - start_time
            suite.add_result(TestResult(test_name, 'ERROR', duration, str(e)))

    def print_all_summaries(self):
        """모든 테스트 스위트 요약 출력"""
        print("\n" + "="*80)
        print("PRIVACY ERASER - COMPREHENSIVE TESTING REPORT")
        print("="*80)
        print(f"테스트 환경: {self.system_info['platform']}")
        print(f"Python 버전: {self.system_info['python_version'].split()[0]}")
        print(f"프로젝트 경로: {self.system_info['project_path']}")
        print("="*80)

        total_passed = 0
        total_tests = 0

        for suite_name, suite in self.suites.items():
            suite.print_summary()
            summary = suite.get_summary()
            total_passed += summary['passed']
            total_tests += summary['total']

        print("\n" + "="*80)
        print("전체 결과 요약")
        print(f"총 테스트 수: {total_tests}")
        print(f"전체 통과율: {(total_passed/total_tests*100):.1f}%" if total_tests > 0 else "테스트 없음")
        print("="*80)

        return total_passed == total_tests

# 전역 테스터 인스턴스
tester = Tester()

# 테스트 함수들
def test_imports():
    """기본 모듈 임포트 테스트"""
    try:
        import privacy_eraser.daemon
        import privacy_eraser.settings_db
        import privacy_eraser.scheduler
        import privacy_eraser.app_state
        import privacy_eraser.gui
        return True
    except Exception as e:
        return f"Import error: {e}"

def test_database():
    """데이터베이스 기능 테스트"""
    try:
        from privacy_eraser.settings_db import get_database_manager, save_setting, load_setting

        # 데이터베이스 매니저 생성
        db = get_database_manager()

        # 기본 설정 저장/로드 테스트
        test_key = "test_setting"
        test_value = "test_value_123"

        save_setting(test_key, test_value)
        loaded_value = load_setting(test_key, "default")

        if loaded_value != test_value:
            return f"Setting save/load failed: expected {test_value}, got {loaded_value}"

        # 정리
        save_setting(test_key, "")

        return True
    except Exception as e:
        return f"Database test error: {e}"

def test_daemon_creation():
    """데몬 생성 테스트"""
    try:
        from privacy_eraser.daemon import get_daemon

        daemon = get_daemon()

        if daemon is None:
            return "Daemon creation returned None"

        return True
    except Exception as e:
        return f"Daemon creation error: {e}"

def test_scheduler_creation():
    """스케줄러 생성 테스트"""
    try:
        from privacy_eraser.daemon import DaemonSignals
        from privacy_eraser.scheduler import get_scheduler

        signals = DaemonSignals()
        scheduler = get_scheduler(signals)

        if scheduler is None:
            return "Scheduler creation returned None"

        # 기본 프리셋 확인
        presets = scheduler.get_builtin_presets()
        if not presets:
            return "No builtin presets found"

        return True
    except Exception as e:
        return f"Scheduler creation error: {e}"

def test_app_state():
    """앱 상태 관리 테스트"""
    try:
        from privacy_eraser.app_state import app_state

        # 초기 상태 확인
        initial_mode = app_state.ui_mode
        initial_debug = app_state.debug_enabled

        # 상태 변경 테스트
        app_state.ui_mode = "advanced"
        app_state.debug_enabled = True

        if app_state.ui_mode != "advanced":
            return "UI mode change failed"

        if not app_state.debug_enabled:
            return "Debug enabled change failed"

        # 상태 복원
        app_state.ui_mode = initial_mode
        app_state.debug_enabled = initial_debug

        return True
    except Exception as e:
        return f"App state test error: {e}"

def test_gui_creation():
    """GUI 생성 테스트"""
    try:
        from privacy_eraser.gui import create_main_window

        window = create_main_window()

        if window is None:
            return "Window creation returned None"

        # 창 제목 확인
        title = window.windowTitle()
        if "Privacy" not in title:
            return f"Unexpected window title: {title}"

        return True
    except Exception as e:
        return f"GUI creation error: {e}"

def test_cleaner_engine():
    """클리너 엔진 테스트"""
    try:
        from privacy_eraser.core.cleaner_engine import load_winclean_scripts

        # WinClean 스크립트 로드 테스트
        scripts = load_winclean_scripts("src/privacy_eraser/core/winclean_scripts")

        if not scripts:
            return "No WinClean scripts loaded"

        script_count = len(scripts)
        if script_count < 5:  # 최소 5개 스크립트는 있어야 함
            return f"Too few scripts loaded: {script_count}"

        return True
    except Exception as e:
        return f"Cleaner engine test error: {e}"

def test_file_operations():
    """파일 작업 테스트"""
    try:
        from privacy_eraser.core.file_utils import safe_delete_file, calculate_directory_size

        # 임시 파일 생성 (실제로는 삭제하지 않음)
        test_path = Path.home() / ".privacy_eraser_test"

        if test_path.exists():
            test_path.unlink()

        # 디렉토리 크기 계산 테스트
        home_size = calculate_directory_size(str(Path.home()))

        if home_size <= 0:
            return "Directory size calculation failed"

        return True
    except Exception as e:
        return f"File operations test error: {e}"

def test_diagnostics():
    """진단 기능 테스트"""
    try:
        from privacy_eraser.diagnostics import collect_programs

        # 브라우저 감지 테스트
        programs = collect_programs()

        if not programs:
            return "No programs detected"

        # 최소 하나의 브라우저는 감지되어야 함
        browser_found = any("browser" in prog.get("name", "").lower() for prog in programs)
        if not browser_found:
            return "No browsers detected"

        return True
    except Exception as e:
        return f"Diagnostics test error: {e}"

def main():
    """메인 테스트 실행 함수"""
    print("Privacy Eraser - 체계적 테스팅 시작")
    print("=" * 60)

    # 테스트 스위트 생성
    unit_suite = tester.create_suite("단위 테스트")
    integration_suite = tester.create_suite("통합 테스트")
    gui_suite = tester.create_suite("GUI 테스트")
    system_suite = tester.create_suite("시스템 테스트")

    # 단위 테스트 실행
    print("\n단위 테스트 실행 중...")
    tester.run_test(test_imports, "모듈 임포트", "단위 테스트")
    tester.run_test(test_database, "데이터베이스 기능", "단위 테스트")
    tester.run_test(test_app_state, "앱 상태 관리", "단위 테스트")
    tester.run_test(test_file_operations, "파일 작업", "단위 테스트")

    # 통합 테스트 실행
    print("\n통합 테스트 실행 중...")
    tester.run_test(test_daemon_creation, "데몬 생성", "통합 테스트")
    tester.run_test(test_scheduler_creation, "스케줄러 생성", "통합 테스트")
    tester.run_test(test_cleaner_engine, "클리너 엔진", "통합 테스트")
    tester.run_test(test_diagnostics, "진단 기능", "통합 테스트")

    # GUI 테스트 실행
    print("\nGUI 테스트 실행 중...")
    tester.run_test(test_gui_creation, "메인 윈도우 생성", "GUI 테스트")

    # 결과 출력
    success = tester.print_all_summaries()

    if success:
        print("\n모든 테스트가 성공적으로 완료되었습니다!")
        print("Privacy Eraser가 정상적으로 작동합니다.")
    else:
        print("\n일부 테스트에서 문제가 발견되었습니다.")
        print("구현을 검토하고 수정이 필요할 수 있습니다.")

    return success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n테스트가 사용자에 의해 중단되었습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"\n테스트 실행 중 예상치 못한 오류 발생: {e}")
        sys.exit(1)
