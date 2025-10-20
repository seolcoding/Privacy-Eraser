# PrivacyEraser Architecture (Current MVP)

**Last Updated:** 2025-10-09  
**Status:** MVP implementation in progress

## Overview
PrivacyEraser is a Windows-focused privacy cleaning tool built with Python 3.12+, CustomTkinter GUI, and a modular cleaning engine compatible with BleachBit's CleanerML format.

## Technology Stack

### Core
- **Language:** Python 3.12+
- **Package Manager:** uv
- **GUI Framework:** CustomTkinter 5.2.0 (with tkinter fallback)
- **Logging:** loguru + rich (colored terminal output)
- **Process Management:** psutil 5.9.8

### Current Dependencies
```toml
customtkinter==5.2.0
pillow==10.0.0
loguru==0.7.2
rich==13.7.1
psutil==5.9.8
setuptools>=68
```

### Test Dependencies
```toml
pytest>=8.3.0
pytest-cov>=5.0.0
pytest-mock>=3.14.0
```

## Module Architecture

### Entry Point
- `src/privacy_eraser/__main__.py`
  - Single entry point: `main()` → launches GUI
  - Installed as script: `privacy_eraser`

### GUI Layer (`gui.py`)
**Responsibilities:**
- Main application window (CustomTkinter or tkinter fallback)
- Program detection table (Treeview widget)
- Cleaner options panel with checkboxes
- Preview and Clean action buttons
- Collapsible Debug panel (variables + live console)
- Logging integration (loguru → GUI textbox sink)

**Key Components:**
- Program scan: uses `detect_windows.collect_programs()`
- Cleaner loading: tries CleanerML first, falls back to `chromium_cleaner_options()`
- Select/Clear All, Preview, Execute Clean workflows
- Real-time log display with rich formatting

### Detection Layer (`detect_windows.py`)
**Windows-Only Module**

**Responsibilities:**
- Browser/application detection via registry, files, processes
- `ProgramProbe` dataclass: defines detection criteria
- `registry_key_exists()` - query Windows registry
- `detect_file_glob()` - expand env vars and check file existence
- `is_process_running_windows()` - psutil-based process detection
- `collect_programs()` - aggregate detection results into table rows

**Supported Detection:**
- Registry keys (HKCU, HKLM, etc.)
- File patterns with %ENVVAR% expansion
- Running processes (by executable name)

### Cleaning Engine (`cleaning.py`)
**Cross-Platform Core**

**Responsibilities:**
- `DeleteAction`: single deletion operation (file, glob, walk modes)
- `CleanerOption`: collection of actions with metadata
- `chromium_cleaner_options()`: built-in Chromium browser presets

**Search Modes:**
- `file` - single file
- `glob` - glob pattern
- `walk.files` - recursive files only
- `walk.all` - files + directories
- `walk.top` - walk + include top directory

**Built-in Chromium Options:**
- Cache (Browser Cache, Code Cache, GPU Cache, Shader Cache, Service Worker, File System)
- Cookies (Cookies databases in Default and Network directories)
- History (History, Favicons, Top Sites, Session Storage)
- Session (Current/Last Session/Tabs, Extension State)
- Passwords (Login Data) - marked with warning

### CleanerML Loader (`cleanerml_loader.py`)
**Responsibilities:**
- Parse BleachBit-compatible XML cleaner definitions
- OS filtering (`os="windows"` attribute)
- Variable expansion (`$$VAR$$` tokens)
- Multi-value variable expansion (e.g., ProgramFiles variants)
- Convert XML actions to `DeleteAction` objects

**Supported CleanerML Features:**
- `<cleaner os="...">` - OS filtering
- `<var name="...">` with multiple `<value os="...">` children
- `<option id="...">` with label, description, warning
- `<action command="delete" search="..." path="...">` - only `delete` command
- `$$VAR$$` token replacement in paths

**Currently Used:**
- Loads cleaners from `bleachbit/cleaners/` directory
- Maps well-known browsers (Chrome, Edge, Brave, Opera, Vivaldi) to XML files
- Falls back to built-in Chromium options for unmapped browsers

### Diagnostics (`diagnostics.py`)
**Responsibilities:**
- Startup diagnostic logging
- Check for common browser executables via `shutil.which()`
- Verify existence of common browser data directories
- Log placeholder task categories

**Current Status:** Placeholder implementation for smoke testing

## Data Flow

### Program Detection Flow
1. User clicks "Scan Programs"
2. GUI calls `collect_programs()` with `ProgramProbe` list
3. For each probe:
   - Check registry keys → any match = "present"
   - Check file patterns → any match = "present"
   - Check running processes → any match = "running"
4. Return table rows with detection results
5. GUI populates Treeview widget

### Cleaning Flow
1. User selects detected program from table
2. GUI loads cleaner options:
   - Try CleanerML file (e.g., `bleachbit/cleaners/google_chrome.xml`)
   - Fallback to `chromium_cleaner_options()` for Chromium-like browsers
3. Display checkboxes for each `CleanerOption`
4. User selects options, clicks Preview or Clean
5. Preview: aggregate all `DeleteAction.preview()` results → log items
6. Clean: aggregate all `DeleteAction.execute()` results → log counts and bytes

### Logging Flow
1. App startup: configure loguru with two sinks
   - Sink 1: rich console (colored stdout)
   - Sink 2: GUI textbox (append_console callback)
2. All modules use `logger.info()`, `logger.warning()`, `logger.error()`
3. Stdlib logging is intercepted into loguru via `InterceptHandler`
4. GUI Debug panel displays live log stream

## File System Layout
```
privacy_eraser/
├─ src/privacy_eraser/
│  ├─ __init__.py (version)
│  ├─ __main__.py (entry point)
│  ├─ gui.py (UI)
│  ├─ cleaning.py (engine)
│  ├─ cleanerml_loader.py (XML parser)
│  ├─ detect_windows.py (detection)
│  └─ diagnostics.py (startup checks)
├─ tests/
│  ├─ conftest.py (fixtures)
│  ├─ test_cleaning_actions.py
│  ├─ test_cleaning_chromium.py
│  ├─ test_cleanerml_loader.py
│  └─ test_detect_windows.py
├─ bleachbit/cleaners/ (upstream CleanerML definitions)
├─ docs/ (detailed documentation)
├─ pyproject.toml (uv project config)
├─ uv.lock
└─ readme.md
```

## Platform-Specific Code
- **Windows-only:** `detect_windows.py` (guarded imports: `winreg`)
- **Cross-platform:** `cleaning.py`, `cleanerml_loader.py`
- **Tests:** Windows-only tests skip on non-Windows via pytest marker

## Planned Components (Not Yet Implemented)
- **Scheduler:** APScheduler for background tasks; Windows Task Scheduler integration
- **Settings Persistence:** SQLite database for user preferences, schedules, logs
- **Auto-Update:** GitHub Releases API integration with SHA256 verification
- **License System:** Key validation for commercial/enterprise tiers
- **Presets:** Quick Clean, Security Clean, Full Clean profiles
- **Advanced CleanerML:** Support for `command="winreg.delete"`, `command="json"`, etc.
- **macOS/Linux Detection:** Cross-platform browser detection modules

## Design Principles
1. **Modular:** Each module has single responsibility
2. **Safe:** All tests run in sandbox; no real user data access
3. **Extensible:** CleanerML compatibility allows community cleaners
4. **Transparent:** Rich logging for all operations
5. **Graceful Degradation:** Fallbacks (CustomTkinter → tkinter, CleanerML → built-in)

