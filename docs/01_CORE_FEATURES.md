# 01_CORE_FEATURES

**Last Updated:** 2025-10-09  
**Status:** MVP in progress

This document details the core features of PrivacyEraser MVP, distinguishing between implemented and planned functionality.

---

## Browser Detection (✅ Implemented)

### Supported Browsers (Windows)
PrivacyEraser detects the following browsers via registry keys, file patterns, and running processes:

**Chromium-based:**
- Google Chrome
- Microsoft Edge
- Brave Browser
- Opera
- Vivaldi
- Naver Whale
- Arc Browser

**Gecko-based:**
- Mozilla Firefox

**Email Clients:**
- Mozilla Thunderbird

### Detection Methods
1. **Registry Keys:** Query `HKCU` and `HKLM` for installation keys
2. **File Patterns:** Check for configuration files in `%LOCALAPPDATA%` and `%APPDATA%`
   - Supports `%ENVVAR%` expansion (e.g., `%LOCALAPPDATA%\Google\Chrome\User Data`)
3. **Running Processes:** Detect active browser processes (e.g., `chrome.exe`)

### Detection API
```python
from privacy_eraser.detect_windows import ProgramProbe, collect_programs

probe = ProgramProbe(
    name="Google Chrome",
    registry_keys=(r"HKCU\Software\Google\Chrome",),
    file_patterns=(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Preferences",),
    process_names=("chrome.exe",),
)

rows = collect_programs([probe])
# Returns: [{"name": "Google Chrome", "present": "yes", "running": "no", "source": "registry,files,process"}]
```

### GUI Integration
- **Scan Programs Button:** Populates detection table with installed/running browsers
- **Selection:** Click a browser row to load cleaner options
- **Real-time Logging:** All detection checks logged to debug console

---

## Data Deletion Engine (✅ Implemented)

### Search Modes
The cleaning engine supports multiple search strategies:

| Mode | Description | Example Use |
|------|-------------|-------------|
| `file` | Single file | Delete `Cookies` database |
| `glob` | Glob pattern | Delete `*.tmp` files |
| `walk.files` | Recursive files only | Clear cache directory (files) |
| `walk.all` | Files + directories | Clear cache (including subdirs) |
| `walk.top` | Walk + include top dir | Delete entire directory tree |

### DeleteAction API
```python
from privacy_eraser.cleaning import DeleteAction

action = DeleteAction("glob", r"C:\Temp\*.log")
preview = action.preview()  # List of matching paths
count, bytes_deleted = action.execute()  # Delete and return stats
```

### CleanerOption API
Groups multiple actions with metadata:

```python
from privacy_eraser.cleaning import CleanerOption, DeleteAction

option = CleanerOption(
    id="browser_cache",
    label="Browser Cache",
    description="Delete cached web content",
    warning=None,  # Optional warning message
    actions=[
        DeleteAction("walk.files", r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache"),
        DeleteAction("walk.files", r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Code Cache"),
    ]
)

items = option.preview()  # All items across all actions
count, bytes_deleted = option.execute()  # Execute all actions
```

---

## Built-in Chromium Cleaner Options (✅ Implemented)

### Available Options
For Chromium-based browsers (Chrome, Edge, Brave, Whale, Arc, Vivaldi, Opera):

#### 1. Cache
**Deletes:**
- Browser Cache
- Code Cache
- GPU Cache
- Media Cache
- Shader Cache
- Service Worker cache
- File System cache

**Paths:**
```
{UserData}\Default\Cache\
{UserData}\Default\Code Cache\
{UserData}\Default\GPUCache\
{UserData}\Default\Media Cache\
{UserData}\ShaderCache\
{UserData}\Default\Service Worker\
{UserData}\Default\File System\
```

#### 2. Cookies
**Deletes:**
- Cookies database
- Cookies journal
- Network cookies

**Paths:**
```
{UserData}\Default\Cookies
{UserData}\Default\Cookies-journal
{UserData}\Default\Network\Cookies
{UserData}\Default\Network\Cookies-journal
```

#### 3. History
**Deletes:**
- Browsing history
- Favicons
- Top Sites
- Session Storage

**Paths:**
```
{UserData}\Default\History
{UserData}\Default\History-journal
{UserData}\Default\Favicons
{UserData}\Default\Top Sites
{UserData}\Default\Session Storage\
```

#### 4. Session
**Deletes:**
- Current/Last Session tabs
- Extension state
- Sessions directory

**Paths:**
```
{UserData}\Default\Current Session
{UserData}\Default\Current Tabs
{UserData}\Default\Last Session
{UserData}\Default\Last Tabs
{UserData}\Default\Extension State\
{UserData}\Default\Sessions\
```

#### 5. Passwords ⚠️
**Warning:** This will delete all saved passwords

**Deletes:**
- Login Data database

**Paths:**
```
{UserData}\Default\Login Data
{UserData}\Default\Login Data-journal
```

### Usage in Code
```python
from privacy_eraser.cleaning import chromium_cleaner_options

user_data_dir = r"C:\Users\User\AppData\Local\Google\Chrome\User Data"
options = chromium_cleaner_options(user_data_dir)

for opt in options:
    print(f"{opt.id}: {opt.label}")
    items = opt.preview()
    print(f"  Would delete {len(items)} items")
```

---

## CleanerML Loader (✅ Implemented)

### Overview
BleachBit-compatible XML cleaner definitions can be loaded dynamically.

### Supported XML Features
- ✅ `<cleaner os="windows">` - OS filtering
- ✅ `<var name="...">` - Variable definitions with `$$TOKEN$$` expansion
- ✅ `<option id="...">` - Cleaner options with label, description, warning
- ✅ `<action command="delete" search="..." path="...">` - Delete actions
- ❌ Other commands (`winreg.delete`, `json`, `ini`) - Not yet supported

### Example CleanerML
```xml
<cleaner os="windows">
  <var name="CHROME_DATA">
    <value os="windows">%LOCALAPPDATA%\Google\Chrome\User Data</value>
  </var>
  <option id="cache">
    <label>Browser Cache</label>
    <description>Delete cached files</description>
    <action command="delete" search="walk.files" path="$$CHROME_DATA$$\Default\Cache" />
  </option>
</cleaner>
```

### Loading CleanerML
```python
from privacy_eraser.cleanerml_loader import load_cleaner_options_from_file

options = load_cleaner_options_from_file("bleachbit/cleaners/google_chrome.xml")
```

### GUI Integration
The GUI automatically tries to load CleanerML for known browsers:
- `google_chrome.xml` → Google Chrome
- `microsoft_edge.xml` → Microsoft Edge
- `brave.xml` → Brave
- `opera.xml` → Opera
- Falls back to built-in Chromium options for unmapped browsers

---

## Logging System (✅ Implemented)

### Logging Stack
- **loguru:** Structured logging with levels (INFO, WARNING, ERROR, DEBUG)
- **rich:** Colored terminal output with timestamps
- **GUI sink:** Live log display in Debug panel

### Configuration
```python
# Terminal sink (rich-colored)
logger.add(
    lambda msg: rich_console.print(msg, end=""),
    level="INFO",
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
           "<level>{message}</level>",
)

# GUI sink (textbox)
logger.add(
    lambda msg: append_console(str(msg)),
    level="INFO",
    format="[ {time:HH:mm:ss} ] {level}: {message}",
)
```

### Usage
```python
from loguru import logger

logger.info("Scanning programs...")
logger.warning("Browser is running; skip cleaning")
logger.error("Failed to delete file: permission denied")
```

### GUI Debug Panel
- **Variables Section:** App version, Python version, platform, working directory
- **Console Section:** Live log stream (scrollable, clearable)
- **Toggle:** Show/Hide Debug button in header

---

## GUI Features (✅ Implemented)

### Main Window
- **Framework:** CustomTkinter (with tkinter fallback)
- **Size:** 900x600px
- **Theme:** System-based (light/dark auto-detection)

### Components

#### 1. Program Detection Table
- **Columns:** Program | Present | Running | Source
- **Data:** Populated via "Scan Programs" button
- **Interaction:** Click row to load cleaner options

#### 2. Cleaner Options Panel
- **Collapsible:** Show/Hide Options button
- **Dynamic Loading:** Loads options for selected program
- **Checkboxes:** One per cleaner option (with label + description + warning)
- **Bulk Actions:** Select All, Clear All buttons

#### 3. Action Buttons
- **Preview:** Log all items that would be deleted (dry-run)
- **Clean:** Execute deletion and log counts/bytes
- **Scan Programs:** Run detection and populate table

#### 4. Debug Panel
- **Collapsible:** Show/Hide Debug button
- **Variables:** System info snapshot with Refresh button
- **Console:** Live loguru output with Clear button

### User Workflows

#### Workflow 1: Manual Clean
1. Launch app
2. Click "Scan Programs"
3. Select browser from table
4. Check desired cleaner options
5. Click "Preview" to see what would be deleted
6. Click "Clean" to execute deletion
7. Review results in console

#### Workflow 2: Debug Inspection
1. Click "Show Debug"
2. View Variables section for environment info
3. Monitor Console for detailed operation logs
4. Click "Refresh" to update variables
5. Click "Clear" to reset console

---

## Planned Features (🔜 Not Yet Implemented)

### Scheduling System
**Target:** Windows Task Scheduler integration + APScheduler for background jobs

**Features:**
- Daily/Weekly/Monthly schedules
- Idle-time triggers
- Pre-execution browser closure
- Post-execution notifications
- Battery mode skip

**UI:**
- Schedules tab with CRUD operations
- Schedule preview/test
- Next run countdown

### Quick Clean Presets
**Presets:**
- **Quick Clean:** Cookies + Session only
- **Security Clean:** Cookies + Passwords + Autofill
- **Full Clean:** All options
- **Custom:** User-defined presets

**Storage:** SQLite database for preset definitions

### Settings Persistence
**Database:** SQLite (`privacy_eraser.db`)

**Tables:**
- `settings` - User preferences (theme, auto-scan, etc.)
- `schedules` - Scheduled tasks
- `presets` - Quick Clean presets
- `history` - Deletion logs
- `statistics` - Aggregated stats (bytes saved, runs completed)

### Auto-Update System
**Source:** GitHub Releases API

**Features:**
- Background version check
- SHA256 integrity verification
- Silent install option
- Rollback on failure

**UI:**
- Update notification banner
- Update history log

### License System
**Tiers:**
- Free: Individual, Busan City, Education
- Commercial: ₩19,900/year
- Enterprise: Custom pricing

**Validation:**
- Email-based verification
- Hardware fingerprint binding
- Online/offline activation

### Advanced CleanerML Support
**Commands:**
- `winreg.delete` - Delete registry keys
- `json` - Modify JSON files
- `ini` - Modify INI files
- `command` - Execute shell commands

### macOS/Linux Support
**Detection Modules:**
- `detect_macos.py` - Safari, Chrome, Firefox on macOS
- `detect_linux.py` - Firefox, Chrome on Linux

**Challenges:**
- Different cache locations
- No registry on Unix
- Process detection API differences

---

## API Examples

### Full Cleaning Workflow
```python
from privacy_eraser.detect_windows import ProgramProbe, collect_programs
from privacy_eraser.cleaning import chromium_cleaner_options

# 1. Detect Chrome
probe = ProgramProbe(
    name="Google Chrome",
    registry_keys=(r"HKCU\Software\Google\Chrome",),
    file_patterns=(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Preferences",),
    process_names=("chrome.exe",),
)
rows = collect_programs([probe])
chrome_present = rows[0]["present"] == "yes"

# 2. Load options
if chrome_present:
    user_data = r"C:\Users\User\AppData\Local\Google\Chrome\User Data"
    options = chromium_cleaner_options(user_data)
    
    # 3. Preview cache option
    cache_opt = next(o for o in options if o.id == "cache")
    items = cache_opt.preview()
    print(f"Would delete {len(items)} cache items")
    
    # 4. Execute
    count, bytes_deleted = cache_opt.execute()
    print(f"Deleted {count} items, freed {bytes_deleted} bytes")
```

### Custom CleanerOption
```python
from privacy_eraser.cleaning import CleanerOption, DeleteAction

custom_option = CleanerOption(
    id="my_custom_clean",
    label="My Custom Cleaner",
    description="Deletes my app's temporary files",
    warning=None,
    actions=[
        DeleteAction("glob", r"C:\MyApp\Temp\*.tmp"),
        DeleteAction("walk.files", r"C:\MyApp\Cache"),
    ]
)

# Use in GUI by appending to active_options list
```

---

## Performance Notes

### Current Performance (MVP)
- **Startup Time:** <2 seconds (cold start)
- **Memory Usage:** ~50MB (GUI idle)
- **Scan Time:** <1 second (9 browsers)
- **Clean Time:** Depends on file count (typically <5 seconds for cache)

### Optimization Opportunities (Future)
- Parallel scanning of multiple browsers
- Incremental preview (stream results)
- Background cache size calculation
- Smart deletion (skip empty directories)

---

## Security Considerations

### Current Safeguards
- ✅ All tests run in isolated sandbox
- ✅ No network access (except future updates)
- ✅ No telemetry or data collection
- ✅ CleanerML OS filtering prevents cross-platform accidents
- ✅ Warnings for dangerous options (passwords)

### Future Enhancements
- Secure deletion (DoD 5220.22-M wipe)
- Process termination confirmation
- Deletion undo (recycle bin integration)
- Whitelist/blacklist for files

---

## Limitations (MVP)

### Known Limitations
- **Windows Only:** Detection module requires Windows registry/API
- **Single Profile:** Chromium cleaning targets "Default" profile only
- **No Firefox Support:** Built-in options are Chromium-only (use CleanerML)
- **No Scheduling:** Manual execution only
- **No Persistence:** Settings/selections lost on restart

### Workarounds
- Firefox: Use CleanerML (`firefox.xml` from BleachBit)
- Multi-profile: Manually edit `chromium_default_profile()` function
- Persistence: Edit code to save selections to JSON (temporary)

---

## Testing Coverage

### Tested Features
- ✅ All search modes (`file`, `glob`, `walk.*`)
- ✅ DeleteAction preview and execute
- ✅ CleanerOption aggregation
- ✅ Chromium options (cache, cookies, history, session, passwords)
- ✅ CleanerML parsing (os filtering, var expansion, multi-var)
- ✅ Windows detection (registry, file, process) with mocks

### Manual Testing Required
- GUI interactions (button clicks, table selection)
- Real browser data deletion (use test VM)
- Process termination edge cases

See `docs/09_TESTING_PLAN.md` and `docs/11_AUTOMATED_TESTS.md` for details.

