from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QScrollArea, QFrame, QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt, Signal

try:
    import qtawesome as qta
    HAS_QT_AWESOME = True
except ImportError:
    HAS_QT_AWESOME = False

from .app_state import app_state
from .gui_widgets import OptionCard, Badge, Colors


def _ensure_sample_programs() -> None:
    """Ensure sample programs exist for initial UI"""
    if not app_state.scanned_programs:
        app_state.scanned_programs = [
            {"name": "Google Chrome", "icon": "C", "color": "#1E88E5", "status": "Installed", "present": True, "cache_size": "120 MB", "cookies": "45"},
            {"name": "Microsoft Edge", "icon": "E", "color": "#0F9D58", "status": "Installed", "present": True, "cache_size": "85 MB", "cookies": "32"},
            {"name": "Mozilla Firefox", "icon": "F", "color": "#FF6F00", "status": "Installed", "present": True, "cache_size": "95 MB", "cookies": "28"},
        ]


class BrowserListItem(QWidget):
    """Custom list item widget for browser"""
    
    clicked = Signal(int)  # Emits browser index
    
    def __init__(self, browser_data: dict, index: int, parent=None):
        super().__init__(parent)
        self.browser_data = browser_data
        self.index = index
        self.is_active = False
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Icon
        icon = QLabel(browser_data.get("icon", "?"))
        icon.setFixedSize(36, 36)
        icon.setAlignment(Qt.AlignCenter)
        icon.setStyleSheet(f"""
            QLabel {{
                background-color: {browser_data.get('color', Colors.PRIMARY)};
                color: white;
                border-radius: 6px;
                font-size: 20px;
                font-weight: bold;
            }}
        """)
        layout.addWidget(icon)
        
        # Info section
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)
        
        # Name
        name = QLabel(browser_data.get("name", ""))
        name.setStyleSheet("font-size: 11px; font-weight: bold;")
        info_layout.addWidget(name)
        
        # Status badges
        badges_layout = QHBoxLayout()
        badges_layout.setSpacing(4)
        
        if browser_data.get("present"):
            status_badge = Badge("Installed", Colors.SUCCESS)
            status_badge.setFixedHeight(16)
            badges_layout.addWidget(status_badge)
        
        if browser_data.get("running"):
            running_badge = Badge("● Running", Colors.WARNING)
            running_badge.setFixedHeight(16)
            badges_layout.addWidget(running_badge)
        
        badges_layout.addStretch()
        info_layout.addLayout(badges_layout)
        
        # Stats
        stats_text = f"📁 {browser_data.get('cache_size', 'N/A')}  🍪 {browser_data.get('cookies', 'N/A')}"
        stats = QLabel(stats_text)
        stats.setStyleSheet("font-size: 8px; color: #6c757d;")
        info_layout.addWidget(stats)
        
        layout.addLayout(info_layout, 1)
    
    def mousePressEvent(self, event):
        self.clicked.emit(self.index)
        super().mousePressEvent(event)
    
    def set_active(self, active: bool):
        """Set the active state of this item"""
        self.is_active = active
        if active:
            self.setStyleSheet("""
                BrowserListItem {
                    background-color: #e8eaf6;
                    border-left: 4px solid #667eea;
                    border-radius: 8px;
                }
            """)
        else:
            self.setStyleSheet("""
                BrowserListItem {
                    background-color: transparent;
                    border-left: 4px solid transparent;
                    border-radius: 8px;
                }
                BrowserListItem:hover {
                    background-color: #f5f5f5;
                }
            """)


class AdvancedUI(QWidget):
    """Advanced Mode - Sidebar with main panel"""
    
    # Signals
    scan_requested = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        _ensure_sample_programs()
        
        # Main layout (horizontal: sidebar + main panel)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Sidebar (left, fixed 300px width)
        self.sidebar = self._build_sidebar()
        layout.addWidget(self.sidebar)
        
        # Main panel (right, flexible)
        self.main_panel = self._build_main_panel()
        layout.addWidget(self.main_panel, 1)
        
        # Select first browser by default
        if app_state.scanned_programs:
            self._select_browser(0)
    
    def _build_sidebar(self) -> QFrame:
        """Build the sidebar with browser list"""
        sidebar = QFrame()
        sidebar.setFixedWidth(300)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-right: 1px solid #e9ecef;
            }
        """)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)
        
        # Header
        header = QLabel("🛡️ Browsers")
        header.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(header)
        
        # Search box
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("🔍 Search browsers...")
        self.search_box.setFixedHeight(38)
        self.search_box.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                padding: 8px 12px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #667eea;
            }
        """)
        self.search_box.textChanged.connect(self._filter_browsers)
        layout.addWidget(self.search_box)
        
        # Scan button
        scan_btn = QPushButton("🔄 Scan Programs")
        scan_btn.setFixedHeight(38)
        scan_btn.clicked.connect(self._on_scan_clicked)
        
        # Add icon if qtawesome is available
        if HAS_QT_AWESOME:
            scan_btn.setIcon(qta.icon('fa5s.search'))
            scan_btn.setText("Scan Programs")
        scan_btn.setStyleSheet("""
            QPushButton {
                background-color: #667eea;
                color: white;
                border-radius: 10px;
                padding: 8px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5568d3;
            }
        """)
        layout.addWidget(scan_btn)
        
        # Browser list
        self.browser_list_widget = QWidget()
        self.browser_list_layout = QVBoxLayout(self.browser_list_widget)
        self.browser_list_layout.setContentsMargins(0, 0, 0, 0)
        self.browser_list_layout.setSpacing(4)
        
        self.browser_items = []
        self._populate_browser_list()
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setWidget(self.browser_list_widget)
        layout.addWidget(scroll_area, 1)
        
        return sidebar
    
    def _populate_browser_list(self):
        """Populate the browser list"""
        # Clear existing items
        for item in self.browser_items:
            item.setParent(None)
        self.browser_items.clear()
        
        # Add browser items
        for i, browser in enumerate(app_state.scanned_programs):
            item = BrowserListItem(browser, i)
            item.clicked.connect(self._select_browser)
            item.setCursor(Qt.PointingHandCursor)
            self.browser_list_layout.addWidget(item)
            self.browser_items.append(item)
        
        self.browser_list_layout.addStretch()
    
    def _filter_browsers(self, text: str):
        """Filter browser list based on search text"""
        for item in self.browser_items:
            matches = text.lower() in item.browser_data.get("name", "").lower()
            item.setVisible(matches)
    
    def _select_browser(self, index: int):
        """Select a browser and update main panel"""
        if 0 <= index < len(app_state.scanned_programs):
            browser = app_state.scanned_programs[index]
            app_state.active_browser = browser.get("name")
            
            # Update visual state
            for i, item in enumerate(self.browser_items):
                item.set_active(i == index)
            
            # Update main panel
            self._update_main_panel(browser)
    
    def _build_main_panel(self) -> QFrame:
        """Build the main panel"""
        panel = QFrame()
        panel.setStyleSheet("background-color: white;")
        
        self.main_panel_layout = QVBoxLayout(panel)
        self.main_panel_layout.setContentsMargins(0, 0, 0, 0)
        self.main_panel_layout.setSpacing(0)
        
        return panel
    
    def _update_main_panel(self, browser: dict):
        """Update main panel content for selected browser"""
        # Clear existing content
        for i in reversed(range(self.main_panel_layout.count())):
            widget = self.main_panel_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        # Header section
        header = QFrame()
        header.setFixedHeight(80)
        header.setStyleSheet("background-color: #f8f9fa; border-bottom: 1px solid #e9ecef;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(30, 20, 30, 20)
        
        # Title and path
        title_layout = QVBoxLayout()
        title = QLabel(browser.get("name", ""))
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        title_layout.addWidget(title)
        
        # User data path (placeholder)
        path = QLabel(f"📁 C:\\Users\\User\\AppData\\Local\\{browser.get('name', '')}\\User Data")
        path.setStyleSheet("font-size: 10px; color: #6c757d;")
        title_layout.addWidget(path)
        
        header_layout.addLayout(title_layout, 1)
        
        # Action buttons
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setFixedSize(100, 35)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        header_layout.addWidget(refresh_btn)
        
        preview_btn = QPushButton("👁️ Preview All")
        preview_btn.setFixedSize(120, 35)
        
        # Add icon if qtawesome is available
        if HAS_QT_AWESOME:
            preview_btn.setIcon(qta.icon('fa5s.eye'))
            preview_btn.setText("Preview All")
        preview_btn.setStyleSheet("""
            QPushButton {
                background-color: #667eea;
                color: white;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5568d3;
            }
        """)
        header_layout.addWidget(preview_btn)
        
        clean_btn = QPushButton("🧹 Clean Selected")
        clean_btn.setFixedSize(140, 35)
        
        # Add icon if qtawesome is available
        if HAS_QT_AWESOME:
            clean_btn.setIcon(qta.icon('fa5s.broom'))
            clean_btn.setText("Clean Selected")
        clean_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        header_layout.addWidget(clean_btn)
        
        self.main_panel_layout.addWidget(header)
        
        # Scrollable content area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(30, 20, 30, 20)
        content_layout.setSpacing(20)
        
        # Quick Presets section
        presets_frame = QFrame()
        presets_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 12px;
                padding: 15px;
            }
        """)
        presets_layout = QVBoxLayout(presets_frame)
        
        presets_title = QLabel("⚡ Quick Presets")
        presets_title.setStyleSheet("font-size: 14px; font-weight: bold;")
        presets_layout.addWidget(presets_title)
        
        presets_btn_layout = QHBoxLayout()
        presets = [
            "🍪 Cookies Only",
            "🚀 Quick Clean",
            "🔒 Security Clean",
            "💥 Full Clean"
        ]
        for preset in presets:
            btn = QPushButton(preset)
            btn.setFixedHeight(35)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    border: 2px solid #667eea;
                    color: #667eea;
                    border-radius: 8px;
                    padding: 6px 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #f8f9ff;
                }
            """)
            presets_btn_layout.addWidget(btn)
        
        presets_layout.addLayout(presets_btn_layout)
        content_layout.addWidget(presets_frame)
        
        # Cleaning Options section
        options_frame = QFrame()
        options_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
            }
        """)
        options_layout = QVBoxLayout(options_frame)
        options_layout.setContentsMargins(20, 20, 20, 20)
        
        options_title = QLabel("🎯 Cleaning Options")
        options_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        options_layout.addWidget(options_title)
        
        # Bulk actions
        bulk_layout = QHBoxLayout()
        select_all_btn = QPushButton("✓ Select All")
        select_all_btn.setFixedSize(100, 30)
        select_all_btn.clicked.connect(self._select_all_options)
        select_all_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #667eea;
                color: #667eea;
                border-radius: 6px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #f8f9ff;
            }
        """)
        bulk_layout.addWidget(select_all_btn)
        
        clear_all_btn = QPushButton("✗ Clear All")
        clear_all_btn.setFixedSize(100, 30)
        clear_all_btn.clicked.connect(self._clear_all_options)
        clear_all_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #6c757d;
                color: #6c757d;
                border-radius: 6px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #f8f9fa;
            }
        """)
        bulk_layout.addWidget(clear_all_btn)
        bulk_layout.addStretch()
        
        options_layout.addLayout(bulk_layout)
        
        # Sample options
        sample_options = [
            {"id": "cache", "label": "Cache", "description": "Temporary files stored for faster loading", "size": "120 MB", "file_count": "1,234", "last_cleaned": "Never"},
            {"id": "cookies", "label": "Cookies", "description": "Small files that websites store on your computer", "size": "2.5 MB", "file_count": "45", "last_cleaned": "2 days ago"},
            {"id": "history", "label": "Browsing History", "description": "Record of websites you've visited", "size": "5 MB", "file_count": "892", "last_cleaned": "Never"},
            {"id": "downloads", "label": "Download History", "description": "List of files you've downloaded", "size": "500 KB", "file_count": "156", "last_cleaned": "1 week ago"},
        ]
        
        self.option_cards = []
        for option in sample_options:
            card = OptionCard(option)
            card.selection_changed.connect(self._on_option_selected)
            options_layout.addWidget(card)
            self.option_cards.append(card)
        
        content_layout.addWidget(options_frame)
        content_layout.addStretch()
        
        scroll_area.setWidget(content)
        self.main_panel_layout.addWidget(scroll_area, 1)
    
    def _on_scan_clicked(self):
        """Handle scan button click"""
        self.scan_requested.emit()
        # In real implementation, would refresh browser list
    
    def _select_all_options(self):
        """Select all option cards"""
        for card in self.option_cards:
            card.set_checked(True)
    
    def _clear_all_options(self):
        """Clear all option cards"""
        for card in self.option_cards:
            card.set_checked(False)
    
    def _on_option_selected(self, option_id: str, checked: bool):
        """Handle option selection change"""
        if checked:
            app_state.selected_option_ids.add(option_id)
        else:
            app_state.selected_option_ids.discard(option_id)


def build_advanced_ui(parent=None) -> AdvancedUI:
    """Build and return the advanced UI"""
    return AdvancedUI(parent)


__all__ = ["AdvancedUI", "build_advanced_ui"]
