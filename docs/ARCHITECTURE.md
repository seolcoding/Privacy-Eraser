# Privacy Eraser Architecture

**Last Updated:** 2025-10-27
**Status:** Production - v2.0.x (Flet UI)

## Overview

Privacy Eraser is a Windows desktop application for automated browser privacy cleaning. Built with Python 3.12+, Flet UI (Flutter for Python), and BleachBit's cleaning engine, it provides a Material Design 3 interface with powerful scheduled deletion capabilities.

## Technology Stack

### Core Technologies
- **Language:** Python 3.12+
- **Package Manager:** uv
- **UI Framework:** Flet >= 0.28.0 (Flutter for Python)
- **Design System:** Material Design 3
- **Scheduler:** APScheduler 3.10+
- **Logging:** loguru (structured logging)
- **Process Management:** psutil 5.9.8
- **Notifications:** winotify (Windows Toast notifications)

### Dependencies

```toml
[project.dependencies]
flet = ">=0.28.0"
pillow = ">=10.0.0"
loguru = ">=0.7.2"
psutil = ">=5.9.8"
apscheduler = ">=3.10.0"
winotify = ">=1.1.0"
```

### Build & Distribution
- **Build Tool:** Flet Build (Flutter SDK)
- **Package Format:** ZIP archive (onedir structure)
- **Target Platform:** Windows 10/11 (64-bit)

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                          │
│                    (Flet Material Design 3)                     │
│                   src/privacy_eraser/ui/main.py                 │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                ┌───────────┼───────────┐
                │           │           │
                ▼           ▼           ▼
    ┌──────────────┐ ┌────────────┐ ┌─────────────┐
    │   Browser    │ │  Schedule  │ │   Backup    │
    │  Detection   │ │  Manager   │ │  Manager    │
    │              │ │            │ │             │
    │ data_config  │ │ schedule_  │ │ backup_     │
    │   .py        │ │ manager.py │ │ manager.py  │
    └──────┬───────┘ └─────┬──────┘ └──────┬──────┘
           │               │                │
           │               ▼                │
           │    ┌──────────────────┐        │
           │    │   Scheduler      │        │
           │    │  (APScheduler)   │        │
           │    │                  │        │
           │    │ schedule_        │        │
           │    │ executor.py      │        │
           │    │ scheduler.py     │        │
           │    └────────┬─────────┘        │
           │             │                  │
           └─────────────┼──────────────────┘
                         │
                         ▼
              ┌──────────────────┐
              │  Cleaning Engine │
              │   (BleachBit)    │
              │                  │
              │ cleanerml_loader │
              │ cleaning.py      │
              └──────────────────┘
                         │
                         ▼
              ┌──────────────────┐
              │  File System     │
              │  Operations      │
              └──────────────────┘
```

## Module Architecture

### Entry Point
- **`src/privacy_eraser/ui/main.py`**
  - Main entry point: `main()` → launches Flet application
  - Installed as console script: `privacy_eraser`
  - Flet target: `flet` function

### UI Layer (`ui/main.py`)

**Responsibilities:**
- Material Design 3 interface using Flet
- Browser detection and display (2x4 grid layout with logos)
- Delete options panel (checkboxes for cache, cookies, history, etc.)
- Backup/restore functionality
- Schedule management UI
- Real-time progress display
- Windows notifications

**Key Features:**
- Responsive grid layout (browsers arranged in 2x4 grid)
- Real browser logo images (`static/images/`)
- Delete options: Cache, Cookies, History, Session, Passwords
- Additional options: Bookmarks, Downloads, Download Files
- Backup creation before deletion
- Restore from backup functionality
- Schedule creation and management
- Progress indicators during operations
- Windows toast notifications

**UI Components:**
- `ft.Container` - Layout containers
- `ft.GridView` - Browser grid display
- `ft.Checkbox` - Delete options
- `ft.ElevatedButton` - Primary actions
- `ft.AlertDialog` - Confirmations and schedules
- `ft.SnackBar` - Quick notifications

### Core Modules

#### 1. Browser Detection (`ui/core/data_config.py`)

**Responsibilities:**
- Browser information database
- Browser installation detection (via registry and file paths)
- CleanerML file mapping

**Browser Support:**
- Chrome
- Edge
- Firefox
- Brave
- Opera
- Whale (Naver)
- Safari

**Data Structures:**
```python
@dataclass
class BrowserInfo:
    id: str
    name: str
    logo_path: str
    color: str
    is_installed: bool
    cleanerml_path: Optional[str]
```

#### 2. Schedule Manager (`ui/core/schedule_manager.py`)

**Responsibilities:**
- Schedule CRUD operations
- JSON file persistence
- Schedule validation

**Schedule Types:**
- `once` - One-time execution
- `daily` - Daily at specific time
- `weekly` - Weekly on specific day
- `monthly` - Monthly on specific date

**Data Structures:**
```python
@dataclass
class ScheduleScenario:
    id: str
    name: str
    enabled: bool
    schedule_type: str  # once, daily, weekly, monthly
    time: str  # HH:MM
    browsers: List[str]
    delete_bookmarks: bool
    delete_downloads: bool
    created_at: str
    description: Optional[str]
```

#### 3. Backup Manager (`ui/core/backup_manager.py`)

**Responsibilities:**
- Backup creation before deletion
- Backup restoration
- Backup list management
- 30-day retention policy

**Backup Structure:**
```
backups/
├── 2025-10-27_14-30-15/
│   ├── chrome/
│   │   ├── Cookies
│   │   ├── History
│   │   └── ...
│   ├── edge/
│   └── metadata.json
```

#### 4. Scheduler (`scheduler.py`)

**Responsibilities:**
- APScheduler integration
- Background scheduler management
- Job registration and removal

**Features:**
- Background job execution
- Cron-based scheduling
- Job persistence (optional)

#### 5. Schedule Executor (`schedule_executor.py`)

**Responsibilities:**
- Execute scheduled cleaning tasks
- Browser process termination
- Windows notifications
- Error handling

**Execution Flow:**
1. Load schedule scenario
2. Check browser processes
3. Terminate if running
4. Execute cleaning operations
5. Send notification
6. Log results

#### 6. Notification Manager (`notification_manager.py`)

**Responsibilities:**
- Windows toast notifications
- Notification history
- User feedback

**Notification Types:**
- Cleaning started
- Cleaning completed
- Backup created
- Restore completed
- Schedule executed
- Errors

### Cleaning Engine

#### CleanerML Loader (`cleanerml_loader.py`)

**Responsibilities:**
- Parse BleachBit XML cleaner definitions
- OS filtering (`os="windows"`)
- Variable expansion
- Action conversion

**Supported CleanerML Features:**
- `<cleaner>` with OS filtering
- `<option>` with label, description, warning
- `<action command="delete">` with search patterns
- Variable substitution (`$$VAR$$`)

**CleanerML Files:**
```
src/privacy_eraser/cleaners/
├── google_chrome.xml
├── microsoft_edge.xml
├── firefox.xml
├── brave.xml
├── opera.xml
├── whale.xml
└── safari.xml
```

#### Cleaning Engine (`cleaning.py`)

**Responsibilities:**
- File/directory deletion
- Search pattern execution
- Safe deletion with validation

**Search Modes:**
- `file` - Single file
- `glob` - Glob pattern
- `walk.files` - Recursive files only
- `walk.all` - Files and directories
- `walk.top` - Include top directory

## Data Flow

### Main Cleaning Flow

```
User selects browsers
       ↓
User selects delete options
       ↓
Click "삭제하기" button
       ↓
Create backup
       ↓
Load CleanerML for each browser
       ↓
Filter options by user selection
       ↓
Execute DeleteAction for each option
       ↓
Show progress
       ↓
Send notification
       ↓
Display result
```

### Schedule Execution Flow

```
APScheduler triggers job
       ↓
Schedule Executor loads scenario
       ↓
Check if browsers are running
       ↓
Terminate browsers if needed
       ↓
Execute cleaning (same as manual)
       ↓
Send notification
       ↓
Log results
```

### Backup/Restore Flow

```
Backup:
Create timestamped directory
       ↓
Copy browser data files
       ↓
Save metadata.json
       ↓
Enforce 30-day retention

Restore:
User selects backup
       ↓
Load metadata
       ↓
Restore files to original locations
       ↓
Send notification
```

## File System Layout

```
Privacy-Eraser/
├── src/privacy_eraser/
│   ├── __init__.py
│   ├── ui/
│   │   ├── main.py              # Flet UI entry point
│   │   └── core/
│   │       ├── data_config.py   # Browser detection
│   │       ├── schedule_manager.py
│   │       └── backup_manager.py
│   ├── scheduler.py             # APScheduler integration
│   ├── schedule_executor.py     # Execute scheduled tasks
│   ├── notification_manager.py  # Windows notifications
│   ├── cleaning.py              # Cleaning engine
│   ├── cleanerml_loader.py      # XML parser
│   └── cleaners/                # CleanerML files
│       ├── google_chrome.xml
│       ├── microsoft_edge.xml
│       └── ...
├── static/
│   └── images/                  # Browser logos
│       ├── chrome.png
│       ├── edge.png
│       └── ...
├── tests/                       # Unit tests
├── pyproject.toml               # uv project config
└── README.md
```

## Configuration

### Development Mode

Controlled by `AppConfig.is_dev_mode()`:
- Uses test data directory
- Skips actual file deletion
- Shows DEV mode warning in UI

### Storage Locations

**User Data:**
- Schedules: `%APPDATA%/PrivacyEraser/schedules.json`
- Backups: `%APPDATA%/PrivacyEraser/backups/`
- Logs: `%APPDATA%/PrivacyEraser/logs/`

**Dev Data:**
- Test data: `test_data/` (excluded from builds)

## Platform-Specific Code

- **Windows-only:**
  - Registry detection
  - Windows notifications (winotify)
  - Process termination (psutil)
  - File path expansion (`%LOCALAPPDATA%`, etc.)

- **Cross-platform:**
  - Cleaning engine (CleanerML loader, file operations)
  - Schedule management
  - Backup/restore

## Security Considerations

1. **File Validation:**
   - Only delete within user profile directories
   - Validate paths before deletion
   - No system file access

2. **Browser Safety:**
   - Terminate browser before cleaning
   - Skip files in use
   - Backup before deletion

3. **User Data Protection:**
   - 30-day backup retention
   - Metadata tracking
   - Restore capability

## Performance Characteristics

- **Startup Time:** < 2 seconds
- **Browser Detection:** < 500ms
- **Cleaning Operation:** Varies by data size (typically 1-10 seconds)
- **Memory Usage:** ~50-100MB
- **Disk Space:** ~70-100MB (installed)

## Future Enhancements (Not Yet Implemented)

- macOS/Linux support
- Cloud backup integration
- User profiles
- Custom cleaning rules
- Browser extension
- Command-line interface
- Auto-update mechanism

## Design Principles

1. **User-First:** Simple, intuitive UI for non-technical users
2. **Safety:** Backup-first approach, validation, error handling
3. **Transparency:** Clear feedback, detailed logs
4. **Modularity:** Separate concerns, testable components
5. **Extensibility:** CleanerML compatibility, plugin-ready

## References

- [Flet Documentation](https://flet.dev/)
- [BleachBit](https://www.bleachbit.org/)
- [APScheduler](https://apscheduler.readthedocs.io/)
- [Material Design 3](https://m3.material.io/)
