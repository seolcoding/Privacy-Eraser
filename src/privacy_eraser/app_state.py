from __future__ import annotations

from typing import Literal

try:
    from PySide6.QtCore import QObject, Signal, Property
except ImportError:
    # Fallback for when PySide6 is not available
    QObject = object  # type: ignore
    Signal = lambda *args: None  # type: ignore
    Property = lambda *args, **kwargs: lambda f: f  # type: ignore


class AppState(QObject):
    """Application state with Qt signals for reactive updates"""
    
    # Qt Signals
    ui_mode_changed = Signal(str)
    wizard_step_changed = Signal(int)
    browser_selected = Signal(str)
    options_changed = Signal()
    scanned_programs_changed = Signal(list)
    appearance_mode_changed = Signal(str)
    debug_enabled_changed = Signal(bool)
    
    def __init__(self):
        super().__init__()
        # UI Mode
        self._ui_mode: Literal["easy", "advanced"] = "easy"
        
        # Debug
        self._debug_enabled: bool = False
        self._debug_panel_visible: bool = False
        
        # Theme
        self._appearance_mode: Literal["light", "dark", "system"] = "system"
        
        # Wizard State (Easy Mode)
        self._wizard_step: int = 0  # 0=Select Browsers, 1=Choose Options, 2=Review
        self._wizard_selected_browsers: list[str] = []
        
        # Browser Selection (Both Modes)
        self._active_browser: str | None = None
        self._active_cleaner_options: list[dict] = []
        self._selected_option_ids: set[str] = set()
        
        # Scan Results
        self._scanned_programs: list[dict] = []
    
    @Property(str, notify=ui_mode_changed)
    def ui_mode(self) -> str:
        return self._ui_mode
    
    @ui_mode.setter
    def ui_mode(self, value: str):
        if self._ui_mode != value:
            self._ui_mode = value
            self.ui_mode_changed.emit(value)
    
    @Property(int, notify=wizard_step_changed)
    def wizard_step(self) -> int:
        return self._wizard_step
    
    @wizard_step.setter
    def wizard_step(self, value: int):
        if self._wizard_step != value:
            self._wizard_step = value
            self.wizard_step_changed.emit(value)
    
    @Property(str, notify=appearance_mode_changed)
    def appearance_mode(self) -> str:
        return self._appearance_mode
    
    @appearance_mode.setter
    def appearance_mode(self, value: str):
        if self._appearance_mode != value:
            self._appearance_mode = value
            self.appearance_mode_changed.emit(value)
    
    @Property(bool, notify=debug_enabled_changed)
    def debug_enabled(self) -> bool:
        return self._debug_enabled
    
    @debug_enabled.setter
    def debug_enabled(self, value: bool):
        if self._debug_enabled != value:
            self._debug_enabled = value
            self.debug_enabled_changed.emit(value)
    
    @property
    def debug_panel_visible(self) -> bool:
        return self._debug_panel_visible
    
    @debug_panel_visible.setter
    def debug_panel_visible(self, value: bool):
        self._debug_panel_visible = value
    
    @property
    def wizard_selected_browsers(self) -> list[str]:
        return self._wizard_selected_browsers
    
    @wizard_selected_browsers.setter
    def wizard_selected_browsers(self, value: list[str]):
        self._wizard_selected_browsers = value
    
    @property
    def active_browser(self) -> str | None:
        return self._active_browser
    
    @active_browser.setter
    def active_browser(self, value: str | None):
        if self._active_browser != value:
            self._active_browser = value
            if value:
                self.browser_selected.emit(value)
    
    @property
    def active_cleaner_options(self) -> list[dict]:
        return self._active_cleaner_options
    
    @active_cleaner_options.setter
    def active_cleaner_options(self, value: list[dict]):
        self._active_cleaner_options = value
        self.options_changed.emit()
    
    @property
    def selected_option_ids(self) -> set[str]:
        return self._selected_option_ids
    
    @selected_option_ids.setter
    def selected_option_ids(self, value: set[str]):
        self._selected_option_ids = value
        self.options_changed.emit()
    
    @property
    def scanned_programs(self) -> list[dict]:
        return self._scanned_programs
    
    @scanned_programs.setter
    def scanned_programs(self, value: list[dict]):
        self._scanned_programs = value
        self.scanned_programs_changed.emit(value)


# Global instance
app_state = AppState()


__all__ = ["AppState", "app_state"]
