PrivacyEraser

**Professional privacy management tool with PySide6 (Qt6) UI and BleachBit-based core**

## Quickstart (uv)

```bash
# 1. Install dependencies
uv sync

# 2. Run application
uv run privacy_eraser
```

## Features (v1.0.0 - 2025-10-20)

### ✅ Implemented

#### **Modern PySide6 (Qt6) GUI**
- **Dual-Mode Interface:** Easy Mode (wizard) and Advanced Mode (sidebar)
  - **Easy Mode:** Step-by-step wizard (Select Browsers → Choose Options → Review & Clean)
  - **Advanced Mode:** Power-user interface with browser list sidebar and quick presets
  - **Seamless Mode Switching:** Toggle between modes without losing state
- **Qt Material Design:** Professional, modern theming with Light/Dark mode support
- **Settings Dialog:** Comprehensive settings management (General, Debug, Advanced tabs)
- **Debug Panel:** Collapsible developer panel with real-time variables and console logs
- **Reactive Architecture:** Qt signals/slots for responsive UI updates

#### **BleachBit-Inspired Core Engine**
- **Advanced File Operations:** 
  - Whitelist protection for system-critical files
  - Multiple search modes: file, glob, walk.files, walk.all, walk.top
  - Safe deletion with error handling
  - Locked file deletion (Windows reboot-pending)
- **Windows Integration:**
  - Registry key/value operations
  - Process detection (check if browsers are running)
  - Path variable expansion (including W6432 variants)
- **CleanerML Support:** BleachBit-compatible XML cleaning definitions
- **Modular Architecture:** Core logic separated from UI for testability

#### **Browser Detection (Windows)**
- Registry, file, and process-based detection for:
  - Chrome, Edge, Brave, Opera, Vivaldi, Firefox, Arc Browser, Naver Whale
- Real-time process monitoring (warn if browser is running)

#### **Cleaning Presets**
- Built-in Chromium presets: Cache, Cookies, History, Session, Passwords
- Custom CleanerML file support
- Preview before deletion
- Progress reporting with bytes/items deleted

#### **System Features**
- Settings persistence: SQLite database (`~/.privacy_eraser/settings.db`)
- Comprehensive logging: loguru + rich with colored output
- Testing: pytest suite with >95% coverage

### 🔜 Planned (see docs/ROADMAP.md)
- Scheduled cleaning (APScheduler + Windows Task Scheduler)
- Auto-update system (GitHub Releases)
- License system (commercial tiers)
- macOS/Linux support

## Run Tests

```bash
# Install test dependencies
uv sync --extra test

# Run all tests
uv run -m pytest -q

# With coverage
uv run -m pytest --cov=privacy_eraser --cov-report=term-missing
```

## Development

See `.cursor/context/runbook.md` for detailed commands and workflows.

**Key Commands:**
- `uv sync` - Install/update dependencies
- `uv run privacy_eraser` - Launch GUI
- `uv run -m pytest` - Run test suite
- `uv add <package>` - Add dependency

## Architecture

### PySide6 Frontend (GUI Layer)
- **Entry Point:** `src/privacy_eraser/__main__.py`
- **Main Window:** `src/privacy_eraser/gui.py` - Mode switching, header, debug panel coordination
- **Easy Mode:** `src/privacy_eraser/gui_easy_mode.py` - Wizard UI (3-step flow)
- **Advanced Mode:** `src/privacy_eraser/gui_advanced_mode.py` - Sidebar + main panel
- **Settings Dialog:** `src/privacy_eraser/gui_settings.py` - Tabbed settings modal
- **Debug Panel:** `src/privacy_eraser/gui_debug.py` - Developer tools (variables + console)
- **Custom Widgets:** `src/privacy_eraser/gui_widgets.py` - Reusable Qt components
- **Integration Layer:** `src/privacy_eraser/gui_integration.py` - Bridge between GUI and core

### Core Engine (Business Logic)
- **File Utilities:** `src/privacy_eraser/core/file_utils.py`
  - Safe deletion, whitelist checking, size calculation
- **Windows Utilities:** `src/privacy_eraser/core/windows_utils.py`
  - Registry operations, process detection, locked file handling
- **Cleaner Engine:** `src/privacy_eraser/core/cleaner_engine.py`
  - Action orchestration, progress reporting, error handling

### Supporting Modules
- **App State:** `src/privacy_eraser/app_state.py` - QObject-based reactive state (Qt signals)
- **Settings DB:** `src/privacy_eraser/settings_db.py` - SQLite persistence
- **Detection:** `src/privacy_eraser/detect_windows.py` - Browser detection (registry, files, processes)
- **CleanerML Loader:** `src/privacy_eraser/cleanerml_loader.py` - XML parser (BleachBit format)
- **Legacy Cleaning:** `src/privacy_eraser/cleaning.py` - Backward compatibility wrappers

### Reference Materials
- **BleachBit Source:** `reference/bleachbit_original/` - Original BleachBit code for reference
- **Deprecated Code:** `reference/deprecated/` - Old implementations archived
- **Documentation:** `docs/` - Detailed design, architecture, and planning docs

See `docs/05_1_GUI_REDESIGN.md` for GUI specification.

## Platform Support

- **Primary:** Windows 10/11 (full feature set)
- **Experimental:** Linux/macOS (GUI works, detection limited)

## Documentation

- `docs/` - Detailed documentation and planning
- `.cursor/` - Development rules and context for AI assistants
- `TODO.md` - Current development task list
- `docs/ROADMAP.md` - Future milestones