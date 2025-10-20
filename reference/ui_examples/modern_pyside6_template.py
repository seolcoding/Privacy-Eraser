"""
Modern PySide6 UI Template
==========================

A production-ready template demonstrating modern UI patterns and best practices
for the Privacy Eraser application.

Features:
- Clean, modern design with Material-inspired components
- Sidebar navigation + main content layout
- Card-based UI components
- Dark/Light theme support
- Smooth animations
- Responsive design
- Accessibility support

Usage:
    python modern_pyside6_template.py
"""

import sys
from typing import Optional
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame, QScrollArea, QGraphicsDropShadowEffect,
    QStackedWidget, QSizePolicy
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize, QRect
from PySide6.QtGui import QFont, QPalette, QColor, QIcon


# ============================================================================
# Design Tokens
# ============================================================================

class Colors:
    """Color palette following Material Design principles"""
    # Light Theme
    PRIMARY = "#2196F3"
    PRIMARY_DARK = "#1976D2"
    PRIMARY_LIGHT = "#BBDEFB"
    
    SUCCESS = "#4CAF50"
    WARNING = "#FF9800"
    DANGER = "#F44336"
    INFO = "#2196F3"
    
    BACKGROUND = "#FFFFFF"
    SURFACE = "#F5F5F5"
    BORDER = "#E0E0E0"
    TEXT_PRIMARY = "#212121"
    TEXT_SECONDARY = "#757575"
    
    # Dark Theme
    BACKGROUND_DARK = "#121212"
    SURFACE_DARK = "#1E1E1E"
    BORDER_DARK = "#2C2C2C"
    TEXT_PRIMARY_DARK = "#FFFFFF"
    TEXT_SECONDARY_DARK = "#B0B0B0"


class Spacing:
    """Consistent spacing based on 8px grid"""
    XS = 4
    SM = 8
    MD = 16
    LG = 24
    XL = 32
    XXL = 48


class Typography:
    """Font styles and sizes"""
    FAMILY = "Segoe UI"
    FAMILY_MONO = "Consolas"
    
    SIZE_XS = 10
    SIZE_SM = 11
    SIZE_MD = 12
    SIZE_LG = 14
    SIZE_XL = 18
    SIZE_XXL = 24
    SIZE_XXXL = 32
    
    WEIGHT_LIGHT = 300
    WEIGHT_REGULAR = 400
    WEIGHT_MEDIUM = 500
    WEIGHT_SEMIBOLD = 600
    WEIGHT_BOLD = 700


# ============================================================================
# Reusable Components
# ============================================================================

class PrimaryButton(QPushButton):
    """Modern primary button with hover effects"""
    
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.setFont(QFont(Typography.FAMILY, Typography.SIZE_MD, Typography.WEIGHT_MEDIUM))
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(40)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.PRIMARY};
                color: white;
                border: none;
                border-radius: 4px;
                padding: {Spacing.SM}px {Spacing.MD}px;
            }}
            QPushButton:hover {{
                background-color: {Colors.PRIMARY_DARK};
            }}
            QPushButton:pressed {{
                background-color: #1565C0;
            }}
            QPushButton:disabled {{
                background-color: #BDBDBD;
                color: #757575;
            }}
        """)


class SecondaryButton(QPushButton):
    """Outlined button for secondary actions"""
    
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.setFont(QFont(Typography.FAMILY, Typography.SIZE_MD))
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(40)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {Colors.PRIMARY};
                border: 2px solid {Colors.PRIMARY};
                border-radius: 4px;
                padding: {Spacing.SM}px {Spacing.MD}px;
            }}
            QPushButton:hover {{
                background-color: rgba(33, 150, 243, 0.08);
            }}
        """)


class Card(QFrame):
    """Card component with shadow for grouping content"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BACKGROUND};
                border: 1px solid {Colors.BORDER};
                border-radius: 8px;
                padding: {Spacing.MD}px;
            }}
        """)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(8)
        shadow.setColor(QColor(0, 0, 0, 25))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)


class SidebarButton(QPushButton):
    """Sidebar navigation button"""
    
    def __init__(self, text: str, icon_name: Optional[str] = None, parent=None):
        super().__init__(text, parent)
        self.icon_name = icon_name
        self.is_active = False
        self.setup_ui()
    
    def setup_ui(self):
        self.setFont(QFont(Typography.FAMILY, Typography.SIZE_MD))
        self.setCursor(Qt.PointingHandCursor)
        self.setCheckable(True)
        self.setMinimumHeight(44)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.update_style()
    
    def set_active(self, active: bool):
        self.is_active = active
        self.setChecked(active)
        self.update_style()
    
    def update_style(self):
        if self.is_active:
            bg_color = Colors.PRIMARY_LIGHT
            text_color = Colors.PRIMARY_DARK
            border_left = f"border-left: 4px solid {Colors.PRIMARY};"
        else:
            bg_color = "transparent"
            text_color = Colors.TEXT_PRIMARY
            border_left = "border-left: 4px solid transparent;"
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border: none;
                {border_left}
                border-radius: 0px;
                padding: {Spacing.SM}px {Spacing.MD}px;
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: rgba(33, 150, 243, 0.08);
            }}
        """)


class StatusCard(Card):
    """Card displaying a metric or status"""
    
    def __init__(self, title: str, value: str, color: str = Colors.PRIMARY, parent=None):
        super().__init__(parent)
        self.title_label = QLabel(title)
        self.value_label = QLabel(value)
        self.setup_content(color)
    
    def setup_content(self, color: str):
        layout = QVBoxLayout(self)
        layout.setSpacing(Spacing.SM)
        
        self.title_label.setFont(QFont(Typography.FAMILY, Typography.SIZE_LG, Typography.WEIGHT_SEMIBOLD))
        self.title_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        
        self.value_label.setFont(QFont(Typography.FAMILY, Typography.SIZE_XXL, Typography.WEIGHT_BOLD))
        self.value_label.setStyleSheet(f"color: {color};")
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        layout.addStretch()
    
    def update_value(self, value: str):
        self.value_label.setText(value)


# ============================================================================
# Main Application
# ============================================================================

class ModernMainWindow(QMainWindow):
    """Modern main window with sidebar navigation"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Privacy Eraser - Modern UI")
        self.setMinimumSize(1000, 700)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout (horizontal: sidebar + content)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create sidebar
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar)
        
        # Create content area
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet(f"background-color: {Colors.SURFACE};")
        main_layout.addWidget(self.content_stack)
        
        # Create pages
        self.dashboard_page = self.create_dashboard_page()
        self.browser_page = self.create_browser_page()
        self.system_page = self.create_system_page()
        
        self.content_stack.addWidget(self.dashboard_page)
        self.content_stack.addWidget(self.browser_page)
        self.content_stack.addWidget(self.system_page)
        
        # Apply theme
        self.apply_theme()
        
        # Initialize sidebar buttons
        self.sidebar_buttons[0].set_active(True)
    
    def create_sidebar(self) -> QWidget:
        """Create navigation sidebar"""
        sidebar = QFrame()
        sidebar.setFixedWidth(240)
        sidebar.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BACKGROUND};
                border-right: 1px solid {Colors.BORDER};
            }}
        """)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, Spacing.MD, 0, Spacing.MD)
        layout.setSpacing(Spacing.SM)
        
        # Logo/Title
        title = QLabel("Privacy Eraser")
        title.setFont(QFont(Typography.FAMILY, Typography.SIZE_XL, Typography.WEIGHT_BOLD))
        title.setStyleSheet(f"color: {Colors.PRIMARY}; padding: {Spacing.MD}px;")
        layout.addWidget(title)
        
        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet(f"background-color: {Colors.BORDER};")
        layout.addWidget(divider)
        
        # Navigation buttons
        self.sidebar_buttons = []
        
        dashboard_btn = SidebarButton("Dashboard")
        dashboard_btn.clicked.connect(lambda: self.switch_page(0))
        self.sidebar_buttons.append(dashboard_btn)
        layout.addWidget(dashboard_btn)
        
        browser_btn = SidebarButton("Browser Clean")
        browser_btn.clicked.connect(lambda: self.switch_page(1))
        self.sidebar_buttons.append(browser_btn)
        layout.addWidget(browser_btn)
        
        system_btn = SidebarButton("System Clean")
        system_btn.clicked.connect(lambda: self.switch_page(2))
        self.sidebar_buttons.append(system_btn)
        layout.addWidget(system_btn)
        
        layout.addStretch()
        
        # Settings button (bottom)
        settings_btn = SidebarButton("Settings")
        layout.addWidget(settings_btn)
        
        return sidebar
    
    def create_dashboard_page(self) -> QWidget:
        """Create dashboard page with statistics"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(Spacing.XL, Spacing.XL, Spacing.XL, Spacing.XL)
        layout.setSpacing(Spacing.LG)
        
        # Page title
        title = QLabel("Dashboard")
        title.setFont(QFont(Typography.FAMILY, Typography.SIZE_XXL, Typography.WEIGHT_BOLD))
        layout.addWidget(title)
        
        # Status cards row
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(Spacing.MD)
        
        total_cleaned = StatusCard("Total Cleaned", "2.4 GB", Colors.SUCCESS)
        last_clean = StatusCard("Last Clean", "2 hours ago", Colors.INFO)
        browsers_found = StatusCard("Browsers Found", "4", Colors.PRIMARY)
        
        cards_layout.addWidget(total_cleaned)
        cards_layout.addWidget(last_clean)
        cards_layout.addWidget(browsers_found)
        
        layout.addLayout(cards_layout)
        
        # Recent activity card
        activity_card = Card()
        activity_layout = QVBoxLayout(activity_card)
        
        activity_title = QLabel("Recent Activity")
        activity_title.setFont(QFont(Typography.FAMILY, Typography.SIZE_LG, Typography.WEIGHT_SEMIBOLD))
        activity_layout.addWidget(activity_title)
        
        activity_text = QLabel("No recent cleaning activity.\nClick 'Browser Clean' to get started.")
        activity_text.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        activity_text.setFont(QFont(Typography.FAMILY, Typography.SIZE_MD))
        activity_layout.addWidget(activity_text)
        
        layout.addWidget(activity_card)
        layout.addStretch()
        
        return page
    
    def create_browser_page(self) -> QWidget:
        """Create browser cleaning page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(Spacing.XL, Spacing.XL, Spacing.XL, Spacing.XL)
        layout.setSpacing(Spacing.LG)
        
        # Page title
        title = QLabel("Browser Clean")
        title.setFont(QFont(Typography.FAMILY, Typography.SIZE_XXL, Typography.WEIGHT_BOLD))
        layout.addWidget(title)
        
        subtitle = QLabel("Clean browser cache, cookies, history, and more")
        subtitle.setFont(QFont(Typography.FAMILY, Typography.SIZE_MD))
        subtitle.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        layout.addWidget(subtitle)
        
        # Controls
        controls_layout = QHBoxLayout()
        scan_btn = PrimaryButton("Scan Browsers")
        preview_btn = SecondaryButton("Preview")
        clean_btn = PrimaryButton("Clean Now")
        
        controls_layout.addWidget(scan_btn)
        controls_layout.addWidget(preview_btn)
        controls_layout.addStretch()
        controls_layout.addWidget(clean_btn)
        
        layout.addLayout(controls_layout)
        
        # Content card
        content_card = Card()
        content_layout = QVBoxLayout(content_card)
        
        placeholder = QLabel("Click 'Scan Browsers' to detect installed browsers")
        placeholder.setFont(QFont(Typography.FAMILY, Typography.SIZE_MD))
        placeholder.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; padding: {Spacing.XXL}px;")
        placeholder.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(placeholder)
        
        layout.addWidget(content_card, 1)
        
        return page
    
    def create_system_page(self) -> QWidget:
        """Create system cleaning page (WinClean scripts)"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(Spacing.XL, Spacing.XL, Spacing.XL, Spacing.XL)
        layout.setSpacing(Spacing.LG)
        
        # Page title
        title = QLabel("System Clean")
        title.setFont(QFont(Typography.FAMILY, Typography.SIZE_XXL, Typography.WEIGHT_BOLD))
        layout.addWidget(title)
        
        subtitle = QLabel("Optimize Windows with privacy and performance scripts")
        subtitle.setFont(QFont(Typography.FAMILY, Typography.SIZE_MD))
        subtitle.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        layout.addWidget(subtitle)
        
        # WinClean scripts card
        scripts_card = Card()
        scripts_layout = QVBoxLayout(scripts_card)
        
        scripts_title = QLabel("Available Scripts")
        scripts_title.setFont(QFont(Typography.FAMILY, Typography.SIZE_LG, Typography.WEIGHT_SEMIBOLD))
        scripts_layout.addWidget(scripts_title)
        
        # Example script items
        script_items = [
            "Disable telemetry and data collection",
            "Clear File Explorer history",
            "Remove useless apps",
            "Stop apps from running in the background",
        ]
        
        for item in script_items:
            item_label = QLabel(f"• {item}")
            item_label.setFont(QFont(Typography.FAMILY, Typography.SIZE_MD))
            scripts_layout.addWidget(item_label)
        
        layout.addWidget(scripts_card, 1)
        
        return page
    
    def switch_page(self, index: int):
        """Switch to a different page and update sidebar"""
        self.content_stack.setCurrentIndex(index)
        
        # Update sidebar button states
        for i, btn in enumerate(self.sidebar_buttons):
            btn.set_active(i == index)
        
        # Animate transition (optional)
        self.animate_page_transition()
    
    def animate_page_transition(self):
        """Add smooth page transition animation"""
        current_widget = self.content_stack.currentWidget()
        
        # Fade animation
        animation = QPropertyAnimation(current_widget, b"windowOpacity")
        animation.setDuration(150)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        animation.start()
    
    def apply_theme(self):
        """Apply light theme to the application"""
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(Colors.SURFACE))
        palette.setColor(QPalette.WindowText, QColor(Colors.TEXT_PRIMARY))
        palette.setColor(QPalette.Base, QColor(Colors.BACKGROUND))
        palette.setColor(QPalette.Text, QColor(Colors.TEXT_PRIMARY))
        palette.setColor(QPalette.Button, QColor(Colors.PRIMARY))
        palette.setColor(QPalette.ButtonText, QColor("#FFFFFF"))
        
        self.setPalette(palette)


# ============================================================================
# Application Entry Point
# ============================================================================

def main():
    """Run the modern UI demo"""
    app = QApplication(sys.argv)
    
    # Set application-wide font
    app.setFont(QFont(Typography.FAMILY, Typography.SIZE_MD))
    
    # Create and show main window
    window = ModernMainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

