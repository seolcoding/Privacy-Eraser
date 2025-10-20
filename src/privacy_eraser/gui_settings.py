from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTabWidget, QWidget, QComboBox, QCheckBox, QLineEdit,
    QFileDialog, QFrame
)
from PySide6.QtCore import Qt, Signal

from .app_state import app_state
from .settings_db import save_setting, load_setting


class SettingsDialog(QDialog):
    """Settings dialog with tabbed interface"""
    
    # Signals
    theme_changed = Signal(str)
    ui_mode_changed = Signal(str)
    debug_toggled = Signal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("⚙️ 설정")
        self.setMinimumSize(600, 500)
        self.setModal(True)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Create tabs
        self._create_general_tab()
        self._create_debug_tab()
        self._create_advanced_tab()
        
        # Footer buttons
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(0, 20, 0, 0)
        
        # Reset button (left)
        reset_btn = QPushButton("기본값으로 재설정")
        reset_btn.setFixedWidth(140)
        reset_btn.clicked.connect(self._reset_to_defaults)
        reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        footer_layout.addWidget(reset_btn)
        
        footer_layout.addStretch()
        
        # Cancel button
        cancel_btn = QPushButton("취소")
        cancel_btn.setFixedWidth(100)
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        footer_layout.addWidget(cancel_btn)
        
        # Save button
        save_btn = QPushButton("저장")
        save_btn.setFixedWidth(100)
        save_btn.clicked.connect(self._save_settings)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #667eea;
                color: white;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5568d3;
            }
        """)
        footer_layout.addWidget(save_btn)
        
        main_layout.addLayout(footer_layout)
    
    def _create_general_tab(self):
        """Create the General settings tab"""
        general_widget = QWidget()
        layout = QVBoxLayout(general_widget)
        layout.setContentsMargins(24, 16, 24, 16)
        layout.setSpacing(18)
        
        # UI Mode Section
        mode_section = QFrame()
        mode_layout = QVBoxLayout(mode_section)
        
        mode_title = QLabel("인터페이스 모드")
        mode_title.setStyleSheet("font-size: 14px; font-weight: bold;")
        mode_layout.addWidget(mode_title)
        
        mode_desc = QLabel("마법사 방식의 쉬운 모드와 사이드바 기반의 고급 모드 중에서 선택하세요.")
        mode_desc.setStyleSheet("font-size: 11px; color: #6c757d;")
        mode_desc.setWordWrap(True)
        mode_layout.addWidget(mode_desc)
        
        self.mode_selector = QComboBox()
        self.mode_selector.addItem("쉬운 모드 (마법사)", "easy")
        self.mode_selector.addItem("고급 모드 (사이드바)", "advanced")
        current_mode = app_state.ui_mode
        index = 0 if current_mode == "easy" else 1
        self.mode_selector.setCurrentIndex(index)
        self.mode_selector.setFixedHeight(36)
        mode_layout.addWidget(self.mode_selector)
        
        layout.addWidget(mode_section)
        
        # Theme Section
        theme_section = QFrame()
        theme_layout = QVBoxLayout(theme_section)
        
        theme_title = QLabel("화면 테마")
        theme_title.setStyleSheet("font-size: 14px; font-weight: bold;")
        theme_layout.addWidget(theme_title)
        
        self.theme_selector = QComboBox()
        theme_items = [
            ("밝은 테마", "light"),
            ("어두운 테마", "dark"),
            ("시스템 기본", "system"),
        ]
        for label, value in theme_items:
            self.theme_selector.addItem(label, value)
        current_theme = app_state.appearance_mode
        theme_index = next((i for i in range(self.theme_selector.count())
                            if self.theme_selector.itemData(i) == current_theme), 0)
        self.theme_selector.setCurrentIndex(theme_index)
        self.theme_selector.setFixedHeight(36)
        theme_layout.addWidget(self.theme_selector)
        
        layout.addWidget(theme_section)
        
        # Auto-scan Section
        self.autoscan_checkbox = QCheckBox("시작할 때 브라우저 자동 검색")
        autoscan_enabled = load_setting("autoscan_on_startup", "false") == "true"
        self.autoscan_checkbox.setChecked(autoscan_enabled)
        layout.addWidget(self.autoscan_checkbox)
        
        layout.addStretch()
        
        self.tab_widget.addTab(general_widget, "일반")
    
    def _create_debug_tab(self):
        """Create the Debug settings tab"""
        debug_widget = QWidget()
        layout = QVBoxLayout(debug_widget)
        layout.setContentsMargins(24, 16, 24, 16)
        layout.setSpacing(14)
        
        # Debug Section
        debug_title = QLabel("디버그 설정")
        debug_title.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(debug_title)
        
        debug_desc = QLabel("앱 하단 패널에 로그와 변수를 표시합니다.")
        debug_desc.setStyleSheet("font-size: 11px; color: #6c757d;")
        debug_desc.setWordWrap(True)
        layout.addWidget(debug_desc)
        
        self.debug_checkbox = QCheckBox("디버그 패널 활성화")
        self.debug_checkbox.setChecked(app_state.debug_enabled)
        layout.addWidget(self.debug_checkbox)
        
        # Log Level Section
        log_section = QFrame()
        log_layout = QVBoxLayout(log_section)
        
        log_title = QLabel("로그 레벨")
        log_title.setStyleSheet("font-size: 12px; font-weight: bold;")
        log_layout.addWidget(log_title)
        
        self.log_level_selector = QComboBox()
        self.log_level_selector.addItems(["DEBUG", "INFO", "WARNING", "ERROR"])
        log_level = load_setting("log_level", "INFO")
        self.log_level_selector.setCurrentText(log_level)
        self.log_level_selector.setFixedHeight(35)
        log_layout.addWidget(self.log_level_selector)
        
        layout.addWidget(log_section)
        layout.addStretch()
        
        self.tab_widget.addTab(debug_widget, "디버그")
    
    def _create_advanced_tab(self):
        """Create the Advanced settings tab"""
        advanced_widget = QWidget()
        layout = QVBoxLayout(advanced_widget)
        layout.setContentsMargins(24, 16, 24, 16)
        layout.setSpacing(14)
        
        # CleanerML Directory Section
        cleanerml_section = QFrame()
        cleanerml_layout = QVBoxLayout(cleanerml_section)
        
        cleanerml_title = QLabel("CleanerML 디렉터리")
        cleanerml_title.setStyleSheet("font-size: 12px; font-weight: bold;")
        cleanerml_layout.addWidget(cleanerml_title)
        
        # Path input + Browse button
        path_layout = QHBoxLayout()
        
        self.cleanerml_entry = QLineEdit()
        self.cleanerml_entry.setPlaceholderText("bleachbit/cleaners")
        cleanerml_path = load_setting("cleanerml_directory", "")
        self.cleanerml_entry.setText(cleanerml_path)
        self.cleanerml_entry.setFixedHeight(35)
        path_layout.addWidget(self.cleanerml_entry)
        
        browse_btn = QPushButton("찾아보기")
        browse_btn.setFixedSize(90, 35)
        browse_btn.clicked.connect(self._browse_cleanerml_dir)
        path_layout.addWidget(browse_btn)
        
        cleanerml_layout.addLayout(path_layout)
        layout.addWidget(cleanerml_section)
        
        layout.addStretch()
        
        self.tab_widget.addTab(advanced_widget, "고급")
    
    def _browse_cleanerml_dir(self):
        """Open file dialog to browse for CleanerML directory"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "CleanerML 디렉터리를 선택하세요",
            self.cleanerml_entry.text() or ""
        )
        if directory:
            self.cleanerml_entry.setText(directory)
    
    def _save_settings(self):
        """Save all settings and emit signals"""
        try:
            # UI Mode
            mode = self.mode_selector.currentData() or "easy"
            if mode != app_state.ui_mode:
                save_setting("ui_mode", mode)
                self.ui_mode_changed.emit(mode)
            
            # Theme
            theme = self.theme_selector.currentData() or "system"
            if theme != app_state.appearance_mode:
                app_state.appearance_mode = theme
                save_setting("appearance_mode", theme)
                self.theme_changed.emit(theme)
            
            # Debug
            debug_enabled = self.debug_checkbox.isChecked()
            if debug_enabled != app_state.debug_enabled:
                app_state.debug_enabled = debug_enabled
                save_setting("debug_enabled", "true" if debug_enabled else "false")
                self.debug_toggled.emit(debug_enabled)
            
            # Auto-scan
            autoscan = "true" if self.autoscan_checkbox.isChecked() else "false"
            save_setting("autoscan_on_startup", autoscan)
            
            # Log level
            log_level = self.log_level_selector.currentText()
            save_setting("log_level", log_level)
            
            # CleanerML directory
            cleanerml_dir = self.cleanerml_entry.text()
            save_setting("cleanerml_directory", cleanerml_dir)
            
            self.accept()
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def _reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.mode_selector.setCurrentIndex(0)
        for i in range(self.theme_selector.count()):
            if self.theme_selector.itemData(i) == "system":
                self.theme_selector.setCurrentIndex(i)
                break
        self.debug_checkbox.setChecked(False)
        self.autoscan_checkbox.setChecked(False)
        self.log_level_selector.setCurrentText("INFO")
        self.cleanerml_entry.clear()


def open_settings_dialog(parent=None) -> SettingsDialog:
    """Open the settings dialog"""
    dialog = SettingsDialog(parent)
    return dialog


__all__ = ["SettingsDialog", "open_settings_dialog"]
