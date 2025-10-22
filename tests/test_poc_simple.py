"""POC 간단한 단위 테스트 - UI 없이 핵심 기능만 테스트"""

import os
import sys
import pytest
from pathlib import Path

# macOS/Linux 환경 확인
IS_WINDOWS = os.name == "nt"


class TestBrowserInfo:
    """BrowserInfo 데이터 클래스 테스트"""

    def test_browser_info_creation(self):
        """BrowserInfo 생성 테스트"""
        from privacy_eraser.ui.core.browser_info import BrowserInfo

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
        from privacy_eraser.ui.core.browser_info import BrowserInfo

        browser_installed = BrowserInfo(
            name="Chrome", icon="🌐", color="#4285F4", installed=True
        )
        browser_not_installed = BrowserInfo(
            name="Brave", icon="🦁", color="#FB542B", installed=False
        )

        assert "Chrome" in str(browser_installed)
        assert "✓" in str(browser_installed)
        assert "Brave" in str(browser_not_installed)
        assert "✗" in str(browser_not_installed)


class TestCleaningStats:
    """CleaningStats 데이터 클래스 테스트"""

    def test_cleaning_stats_creation(self):
        """CleaningStats 생성 테스트"""
        from privacy_eraser.ui.core.browser_info import CleaningStats

        stats = CleaningStats(
            total_files=100,
            deleted_files=95,
            failed_files=5,
            total_size=100 * 1024 * 1024,  # 100 MB
            deleted_size=95 * 1024 * 1024,  # 95 MB
            duration=10.5,
            errors=["Error 1", "Error 2"]
        )

        assert stats.total_files == 100
        assert stats.deleted_files == 95
        assert stats.failed_files == 5
        assert stats.duration == 10.5
        assert len(stats.errors) == 2

    def test_cleaning_stats_properties(self):
        """CleaningStats 속성 테스트"""
        from privacy_eraser.ui.core.browser_info import CleaningStats

        stats = CleaningStats(
            total_files=100,
            deleted_files=80,
            failed_files=20,
            total_size=100 * 1024 * 1024,  # 100 MB
            deleted_size=80 * 1024 * 1024,  # 80 MB
            duration=5.0
        )

        assert stats.success_rate == 80.0
        assert stats.total_size_mb == 100.0
        assert stats.deleted_size_mb == 80.0

    def test_cleaning_stats_empty(self):
        """빈 CleaningStats 테스트"""
        from privacy_eraser.ui.core.browser_info import CleaningStats

        stats = CleaningStats(
            total_files=0,
            deleted_files=0,
            failed_files=0,
            total_size=0,
            deleted_size=0,
            duration=0.0
        )

        assert stats.success_rate == 100.0  # No files = 100% success
        assert stats.total_size_mb == 0.0
        assert stats.deleted_size_mb == 0.0


class TestDataConfig:
    """데이터 설정 모듈 테스트"""

    def test_browser_color_mapping(self):
        """브라우저 색상 매핑 테스트"""
        from privacy_eraser.ui.core.data_config import get_browser_color

        assert get_browser_color("chrome") == "#4285F4"
        assert get_browser_color("firefox") == "#FF7139"
        assert get_browser_color("edge") == "#0078D4"
        assert get_browser_color("unknown") == "#666666"  # Default

    def test_browser_display_name(self):
        """브라우저 표시 이름 테스트"""
        from privacy_eraser.ui.core.data_config import get_browser_display_name

        assert get_browser_display_name("chrome") == "Chrome"
        assert get_browser_display_name("firefox") == "Firefox"
        assert get_browser_display_name("edge") == "Edge"
        assert get_browser_display_name("unknown") == "unknown"  # As is

    def test_cleaner_options_without_bookmarks(self):
        """북마크 제외 옵션 테스트"""
        from privacy_eraser.ui.core.data_config import get_cleaner_options

        options = get_cleaner_options(delete_bookmarks=False)

        assert "cache" in options
        assert "cookies" in options
        assert "history" in options
        assert "session" in options
        assert "passwords" in options
        assert "bookmarks" not in options
        assert "favicons" not in options

    def test_cleaner_options_with_bookmarks(self):
        """북마크 포함 옵션 테스트"""
        from privacy_eraser.ui.core.data_config import get_cleaner_options

        options = get_cleaner_options(delete_bookmarks=True)

        assert "cache" in options
        assert "cookies" in options
        assert "bookmarks" in options
        assert "favicons" in options

    def test_browser_xml_path_mapping(self):
        """브라우저 XML 경로 매핑 테스트"""
        from privacy_eraser.ui.core.data_config import get_browser_xml_path

        assert "chrome.xml" in get_browser_xml_path("chrome")
        assert "firefox.xml" in get_browser_xml_path("firefox")
        assert "brave.xml" in get_browser_xml_path("brave")
        assert get_browser_xml_path("unknown") == ""  # Empty for unknown


class TestMocking:
    """모킹 관련 테스트"""

    @pytest.mark.skipif(IS_WINDOWS, reason="macOS/Linux 전용")
    def test_mock_browser_detection(self):
        """모킹된 브라우저 감지 테스트"""
        # macOS에서는 mock_windows.py 사용
        try:
            from privacy_eraser.mock_windows import MOCK_BROWSERS

            assert len(MOCK_BROWSERS) > 0
            assert any(b["name"] == "Google Chrome" for b in MOCK_BROWSERS)
            assert any(b["name"] == "Mozilla Firefox" for b in MOCK_BROWSERS)

        except ImportError:
            # Windows에서는 실제 감지
            from privacy_eraser.detect_windows import detect_browsers
            browsers = detect_browsers()
            assert isinstance(browsers, list)


# 통합 테스트는 별도 파일로 분리
if __name__ == "__main__":
    pytest.main([__file__, "-v"])