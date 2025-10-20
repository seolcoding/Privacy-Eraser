from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton,
    QLabel, QScrollArea, QFrame, QTextEdit, QProgressBar, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from loguru import logger

try:
    import qtawesome as qta
    HAS_QT_AWESOME = True
except ImportError:
    HAS_QT_AWESOME = False

from .app_state import app_state
from .gui_widgets import BrowserCard, OptionCard, StepIndicator
from .gui_integration import (
    guess_user_data_path,
    load_cleaner_options,
    preview_selected_options,
    execute_clean,
)


def _ensure_sample_programs() -> None:
    """Ensure sample programs exist for initial UI"""
    if not app_state.scanned_programs:
        app_state.scanned_programs = [
            {
                "name": "Google Chrome",
                "icon": "C",
                "fa_icon": "fa5b.chrome",
                "color": "#1E88E5",
                "status": "설치됨",
                "present": True,
                "running": False,
            },
            {
                "name": "Microsoft Edge",
                "icon": "E",
                "fa_icon": "fa5b.edge",
                "color": "#0F9D58",
                "status": "설치됨",
                "present": True,
                "running": False,
            },
            {
                "name": "Mozilla Firefox",
                "icon": "F",
                "fa_icon": "fa5b.firefox",
                "color": "#FF6F00",
                "status": "설치됨",
                "present": True,
                "running": False,
            },
        ]


class WizardUI(QWidget):
    """Easy Mode - Wizard-style interface"""
    
    # Signals
    mode_switch_requested = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        _ensure_sample_programs()
        app_state.scanned_programs_changed.connect(self._on_scanned_programs_changed)
        self.browser_options: dict[str, list] = {}
        self.option_lookup: dict[str, object] = {}
        self.option_card_map: dict[str, OptionCard] = {}
        self._preview_cache: tuple[int, list[str]] | None = None
        self._selected_options_cache: list = []
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Progress indicator
        self.progress_indicator = StepIndicator([
            "브라우저 선택",
            "정리 항목 선택",
            "검토 및 정리"
        ])
        self.progress_indicator.set_current_step(app_state.wizard_step)
        layout.addWidget(self.progress_indicator)
        
        # Content area (stacked widgets for each step)
        self.content_container = QWidget()
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.content_container, 1)
        
        # Footer with navigation buttons
        footer = QFrame()
        footer.setFixedHeight(64)
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(16, 10, 16, 10)
        
        self.back_btn = QPushButton("뒤로")
        self.back_btn.setFixedWidth(120)
        self.back_btn.clicked.connect(self._previous_step)
        
        # Add icon if qtawesome is available
        if HAS_QT_AWESOME:
            self.back_btn.setIcon(qta.icon('fa5s.arrow-left'))
            self.back_btn.setText("Back")
        footer_layout.addWidget(self.back_btn)
        
        footer_layout.addStretch()
        
        self.next_btn = QPushButton("다음")
        self.next_btn.setFixedWidth(140)
        self.next_btn.clicked.connect(self._next_step)
        
        # Add icon if qtawesome is available
        if HAS_QT_AWESOME:
            self.next_btn.setIcon(qta.icon('fa5s.arrow-right'))
            self.next_btn.setText("다음")
        footer_layout.addWidget(self.next_btn)
        
        layout.addWidget(footer)
        
        # Build initial step
        self._build_current_step()
    
    def _build_current_step(self):
        """Build the UI for the current wizard step"""
        # Clear content
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        step = app_state.wizard_step
        
        if step == 0:
            self._build_step0_browser_selection()
        elif step == 1:
            self._build_step1_options_selection()
        elif step == 2:
            self._build_step2_review()
        
        self.progress_indicator.set_current_step(step)
        self._update_navigation_state()

    def _make_option_key(self, browser: str, option_id: str) -> str:
        return f"{browser}::{option_id}"

    def _load_options_for_browser(self, browser: str):
        user_data_path = guess_user_data_path(browser)
        try:
            options = load_cleaner_options(browser, user_data_path)
        except Exception:
            options = []
        self.browser_options[browser] = options or []
        return self.browser_options[browser]

    def _get_selected_options(self):
        return [
            self.option_lookup[key]
            for key in app_state.selected_option_ids
            if key in self.option_lookup
        ]

    def _apply_preset(self, base_option_ids: set[str]):
        selection = set()
        for browser in app_state.wizard_selected_browsers:
            for option_id in base_option_ids:
                key = self._make_option_key(browser, option_id)
                if key in self.option_card_map:
                    selection.add(key)
        app_state.selected_option_ids = selection
        for key, card in self.option_card_map.items():
            card.set_checked(key in selection)
        self._preview_cache = None
        self._update_navigation_state()

    def _update_navigation_state(self):
        step = app_state.wizard_step
        self.back_btn.setEnabled(step > 0)

        if step == 2:
            self.next_btn.setText("정리 실행")
            if HAS_QT_AWESOME:
                self.next_btn.setIcon(qta.icon('fa5s.broom'))
                self.next_btn.setText("정리 실행")
        else:
            self.next_btn.setText("다음")
            if HAS_QT_AWESOME:
                self.next_btn.setIcon(qta.icon('fa5s.arrow-right'))
                self.next_btn.setText("다음")

        if step == 0:
            self.next_btn.setEnabled(bool(app_state.wizard_selected_browsers))
        elif step == 1:
            self.next_btn.setEnabled(bool(app_state.selected_option_ids))
        else:
            self.next_btn.setEnabled(True)

    def _build_step0_browser_selection(self):
        """Step 0: Browser selection grid"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 16, 24, 16)
        layout.setSpacing(16)
        
        # Title
        title = QLabel("정리할 브라우저를 선택하세요")
        title.setStyleSheet("font-size: 22px; font-weight: 700;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Browser grid (3 columns)
        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setSpacing(12)
        
        self.browser_cards = []
        for i, browser in enumerate(app_state.scanned_programs):
            row = i // 3
            col = i % 3
            
            card = BrowserCard(browser)
            card.selection_changed.connect(self._on_browser_selected)
            
            # Restore previous selection
            if browser["name"] in app_state.wizard_selected_browsers:
                card.set_checked(True)
            
            grid_layout.addWidget(card, row, col, Qt.AlignCenter)
            self.browser_cards.append(card)
        
        layout.addWidget(grid_widget)
        layout.addStretch()
        
        scroll_area.setWidget(container)
        self.content_layout.addWidget(scroll_area)
    
    def _build_step1_options_selection(self):
        """Step 1: Options selection"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 16, 24, 16)
        layout.setSpacing(16)
        
        # Title
        title = QLabel("정리할 항목을 선택하세요")
        title.setStyleSheet("font-size: 22px; font-weight: 700;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle with selected browsers
        if app_state.wizard_selected_browsers:
            subtitle = QLabel(f"대상 브라우저: {', '.join(app_state.wizard_selected_browsers)}")
            subtitle.setStyleSheet("font-size: 13px; color: #4b5563;")
            subtitle.setAlignment(Qt.AlignCenter)
            layout.addWidget(subtitle)

            presets_layout = QHBoxLayout()
            presets_layout.setSpacing(8)
            presets_layout.setAlignment(Qt.AlignCenter)
            preset_definitions = [
                ("빠른 정리 (캐시·쿠키)", {"cache", "cookies"}),
                ("철저한 정리 (캐시·쿠키·기록)", {"cache", "cookies", "history"}),
                ("보안 정리 (쿠키·기록)", {"cookies", "history"}),
            ]
            for label_text, option_ids in preset_definitions:
                btn = QPushButton(label_text)
                btn.setCursor(Qt.PointingHandCursor)
                btn.setStyleSheet("QPushButton { font-size: 13px; padding: 6px 14px; }")
                btn.clicked.connect(lambda _, ids=option_ids: self._apply_preset(ids))
                presets_layout.addWidget(btn)
            layout.addLayout(presets_layout)

        self.option_cards = []
        self.option_card_map.clear()
        self.option_lookup.clear()
        current_selection = set(app_state.selected_option_ids)
        options_found = False

        for browser in app_state.wizard_selected_browsers:
            options = self._load_options_for_browser(browser)
            if not options:
                empty_label = QLabel(f"{browser}에 사용할 수 있는 정리 항목이 없습니다.")
                empty_label.setStyleSheet("font-size: 12px; color: #6c757d;")
                empty_label.setAlignment(Qt.AlignCenter)
                layout.addWidget(empty_label)
                continue

            section_label = QLabel(browser)
            section_label.setStyleSheet("font-size: 15px; font-weight: bold; margin-top: 10px;")
            layout.addWidget(section_label)

            for opt in options:
                key = self._make_option_key(browser, opt.id)
                self.option_lookup[key] = opt
                description = opt.description or ""
                if opt.warning:
                    warn_text = f" [주의] {opt.warning}"
                    description = f"{description}{warn_text}" if description else warn_text.strip()
                option_dict = {
                    "id": key,
                    "label": opt.label,
                    "description": description,
                    "size": "—",
                }
                card = OptionCard(option_dict)
                card.selection_changed.connect(self._on_option_selected)
                if key in current_selection:
                    card.set_checked(True)
                layout.addWidget(card)
                self.option_cards.append(card)
                self.option_card_map[key] = card
                options_found = True

        # Prune selections that no longer exist in the available options
        valid_selection = {key for key in current_selection if key in self.option_lookup}
        app_state.selected_option_ids = valid_selection
        for card in self.option_cards:
            card.set_checked(card.option_id in valid_selection)

        if not options_found:
            placeholder = QLabel("정리 가능 항목을 보려면 브라우저를 먼저 선택하세요.")
            placeholder.setAlignment(Qt.AlignCenter)
            placeholder.setStyleSheet("font-size: 13px; color: #6c757d;")
            layout.addWidget(placeholder)

        layout.addStretch()
        
        scroll_area.setWidget(container)
        self.content_layout.addWidget(scroll_area)
    
    def _build_step2_review(self):
        """Step 2: Review and clean"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 16, 24, 16)
        layout.setSpacing(16)

        # Title
        title = QLabel("선택 내용을 확인하세요")
        title.setStyleSheet("font-size: 22px; font-weight: 700;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Summary cards
        summary_layout = QHBoxLayout()
        summary_layout.setSpacing(12)

        card_style = """
            QFrame {
                background-color: white;
                border: 1px solid #d1d5db;
                border-radius: 10px;
                padding: 16px;
            }
        """

        # Browsers count
        browsers_card = QFrame()
        browsers_card.setStyleSheet(card_style)
        browsers_layout = QVBoxLayout(browsers_card)
        browsers_label = QLabel("선택된 브라우저")
        browsers_label.setStyleSheet("font-size: 13px; color: #4b5563;")
        browsers_label.setAlignment(Qt.AlignCenter)
        browsers_layout.addWidget(browsers_label)
        browsers_value = QLabel(str(len(app_state.wizard_selected_browsers)))
        browsers_value.setStyleSheet("font-size: 24px; font-weight: bold;")
        browsers_value.setAlignment(Qt.AlignCenter)
        browsers_layout.addWidget(browsers_value)
        summary_layout.addWidget(browsers_card)

        # Options count
        options_card = QFrame()
        options_card.setStyleSheet(card_style)
        options_layout = QVBoxLayout(options_card)
        options_label = QLabel("선택된 항목")
        options_label.setStyleSheet("font-size: 13px; color: #4b5563;")
        options_label.setAlignment(Qt.AlignCenter)
        options_layout.addWidget(options_label)
        options_value = QLabel(str(len(app_state.selected_option_ids)))
        options_value.setStyleSheet("font-size: 24px; font-weight: bold;")
        options_value.setAlignment(Qt.AlignCenter)
        options_layout.addWidget(options_value)
        summary_layout.addWidget(options_card)

        # Total items (from preview)
        items_card = QFrame()
        items_card.setStyleSheet(card_style)
        items_layout = QVBoxLayout(items_card)
        items_label = QLabel("미리보기 항목 수")
        items_label.setStyleSheet("font-size: 13px; color: #4b5563;")
        items_label.setAlignment(Qt.AlignCenter)
        items_layout.addWidget(items_label)

        selected_options = self._get_selected_options()
        preview_count = 0
        preview_lines: list[str] = []
        if selected_options:
            try:
                preview_count, preview_lines = preview_selected_options(selected_options)
            except Exception:
                preview_lines = []
                preview_count = 0

        items_value = QLabel(str(preview_count))
        items_value.setStyleSheet("font-size: 24px; font-weight: bold;")
        items_value.setAlignment(Qt.AlignCenter)
        items_layout.addWidget(items_value)
        summary_layout.addWidget(items_card)

        layout.addLayout(summary_layout)
        
        # Preview section
        preview_frame = QFrame()
        preview_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #d1d5db;
                border-radius: 10px;
            }
        """)
        preview_layout = QVBoxLayout(preview_frame)
        preview_layout.setContentsMargins(18, 14, 18, 16)

        preview_title = QLabel("삭제 예정 항목 미리보기")
        preview_title.setStyleSheet("font-size: 15px; font-weight: bold;")
        preview_layout.addWidget(preview_title)
        
        preview_text = QTextEdit()
        preview_text.setReadOnly(True)
        preview_text.setMaximumHeight(200)
        
        if not selected_options:
            preview_text.setPlainText("선택된 항목이 없습니다.")
        elif preview_lines:
            preview_text.setPlainText("\n".join(preview_lines))
        else:
            preview_text.setPlainText("미리보기를 불러오지 못했습니다. 관리자 권한이 필요한 항목일 수 있습니다.")

        preview_layout.addWidget(preview_text)
        
        self._selected_options_cache = selected_options
        self._preview_cache = (preview_count, preview_lines)

        layout.addWidget(preview_frame)
        layout.addStretch()
        
        scroll_area.setWidget(container)
        self.content_layout.addWidget(scroll_area)
    
    def _on_browser_selected(self, browser_name: str, checked: bool):
        """Handle browser selection change"""
        if checked:
            if browser_name not in app_state.wizard_selected_browsers:
                app_state.wizard_selected_browsers.append(browser_name)
        else:
            if browser_name in app_state.wizard_selected_browsers:
                app_state.wizard_selected_browsers.remove(browser_name)
                remaining = {
                    key
                    for key in app_state.selected_option_ids
                    if not key.startswith(f"{browser_name}::")
                }
                app_state.selected_option_ids = remaining

        self._update_navigation_state()
    
    def _on_option_selected(self, option_id: str, checked: bool):
        """Handle option selection change"""
        current = set(app_state.selected_option_ids)
        if checked:
            current.add(option_id)
        else:
            current.discard(option_id)
        app_state.selected_option_ids = current
        self._update_navigation_state()
    
    def _next_step(self):
        """Move to next wizard step"""
        current = app_state.wizard_step
        
        # Validation
        if current == 0 and not app_state.wizard_selected_browsers:
            QMessageBox.warning(self, "PrivacyEraser", "브라우저를 최소 하나 선택해야 계속 진행할 수 있습니다.")
            return
        
        if current == 1 and not app_state.selected_option_ids:
            QMessageBox.warning(self, "PrivacyEraser", "정리할 항목을 최소 하나 선택하세요.")
            return
        
        if current < 2:
            app_state.wizard_step = current + 1
            self._build_current_step()
        else:
            # Execute clean
            self._execute_clean()

    def _on_scanned_programs_changed(self, _programs):
        """Refresh the wizard when scan results change."""
        self.browser_options.clear()
        self.option_lookup.clear()
        self.option_card_map.clear()
        available = {
            prog.get("name") for prog in app_state.scanned_programs if prog.get("present")
        }
        app_state.wizard_selected_browsers = [
            name for name in app_state.wizard_selected_browsers if name in available
        ]
        self._build_current_step()
        self._update_navigation_state()
    
    def _previous_step(self):
        """Move to previous wizard step"""
        if app_state.wizard_step > 0:
            app_state.wizard_step -= 1
            self._build_current_step()
            self._update_navigation_state()
    
    def _execute_clean(self):
        """Execute the cleaning operation"""
        selected_options = self._get_selected_options()
        if not selected_options:
            QMessageBox.warning(self, "PrivacyEraser", "정리할 항목을 선택해 주세요.")
            return

        try:
            total_count, total_bytes = execute_clean(selected_options)
        except Exception as exc:  # pragma: no cover - defensive UI path
            logger.error(f"clean> failed: {exc}")
            QMessageBox.critical(self, "PrivacyEraser", "정리 중 오류가 발생했습니다. 로그를 확인해 주세요.")
            return

        human_bytes = self._format_bytes(total_bytes)
        QMessageBox.information(
            self,
            "PrivacyEraser",
            f"총 {total_count}개 항목을 삭제했습니다 ({human_bytes}).",
        )

        app_state.selected_option_ids = set()
        app_state.wizard_selected_browsers = []
        app_state.wizard_step = 0
        self.progress_indicator.set_current_step(0)
        self._build_current_step()
        self._update_navigation_state()

    @staticmethod
    def _format_bytes(num: int) -> str:
        value = float(num)
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if value < 1024.0 or unit == "TB":
                return f"{value:.1f} {unit}"
            value /= 1024.0
        return f"{value:.1f} TB"


def build_wizard_ui(parent=None) -> WizardUI:
    """Build and return the wizard UI"""
    return WizardUI(parent)


__all__ = ["WizardUI", "build_wizard_ui"]
