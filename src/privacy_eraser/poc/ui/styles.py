"""Material Design 스타일시트 및 테마 정의"""

from PySide6.QtGui import QColor

# ═════════════════════════════════════════════════════════════
# 색상 팔레트 (Material Design 3)
# ═════════════════════════════════════════════════════════════

class Colors:
    """Material Design 색상 팔레트"""

    # Primary Colors - Deep Purple
    PRIMARY = "#5E35B1"
    PRIMARY_LIGHT = "#9162E4"
    PRIMARY_DARK = "#280680"

    # Secondary Colors - Teal
    SECONDARY = "#00BFA5"
    SECONDARY_LIGHT = "#5DF2D6"
    SECONDARY_DARK = "#008E76"

    # Background & Surface - 대비 개선
    BACKGROUND = "#E8EAF6"  # 더 어두운 배경 (연한 보라)
    SURFACE = "#FFFFFF"  # 흰색 카드
    SURFACE_VARIANT = "#F5F5F5"  # 약간 회색

    # Text Colors - 더 진한 텍스트
    TEXT_PRIMARY = "#1A1A1A"  # 거의 검정
    TEXT_SECONDARY = "#5F6368"  # 더 진한 회색
    TEXT_HINT = "#9E9E9E"  # 중간 회색

    # Status Colors
    SUCCESS = "#4CAF50"
    SUCCESS_LIGHT = "#81C784"
    WARNING = "#FF9800"
    ERROR = "#F44336"

    # Shadows
    SHADOW_1 = "rgba(0, 0, 0, 0.05)"
    SHADOW_2 = "rgba(0, 0, 0, 0.10)"
    SHADOW_4 = "rgba(0, 0, 0, 0.15)"
    SHADOW_8 = "rgba(0, 0, 0, 0.20)"

    # Browser Colors
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
# 타이포그래피
# ═════════════════════════════════════════════════════════════

class Typography:
    """타이포그래피 정의"""

    FONT_FAMILY = "Segoe UI, Roboto, -apple-system, BlinkMacSystemFont, sans-serif"

    # Font Sizes (pixels) - 가독성 개선
    SIZE_H1 = 36
    SIZE_H2 = 28
    SIZE_H3 = 22
    SIZE_BODY = 16  # 14 → 16
    SIZE_BODY_SMALL = 15  # 13 → 15
    SIZE_LABEL = 14  # 12 → 14
    SIZE_CAPTION = 14  # 12 → 14

    # Font Weights
    WEIGHT_LIGHT = 300
    WEIGHT_REGULAR = 400
    WEIGHT_MEDIUM = 500
    WEIGHT_SEMIBOLD = 600
    WEIGHT_BOLD = 700

    # Line Heights
    LINE_HEIGHT_TIGHT = 1.2
    LINE_HEIGHT_NORMAL = 1.5
    LINE_HEIGHT_LOOSE = 1.8


# ═════════════════════════════════════════════════════════════
# Spacing System (8px grid)
# ═════════════════════════════════════════════════════════════

class Spacing:
    """8px 기반 Spacing 시스템"""

    XS = 4
    SM = 8
    MD = 16
    LG = 24
    XL = 32
    XXL = 48

    # Component specific
    CARD_PADDING = 16
    CARD_MARGIN = 16
    BUTTON_PADDING_H = 24
    BUTTON_PADDING_V = 12


# ═════════════════════════════════════════════════════════════
# 크기 정의
# ═════════════════════════════════════════════════════════════

class Sizes:
    """컴포넌트 크기 정의"""

    # Card & Component Sizes - 아이콘 48px에 맞춤
    CARD_WIDTH = 160  # 200 → 160 (아이콘 48px + 여백)
    CARD_HEIGHT = 180  # 220 → 180
    CARD_RADIUS = 12

    # Button Sizes
    BUTTON_HEIGHT = 48
    BUTTON_RADIUS = 24
    BUTTON_MIN_WIDTH = 120

    # Input & Controls
    INPUT_HEIGHT = 40
    INPUT_RADIUS = 8
    CHECKBOX_SIZE = 20
    TOGGLE_HEIGHT = 32
    TOGGLE_WIDTH = 56

    # Window Sizes - 축소 (더 컴팩트하게)
    MAIN_WINDOW_WIDTH = 700  # 850 → 700
    MAIN_WINDOW_HEIGHT = 600  # 750 → 600
    PROGRESS_DIALOG_WIDTH = 550  # 650 → 550
    PROGRESS_DIALOG_HEIGHT = 500  # 550 → 500


# ═════════════════════════════════════════════════════════════
# 애니메이션 설정
# ═════════════════════════════════════════════════════════════

class Animation:
    """애니메이션 타이밍 및 설정"""

    # Duration (milliseconds)
    DURATION_FAST = 150  # 호버, 토글
    DURATION_NORMAL = 250  # 기본 전환
    DURATION_SLOW = 400  # 다이얼로그 오픈
    DURATION_VERY_SLOW = 800  # 페이지 전환

    # Easing Curves (CSS format)
    EASE_STANDARD = "cubic-bezier(0.4, 0.0, 0.2, 1)"  # 표준
    EASE_DECELERATE = "cubic-bezier(0.0, 0.0, 0.2, 1)"  # 시작 빠름
    EASE_ACCELERATE = "cubic-bezier(0.4, 0.0, 1, 1)"  # 끝 빠름
    EASE_BOUNCE = "cubic-bezier(0.68, -0.55, 0.265, 1.55)"  # 바운스


# ═════════════════════════════════════════════════════════════
# QSS 스타일시트
# ═════════════════════════════════════════════════════════════

def get_stylesheet() -> str:
    """전체 애플리케이션 스타일시트 반환"""
    return f"""
/* ───────────────────────────────────────────────────────────── */
/* 메인 윈도우                                                    */
/* ───────────────────────────────────────────────────────────── */

QMainWindow {{
    background-color: {Colors.BACKGROUND};
}}

QMainWindow QWidget {{
    background-color: {Colors.BACKGROUND};
}}

/* ───────────────────────────────────────────────────────────── */
/* 일반 위젯                                                      */
/* ───────────────────────────────────────────────────────────── */

QWidget {{
    color: {Colors.TEXT_PRIMARY};
    background-color: transparent;
}}

/* ───────────────────────────────────────────────────────────── */
/* 레이블 & 텍스트                                                */
/* ───────────────────────────────────────────────────────────── */

QLabel {{
    color: {Colors.TEXT_PRIMARY};
    font-family: "{Typography.FONT_FAMILY}";
    font-size: {Typography.SIZE_BODY}px;
}}

QLabel[title="true"] {{
    font-size: {Typography.SIZE_H2}px;
    font-weight: bold;
    color: {Colors.TEXT_PRIMARY};
}}

QLabel[subtitle="true"] {{
    font-size: {Typography.SIZE_BODY}px;
    color: {Colors.TEXT_SECONDARY};
}}

QLabel[hint="true"] {{
    font-size: {Typography.SIZE_CAPTION}px;
    color: {Colors.TEXT_HINT};
}}

/* ───────────────────────────────────────────────────────────── */
/* 버튼 - Primary                                                 */
/* ───────────────────────────────────────────────────────────── */

QPushButton {{
    background-color: {Colors.PRIMARY};
    color: white;
    border: none;
    border-radius: {Sizes.BUTTON_RADIUS}px;
    padding: {Spacing.BUTTON_PADDING_V}px {Spacing.BUTTON_PADDING_H}px;
    font-size: {Typography.SIZE_BODY}px;
    font-weight: {Typography.WEIGHT_MEDIUM};
    font-family: "{Typography.FONT_FAMILY}";
    min-height: {Sizes.BUTTON_HEIGHT}px;
    min-width: {Sizes.BUTTON_MIN_WIDTH}px;
}}

QPushButton:hover {{
    background-color: {Colors.PRIMARY_DARK};
}}

QPushButton:pressed {{
    background-color: {Colors.PRIMARY_DARK};
}}

/* ───────────────────────────────────────────────────────────── */
/* 체크박스                                                       */
/* ───────────────────────────────────────────────────────────── */

QCheckBox {{
    spacing: 8px;
    color: {Colors.TEXT_PRIMARY};
    font-size: {Typography.SIZE_BODY}px;
    font-family: "{Typography.FONT_FAMILY}";
}}

QCheckBox::indicator {{
    width: {Sizes.CHECKBOX_SIZE}px;
    height: {Sizes.CHECKBOX_SIZE}px;
    border-radius: 4px;
}}

QCheckBox::indicator:unchecked {{
    background-color: {Colors.SURFACE};
    border: 2px solid {Colors.TEXT_HINT};
}}

QCheckBox::indicator:unchecked:hover {{
    border: 2px solid {Colors.PRIMARY};
}}

QCheckBox::indicator:checked {{
    background-color: {Colors.PRIMARY};
    border: 2px solid {Colors.PRIMARY};
}}

QCheckBox::indicator:checked:hover {{
    background-color: {Colors.PRIMARY_DARK};
    border: 2px solid {Colors.PRIMARY_DARK};
}}

/* ───────────────────────────────────────────────────────────── */
/* 프로그레스 바                                                  */
/* ───────────────────────────────────────────────────────────── */

QProgressBar {{
    border: none;
    border-radius: 4px;
    background-color: {Colors.SURFACE_VARIANT};
    height: 8px;
    text-align: center;
    color: {Colors.TEXT_SECONDARY};
}}

QProgressBar::chunk {{
    background-color: {Colors.PRIMARY};
    border-radius: 4px;
}}

/* ───────────────────────────────────────────────────────────── */
/* 리스트 위젯                                                    */
/* ───────────────────────────────────────────────────────────── */

QListWidget {{
    border: 1px solid {Colors.SURFACE_VARIANT};
    border-radius: 8px;
    background-color: {Colors.SURFACE};
    color: {Colors.TEXT_PRIMARY};
    font-family: "{Typography.FONT_FAMILY}";
    font-size: {Typography.SIZE_CAPTION}px;
}}

QListWidget::item {{
    padding: 8px;
    margin: 2px 0;
}}

QListWidget::item:hover {{
    background-color: {Colors.SURFACE_VARIANT};
}}

QListWidget::item:selected {{
    background-color: {Colors.PRIMARY_LIGHT};
    color: white;
}}

/* ───────────────────────────────────────────────────────────── */
/* 스크롤바                                                       */
/* ───────────────────────────────────────────────────────────── */

QScrollBar:vertical {{
    background-color: {Colors.SURFACE};
    width: 8px;
    border-radius: 4px;
}}

QScrollBar::handle:vertical {{
    background-color: {Colors.TEXT_HINT};
    border-radius: 4px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {Colors.TEXT_SECONDARY};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    border: none;
    background: none;
}}

/* ───────────────────────────────────────────────────────────── */
/* 다이얼로그                                                     */
/* ───────────────────────────────────────────────────────────── */

QDialog {{
    background-color: {Colors.BACKGROUND};
}}

/* ───────────────────────────────────────────────────────────── */
/* 프레임 (카드 효과)                                              */
/* ───────────────────────────────────────────────────────────── */

QFrame[card="true"] {{
    background-color: {Colors.SURFACE};
    border: none;
    border-radius: {Sizes.CARD_RADIUS}px;
}}

/* ───────────────────────────────────────────────────────────── */
/* 상태 메시지 레이블                                              */
/* ───────────────────────────────────────────────────────────── */

QLabel[status="success"] {{
    color: {Colors.SUCCESS};
    font-weight: {Typography.WEIGHT_MEDIUM};
}}

QLabel[status="warning"] {{
    color: {Colors.WARNING};
    font-weight: {Typography.WEIGHT_MEDIUM};
}}

QLabel[status="error"] {{
    color: {Colors.ERROR};
    font-weight: {Typography.WEIGHT_MEDIUM};
}}
"""


def get_card_stylesheet(
    background_color: str = Colors.SURFACE,
    border_color: str = Colors.SURFACE_VARIANT,
    hover: bool = True,
) -> str:
    """카드 스타일시트 반환 (동적)"""
    base = f"""
    background-color: {background_color};
    border: 2px solid {border_color};
    border-radius: {Sizes.CARD_RADIUS}px;
    """

    if hover:
        base += f"""
        padding: 0px;
    """

    return base


# ═════════════════════════════════════════════════════════════
# 그림자 스타일 (HTML/CSS) - Qt StyleSheet에서는 미지원
# ═════════════════════════════════════════════════════════════
# 주의: Qt StyleSheet는 box-shadow를 지원하지 않습니다.
# 아래는 참고용으로만 남겨둡니다.

SHADOW_STYLES = {
    "elevation_1": (
        f"box-shadow: 0 1px 3px {Colors.SHADOW_1}, "
        f"0 1px 2px rgba(0,0,0,0.24);  /* Qt 미지원 */"
    ),
    "elevation_2": (
        f"box-shadow: 0 3px 6px {Colors.SHADOW_2}, "
        f"0 3px 6px rgba(0,0,0,0.23);  /* Qt 미지원 */"
    ),
    "elevation_4": (
        f"box-shadow: 0 10px 20px {Colors.SHADOW_4}, "
        f"0 6px 6px rgba(0,0,0,0.23);  /* Qt 미지원 */"
    ),
    "elevation_8": (
        f"box-shadow: 0 19px 38px {Colors.SHADOW_8}, "
        f"0 15px 12px rgba(0,0,0,0.22);  /* Qt 미지원 */"
    ),
}
