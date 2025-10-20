#!/usr/bin/env python3
"""Launch CCleaner-style GUI for PrivacyEraser.

Usage:
    uv run python run_ccleaner_ui.py
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt
from loguru import logger

# Configure logging
logger.remove()
logger.add(
    sys.stderr,
    level="INFO",
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>"
)

from src.privacy_eraser.gui_ccleaner_style import CCleanerMainWidget
from src.privacy_eraser.ccleaner_theme import CCColors


class CCleanerWindow(QMainWindow):
    """Main window for CCleaner-style UI."""

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """Set up window."""
        self.setWindowTitle("PrivacyEraser - Browser Cleaner")
        self.setGeometry(100, 100, 600, 350)  # 0.5x size (was 1200x700)

        # Set window style
        self.setStyleSheet(f"background-color: {CCColors.CONTENT_BG};")

        # Create main widget
        main_widget = CCleanerMainWidget()
        self.setCentralWidget(main_widget)


def main():
    """Main entry point."""
    logger.info("Starting CCleaner-style UI...")

    app = QApplication(sys.argv)
    app.setApplicationName("PrivacyEraser")

    # Create and show window
    window = CCleanerWindow()
    window.show()

    logger.info("GUI launched successfully")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
