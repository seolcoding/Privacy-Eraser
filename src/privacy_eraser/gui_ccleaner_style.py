"""CCleaner-style main GUI for PrivacyEraser.

Browser-focused privacy cleaner with CCleaner's classic interface design.
"""

from __future__ import annotations

import os
from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QTabWidget,
    QTreeWidget,
    QTreeWidgetItem,
    QCheckBox,
    QProgressBar,
    QTextEdit,
    QGroupBox,
    QSplitter,
    QScrollArea,
)
from PySide6.QtGui import QFont, QIcon
from loguru import logger
import qtawesome as qta

from .ccleaner_theme import CCColors, CCStyles, CCIcons
from .app_state import app_state
from .gui_integration import run_scan, load_cleaner_options

# Check if using mock data
USE_MOCK = os.name != "nt"


class CCleanerSidebar(QWidget):
    """Left sidebar with navigation buttons (CCleaner style)."""

    cleaner_clicked = Signal()
    registry_clicked = Signal()
    tools_clicked = Signal()
    options_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_button = None
        self.setup_ui()

    def setup_ui(self):
        """Set up sidebar UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Set dark background
        self.setStyleSheet(f"background-color: {CCColors.SIDEBAR_BG};")
        self.setFixedWidth(80)  # Reduced from 160

        # Cleaner button (default selected)
        self.btn_cleaner = self._create_sidebar_button(
            CCIcons.CLEANER,
            "청소",
            self.cleaner_clicked.emit,
            selected=True
        )
        layout.addWidget(self.btn_cleaner)
        self.selected_button = self.btn_cleaner

        # Registry button
        self.btn_registry = self._create_sidebar_button(
            CCIcons.REGISTRY,
            "레지스트리",
            self.registry_clicked.emit
        )
        layout.addWidget(self.btn_registry)

        # Tools button
        self.btn_tools = self._create_sidebar_button(
            CCIcons.TOOLS,
            "도구",
            self.tools_clicked.emit
        )
        layout.addWidget(self.btn_tools)

        # Options button
        self.btn_options = self._create_sidebar_button(
            CCIcons.OPTIONS,
            "설정",
            self.options_clicked.emit
        )
        layout.addWidget(self.btn_options)

        # Stretch to push upgrade button to bottom
        layout.addStretch()

        # Upgrade button (at bottom)
        self.btn_upgrade = self._create_sidebar_button(
            CCIcons.UPGRADE,
            "업그레이드",
            lambda: logger.info("Upgrade clicked")
        )
        layout.addWidget(self.btn_upgrade)

    def _create_sidebar_button(self, icon_name: str, text: str, callback, selected: bool = False) -> QPushButton:
        """Create a sidebar button with CCleaner style and FontAwesome icon."""
        btn = QPushButton()

        # Create icon with qtawesome
        icon = qta.icon(icon_name, color=CCColors.TEXT_LIGHT)
        btn.setIcon(icon)
        btn.setIconSize(Qt.QSize(24, 24))  # Icon size 24x24
        btn.setText(text)

        btn.setStyleSheet(CCStyles.sidebar_button(selected))
        btn.setMinimumHeight(70)  # Reduced from 100
        btn.setFont(QFont("Arial", 8, QFont.Bold))  # Reduced font size
        btn.clicked.connect(callback)
        btn.clicked.connect(lambda: self._on_button_clicked(btn))
        return btn

    def _on_button_clicked(self, button: QPushButton):
        """Handle button selection."""
        if self.selected_button:
            self.selected_button.setStyleSheet(CCStyles.sidebar_button(False))

        button.setStyleSheet(CCStyles.sidebar_button(True))
        self.selected_button = button


class BrowserTreeWidget(QTreeWidget):
    """Tree widget for browser selection (CCleaner style)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """Set up tree widget."""
        self.setHeaderHidden(True)
        self.setStyleSheet(CCStyles.tree_view())
        self.setIndentation(20)
        self.setAnimated(True)

    def load_browsers(self, browsers: list[dict]):
        """Load browser data into tree."""
        self.clear()

        # Group browsers by type
        chromium_browsers = []
        firefox_browsers = []
        other_browsers = []

        for browser in browsers:
            name = browser.get("name", "")
            if "Chrome" in name or "Edge" in name or "Brave" in name or "Whale" in name:
                chromium_browsers.append(browser)
            elif "Firefox" in name:
                firefox_browsers.append(browser)
            else:
                other_browsers.append(browser)

        # Add Chromium group
        if chromium_browsers:
            for browser in chromium_browsers:
                self._add_browser_item(browser)

        # Add Firefox group
        if firefox_browsers:
            for browser in firefox_browsers:
                self._add_browser_item(browser)

        # Add others
        if other_browsers:
            for browser in other_browsers:
                self._add_browser_item(browser)

        # Expand all
        self.expandAll()

    def _add_browser_item(self, browser: dict):
        """Add browser item to tree."""
        name = browser.get("name", "Unknown")
        present = browser.get("present", False)

        # Create browser item
        browser_item = QTreeWidgetItem(self)
        browser_item.setText(0, f"  {name}")
        browser_item.setData(0, Qt.UserRole, browser)

        # Disable if not present
        if not present:
            browser_item.setForeground(0, Qt.gray)
            browser_item.setFlags(browser_item.flags() & ~Qt.ItemIsEnabled)
            return

        # Add cleaner options as children
        options = [
            ("임시 인터넷 파일", "cache", True),
            ("쿠키", "cookies", True),
            ("히스토리", "history", True),
            ("최근 입력한 URL", "session", True),
            ("세션", "session", True),
            ("저장된 비밀번호", "passwords", False),
            ("자동완성 양식 기록", "autofill", False),
        ]

        for label, option_id, default_checked in options:
            option_item = QTreeWidgetItem(browser_item)

            # Create checkbox widget
            checkbox = QCheckBox(label)
            checkbox.setStyleSheet(CCStyles.checkbox_orange())
            checkbox.setChecked(default_checked)
            checkbox.setProperty("browser_name", name)
            checkbox.setProperty("option_id", option_id)

            self.setItemWidget(option_item, 0, checkbox)


class AnalysisResultPanel(QWidget):
    """Right panel showing analysis results (CCleaner style)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """Set up analysis panel."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet(CCStyles.progress_bar())
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("Ready")
        layout.addWidget(self.progress_bar)

        # Status label
        self.status_label = QLabel("Analysis Complete - (0.000 secs)")
        self.status_label.setStyleSheet(CCStyles.label_header())
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        # Size label
        self.size_label = QLabel("0 MB to be removed. (Approximate size)")
        self.size_label.setStyleSheet(CCStyles.label_secondary())
        self.size_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.size_label)

        # Details group
        details_group = QGroupBox("Details of files to be deleted (Note: No files have been deleted yet)")
        details_group.setStyleSheet(CCStyles.group_box())
        details_layout = QVBoxLayout(details_group)

        # Details text area
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: {CCColors.CONTENT_BG};
                border: 1px solid {CCColors.BORDER_LIGHT};
                font-family: 'Consolas', monospace;
                font-size: 12px;
                color: {CCColors.TEXT_PRIMARY};
            }}
        """)
        details_layout.addWidget(self.details_text)

        layout.addWidget(details_group)

    def update_analysis(self, total_size_mb: float, details: list[str]):
        """Update analysis results."""
        self.progress_bar.setValue(100)
        self.progress_bar.setFormat("100%")

        self.size_label.setText(f"{total_size_mb:.1f} MB to be removed. (Approximate size)")

        # Format details
        details_html = "<table style='width:100%; border-collapse: collapse;'>"
        details_html += "<tr style='background-color: #F5F6F7; font-weight: bold;'>"
        details_html += "<td style='padding: 8px;'>Item</td>"
        details_html += "<td style='padding: 8px; text-align: right;'>Size</td>"
        details_html += "<td style='padding: 8px; text-align: right;'>Files</td>"
        details_html += "</tr>"

        for detail in details:
            details_html += f"<tr style='border-bottom: 1px solid #E0E0E0;'><td colspan='3' style='padding: 8px;'>{detail}</td></tr>"

        details_html += "</table>"
        self.details_text.setHtml(details_html)

    def show_analyzing(self):
        """Show analyzing state."""
        self.progress_bar.setValue(50)
        self.progress_bar.setFormat("Analyzing...")
        self.status_label.setText("Analyzing...")
        self.details_text.clear()

    def show_cleaning(self):
        """Show cleaning state."""
        self.progress_bar.setValue(75)
        self.progress_bar.setFormat("Cleaning...")
        self.status_label.setText("Cleaning in progress...")


class CCleanerMainWidget(QWidget):
    """Main CCleaner-style widget."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.connect_signals()

        # Auto-scan on startup if mock data available
        if USE_MOCK:
            self.on_analyze_clicked()

    def setup_ui(self):
        """Set up main UI."""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left sidebar
        self.sidebar = CCleanerSidebar()
        main_layout.addWidget(self.sidebar)

        # Right content area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 10, 10, 10)

        # Tab widget (Windows / Applications)
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(CCStyles.tab_widget())

        # Windows tab (browser cleaning)
        windows_tab = QWidget()
        windows_layout = QVBoxLayout(windows_tab)

        # Splitter for browser list and results
        splitter = QSplitter(Qt.Horizontal)

        # Left: Browser tree
        self.browser_tree = BrowserTreeWidget()
        splitter.addWidget(self.browser_tree)

        # Right: Analysis results
        self.analysis_panel = AnalysisResultPanel()
        splitter.addWidget(self.analysis_panel)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)

        windows_layout.addWidget(splitter)
        self.tab_widget.addTab(windows_tab, "Windows")

        # Applications tab (disabled for now)
        app_tab = QWidget()
        app_layout = QVBoxLayout(app_tab)
        app_label = QLabel("응용 프로그램 (추가 브라우저)")
        app_label.setStyleSheet(CCStyles.label_header())
        app_label.setAlignment(Qt.AlignCenter)
        app_layout.addWidget(app_label)
        self.tab_widget.addTab(app_tab, "응용 프로그램")

        content_layout.addWidget(self.tab_widget)

        # Bottom action buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.btn_analyze = QPushButton("Analyze")
        self.btn_analyze.setStyleSheet(CCStyles.main_button("primary"))
        self.btn_analyze.clicked.connect(self.on_analyze_clicked)
        button_layout.addWidget(self.btn_analyze)

        self.btn_run_cleaner = QPushButton("Run Cleaner")
        self.btn_run_cleaner.setStyleSheet(CCStyles.main_button("success"))
        self.btn_run_cleaner.clicked.connect(self.on_run_cleaner_clicked)
        self.btn_run_cleaner.setEnabled(False)
        button_layout.addWidget(self.btn_run_cleaner)

        content_layout.addLayout(button_layout)

        main_layout.addWidget(content_widget)

    def connect_signals(self):
        """Connect signals."""
        self.sidebar.cleaner_clicked.connect(lambda: logger.info("Cleaner selected"))
        self.sidebar.registry_clicked.connect(lambda: logger.info("Registry selected (disabled for browsers)"))
        self.sidebar.tools_clicked.connect(lambda: logger.info("Tools selected"))
        self.sidebar.options_clicked.connect(lambda: logger.info("Options selected"))

    def on_analyze_clicked(self):
        """Handle analyze button click."""
        logger.info("Analyzing browsers...")
        self.analysis_panel.show_analyzing()

        # Scan for browsers
        browsers = run_scan()
        self.browser_tree.load_browsers(browsers)

        # Simulate analysis
        total_size = 0.0
        details = []

        for browser in browsers:
            if browser.get("present"):
                name = browser.get("name", "")
                cache_size = browser.get("cache_size", "0 MB")

                # Parse size
                try:
                    size_mb = float(cache_size.split()[0])
                    total_size += size_mb
                except:
                    pass

                details.append(f"{name} - 임시 파일: {cache_size}")
                details.append(f"{name} - 쿠키: 1 KB")
                details.append(f"{name} - 히스토리: 16 KB")

        self.analysis_panel.update_analysis(total_size, details)
        self.btn_run_cleaner.setEnabled(True)

        logger.info(f"Analysis complete: {total_size:.1f} MB found")

    def on_run_cleaner_clicked(self):
        """Handle run cleaner button click."""
        logger.info("Running cleaner...")
        self.analysis_panel.show_cleaning()

        # Get checked items
        checked_items = []
        root = self.browser_tree.invisibleRootItem()
        for i in range(root.childCount()):
            browser_item = root.child(i)
            for j in range(browser_item.childCount()):
                option_item = browser_item.child(j)
                checkbox = self.browser_tree.itemWidget(option_item, 0)
                if checkbox and checkbox.isChecked():
                    checked_items.append({
                        "browser": checkbox.property("browser_name"),
                        "option": checkbox.property("option_id"),
                    })

        logger.info(f"Cleaning {len(checked_items)} items...")

        # Simulate cleaning (mock data)
        if USE_MOCK:
            from . import mock_windows
            for item in checked_items:
                result = mock_windows.mock_execute_cleaning(
                    item["option"],
                    item["browser"]
                )
                logger.info(f"Cleaned {item['browser']}/{item['option']}: {result['files_deleted']} files, {result['bytes_deleted']} bytes")

        # Update UI
        self.analysis_panel.update_analysis(0, ["Cleaning complete!"])
        self.btn_run_cleaner.setEnabled(False)

        logger.info("Cleaning complete!")


__all__ = ["CCleanerMainWidget"]
