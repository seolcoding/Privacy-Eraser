"""POC용 삭제 대상 정의 및 브라우저 설정"""

# ═════════════════════════════════════════════════════════════
# 삭제 대상 옵션
# ═════════════════════════════════════════════════════════════

# 기본 삭제 대상 (항상 삭제, 북마크 제외)
DEFAULT_CLEANER_OPTIONS = [
    "cache",  # 캐시 파일
    "cookies",  # 쿠키
    "history",  # 브라우징 히스토리
    "session",  # 세션 데이터
    "passwords",  # 저장된 비밀번호
    "form_history",  # 자동완성 데이터
    "cookies_session",  # 세션 쿠키
    "localstore",  # 로컬 저장소
]

# 북마크 옵션 (토글 활성화 시만 삭제)
BOOKMARK_OPTIONS = [
    "bookmarks",  # 북마크
    "favicons",  # 파비콘
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

CLEANER_XML_MAP = {
    "chrome": "bleachbit/cleaners/chrome.xml",
    "edge": "bleachbit/cleaners/chrome.xml",  # Chromium 기반
    "firefox": "bleachbit/cleaners/firefox.xml",
    "brave": "bleachbit/cleaners/brave.xml",
    "opera": "bleachbit/cleaners/opera.xml",
    "whale": "bleachbit/cleaners/chrome.xml",  # Chromium 기반
    "vivaldi": "bleachbit/cleaners/chrome.xml",  # Chromium 기반
    "librewolf": "bleachbit/cleaners/firefox.xml",  # Firefox 기반
}

# ═════════════════════════════════════════════════════════════
# 브라우저 아이콘 및 색상 매핑
# ═════════════════════════════════════════════════════════════

BROWSER_ICONS = {
    "chrome": "🌐",
    "edge": "🌐",
    "firefox": "🦊",
    "brave": "🦁",
    "opera": "🅾️",
    "whale": "🐋",
    "vivaldi": "🎨",
    "librewolf": "🦊",
}

BROWSER_COLORS = {
    "chrome": "#4285F4",
    "edge": "#0078D4",
    "firefox": "#FF7139",
    "brave": "#FB542B",
    "opera": "#FF1B2D",
    "whale": "#3B5998",
    "vivaldi": "#EF3939",
    "librewolf": "#00539F",
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
    "vivaldi": ["vivaldi.exe"],
    "librewolf": ["librewolf.exe"],
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
    "vivaldi": "Vivaldi",
    "librewolf": "LibreWolf",
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


def get_cleaner_options(delete_bookmarks: bool = False) -> list[str]:
    """삭제 옵션 목록 반환"""
    options = DEFAULT_CLEANER_OPTIONS.copy()
    if delete_bookmarks:
        options.extend(BOOKMARK_OPTIONS)
    return options
