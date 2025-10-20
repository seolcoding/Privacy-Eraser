from __future__ import annotations

import io
import logging
import os
import platform
import sys
from datetime import datetime

from loguru import logger
from rich.console import Console
from rich.traceback import install as rich_install

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QStackedWidget, QFrame
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

try:
    from qt_material import apply_stylesheet
    HAS_QT_MATERIAL = True
except ImportError:
    HAS_QT_MATERIAL = False

try:
    import qtawesome as qta
    HAS_QT_AWESOME = True
except ImportError:
    HAS_QT_AWESOME = False

from .app_state import app_state
from .settings_db import init_settings_db, load_setting, save_setting
from .gui_easy_mode import build_wizard_ui
from .gui_advanced_mode import build_advanced_ui
from .gui_settings import open_settings_dialog
from .gui_debug import DebugPanel, toggle_debug_panel
from .gui_widgets import SegmentedButton
from .gui_integration import run_scan


class _TextWidgetWriter:
    """Writer that appends to GUI console"""
    
    def __init__(self, append_callable):
        self._append = append_callable
    
    def write(self, message: str) -> None:
        if message:
            self._append(message)
    
    def flush(self) -> None:
        pass


class _TkTextHandler(logging.Handler):
    """Logging handler for GUI console"""
    
    def __init__(self, append_callable):
        super().__init__()
        self._append = append_callable
    
    def emit(self, record: logging.LogRecord) -> None:
        msg = self.format(record)
        self._append(msg + "\n")


def _configure_logging(append_console) -> None:
    """Configure loguru and rich logging"""
    rich_console = Console()
    
    class InterceptHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            try:
                level = logger.level(record.levelname).name
            except Exception:
                level = record.levelno
            logger.opt(depth=6, exception=record.exc_info).log(level, record.getMessage())
    
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    
    logger.remove()
    logger.add(
        lambda msg: rich_console.print(msg, end=""),
        level="INFO",
        colorize=True,
        backtrace=True,
        diagnose=False,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
               "<level>{message}</level>",
    )
    logger.add(
        lambda msg: append_console(str(msg)),
        level="INFO",
        format="[ {time:HH:mm:ss} ] {level}: {message}",
    )
    rich_install(show_locals=False)


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Load settings
        init_settings_db()
        app_state.ui_mode = load_setting("ui_mode", "easy")
        app_state.appearance_mode = load_setting("appearance_mode", "system")
        debug_enabled_str = load_setting("debug_enabled", "false")
        app_state.debug_enabled = debug_enabled_str == "true"
        
        # Window setup
        self.setWindowTitle("프라이버시 이레이저")
        self.setMinimumSize(900, 600)
        self.resize(1000, 700)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        
        # Main layout
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(6)
        
        # Header bar
        header = self._create_header()
        main_layout.addWidget(header)
        
        # Content area (stacked widget for mode switching)
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack, 1)
        
        # Build mode UIs
        self.wizard_widget = build_wizard_ui()
        self.advanced_widget = build_advanced_ui()
        
        self.content_stack.addWidget(self.wizard_widget)  # Index 0
        self.content_stack.addWidget(self.advanced_widget)  # Index 1
        
        # Set initial mode
        self._set_mode_ui(app_state.ui_mode)
        
        # Debug panel
        self.debug_panel = DebugPanel()
        main_layout.addWidget(self.debug_panel)
        
        # Configure logging to debug console
        _configure_logging(self.debug_panel.append_console)
        
        # Show debug panel if enabled
        if app_state.debug_enabled:
            self.debug_panel.show()
        else:
            self.debug_panel.hide()
        
        # Log startup
        logger.info(f"PrivacyEraser started ({app_state.ui_mode.capitalize()} Mode)")
        try:
            from .diagnostics import emit_startup_placeholders
            emit_startup_placeholders()
        except Exception as e:
            logger.warning(f"diagnostics failed: {e}")

        # Trigger an initial browser scan once the event loop starts
        QTimer.singleShot(0, run_scan)
        
        # Connect signals
        app_state.ui_mode_changed.connect(self._on_mode_changed)
        app_state.debug_enabled_changed.connect(self._on_debug_toggled)
    
    def _create_header(self) -> QFrame:
        """Create the header bar with title and controls"""
        header = QFrame()
        header.setFrameShape(QFrame.StyledPanel)
        header.setFixedHeight(60)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(16, 10, 16, 10)
        
        # Title
        title = QLabel("프라이버시 이레이저")
        title.setStyleSheet("font-size: 22px; font-weight: 700;")
        layout.addWidget(title)
        
        layout.addStretch()
        
        # Mode toggle
        self.mode_toggle = SegmentedButton(["쉬운 모드", "고급 모드"])
        self.mode_toggle.set_current_index(0 if app_state.ui_mode == "easy" else 1)
        self.mode_toggle.current_changed.connect(self._on_mode_toggle_changed)
        layout.addWidget(self.mode_toggle)
        
        # Settings button
        settings_btn = QPushButton("설정")
        settings_btn.clicked.connect(self._open_settings)
        
        # Add icon if qtawesome is available
        if HAS_QT_AWESOME:
            settings_btn.setIcon(qta.icon('fa5s.cog'))
            settings_btn.setText("설정")
        
        layout.addWidget(settings_btn)
        
        return header
    
    def _set_mode_ui(self, mode: str):
        """Switch the UI mode"""
        if mode == "easy":
            self.content_stack.setCurrentIndex(0)
            self.mode_toggle.set_current_index(0)
        else:
            self.content_stack.setCurrentIndex(1)
            self.mode_toggle.set_current_index(1)
    
    def _on_mode_toggle_changed(self, index: int):
        """Handle mode toggle change"""
        new_mode = "easy" if index == 0 else "advanced"
        if new_mode != app_state.ui_mode:
            app_state.ui_mode = new_mode
            save_setting("ui_mode", new_mode)
            self._set_mode_ui(new_mode)
            logger.info(f"ui> switched to {new_mode} mode")
    
    def _on_mode_changed(self, new_mode: str):
        """Handle mode change from app state"""
        self._set_mode_ui(new_mode)
    
    def _on_debug_toggled(self, enabled: bool):
        """Handle debug panel toggle"""
        if enabled:
            self.debug_panel.show()
            self.debug_panel.refresh_variables()
        else:
            self.debug_panel.hide()
    
    def _open_settings(self):
        """Open settings dialog"""
        dialog = open_settings_dialog(self)
        
        # Connect signals
        dialog.theme_changed.connect(self._apply_theme)
        dialog.ui_mode_changed.connect(self._on_settings_mode_changed)
        dialog.debug_toggled.connect(self._on_debug_toggled)
        
        dialog.exec()
    
    def _on_settings_mode_changed(self, new_mode: str):
        """Handle mode change from settings"""
        app_state.ui_mode = new_mode
        self._set_mode_ui(new_mode)
    
    def _apply_theme(self, theme: str):
        """Apply the selected theme"""
        app_state.appearance_mode = theme
        save_setting("appearance_mode", theme)
        
        if HAS_QT_MATERIAL:
            app = QApplication.instance()
            if app:
                if theme == "dark":
                    apply_stylesheet(app, theme='dark_blue.xml')
                elif theme == "light":
                    apply_stylesheet(app, theme='light_blue.xml')
                else:
                    # System theme - detect and apply
                    apply_stylesheet(app, theme='dark_blue.xml')
        
        logger.info(f"Applied theme: {theme}")


def switch_ui_mode(new_mode: str) -> None:
    """Switch UI mode (compatibility function)"""
    try:
        mode = "advanced" if str(new_mode).lower().startswith("adv") else "easy"
        prev = app_state.ui_mode
        app_state.ui_mode = mode
        logger.info(f"ui> switched from {prev} to {mode}")
    except Exception as e:
        logger.warning(f"ui> switch_ui_mode failed: {e}")


def run_gui() -> int:
    """Run the PySide6 GUI application (daemon mode integration)"""
    try:
        from .daemon import get_daemon

        # 데몬 인스턴스 가져오기
        daemon = get_daemon()

        # GUI 모드로 실행
        return daemon.run_gui_mode()

    except Exception as e:
        logger.error(f"Failed to run GUI: {e}")
        return 1


def create_main_window() -> MainWindow:
    """메인 윈도우 생성 (데몬과 분리된 경우 사용)"""
    app = QApplication.instance()
    if app is None:
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
        QApplication([])
    return MainWindow()


__all__ = ["run_gui", "switch_ui_mode"]
