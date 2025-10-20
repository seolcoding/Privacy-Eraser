"""CCleaner-inspired color theme and styling for PrivacyEraser.

Colors and design patterns inspired by CCleaner's classic interface.
"""

from __future__ import annotations


# CCleaner Color Palette
class CCColors:
    """CCleaner-inspired color scheme."""

    # Primary Colors
    BLUE_PRIMARY = "#4A90E2"  # Main blue accent
    BLUE_HOVER = "#5BA3F5"    # Lighter blue for hover
    BLUE_PRESSED = "#3A7AC8"  # Darker blue for pressed

    # Sidebar Colors
    SIDEBAR_BG = "#3C4650"        # Dark gray background
    SIDEBAR_DARK = "#2E3842"      # Darker gray for depth
    SIDEBAR_LIGHT = "#4A5360"     # Lighter gray for hover
    SIDEBAR_SELECTED = "#2A5A8F"  # Blue-gray for selected

    # Content Area Colors
    CONTENT_BG = "#FFFFFF"        # White background
    CONTENT_ALT = "#F5F6F7"       # Light gray alternate
    BORDER_LIGHT = "#E0E0E0"      # Light border
    BORDER_DARK = "#CCCCCC"       # Darker border

    # Text Colors
    TEXT_PRIMARY = "#2C3E50"      # Dark text
    TEXT_SECONDARY = "#7F8C8D"    # Gray text
    TEXT_LIGHT = "#FFFFFF"        # White text (sidebar)
    TEXT_DISABLED = "#BDC3C7"     # Disabled text

    # Accent Colors
    ORANGE_ACCENT = "#FF8C42"     # Orange for checkboxes/highlights
    GREEN_SUCCESS = "#27AE60"     # Green for success
    RED_WARNING = "#E74C3C"       # Red for warnings
    YELLOW_CAUTION = "#F39C12"    # Yellow for caution

    # Progress/Analysis Colors
    PROGRESS_BG = "#ECF0F1"       # Light gray progress background
    PROGRESS_FILL = "#2ECC71"     # Green progress fill

    # Special UI Elements
    TAB_ACTIVE = "#4A90E2"        # Active tab color
    TAB_INACTIVE = "#95A5A6"      # Inactive tab color
    CHECKBOX_CHECKED = "#FF8C42"  # Orange checkmark


# Qt StyleSheet Templates
class CCStyles:
    """CCleaner-inspired Qt StyleSheets."""

    @staticmethod
    def sidebar_button(selected: bool = False) -> str:
        """Sidebar navigation button style."""
        bg_color = CCColors.SIDEBAR_SELECTED if selected else CCColors.SIDEBAR_BG
        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: {CCColors.TEXT_LIGHT};
                border: none;
                padding: 20px;
                text-align: center;
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {CCColors.SIDEBAR_LIGHT};
            }}
            QPushButton:pressed {{
                background-color: {CCColors.SIDEBAR_DARK};
            }}
        """

    @staticmethod
    def main_button(variant: str = "primary") -> str:
        """Main action button style (Analyze/Run Cleaner)."""
        if variant == "primary":
            bg = CCColors.BLUE_PRIMARY
            hover = CCColors.BLUE_HOVER
            pressed = CCColors.BLUE_PRESSED
        elif variant == "success":
            bg = CCColors.GREEN_SUCCESS
            hover = "#2ECC71"
            pressed = "#229954"
        else:
            bg = CCColors.TEXT_SECONDARY
            hover = "#95A5A6"
            pressed = "#7F8C8D"

        return f"""
            QPushButton {{
                background-color: {bg};
                color: {CCColors.TEXT_LIGHT};
                border: none;
                border-radius: 4px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background-color: {hover};
            }}
            QPushButton:pressed {{
                background-color: {pressed};
            }}
            QPushButton:disabled {{
                background-color: {CCColors.TEXT_DISABLED};
            }}
        """

    @staticmethod
    def checkbox_orange() -> str:
        """Orange checkbox style (CCleaner signature)."""
        return f"""
            QCheckBox {{
                spacing: 8px;
                color: {CCColors.TEXT_PRIMARY};
                font-size: 13px;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border: 2px solid {CCColors.BORDER_DARK};
                border-radius: 3px;
                background-color: {CCColors.CONTENT_BG};
            }}
            QCheckBox::indicator:hover {{
                border-color: {CCColors.ORANGE_ACCENT};
            }}
            QCheckBox::indicator:checked {{
                background-color: {CCColors.ORANGE_ACCENT};
                border-color: {CCColors.ORANGE_ACCENT};
                image: url(:/icons/check_white.png);
            }}
            QCheckBox::indicator:checked:hover {{
                background-color: #FF9D5C;
            }}
        """

    @staticmethod
    def tree_view() -> str:
        """Tree view style for browser/options list."""
        return f"""
            QTreeView {{
                background-color: {CCColors.CONTENT_BG};
                border: 1px solid {CCColors.BORDER_LIGHT};
                border-radius: 4px;
                font-size: 13px;
                outline: none;
            }}
            QTreeView::item {{
                padding: 6px;
                border-bottom: 1px solid {CCColors.CONTENT_ALT};
            }}
            QTreeView::item:hover {{
                background-color: {CCColors.CONTENT_ALT};
            }}
            QTreeView::item:selected {{
                background-color: {CCColors.BLUE_PRIMARY};
                color: {CCColors.TEXT_LIGHT};
            }}
            QTreeView::branch {{
                background-color: {CCColors.CONTENT_BG};
            }}
            QTreeView::branch:has-children:closed {{
                image: url(:/icons/branch_closed.png);
            }}
            QTreeView::branch:has-children:open {{
                image: url(:/icons/branch_open.png);
            }}
        """

    @staticmethod
    def tab_widget() -> str:
        """Tab widget style (Windows/Applications)."""
        return f"""
            QTabWidget::pane {{
                border: 1px solid {CCColors.BORDER_LIGHT};
                background-color: {CCColors.CONTENT_BG};
                border-radius: 4px;
            }}
            QTabBar::tab {{
                background-color: {CCColors.CONTENT_ALT};
                color: {CCColors.TEXT_SECONDARY};
                padding: 10px 20px;
                margin-right: 2px;
                border: 1px solid {CCColors.BORDER_LIGHT};
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                font-weight: bold;
            }}
            QTabBar::tab:selected {{
                background-color: {CCColors.CONTENT_BG};
                color: {CCColors.TAB_ACTIVE};
                border-bottom: 2px solid {CCColors.TAB_ACTIVE};
            }}
            QTabBar::tab:hover {{
                background-color: {CCColors.CONTENT_BG};
            }}
        """

    @staticmethod
    def progress_bar() -> str:
        """Progress bar style (green fill)."""
        return f"""
            QProgressBar {{
                border: 1px solid {CCColors.BORDER_LIGHT};
                border-radius: 4px;
                background-color: {CCColors.PROGRESS_BG};
                text-align: center;
                height: 24px;
                font-weight: bold;
                color: {CCColors.TEXT_PRIMARY};
            }}
            QProgressBar::chunk {{
                background-color: {CCColors.PROGRESS_FILL};
                border-radius: 3px;
            }}
        """

    @staticmethod
    def info_panel() -> str:
        """Right-side info panel style."""
        return f"""
            QWidget {{
                background-color: {CCColors.CONTENT_BG};
                border: 1px solid {CCColors.BORDER_LIGHT};
                border-radius: 4px;
            }}
        """

    @staticmethod
    def group_box() -> str:
        """Group box style for sections."""
        return f"""
            QGroupBox {{
                border: 1px solid {CCColors.BORDER_LIGHT};
                border-radius: 4px;
                margin-top: 12px;
                padding-top: 12px;
                font-weight: bold;
                color: {CCColors.TEXT_PRIMARY};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 10px;
                padding: 0 5px;
            }}
        """

    @staticmethod
    def label_header() -> str:
        """Header label style."""
        return f"""
            QLabel {{
                color: {CCColors.TEXT_PRIMARY};
                font-size: 16px;
                font-weight: bold;
                padding: 8px;
            }}
        """

    @staticmethod
    def label_secondary() -> str:
        """Secondary/info label style."""
        return f"""
            QLabel {{
                color: {CCColors.TEXT_SECONDARY};
                font-size: 12px;
                padding: 4px;
            }}
        """


# Icon definitions using FontAwesome (qtawesome)
class CCIcons:
    """CCleaner-style FontAwesome icon names."""

    # Main navigation (fa5s = FontAwesome 5 Solid)
    CLEANER = "fa5s.broom"           # Cleaner/broom
    REGISTRY = "fa5s.database"       # Registry/database
    TOOLS = "fa5s.wrench"            # Tools
    OPTIONS = "fa5s.cog"             # Options/settings
    UPGRADE = "fa5s.arrow-up"        # Upgrade

    # Tabs
    WINDOWS = "fa5b.windows"         # Windows logo (brands)
    APPLICATIONS = "fa5s.th"         # Applications grid

    # Browsers (brands)
    BROWSER_CHROME = "fa5b.chrome"   # Chrome
    BROWSER_FIREFOX = "fa5b.firefox" # Firefox
    BROWSER_EDGE = "fa5b.edge"       # Edge
    BROWSER_OPERA = "fa5b.opera"     # Opera
    BROWSER_GENERIC = "fa5s.globe"   # Generic browser

    # Tree/List
    CHECKMARK = "fa5s.check"         # Checked
    ARROW_DOWN = "fa5s.caret-down"   # Collapsed
    ARROW_RIGHT = "fa5s.caret-right" # Expanded

    # Status
    INFO = "fa5s.info-circle"        # Information
    WARNING = "fa5s.exclamation-triangle"  # Warning
    SUCCESS = "fa5s.check-circle"    # Success
    ERROR = "fa5s.times-circle"      # Error

    # Actions
    ANALYZE = "fa5s.search"          # Analyze/search
    CLEAN = "fa5s.trash-alt"         # Clean/delete
    REFRESH = "fa5s.sync"            # Refresh


__all__ = [
    "CCColors",
    "CCStyles",
    "CCIcons",
]
