# 02_TECHNICAL_ARCHITECTURE

**Last Updated:** 2025-10-09  
**Status:** MVP implementation in progress

---

## Technology Stack

### Core Technologies (✅ Implemented)
- **Language:** Python 3.12+
- **Package Manager:** uv (fast, modern Python package installer)
- **GUI Framework:** CustomTkinter 5.2.0 (with tkinter fallback)
- **Logging:** loguru 0.7.2 + rich 13.7.1
- **Process Management:** psutil 5.9.8
- **Testing:** pytest 8.3+, pytest-cov 5.0+

### Dependencies (pyproject.toml)
```toml
[project.dependencies]
customtkinter==5.2.0
pillow==10.0.0
setuptools>=68
loguru==0.7.2
rich==13.7.1
psutil==5.9.8

[project.optional-dependencies.test]
pytest>=8.3.0
pytest-cov>=5.0.0
pytest-mock>=3.14.0
```

### Planned Technologies (🔜 Not Implemented)
- **Scheduler:** APScheduler 3.10+ (background jobs) + Windows Task Scheduler API
- **Database:** SQLite3 (settings, logs, statistics)
- **Installer:** PyInstaller + Inno Setup
- **Auto-Update:** requests 2.31+ (GitHub Releases API)
- **Notifications:** winotify 1.1+ (Windows toast notifications)

---

## Module Architecture

### Current Module Structure (✅ Implemented)

```
src/privacy_eraser/
├─ __init__.py              # Package version (__version__ = "0.1.0")
├─ __main__.py              # Entry point (main() → run_gui())
├─ gui.py                   # CustomTkinter GUI application
├─ cleaning.py              # Deletion engine (DeleteAction, CleanerOption)
├─ cleanerml_loader.py      # BleachBit XML parser
├─ detect_windows.py        # Windows program detection (registry/file/process)
└─ diagnostics.py           # Startup diagnostics (placeholder)
```

### Module Responsibilities

#### `__main__.py`
**Purpose:** Application entry point

**Exports:**
- `main()` → int - Launches GUI and returns exit code

**Flow:**
```python
def main() -> int:
    run_gui()  # Blocks until GUI closed
    return 0
```

#### `gui.py`
**Purpose:** GUI application and user interaction

**Framework:**
- Primary: CustomTkinter (modern themed widgets)
- Fallback: tkinter (stdlib, always available)

**Components:**
- Main window (900x600)
- Program detection table (ttk.Treeview)
- Cleaner options panel (checkboxes, Select/Clear All)
- Action buttons (Scan, Preview, Clean, Hide/Show Options)
- Debug panel (Variables snapshot, Console log stream)

**Key Functions:**
- `run_gui()` - Initialize and run main loop
- `_configure_logging(append_console)` - Wire loguru sinks
- `_default_probes()` - Define browser detection probes
- `_populate_cleaners_for(program, user_data)` - Load CleanerML or built-in options

**Dependencies:**
- `detect_windows.collect_programs()` - Scan for installed browsers
- `cleaning.chromium_cleaner_options()` - Built-in Chromium cleaners
- `cleanerml_loader.load_cleaner_options_from_file()` - XML cleaners
- `diagnostics.emit_startup_placeholders()` - Startup checks

#### `cleaning.py`
**Purpose:** Core deletion engine (cross-platform)

**Classes:**
- `DeleteAction` - Single file/glob/walk deletion operation
  - `.preview()` → list[str] - List matching paths
  - `.execute()` → (count, bytes) - Delete and return stats
- `CleanerOption` - Group of actions with metadata
  - `.preview()` → list[str] - Aggregate all action previews
  - `.execute()` → (count, bytes) - Execute all actions

**Functions:**
- `iter_search(search_type, pattern)` - Yield matching paths
- `chromium_cleaner_options(user_data_dir)` - Built-in Chromium presets

**Search Modes:**
- `file` - Single file (os.path.lexists)
- `glob` - Glob pattern (glob.iglob)
- `walk.files` - Recursive files (os.walk)
- `walk.all` - Files + directories (os.walk)
- `walk.top` - Walk + include top directory

**Example:**
```python
action = DeleteAction("glob", r"C:\Temp\*.log")
items = action.preview()  # ["C:\Temp\a.log", "C:\Temp\b.log"]
count, bytes = action.execute()  # (2, 1024)
```

#### `cleanerml_loader.py`
**Purpose:** Parse BleachBit-compatible XML cleaner definitions

**Main Function:**
- `load_cleaner_options_from_file(pathname)` → list[CleanerOption]

**XML Features Supported:**
- ✅ OS filtering (`<cleaner os="windows">`)
- ✅ Variables (`<var name="TMP"><value os="windows">%TEMP%</value></var>`)
- ✅ Multi-var expansion (`$$TMP$$` → multiple values)
- ✅ Delete actions (`<action command="delete" search="glob" path="...">`)

**XML Features NOT Supported (Future):**
- ❌ Registry deletion (`command="winreg.delete"`)
- ❌ JSON modification (`command="json"`)
- ❌ INI modification (`command="ini"`)

**Example CleanerML:**
```xml
<cleaner os="windows">
  <var name="CHROME"><value>%LOCALAPPDATA%\Google\Chrome\User Data</value></var>
  <option id="cache">
    <label>Cache</label>
    <description>Delete browser cache</description>
    <action command="delete" search="walk.files" path="$$CHROME$$\Default\Cache" />
  </option>
</cleaner>
```

#### `detect_windows.py`
**Purpose:** Windows-only program detection

**Platform Guard:**
```python
if os.name == "nt":
    import winreg
else:
    winreg = None  # Graceful no-op on non-Windows
```

**Classes:**
- `ProgramProbe` - Detection criteria for a single program
  - `registry_keys` - HKCU/HKLM paths
  - `file_patterns` - Paths with %ENVVAR% expansion
  - `process_names` - Executable names

**Functions:**
- `registry_key_exists(full_key)` → bool - Check registry (e.g., `HKLM\SOFTWARE\...`)
- `detect_file_glob(pattern)` → bool - Expand vars and check files
- `is_process_running_windows(exename, same_user)` → bool - psutil check
- `collect_programs(probes)` → list[dict] - Aggregate detection results

**Detection Logic:**
```python
probe = ProgramProbe(
    name="Chrome",
    registry_keys=("HKCU\\Software\\Google\\Chrome",),
    file_patterns=(r"%LOCALAPPDATA%\Google\Chrome\User Data",),
    process_names=("chrome.exe",),
)
rows = collect_programs([probe])
# [{"name": "Chrome", "present": "yes", "running": "no", "source": "registry,files,process"}]
```

#### `diagnostics.py`
**Purpose:** Startup diagnostics and smoke tests

**Current Implementation:** Placeholder

**Function:**
- `emit_startup_placeholders()` - Log browser executables, data paths, task categories

**Output:**
```
[INFO] found executable: chrome -> C:\Program Files\Google\Chrome\chrome.exe
[INFO] path exists: C:\Users\...\Chrome\User Data\Default (15 entries)
[INFO] placeholder tasks: browser cache, cookies, history, session, autofill
```

**Future:** Real browser size calculation, schedule validation, warnings

---

## Data Flow

### 1. Application Startup
```
main() → run_gui()
  ├─ Initialize CustomTkinter window
  ├─ Configure loguru sinks (rich + GUI textbox)
  ├─ Create UI components (table, buttons, debug panel)
  ├─ Call emit_startup_placeholders()
  └─ Enter mainloop (blocking)
```

### 2. Program Detection (Scan)
```
User clicks "Scan Programs"
  └─ run_scan()
      ├─ Create _default_probes() (9 browsers)
      ├─ For each probe:
      │   ├─ Log registry/file/process checks
      │   └─ Aggregate detection results
      ├─ collect_programs(probes) → rows
      └─ Populate Treeview table
```

### 3. Cleaner Loading (Selection)
```
User clicks browser row in table
  └─ on_select_program()
      ├─ _guess_user_data(program_name) → user_data_dir
      ├─ Try load CleanerML:
      │   ├─ Map program → XML file (xml_map)
      │   ├─ load_cleaner_options_from_file()
      │   └─ On success: use CleanerML options
      └─ Fallback: chromium_cleaner_options(user_data_dir)
      ├─ Clear old checkboxes
      └─ Create new checkboxes for each option
```

### 4. Preview Workflow
```
User selects options, clicks "Preview"
  └─ preview_clean()
      ├─ Filter selected options (checked checkboxes)
      ├─ For each option:
      │   ├─ items = option.preview()
      │   ├─ Log first 50 items
      │   └─ Log "... and N more"
      └─ Log total item count
```

### 5. Clean Workflow
```
User clicks "Clean"
  └─ execute_clean()
      ├─ Filter selected options
      ├─ For each option:
      │   ├─ count, bytes = option.execute()
      │   └─ Log "{label}: deleted {count} items, {bytes} bytes"
      └─ Log total stats
```

---

## Logging Architecture (✅ Implemented)

### Logging Stack
1. **loguru** - Structured logging with levels, context, formatting
2. **rich** - Terminal color/formatting (ANSI escape codes)
3. **GUI sink** - Custom callback to append to Tkinter Text widget

### Configuration (in `gui.py`)
```python
logger.remove()  # Remove default handler

# Sink 1: Terminal (rich-colored)
logger.add(
    lambda msg: rich_console.print(msg, end=""),
    level="INFO",
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
           "<level>{message}</level>",
)

# Sink 2: GUI (plain text)
logger.add(
    lambda msg: append_console(str(msg)),
    level="INFO",
    format="[ {time:HH:mm:ss} ] {level}: {message}",
)
```

### Stdlib Logging Interception
```python
class InterceptHandler(logging.Handler):
    def emit(self, record):
        level = logger.level(record.levelname).name
        logger.opt(depth=6, exception=record.exc_info).log(level, record.getMessage())

logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
```

**Effect:** All stdlib `logging` calls (including third-party libraries) flow into loguru.

### Log Levels
- `DEBUG` - Verbose internal details (not used in MVP)
- `INFO` - Normal operation (scan, preview, clean)
- `WARNING` - Non-fatal issues (missing file, browser running)
- `ERROR` - Fatal issues (permission denied, exception)

### GUI Integration
- **Debug Panel Console:** Live stream of loguru messages
- **Scrolling:** Auto-scroll to bottom on new message
- **Clear Button:** Reset console textbox

---

## Planned Architecture (🔜 Not Implemented)

### Scheduler Module (Future)
**File:** `src/privacy_eraser/scheduler.py`

**Dependencies:**
- APScheduler (background jobs)
- `win32com.client` (Windows Task Scheduler COM API)

**Features:**
- Schedule creation (daily/weekly/monthly/idle)
- Pre-execution browser closure
- Post-execution notifications
- SQLite persistence (`schedules` table)

**Example:**
```python
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(
    func=run_clean_job,
    trigger="cron",
    hour=23,
    minute=0,
    id="nightly_clean",
)
scheduler.start()
```

### Settings Persistence (Future)
**File:** `src/privacy_eraser/database.py`

**Database:** `privacy_eraser.db` (SQLite3)

**Tables:**
```sql
CREATE TABLE settings (
    key TEXT PRIMARY KEY,
    value TEXT
);

CREATE TABLE schedules (
    id INTEGER PRIMARY KEY,
    name TEXT,
    cron TEXT,
    preset_id TEXT,
    enabled INTEGER
);

CREATE TABLE presets (
    id TEXT PRIMARY KEY,
    name TEXT,
    options_json TEXT  -- JSON array of option IDs
);

CREATE TABLE history (
    id INTEGER PRIMARY KEY,
    timestamp INTEGER,
    preset_id TEXT,
    count INTEGER,
    bytes INTEGER
);
```

**API:**
```python
from privacy_eraser.database import save_setting, load_setting

save_setting("theme", "dark")
theme = load_setting("theme", default="system")
```

### Auto-Update Module (Future)
**File:** `src/privacy_eraser/updater.py`

**Dependencies:**
- `requests` (HTTP client)
- `packaging` (version comparison)
- `hashlib` (SHA256 verification)

**GitHub Releases API:**
```python
import requests

response = requests.get("https://api.github.com/repos/user/privacy_eraser/releases/latest")
latest_version = response.json()["tag_name"]  # "v0.2.0"
download_url = response.json()["assets"][0]["browser_download_url"]
```

**Update Flow:**
1. Background check (on startup or daily)
2. Compare `__version__` with latest
3. Download installer to temp directory
4. Verify SHA256 checksum
5. Prompt user or silent install
6. Restart application

### License System (Future)
**File:** `src/privacy_eraser/license.py`

**Tiers:**
- Free (individual, Busan City, education)
- Commercial (₩19,900/year)
- Enterprise (custom)

**Validation:**
```python
def validate_license(email: str, key: str) -> dict:
    # Online validation via API
    response = requests.post("https://api.privacyeraser.com/validate", {
        "email": email,
        "key": key,
        "hardware_id": get_hardware_id(),
    })
    return response.json()  # {"valid": True, "tier": "commercial", "expires": "2026-01-01"}
```

**Storage:** Encrypted license file (`license.dat`)

---

## Security Architecture

### Current Safeguards (✅ Implemented)
1. **Sandboxed Tests:** All tests run in `tmp_path` with patched env vars
2. **No Network:** No HTTP requests in MVP (except future updates)
3. **No Telemetry:** Zero data collection or phone-home
4. **OS Filtering:** CleanerML `os="windows"` prevents cross-platform accidents
5. **Warnings:** Dangerous options (passwords) show explicit warnings

### Future Security Enhancements (🔜 Planned)
1. **Secure Deletion:** DoD 5220.22-M multi-pass overwrite
2. **Process Termination:** Confirm before killing browser processes
3. **Whitelist:** Never delete from protected directories (e.g., System32)
4. **Code Signing:** DigiCert certificate for installer
5. **HTTPS:** TLS 1.3 for license/update API calls
6. **Sandboxing:** Run deletion engine in restricted process (future)

---

## Performance Considerations

### Current Performance (MVP)
| Metric | Value | Notes |
|--------|-------|-------|
| Startup Time | <2s | Cold start with GUI |
| Memory Usage | ~50MB | Idle with Debug panel closed |
| Scan Time | <1s | 9 browsers, 27 checks |
| Clean Time | Varies | Depends on file count (typically <5s for cache) |

### Optimization Opportunities (Future)
1. **Parallel Scanning:** Thread pool for multi-browser detection
2. **Incremental Preview:** Stream results instead of blocking
3. **Smart Caching:** Remember detection results (invalidate on schedule)
4. **Lazy Loading:** Load CleanerML only when program selected
5. **Batch Deletion:** OS-level batch delete API (faster than file-by-file)

---

## Testing Architecture

### Test Structure (✅ Implemented)
```
tests/
├─ conftest.py                   # Fixtures (sandbox, seed_walk_tree, make_glob_files)
├─ test_cleaning_actions.py      # DeleteAction, iter_search
├─ test_cleaning_chromium.py     # Built-in Chromium options
├─ test_cleanerml_loader.py      # XML parsing, var expansion
└─ test_detect_windows.py        # Windows detection (skipped on non-Windows)
```

### Coverage (2025-10-09)
- `cleaning.py`: 90%
- `cleanerml_loader.py`: 85%
- `detect_windows.py`: 70% (Windows-only)
- `gui.py`: <10% (manual testing)

### Sandbox Fixture
All tests use `sandbox` fixture from `conftest.py`:
```python
@pytest.fixture
def sandbox(tmp_path, monkeypatch):
    sandbox_root = tmp_path / "sandbox"
    sandbox_root.mkdir()
    monkeypatch.setenv("LOCALAPPDATA", str(sandbox_root / "LOCALAPPDATA"))
    monkeypatch.setenv("APPDATA", str(sandbox_root / "APPDATA"))
    # ... more env vars
    return sandbox_root
```

**Guarantees:**
- All file operations isolated to `tmp_path`
- Environment variables point inside sandbox
- No real user data accessed
- Automatic cleanup via pytest

### Running Tests
```bash
# Quick run
uv run -m pytest -q

# With coverage
uv run -m pytest --cov=privacy_eraser --cov-report=term-missing

# Specific module
uv run -m pytest tests/test_cleaning.py -v
```

---

## Deployment Architecture (🔜 Planned)

### Build Pipeline (Future)
1. **PyInstaller:** Bundle Python + dependencies into `.exe`
2. **Inno Setup:** Create professional Windows installer
3. **Code Signing:** Sign `.exe` and installer with DigiCert certificate
4. **GitHub Actions:** Automated CI/CD on tag push

### Installer Features (Future)
- Custom install directory
- Start menu shortcuts
- Uninstaller
- Silent install (`/SILENT` flag)
- Upgrade detection

### Distribution Channels (Future)
1. **GitHub Releases:** Direct download
2. **Microsoft Store:** Future consideration
3. **Chocolatey:** Community package
4. **Ninite:** Partner integration (enterprise)

---

## Platform-Specific Details

### Windows 10/11 (Primary Target)
- ✅ Registry detection (`winreg`)
- ✅ Process detection (`psutil`)
- ✅ CustomTkinter GUI (native look)
- 🔜 Task Scheduler API (`win32com`)
- 🔜 Toast notifications (`winotify`)

### Linux (Experimental)
- ✅ GUI works (CustomTkinter)
- ✅ File deletion works
- ❌ No registry detection (module no-op)
- 🔜 Browser detection via `.desktop` files

### macOS (Experimental)
- ✅ GUI works (CustomTkinter)
- ✅ File deletion works
- ❌ No registry detection (module no-op)
- 🔜 Browser detection via `.app` bundles

---

## External Dependencies

### BleachBit Cleaners (Referenced)
- **Location:** `bleachbit/cleaners/` (not modified by us)
- **Format:** CleanerML XML
- **License:** GPL-3.0 (BleachBit upstream)
- **Usage:** Read-only; loaded dynamically by `cleanerml_loader.py`

### Supported CleanerML Files (Current)
- `google_chrome.xml`
- `microsoft_edge.xml`
- `brave.xml`
- `opera.xml`
- (Others available but not mapped in GUI yet)

---

## Configuration Files (Future)

### `config.json` (Planned)
```json
{
  "theme": "system",
  "auto_scan_on_startup": true,
  "show_debug_panel": false,
  "language": "en",
  "check_for_updates": true
}
```

### `privacy_eraser.db` (Planned)
SQLite database for settings, schedules, presets, history.

---

## Error Handling Strategy

### Current Approach
- **Graceful Degradation:** CustomTkinter → tkinter fallback
- **Try-Except:** Import guards for optional modules
- **Logging:** All errors logged to console (no silent failures)

### Exception Hierarchy (Future)
```python
class PrivacyEraserError(Exception): pass
class DetectionError(PrivacyEraserError): pass
class CleaningError(PrivacyEraserError): pass
class SchedulerError(PrivacyEraserError): pass
class LicenseError(PrivacyEraserError): pass
```

---

## Maintainability Principles

1. **Modular:** Each module has single responsibility
2. **Testable:** All business logic isolated from GUI
3. **Documented:** Docstrings, type hints, architecture docs
4. **Versioned:** Semantic versioning (`__version__` in `__init__.py`)
5. **Logged:** Comprehensive logging for debugging
6. **Cross-Platform:** Core engine works on Windows/Linux/macOS

---

For detailed API examples and usage, see `docs/01_CORE_FEATURES.md`.  
For development workflows, see `.cursor/context/runbook.md`.

