"""POC용 삭제 대상 정의 및 브라우저 설정"""

import os
from pathlib import Path

# ═════════════════════════════════════════════════════════════
# 삭제 대상 옵션
# ═════════════════════════════════════════════════════════════

# 기본 삭제 대상 (개인정보만 삭제, 캐시 및 브라우저 설정 제외)
# 캐시 파일(이미지 등)은 개인정보가 아니므로 기본적으로 삭제하지 않음
# sync 옵션은 제외 - Local State의 profile 키를 삭제하여 브라우저 초기화 문제 발생
DEFAULT_CLEANER_OPTIONS = [
    "cookies",  # 쿠키
    "history",  # 브라우징 히스토리
    "session",  # 세션 데이터
    "passwords",  # 저장된 비밀번호
    "form_history",  # 자동완성 데이터
]

# 북마크 옵션 (토글 활성화 시만 삭제)
BOOKMARK_OPTIONS = [
    "bookmarks",  # 북마크
    "favicons",  # 파비콘
]

# 다운로드 파일 옵션 (토글 활성화 시만 삭제)
DOWNLOAD_OPTIONS = [
    "download_history",  # 다운로드 히스토리
]

# 제외할 옵션 (항상 보존)
EXCLUDE_OPTIONS = [
    "extensions",  # 확장 프로그램
    "settings",  # 브라우저 설정
    "preferences",  # 설정
]

# ═════════════════════════════════════════════════════════════
# 브라우저별 CleanerML 파일 매핑
# ═════════════════════════════════════════════════════════════

def _get_cleaner_xml_path(filename: str) -> str:
    """Get absolute path to CleanerML file"""
    # Get package root directory (privacy_eraser/)
    package_root = Path(__file__).parent.parent.parent
    xml_path = package_root / "cleaners" / filename
    return str(xml_path.absolute())

CLEANER_XML_MAP = {
    "chrome": _get_cleaner_xml_path("google_chrome.xml"),
    "edge": _get_cleaner_xml_path("microsoft_edge.xml"),
    "firefox": _get_cleaner_xml_path("firefox.xml"),
    "brave": _get_cleaner_xml_path("brave.xml"),
    "opera": _get_cleaner_xml_path("opera.xml"),
    "whale": _get_cleaner_xml_path("whale.xml"),  # Naver Whale 전용 XML
    "safari": _get_cleaner_xml_path("safari.xml"),
}

# ═════════════════════════════════════════════════════════════
# 브라우저 아이콘 및 색상 매핑
# ═════════════════════════════════════════════════════════════

BROWSER_ICONS = {
    "chrome": "fa5b.chrome",  # Chrome 로고
    "edge": "fa5b.edge",  # Edge 로고
    "firefox": "fa5b.firefox",  # Firefox 로고
    "brave": "fa5s.shield-alt",  # Brave (방패)
    "opera": "fa5b.opera",  # Opera 로고
    "whale": "fa5s.fish",  # Whale (물고기)
    "safari": "fa5b.safari",  # Safari
}

BROWSER_COLORS = {
    "chrome": "#4285F4",
    "edge": "#0078D4",
    "firefox": "#FF7139",
    "brave": "#FB542B",
    "opera": "#FF1B2D",
    "whale": "#3B5998",
    "safari": "#1F8FF0",
}

# ═════════════════════════════════════════════════════════════
# 브라우저 프로세스 이름
# ═════════════════════════════════════════════════════════════

BROWSER_PROCESSES = {
    "chrome": ["chrome.exe", "chromium.exe"],
    "edge": ["msedge.exe"],
    "firefox": ["firefox.exe"],
    "brave": ["brave.exe"],
    "opera": ["opera.exe"],
    "whale": ["whale.exe"],
    "safari": ["safari.exe"],
}

# ═════════════════════════════════════════════════════════════
# 브라우저 표시 이름 정규화
# ═════════════════════════════════════════════════════════════

BROWSER_DISPLAY_NAMES = {
    "chrome": "Chrome",
    "edge": "Edge",
    "firefox": "Firefox",
    "brave": "Brave",
    "opera": "Opera",
    "whale": "Whale",
    "safari": "Safari",
}


def get_browser_display_name(browser_name: str) -> str:
    """브라우저 표시 이름 반환"""
    return BROWSER_DISPLAY_NAMES.get(browser_name.lower(), browser_name)


def get_browser_icon(browser_name: str) -> str:
    """브라우저 아이콘 반환"""
    return BROWSER_ICONS.get(browser_name.lower(), "🌐")


def get_browser_color(browser_name: str) -> str:
    """브라우저 색상 반환"""
    return BROWSER_COLORS.get(browser_name.lower(), "#666666")


def get_browser_xml_path(browser_name: str) -> str:
    """브라우저 CleanerML XML 파일 경로 반환"""
    return CLEANER_XML_MAP.get(browser_name.lower(), "")


def get_cleaner_options(delete_bookmarks: bool = False, delete_downloads: bool = False) -> list[str]:
    """삭제 옵션 목록 반환

    Args:
        delete_bookmarks: 북마크 삭제 여부
        delete_downloads: 다운로드 파일 삭제 여부

    Returns:
        삭제할 옵션 목록
    """
    options = DEFAULT_CLEANER_OPTIONS.copy()
    if delete_bookmarks:
        options.extend(BOOKMARK_OPTIONS)
    if delete_downloads:
        options.extend(DOWNLOAD_OPTIONS)
    return options
