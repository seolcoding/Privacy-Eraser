from __future__ import annotations

import os
import platform
import sys
from datetime import datetime

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTabWidget, QTextEdit
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from .app_state import app_state


def _collect_variables() -> list[tuple[str, str]]:
    """Collect system and application variables for debugging"""
    try:
        from . import __version__ as app_version
    except Exception:
        app_version = "unknown"
    return [
        ("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        ("app_version", app_version),
        ("python", sys.version.split()[0]),
        ("platform", platform.platform()),
        ("cwd", os.getcwd()),
        ("venv", os.environ.get("VIRTUAL_ENV", "")),
        ("ui_mode", str(app_state.ui_mode)),
        ("wizard_step", str(app_state.wizard_step)),
        ("scanned_programs_count", str(len(app_state.scanned_programs))),
    ]


class DebugPanel(QWidget):
    """Debug panel with Variables and Console tabs"""
    
    # Signal to append to console
    console_append_requested = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(280)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # --- Variables Tab ---
        variables_widget = QWidget()
        variables_layout = QVBoxLayout(variables_widget)
        variables_layout.setContentsMargins(8, 8, 8, 8)
        
        # Variables text display
        self.variables_display = QTextEdit()
        self.variables_display.setReadOnly(True)
        self.variables_display.setFont(QFont("Consolas", 10))
        variables_layout.addWidget(self.variables_display)
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setFixedSize(100, 28)
        refresh_btn.clicked.connect(self.refresh_variables)
        variables_layout.addWidget(refresh_btn, alignment=Qt.AlignRight)
        
        self.tab_widget.addTab(variables_widget, "Variables")
        
        # --- Console Tab ---
        console_widget = QWidget()
        console_layout = QVBoxLayout(console_widget)
        console_layout.setContentsMargins(8, 8, 8, 8)
        
        # Console text display
        self.console_textbox = QTextEdit()
        self.console_textbox.setReadOnly(True)
        self.console_textbox.setFont(QFont("Consolas", 10))
        console_layout.addWidget(self.console_textbox)
        
        # Clear button
        clear_btn = QPushButton("🗑️ Clear")
        clear_btn.setFixedSize(100, 28)
        clear_btn.clicked.connect(self.clear_console)
        console_layout.addWidget(clear_btn, alignment=Qt.AlignRight)
        
        self.tab_widget.addTab(console_widget, "Console")
        
        # Wire the signal to append function
        self.console_append_requested.connect(self._append_console_safe)
        
        # Initial populate
        self.refresh_variables()
    
    def refresh_variables(self):
        """Refresh the variables display"""
        try:
            self.variables_display.clear()
            for key, value in _collect_variables():
                self.variables_display.append(f"{key:25s}: {value}")
        except Exception:
            # Widget may have been destroyed
            pass
    
    def append_console(self, text: str):
        """Append text to console (thread-safe via signal)"""
        self.console_append_requested.emit(text)
    
    def _append_console_safe(self, text: str):
        """Internal method to append to console (runs in GUI thread)"""
        try:
            self.console_textbox.moveCursor(self.console_textbox.textCursor().End)
            self.console_textbox.insertPlainText(text)
            self.console_textbox.moveCursor(self.console_textbox.textCursor().End)
        except Exception:
            # Widget may have been destroyed during UI mode switching
            pass
    
    def clear_console(self):
        """Clear the console display"""
        try:
            self.console_textbox.clear()
        except Exception:
            # Widget may have been destroyed
            pass


def toggle_debug_panel(debug_panel: DebugPanel, is_visible: bool) -> bool:
    """Toggle debug panel visibility"""
    if debug_panel is None:
        return is_visible
    
    if is_visible:
        debug_panel.hide()
        return False
    else:
        debug_panel.show()
        debug_panel.refresh_variables()
        return True


__all__ = ["DebugPanel", "toggle_debug_panel"]
