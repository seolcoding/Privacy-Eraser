"""POC UI 컴포넌트 테스트 - Material Design UI 및 모킹 기반"""

import os
import sys
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QTimer

# macOS 환경 확인
IS_MACOS = sys.platform == "darwin"
IS_WINDOWS = os.name == "nt"


@pytest.fixture(scope="session")
def qapp():
    """Qt 애플리케이션 고정 (세션 레벨)"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


@pytest.fixture
def mock_browsers():
    """모의 브라우저 데이터"""
    from privacy_eraser.poc.core.browser_info import BrowserInfo

    return [
        BrowserInfo(name="Chrome", icon="🌐", color="#4285F4", installed=True),
        BrowserInfo(name="Firefox", icon="🦊", color="#FF7139", installed=True),
        BrowserInfo(name="Edge", icon="🌐", color="#0078D4", installed=True),
        BrowserInfo(name="Brave", icon="🦁", color="#FB542B", installed=False),
    ]


@pytest.fixture
def sandbox(tmp_path):
    """테스트용 샌드박스 디렉토리"""
    # 테스트 파일 구조 생성
    cache_dir = tmp_path / "cache"
    cookies_file = tmp_path / "cookies.db"
    history_file = tmp_path / "history.txt"

    cache_dir.mkdir()
    cookies_file.write_text("mock_cookies_data")
    history_file.write_text("mock_history_data")

    return tmp_path


class TestBrowserCard:
    """BrowserCard 위젯 테스트"""

    def test_browser_card_creation(self, mock_browsers, qapp):
        """브라우저 카드 생성 테스트"""
        from privacy_eraser.poc.ui.browser_card import BrowserCard

        browser_info = mock_browsers[0]  # Chrome
        card = BrowserCard(browser_info)

        assert card.browser_info.name == "Chrome"
        assert card.is_selected is True
        assert card.checkbox.isChecked() is True

    def test_browser_card_selection_toggle(self, mock_browsers, qapp):
        """브라우저 카드 선택 토글 테스트"""
        from privacy_eraser.poc.ui.browser_card import BrowserCard

        browser_info = mock_browsers[0]
        card = BrowserCard(browser_info)

        # 초기 상태
        assert card.is_selected is True

        # 토글
        card.checkbox.setChecked(False)
        assert card.is_selected is False

        # 다시 토글
        card.checkbox.setChecked(True)
        assert card.is_selected is True

    def test_browser_card_signal_emission(self, mock_browsers, qapp):
        """브라우저 카드 신호 발생 테스트"""
        from privacy_eraser.poc.ui.browser_card import BrowserCard

        browser_info = mock_browsers[0]
        card = BrowserCard(browser_info)

        # 신호 수신기 설정
        signal_received = []

        def on_selection_changed(name, selected):
            signal_received.append((name, selected))

        card.selection_changed.connect(on_selection_changed)

        # 토글
        card.checkbox.setChecked(False)
        assert signal_received[-1] == ("Chrome", False)

        # 다시 토글
        card.checkbox.setChecked(True)
        assert signal_received[-1] == ("Chrome", True)


class TestProgressDialog:
    """ProgressDialog 다이얼로그 테스트"""

    def test_progress_dialog_creation(self, qapp):
        """진행 팝업 생성 테스트"""
        from privacy_eraser.poc.ui.progress_dialog import ProgressDialog

        dialog = ProgressDialog()

        assert dialog.total_files == 0
        assert dialog.total_size == 0
        assert dialog.deleted_files == 0
        assert dialog.deleted_size == 0

    def test_progress_dialog_set_totals(self, qapp):
        """전체 파일/크기 설정 테스트"""
        from privacy_eraser.poc.ui.progress_dialog import ProgressDialog

        dialog = ProgressDialog()
        dialog.set_total_files(100)
        dialog.set_total_size(1024 * 1024 * 100)  # 100 MB

        assert dialog.total_files == 100
        assert dialog.total_size == 1024 * 1024 * 100

    def test_progress_dialog_update(self, qapp):
        """진행 상황 업데이트 테스트"""
        from privacy_eraser.poc.ui.progress_dialog import ProgressDialog

        dialog = ProgressDialog()
        dialog.set_total_files(10)
        dialog.set_total_size(10 * 1024 * 1024)  # 10 MB

        # 파일 삭제 시뮬레이션
        for i in range(5):
            file_path = f"/mock/path/file_{i}"
            file_size = 1024 * 1024  # 1 MB
            dialog.update_progress(file_path, file_size)

        assert dialog.deleted_files == 5
        assert dialog.deleted_size == 5 * 1024 * 1024
        assert dialog.progress_bar.value() == 50  # 50% 진행

    def test_progress_dialog_completion(self, qapp):
        """완료 표시 테스트"""
        from privacy_eraser.poc.ui.progress_dialog import ProgressDialog
        from privacy_eraser.poc.core.browser_info import CleaningStats

        dialog = ProgressDialog()

        stats = CleaningStats(
            total_files=100,
            deleted_files=100,
            failed_files=0,
            total_size=100 * 1024 * 1024,
            deleted_size=100 * 1024 * 1024,
            duration=5.5,
            errors=[]
        )

        dialog.show_completion(stats)

        # 완료 상태 확인
        assert "삭제 완료" in dialog.status_label.text()
        assert dialog.progress_bar.value() == 100


class TestMainWindow:
    """MainWindow 테스트"""

    @pytest.mark.skipif(IS_WINDOWS, reason="macOS/Linux 전용 (모킹 기반)")
    def test_main_window_creation(self, qapp):
        """메인 윈도우 생성 테스트"""
        from privacy_eraser.poc.ui.main_window import MainWindow

        window = MainWindow()

        assert window.windowTitle() == "Privacy Eraser POC"
        assert window.selected_browsers is not None

    @pytest.mark.skipif(IS_WINDOWS, reason="macOS/Linux 전용")
    def test_main_window_bookmark_toggle(self, qapp):
        """북마크 토글 테스트"""
        from privacy_eraser.poc.ui.main_window import MainWindow

        window = MainWindow()

        # 초기 상태
        assert window.delete_bookmarks is False

        # 토글
        window.bookmark_checkbox.setChecked(True)
        assert window.delete_bookmarks is True

        # 다시 토글
        window.bookmark_checkbox.setChecked(False)
        assert window.delete_bookmarks is False

    @pytest.mark.skipif(IS_WINDOWS, reason="macOS/Linux 전용")
    def test_main_window_browser_detection(self, qapp):
        """브라우저 감지 테스트 (모킹)"""
        from privacy_eraser.poc.ui.main_window import MainWindow
        from privacy_eraser.poc.core.browser_info import BrowserInfo

        window = MainWindow()

        # 모의 브라우저 데이터
        mock_browsers = [
            BrowserInfo(name="Chrome", icon="🌐", color="#4285F4", installed=True),
            BrowserInfo(name="Firefox", icon="🦊", color="#FF7139", installed=True),
        ]

        # 브라우저 감지 콜백 호출
        window.on_browsers_detected(mock_browsers)

        # 브라우저 카드 생성 확인
        assert "Chrome" in window.browser_cards
        assert "Firefox" in window.browser_cards
        assert window.selected_browsers["Chrome"] is True
        assert window.selected_browsers["Firefox"] is True


class TestBrowserInfo:
    """BrowserInfo 데이터 클래스 테스트"""

    def test_browser_info_creation(self):
        """BrowserInfo 생성 테스트"""
        from privacy_eraser.poc.core.browser_info import BrowserInfo

        browser = BrowserInfo(
            name="Chrome",
            icon="🌐",
            color="#4285F4",
            installed=True
        )

        assert browser.name == "Chrome"
        assert browser.icon == "🌐"
        assert browser.color == "#4285F4"
        assert browser.installed is True

    def test_browser_info_string_representation(self):
        """BrowserInfo 문자열 표현 테스트"""
        from privacy_eraser.poc.core.browser_info import BrowserInfo

        browser = BrowserInfo(name="Chrome", icon="🌐", color="#4285F4", installed=True)
        assert "Chrome" in str(browser)
        assert "🌐" in str(browser)


class TestCleaningStats:
    """CleaningStats 데이터 클래스 테스트"""

    def test_cleaning_stats_creation(self):
        """CleaningStats 생성 테스트"""
        from privacy_eraser.poc.core.browser_info import CleaningStats

        stats = CleaningStats(
            total_files=100,
            deleted_files=100,
            failed_files=0,
            total_size=100 * 1024 * 1024,
            deleted_size=100 * 1024 * 1024,
            duration=5.5,
            errors=[]
        )

        assert stats.total_files == 100
        assert stats.deleted_files == 100
        assert stats.success_rate == 100.0

    def test_cleaning_stats_size_conversion(self):
        """크기 변환 테스트"""
        from privacy_eraser.poc.core.browser_info import CleaningStats

        stats = CleaningStats(
            total_files=10,
            deleted_files=10,
            failed_files=0,
            total_size=100 * 1024 * 1024,  # 100 MB
            deleted_size=50 * 1024 * 1024,  # 50 MB
            duration=10.0,
            errors=[]
        )

        assert stats.total_size_mb == 100.0
        assert stats.deleted_size_mb == 50.0

    def test_cleaning_stats_success_rate(self):
        """성공률 계산 테스트"""
        from privacy_eraser.poc.core.browser_info import CleaningStats

        stats = CleaningStats(
            total_files=100,
            deleted_files=80,
            failed_files=20,
            total_size=100 * 1024 * 1024,
            deleted_size=80 * 1024 * 1024,
            duration=10.0,
            errors=[]
        )

        assert stats.success_rate == 80.0


class TestDataConfig:
    """데이터 설정 테스트"""

    def test_get_browser_icon(self):
        """브라우저 아이콘 조회 테스트"""
        from privacy_eraser.poc.core.data_config import get_browser_icon

        assert get_browser_icon("chrome") == "fa5b.chrome"
        assert get_browser_icon("firefox") == "fa5b.firefox"
        assert get_browser_icon("brave") == "fa5s.shield-alt"

    def test_get_browser_color(self):
        """브라우저 색상 조회 테스트"""
        from privacy_eraser.poc.core.data_config import get_browser_color

        assert get_browser_color("chrome") == "#4285F4"
        assert get_browser_color("firefox") == "#FF7139"

    def test_get_cleaner_options_default(self):
        """기본 삭제 옵션 조회 테스트"""
        from privacy_eraser.poc.core.data_config import get_cleaner_options

        options = get_cleaner_options(delete_bookmarks=False)
        assert "cache" in options
        assert "cookies" in options
        assert "history" in options
        assert "bookmarks" not in options

    def test_get_cleaner_options_with_bookmarks(self):
        """북마크 포함 삭제 옵션 조회 테스트"""
        from privacy_eraser.poc.core.data_config import get_cleaner_options

        options = get_cleaner_options(delete_bookmarks=True)
        assert "bookmarks" in options
        assert "cache" in options


class TestStyles:
    """스타일 테스트"""

    def test_get_stylesheet(self):
        """전체 스타일시트 조회 테스트"""
        from privacy_eraser.poc.ui.styles import get_stylesheet

        stylesheet = get_stylesheet()

        assert isinstance(stylesheet, str)
        assert len(stylesheet) > 0
        assert "QMainWindow" in stylesheet
        assert "QPushButton" in stylesheet

    def test_colors_defined(self):
        """색상 정의 테스트"""
        from privacy_eraser.poc.ui.styles import Colors

        assert Colors.PRIMARY == "#5E35B1"
        assert Colors.SECONDARY == "#00BFA5"
        assert Colors.SUCCESS == "#4CAF50"
        assert Colors.ERROR == "#F44336"

    def test_typography_defined(self):
        """타이포그래피 정의 테스트"""
        from privacy_eraser.poc.ui.styles import Typography

        assert Typography.SIZE_H2 == 28  # 24 → 28
        assert Typography.SIZE_BODY == 16  # 14 → 16
        assert Typography.WEIGHT_BOLD == 700

    def test_sizes_defined(self):
        """크기 정의 테스트"""
        from privacy_eraser.poc.ui.styles import Sizes

        assert Sizes.CARD_WIDTH == 160  # 150 → 160
        assert Sizes.BUTTON_HEIGHT == 48
        assert Sizes.MAIN_WINDOW_WIDTH == 700  # 850 → 700


class TestCleanerWorkerMocked:
    """CleanerWorker 테스트 (모킹)"""

    @pytest.mark.skipif(IS_WINDOWS, reason="macOS/Linux 전용")
    def test_cleaner_worker_creation(self, qapp):
        """CleanerWorker 생성 테스트"""
        from privacy_eraser.poc.core.poc_cleaner import CleanerWorker

        worker = CleanerWorker(
            browsers=["Chrome", "Firefox"],
            delete_bookmarks=False
        )

        assert worker.browsers == ["Chrome", "Firefox"]
        assert worker.delete_bookmarks is False
        assert worker.is_cancelled is False

    @pytest.mark.skipif(IS_WINDOWS, reason="macOS/Linux 전용")
    def test_cleaner_worker_cancel(self, qapp):
        """CleanerWorker 취소 테스트"""
        from privacy_eraser.poc.core.poc_cleaner import CleanerWorker

        worker = CleanerWorker(browsers=["Chrome"], delete_bookmarks=False)

        assert worker.is_cancelled is False
        worker.cancel()
        assert worker.is_cancelled is True

    @pytest.mark.skipif(IS_WINDOWS, reason="macOS/Linux 전용")
    def test_cleaner_worker_get_file_size(self, qapp, sandbox):
        """파일 크기 계산 테스트"""
        from privacy_eraser.poc.core.poc_cleaner import CleanerWorker

        worker = CleanerWorker(browsers=["Chrome"], delete_bookmarks=False)

        # 테스트 파일 생성
        test_file = sandbox / "test.txt"
        test_file.write_text("test content")

        size = worker._get_file_size(str(test_file))
        assert size == len("test content")

    @pytest.mark.skipif(IS_WINDOWS, reason="macOS/Linux 전용")
    def test_cleaner_worker_expand_path(self, qapp):
        """경로 확장 테스트"""
        from privacy_eraser.poc.core.poc_cleaner import CleanerWorker

        worker = CleanerWorker(browsers=["Chrome"], delete_bookmarks=False)

        # 환경변수 없는 경로
        result = worker._expand_path("/tmp/test.txt")
        assert isinstance(result, list)


# ═════════════════════════════════════════════════════════════
# 통합 테스트
# ═════════════════════════════════════════════════════════════

class TestIntegration:
    """통합 테스트"""

    @pytest.mark.skipif(IS_WINDOWS, reason="macOS/Linux 전용")
    def test_full_workflow_dry_run(self, qapp):
        """전체 워크플로우 dry run 테스트"""
        from privacy_eraser.poc.core.browser_info import BrowserInfo, CleaningStats
        from privacy_eraser.poc.ui.main_window import MainWindow

        # 1. 메인 윈도우 생성
        window = MainWindow()
        assert window is not None

        # 2. 모의 브라우저 감지
        mock_browsers = [
            BrowserInfo(name="Chrome", icon="🌐", color="#4285F4", installed=True),
            BrowserInfo(name="Firefox", icon="🦊", color="#FF7139", installed=True),
        ]
        window.on_browsers_detected(mock_browsers)
        assert len(window.browser_cards) == 2

        # 3. 북마크 토글
        window.bookmark_checkbox.setChecked(True)
        assert window.delete_bookmarks is True

        # 4. 통계 생성 및 검증
        stats = CleaningStats(
            total_files=100,
            deleted_files=100,
            failed_files=0,
            total_size=100 * 1024 * 1024,
            deleted_size=100 * 1024 * 1024,
            duration=5.5,
            errors=[]
        )
        assert stats.success_rate == 100.0
        assert "삭제 완료" in str(stats)

        print("\n✅ 전체 워크플로우 dry run 성공!")
