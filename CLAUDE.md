# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**PrivacyEraser** is a professional privacy management tool with a PySide6 (Qt6) GUI and BleachBit-inspired cleaning engine. It detects installed browsers on Windows and cleans privacy-sensitive data (cache, cookies, history, passwords, etc.) using CleanerML definitions.

**Primary Platform:** Windows 10/11
**Package Manager:** `uv` (NOT pip, poetry, or conda)
**Python Version:** 3.12+
**GUI Framework:** PySide6 (Qt6) with Qt Material theming

## Common Development Commands

### Environment Setup
```bash
# Install dependencies
uv sync

# Install with test dependencies
uv sync --extra test
```

### Running the Application
```bash
# Launch GUI (standard method)
uv run privacy_eraser

# Launch with debug mode
uv run privacy_eraser --debug

# Launch background/daemon mode
uv run privacy_eraser --mode background
```

### Testing
```bash
# Run all tests (quick mode)
uv run -m pytest -q

# Run with verbose output
uv run -m pytest -v

# Run specific test file
uv run -m pytest tests/test_cleaning.py -v

# Run specific test function
uv run -m pytest tests/test_cleaning.py::test_iter_search_file_and_glob -v

# Show coverage report
uv run -m pytest --cov=privacy_eraser --cov-report=term-missing

# Coverage HTML report
uv run -m pytest --cov=privacy_eraser --cov-report=html
# Then open htmlcov/index.html
```

### Dependency Management
```bash
# Add new runtime dependency
uv add <package>

# Add new test dependency
uv add --optional test <package>

# Update all dependencies
uv lock --upgrade

# Sync after pulling changes
uv sync
```

## Architecture Overview

### Three-Layer Architecture

#### 1. **PySide6 Frontend (GUI Layer)**
The GUI is built with dual-mode support (Easy Mode wizard + Advanced Mode sidebar):

- **Entry Point:** [src/privacy_eraser/__main__.py](src/privacy_eraser/__main__.py) - CLI argument parsing, daemon launcher
- **Main Window:** [src/privacy_eraser/gui.py](src/privacy_eraser/gui.py) - Qt application lifecycle, mode switching, header coordination
- **Easy Mode:** [src/privacy_eraser/gui_easy_mode.py](src/privacy_eraser/gui_easy_mode.py) - 3-step wizard UI (Select Browsers → Choose Options → Review & Clean)
- **Advanced Mode:** [src/privacy_eraser/gui_advanced_mode.py](src/privacy_eraser/gui_advanced_mode.py) - Sidebar navigation with browser list + main panel
- **Settings Dialog:** [src/privacy_eraser/gui_settings.py](src/privacy_eraser/gui_settings.py) - Tabbed modal for theme, debug, advanced settings
- **Debug Panel:** [src/privacy_eraser/gui_debug.py](src/privacy_eraser/gui_debug.py) - Collapsible developer panel with variables + console
- **Custom Widgets:** [src/privacy_eraser/gui_widgets.py](src/privacy_eraser/gui_widgets.py) - Reusable Qt components (cards, buttons, etc.)
- **Integration Layer:** [src/privacy_eraser/gui_integration.py](src/privacy_eraser/gui_integration.py) - Bridge between GUI and core engine

#### 2. **Core Engine (Business Logic)**
BleachBit-inspired cleaning engine with platform abstraction:

- **Cleaner Engine:** [src/privacy_eraser/core/cleaner_engine.py](src/privacy_eraser/core/cleaner_engine.py) - Action orchestration, CleaningAction dataclasses, WinClean script execution
- **File Utilities:** [src/privacy_eraser/core/file_utils.py](src/privacy_eraser/core/file_utils.py) - Safe deletion with whitelist checking, size calculation, search modes (file/glob/walk)
- **Windows Utilities:** [src/privacy_eraser/core/windows_utils.py](src/privacy_eraser/core/windows_utils.py) - Registry operations, process detection, locked file handling

#### 3. **Supporting Modules**
State management, persistence, and platform detection:

- **App State:** [src/privacy_eraser/app_state.py](src/privacy_eraser/app_state.py) - QObject-based reactive state with Qt signals (ui_mode, wizard_step, selections)
- **Settings DB:** [src/privacy_eraser/settings_db.py](src/privacy_eraser/settings_db.py) - SQLite persistence for preferences, presets, history (~/.privacy_eraser/settings.db)
- **Detection:** [src/privacy_eraser/detect_windows.py](src/privacy_eraser/detect_windows.py) - Browser detection via registry, files, process checks (Chrome, Edge, Firefox, Brave, Opera, Whale, etc.)
- **CleanerML Loader:** [src/privacy_eraser/cleanerml_loader.py](src/privacy_eraser/cleanerml_loader.py) - XML parser for BleachBit-compatible cleaning definitions
- **Scheduler:** [src/privacy_eraser/scheduler.py](src/privacy_eraser/scheduler.py) - APScheduler integration for automated cleaning (Phase 3 feature)
- **Daemon:** [src/privacy_eraser/daemon.py](src/privacy_eraser/daemon.py) - Background service and GUI launcher

### Key Design Patterns

#### Reactive State with Qt Signals
The app uses Qt signals/slots for UI updates:
```python
# app_state.py
class AppState(QObject):
    ui_mode_changed = Signal(str)
    browser_selected = Signal(str)
    # ...

# GUI components connect to signals
app_state.ui_mode_changed.connect(on_mode_change)
```

#### Dual-Mode Architecture
Easy Mode (wizard) and Advanced Mode (sidebar) share the same underlying state but render differently. Mode switching destroys/rebuilds UI while preserving selections.

#### BleachBit CleanerML Compatibility
Cleaning definitions are loaded from XML files in `bleachbit/cleaners/`. This allows community-contributed browser support without code changes.

#### Search Modes for File Operations
The file_utils module supports multiple search patterns:
- `file`: Single file path
- `glob`: Glob pattern matching
- `walk.files`: Recursive files only
- `walk.all`: Recursive files + directories
- `walk.top`: walk.all + parent directory itself

## Critical Development Notes

### 1. **Always Use `uv` for Package Management**
This project MUST use `uv` for all Python operations. Never use pip, poetry, or conda:
```bash
# ✅ Correct
uv add loguru
uv run privacy_eraser

# ❌ Wrong
pip install loguru
python -m privacy_eraser
```

### 2. **Windows-Specific Code Must Be Guarded**
Detection and Windows utilities should be platform-aware:
```python
import os

if os.name == "nt":
    # Windows-only imports and logic
    import winreg
    from .core import windows_utils
```

Tests for Windows-only features should use skip markers:
```python
@pytest.mark.skipif(os.name != "nt", reason="Windows-only")
def test_registry_detection():
    ...
```

### 3. **Reactive State Management with Qt Signals**
Always update state through properties to trigger Qt signals:
```python
# ✅ Correct - triggers ui_mode_changed signal
app_state.ui_mode = "advanced"

# ❌ Wrong - bypasses signal system
app_state._ui_mode = "advanced"
```

### 4. **Safe File Operations**
The file_utils module provides whitelist protection. Use it instead of direct file operations:
```python
# ✅ Correct - respects whitelist, handles errors
from privacy_eraser.core import file_utils
file_utils.safe_delete(path)

# ❌ Wrong - no safety checks
os.remove(path)
```

### 5. **Testing Isolation with Sandbox**
All tests MUST use the `sandbox` fixture to avoid touching real user data:
```python
def test_cache_cleaning(sandbox):
    # sandbox provides isolated LOCALAPPDATA, APPDATA, etc.
    cache_path = sandbox / "LOCALAPPDATA" / "Google" / "Chrome" / "User Data" / "Default" / "Cache"
    cache_path.mkdir(parents=True)
    # ... test logic ...
```

### 6. **CleanerML Path Resolution**
Browser data paths use environment variable expansion:
```xml
<!-- CleanerML definition -->
<action search="walk.files" path="%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache\*"/>
```

The engine expands `%ENVVAR%` and Windows-specific variants (e.g., `%ProgramW6432%`).

### 7. **Settings Persistence**
Settings are stored in SQLite at `~/.privacy_eraser/settings.db`:
```python
from privacy_eraser.settings_db import save_setting, load_setting

# Save preference
save_setting("ui_mode", "advanced")

# Load on startup
ui_mode = load_setting("ui_mode", default="easy")
```

## Testing Strategy

### Test Organization
- `tests/` - All test files (pytest suite)
- `tests/conftest.py` - Shared fixtures (sandbox, monkeypatch helpers)
- Test files follow `test_*.py` naming convention

### Running Specific Tests
```bash
# Single test file
uv run -m pytest tests/test_cleaning.py

# Single test function
uv run -m pytest tests/test_cleaning.py::test_name

# Tests matching pattern
uv run -m pytest -k "cache"

# Show print statements
uv run -m pytest -s

# Drop into debugger on failure
uv run -m pytest --pdb
```

### Coverage Requirements
- Target: >95% coverage for core modules
- Current: ~80-90% (see [README.md](readme.md#run-tests))
- Check with: `uv run -m pytest --cov=privacy_eraser --cov-report=term-missing`

## Code Style Guidelines

### Type Hints
All public functions must have type hints:
```python
from __future__ import annotations

def calculate_size(path: str) -> int:
    """Calculate total size of files in path."""
    ...
```

### Logging
Use `loguru` for logging (NOT stdlib logging directly):
```python
from loguru import logger

logger.info("Scanning for browsers...")
logger.warning("Browser is running: {}", browser_name)
logger.error("Failed to delete: {}", path)
```

### Import Organization
Organize imports as: stdlib, third-party, local (separated by blank lines):
```python
import os
import sys
from pathlib import Path

from loguru import logger
from PySide6.QtWidgets import QWidget

from .app_state import app_state
from .core import file_utils
```

## Platform Support

### Current Status
- **Primary:** Windows 10/11 (full feature set)
- **Development:** macOS/Linux (GUI works with automatic mocking)

### Detection Behavior by Platform
- **Windows:** Registry + file + process detection (real data)
- **macOS/Linux:** Automatic mock data for UI development

### macOS/Linux Development with Mock Data

The project includes automatic mock data support for developing the GUI on non-Windows platforms:

**What gets mocked automatically:**
- **Browser detection** ([src/privacy_eraser/mock_windows.py](src/privacy_eraser/mock_windows.py))
  - Returns 6 fake browsers: Chrome, Edge, Firefox, Brave, Opera (not installed), Whale
  - Simulates registry checks, file glob detection, process detection
- **Cleaner options**
  - Returns realistic options: Cache, Cookies, History, Session, Passwords, Autofill
  - Includes fake sizes (MB), file counts, last cleaned timestamps, warnings
- **Cleaning execution**
  - Simulates file deletion with random counts (10-500 files) and sizes (1MB-200MB)
  - 10% chance of simulated permission errors for testing error handling

**How to use on macOS:**
```bash
# Just run normally - mocking activates automatically
uv run privacy_eraser

# The GUI launches with mock browsers and options
# All cleaning operations are simulated (no real files touched)
```

**Automatic activation:**
Mock data activates when `os.name != "nt"` in these modules:
- [src/privacy_eraser/detect_windows.py](src/privacy_eraser/detect_windows.py) - Mock registry/file/process checks
- [src/privacy_eraser/gui_integration.py](src/privacy_eraser/gui_integration.py) - Mock scan results and cleaner options

**For UI development workflow:**
1. Launch app: `uv run privacy_eraser`
2. Click "Scan Programs" → See 6 mock browsers
3. Select browser (e.g., Chrome) → See mock cleaner options with sizes
4. Test Easy Mode wizard flow (3 steps)
5. Test Advanced Mode sidebar navigation
6. Click "Preview" → See fake file paths
7. Click "Clean" → See simulated deletion results
8. All UI interactions work identically to Windows

**Customizing mock data:**
Edit [src/privacy_eraser/mock_windows.py](src/privacy_eraser/mock_windows.py):
```python
# Add/modify browsers
MOCK_BROWSERS = [
    {
        "name": "Custom Browser",
        "icon": "X",
        "color": "#FF0000",
        "present": "yes",
        "cache_size": "100 MB",
        # ...
    }
]

# Modify cleaner options
MOCK_CLEANER_OPTIONS = [...]

# Adjust simulation behavior
def mock_execute_cleaning(...):
    # Change success rate, file counts, error frequency
```

### Future Plans
See [docs/ROADMAP.md](docs/ROADMAP.md) Phase 6 for native macOS/Linux support (real detection).

## Reference Materials

### Documentation
- [README.md](readme.md) - Quickstart and feature overview
- [docs/05_1_GUI_REDESIGN.md](docs/05_1_GUI_REDESIGN.md) - Detailed GUI specification
- [docs/ROADMAP.md](docs/ROADMAP.md) - Development roadmap and milestones
- [TODO.md](TODO.md) - Current sprint tasks
- [.cursor/context/runbook.md](.cursor/context/runbook.md) - Detailed commands and workflows
- [.cursor/rules](.cursor/rules) - Project-specific development rules

### Legacy/Reference Code
- [reference/bleachbit_original/](reference/bleachbit_original/) - Original BleachBit code for reference
- [reference/deprecated/](reference/deprecated/) - Old implementations archived

### BleachBit Integration
CleanerML files are in `bleachbit/cleaners/`:
- `chrome.xml`, `firefox.xml`, `opera.xml` - Browser cleaning definitions
- `brave.xml`, `vivaldi.xml`, `whale.xml` - Additional browser support
- Format is BleachBit-compatible (can share community definitions)

## Common Pitfalls to Avoid

1. **Never access real browser data in tests** - Always use `sandbox` fixture
2. **Never use pip/poetry** - Always use `uv` commands
3. **Never commit platform-specific config** - Guard with `if os.name == "nt"`
4. **Never bypass state signals** - Use properties, not private `_` attributes
5. **Never hardcode paths** - Use environment variable expansion or Path objects
6. **Never skip failing tests** - Fix the root cause instead
7. **Never access Windows registry without try/except** - Not all users have admin rights

## Debugging Tips

### Enable Debug Panel in GUI
1. Launch app: `uv run privacy_eraser`
2. Click Settings → Debug tab → Enable Debug Panel
3. View Variables and Console tabs at bottom

### Increase Log Verbosity
```bash
# Debug mode via CLI
uv run privacy_eraser --debug

# Or edit gui.py temporarily:
logger.add(..., level="DEBUG")
```

### Test-Specific Debugging
```bash
# Show print/log output
uv run -m pytest -s

# Drop into debugger on failure
uv run -m pytest --pdb

# Run single test with full output
uv run -m pytest tests/test_name.py::test_function -vv -s
```

## Development Workflow Best Practices

1. **Sync dependencies** after pulling: `uv sync`
2. **Run tests before commit**: `uv run -m pytest -q`
3. **Check coverage periodically**: `uv run -m pytest --cov`
4. **Update TODO.md** when completing tasks
5. **Test on Windows** before pushing GUI changes
6. **Keep commits focused** - one feature/fix per commit
7. **Write descriptive commit messages** - `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`

## Current Development Status (v1.0.0)

### ✅ Completed (Phase 1)
- PySide6 dual-mode GUI (Easy + Advanced)
- BleachBit-inspired core engine
- Browser detection (Windows registry + files + processes)
- CleanerML support (Chrome, Edge, Firefox, Brave, Opera, Whale)
- Settings persistence (SQLite)
- Debug panel with console + variables
- Comprehensive test suite (>95% coverage)

### 🚧 In Progress (Phase 2)
- Additional browser probes (Vivaldi, LibreWolf, Waterfox)
- Error handling improvements
- File count/size preview before deletion

### 🔜 Planned
- **Phase 3:** Scheduling system (APScheduler + Windows Task Scheduler)
- **Phase 4:** Auto-update + License system
- **Phase 5:** Installer (PyInstaller + Inno Setup) + Code signing
- **Phase 6:** macOS/Linux support

See [docs/ROADMAP.md](docs/ROADMAP.md) for detailed milestones.

## Frequently Asked Questions

### Q: How do I add support for a new browser?
A: Create or obtain a CleanerML XML file in `bleachbit/cleaners/`, then update the probe list in `gui.py` → `_default_probes()`.

### Q: How do I add a new built-in cleaner option?
A: Edit `cleaning.py` → `chromium_cleaner_options()` and add a new `CleanerOption` with appropriate `DeleteAction` list. Write tests in `tests/test_cleaning_chromium.py`.

### Q: Why use `uv` instead of pip?
A: Faster, deterministic builds with lockfile support. See [pyproject.toml](pyproject.toml) for project configuration.

### Q: How do I test Windows-specific code on Linux/macOS?
A: Tests for Windows-only features use `@pytest.mark.skipif(os.name != "nt")` and are automatically skipped on non-Windows platforms.

### Q: Where are user settings stored?
A: SQLite database at `~/.privacy_eraser/settings.db` (see [settings_db.py](src/privacy_eraser/settings_db.py))

---

**For additional help:**
- Check [.cursor/context/runbook.md](.cursor/context/runbook.md) for detailed commands
- Review [docs/](docs/) for architecture and design documents
- See [TODO.md](TODO.md) for current task priorities
