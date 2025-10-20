from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget, QFrame, QLabel, QPushButton, QCheckBox,
    QVBoxLayout, QHBoxLayout, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QPalette

try:
    import qtawesome as qta
    HAS_QT_AWESOME = True
except ImportError:  # pragma: no cover - optional dependency
    HAS_QT_AWESOME = False


# Material Design Color Palette
class Colors:
    """Material Design color constants"""
    # Primary
    PRIMARY = "#667eea"
    PRIMARY_HOVER = "#5568d3"
    PRIMARY_LIGHT = "#818cf8"
    PRIMARY_DARK = "#4c51bf"
    
    # Success
    SUCCESS = "#10b981"
    SUCCESS_HOVER = "#059669"
    
    # Warning
    WARNING = "#fbbf24"
    WARNING_BG = "#fef3c7"
    WARNING_TEXT = "#92400e"
    
    # Danger
    DANGER = "#ef4444"
    DANGER_HOVER = "#dc2626"
    
    # Gray Scale
    GRAY = "#6c757d"
    GRAY_LIGHT = "#f8f9fa"
    GRAY_DARK = "#343a40"
    BORDER = "#e9ecef"
    
    # Text
    TEXT = "#212529"
    TEXT_SECONDARY = "#6c757d"
    
    # Dark Mode
    DARK_BG = "#1e293b"
    DARK_SURFACE = "#334155"
    DARK_BORDER = "#475569"
    DARK_TEXT = "#f8f9fa"
    DARK_TEXT_SECONDARY = "#94a3b8"


class Badge(QLabel):
    """Styled status badge"""
    
    def __init__(self, text: str, color: str = Colors.SUCCESS, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {color};
                color: white;
                border-radius: 8px;
                padding: 2px 8px;
                font-size: 9px;
                font-weight: bold;
            }}
        """)
        self.setAlignment(Qt.AlignCenter)


class BrowserCard(QFrame):
    """Clickable browser card with icon, name, status, and checkbox"""
    
    clicked = Signal(str)  # Emits browser name
    selection_changed = Signal(str, bool)  # Emits (browser_name, checked)
    
    def __init__(self, browser_data: dict, parent=None):
        super().__init__(parent)
        self.browser_data = browser_data
        self.browser_name = browser_data.get("name", "")
        
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setFixedSize(180, 160)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        
        # Icon
        icon_label = QLabel()
        icon_label.setFixedSize(44, 44)
        icon_label.setAlignment(Qt.AlignCenter)

        fa_icon = browser_data.get("fa_icon")
        icon_letter = browser_data.get("icon", "?")
        icon_color = browser_data.get("color", "#2d7dd2")

        if HAS_QT_AWESOME and fa_icon:
            qicon = qta.icon(fa_icon, color=icon_color)
            icon_label.setPixmap(qicon.pixmap(36, 36))
        else:
            icon_label.setText(icon_letter)
            icon_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        layout.addWidget(icon_label, alignment=Qt.AlignHCenter)
        
        # Name
        name_label = QLabel(self.browser_name)
        name_label.setStyleSheet("font-size: 15px; font-weight: bold; margin-top: 6px;")
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setWordWrap(True)
        layout.addWidget(name_label)
        
        # Status badge
        status = browser_data.get("status", "Not Found")
        present = bool(browser_data.get("present", False))
        status_badge = Badge(status, Colors.SUCCESS if present else Colors.GRAY)
        layout.addWidget(status_badge, alignment=Qt.AlignHCenter)
        
        layout.addStretch()
        
        # Checkbox
        self.checkbox = QCheckBox("선택")
        self.checkbox.setStyleSheet("QCheckBox { font-size: 13px; }")
        self.checkbox.setEnabled(present)
        self.checkbox.stateChanged.connect(self._on_checkbox_changed)
        layout.addWidget(self.checkbox, alignment=Qt.AlignHCenter)
        
        self.setCursor(Qt.PointingHandCursor if present else Qt.ForbiddenCursor)
    
    def _on_checkbox_changed(self, state):
        checked = Qt.CheckState(state) == Qt.CheckState.Checked
        self.selection_changed.emit(self.browser_name, checked)
    
    def mousePressEvent(self, event):
        if self.browser_data.get("present", False):
            self.checkbox.setChecked(not self.checkbox.isChecked())
            self.clicked.emit(self.browser_name)
        super().mousePressEvent(event)
    
    def is_checked(self) -> bool:
        return self.checkbox.isChecked()
    
    def set_checked(self, checked: bool):
        self.checkbox.setChecked(checked)


class OptionCard(QFrame):
    """Cleaner option card with checkbox, icon, title, description, and size"""
    
    selection_changed = Signal(str, bool)  # Emits (option_id, checked)
    
    def __init__(self, option_data: dict, parent=None):
        super().__init__(parent)
        self.option_data = option_data
        self.option_id = option_data.get("id", "")
        
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("""
            OptionCard {
                background-color: white;
                border: 1px solid #d1d5db;
                border-radius: 10px;
            }
            OptionCard:hover {
                border-color: #4f46e5;
                background-color: #f5f6ff;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        
        # Checkbox
        self.checkbox = QCheckBox()
        self.checkbox.setFixedSize(22, 22)
        self.checkbox.setStyleSheet("QCheckBox { font-size: 13px; }")
        self.checkbox.stateChanged.connect(self._on_checkbox_changed)
        layout.addWidget(self.checkbox)
        
        # Icon (optional)
        if "icon" in option_data:
            icon_label = QLabel(option_data["icon"])
            icon_label.setStyleSheet("""
                QLabel {
                    background-color: #4f46e5;
                    color: white;
                    border-radius: 10px;
                    font-size: 24px;
                    padding: 10px;
                }
            """)
            icon_label.setFixedSize(48, 48)
            icon_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(icon_label)
        
        # Details (title + description + stats)
        details_layout = QVBoxLayout()
        details_layout.setSpacing(3)
        
        # Title
        title_label = QLabel(option_data.get("label", ""))
        title_label.setStyleSheet("font-size: 15px; font-weight: bold;")
        details_layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(option_data.get("description", ""))
        desc_label.setStyleSheet("font-size: 12px; color: #4b5563;")
        desc_label.setWordWrap(True)
        details_layout.addWidget(desc_label)
        
        # Stats (optional)
        if "file_count" in option_data or "last_cleaned" in option_data:
            stats_text = f"{option_data.get('file_count', 'N/A')} files • Last cleaned: {option_data.get('last_cleaned', 'Never')}"
            stats_label = QLabel(stats_text)
            stats_label.setStyleSheet("font-size: 9px; color: #6c757d;")
            details_layout.addWidget(stats_label)
        
        layout.addLayout(details_layout, 1)
        
        # Size indicator
        size_label = QLabel(option_data.get("size", "정보 없음"))
        size_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #4f46e5;")
        size_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(size_label)
    
    def _on_checkbox_changed(self, state):
        checked = Qt.CheckState(state) == Qt.CheckState.Checked
        self.selection_changed.emit(self.option_id, checked)
    
    def mousePressEvent(self, event):
        self.checkbox.setChecked(not self.checkbox.isChecked())
        super().mousePressEvent(event)
    
    def is_checked(self) -> bool:
        return self.checkbox.isChecked()
    
    def set_checked(self, checked: bool):
        self.checkbox.setChecked(checked)


class SegmentedButton(QWidget):
    """iOS-style segmented button control"""
    
    current_changed = Signal(int)  # Emits index of selected segment
    
    def __init__(self, options: list[str], parent=None):
        super().__init__(parent)
        self.options = options
        self.buttons = []
        self.current_index = 0
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        for i, option in enumerate(options):
            btn = QPushButton(option)
            btn.setCheckable(True)
            btn.setFixedHeight(38)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setStyleSheet("QPushButton { font-size: 14px; }")
            btn.clicked.connect(lambda checked, idx=i: self._on_button_clicked(idx))
            self.buttons.append(btn)
            layout.addWidget(btn)
        
        if self.buttons:
            self.buttons[0].setChecked(True)
        
        self._update_styles()
    
    def _on_button_clicked(self, index: int):
        self.set_current_index(index)
    
    def set_current_index(self, index: int):
        if 0 <= index < len(self.buttons) and index != self.current_index:
            self.current_index = index
            for i, btn in enumerate(self.buttons):
                btn.setChecked(i == index)
            self._update_styles()
            self.current_changed.emit(index)
    
    def current_text(self) -> str:
        return self.options[self.current_index] if self.current_index < len(self.options) else ""
    
    def _update_styles(self):
        for i, btn in enumerate(self.buttons):
            border_radius = ""
            if i == 0:
                border_radius = "border-top-left-radius: 8px; border-bottom-left-radius: 8px;"
            elif i == len(self.buttons) - 1:
                border_radius = "border-top-right-radius: 8px; border-bottom-right-radius: 8px;"

            pal = btn.palette()
            if btn.isChecked():
                active_bg = pal.color(QPalette.ColorRole.Highlight).name()
                active_fg = pal.color(QPalette.ColorRole.HighlightedText).name()
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {active_bg};
                        color: {active_fg};
                        border: 1px solid {active_bg};
                        {border_radius}
                        font-weight: bold;
                        padding: 5px 14px;
                    }}
                    """)
            else:
                inactive_bg = pal.color(QPalette.ColorRole.Button).name()
                inactive_fg = pal.color(QPalette.ColorRole.ButtonText).name()
                border_color = pal.color(QPalette.ColorRole.Mid).name()
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {inactive_bg};
                        color: {inactive_fg};
                        border: 1px solid {border_color};
                        {border_radius}
                        padding: 5px 14px;
                    }}
                    """)


class StepIndicator(QWidget):
    """Custom progress indicator for wizard steps"""
    
    def __init__(self, steps: list[str], parent=None):
        super().__init__(parent)
        self.steps = steps
        self.current_step = 0
        self.setMinimumHeight(88)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        
        self.step_widgets = []
        for i, step_name in enumerate(steps):
            step_layout = QVBoxLayout()
            step_layout.setAlignment(Qt.AlignCenter)
            
            # Circle
            circle = QLabel(str(i + 1))
            circle.setFixedSize(44, 44)
            circle.setAlignment(Qt.AlignCenter)
            circle.setStyleSheet("""
                QLabel {
                    background-color: #94a3b8;
                    color: white;
                    border-radius: 22px;
                    font-size: 18px;
                    font-weight: bold;
                }
            """)
            step_layout.addWidget(circle, alignment=Qt.AlignHCenter)
            
            # Label
            label = QLabel(step_name)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("font-size: 14px; color: #475569; margin-top: 6px;")
            step_layout.addWidget(label)
            
            self.step_widgets.append((circle, label))
            layout.addLayout(step_layout)
            
            # Add connector line (except for last step)
            if i < len(steps) - 1:
                layout.addStretch()
    
    def set_current_step(self, step: int):
        self.current_step = step
        palette = self.palette()
        active_bg = palette.color(QPalette.ColorRole.Highlight).name()
        active_fg = palette.color(QPalette.ColorRole.HighlightedText).name()
        inactive_bg = palette.color(QPalette.ColorRole.Button).name()
        inactive_fg = palette.color(QPalette.ColorRole.ButtonText).name()
        for i, (circle, label) in enumerate(self.step_widgets):
            if i <= step:
                # Active/completed
                circle.setStyleSheet(f"""
                    QLabel {{
                        background-color: {active_bg};
                        color: {active_fg};
                        border-radius: 22px;
                        font-size: 18px;
                        font-weight: bold;
                    }}
                """)
                label.setStyleSheet(f"font-size: 14px; font-weight: bold; color: {active_bg}; margin-top: 6px;")
            else:
                # Pending
                circle.setStyleSheet(f"""
                    QLabel {{
                        background-color: {inactive_bg};
                        color: {inactive_fg};
                        border-radius: 22px;
                        font-size: 18px;
                        font-weight: bold;
                    }}
                """)
                label.setStyleSheet(f"font-size: 14px; color: {inactive_fg}; margin-top: 6px;")


__all__ = [
    "Colors",
    "Badge",
    "BrowserCard",
    "OptionCard",
    "SegmentedButton",
    "StepIndicator",
]
