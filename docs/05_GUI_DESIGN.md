# 05_GUI_DESIGN

**Last Updated:** 2025-10-09  
**Status:** MVP implementation in progress

---

## GUI Framework

### Primary: CustomTkinter 5.2.0
- Modern themed widgets (buttons, labels, frames)
- System appearance mode (light/dark auto-detection)
- Cross-platform (Windows, macOS, Linux)
- Built on top of tkinter (stdlib)

### Fallback: tkinter (stdlib)
- Always available (no dependencies)
- Basic widgets (Button, Label, Frame, Text)
- Less modern appearance but fully functional

### Import Strategy
```python
try:
    import customtkinter as ctk
    USE_CT = True
except Exception:
    import tkinter as tk
    USE_CT = False
```

---

## Main Window

### Window Properties
- **Size:** 900x600 pixels
- **Title:** "PrivacyEraser"
- **Theme:** System-based (auto light/dark)
- **Resizable:** Yes (future: remember size)
- **Icon:** Default (future: custom icon)

### Layout Structure
```
┌─────────────────────────────────────────────────────────────┐
│ HEADER                                         [Show Debug] │
│ ┌─ PrivacyEraser ──────────────────────────────────────┐   │
├─────────────────────────────────────────────────────────────┤
│ CONTENT                                                     │
│ ┌─ Subtitle ──────────────────────────────────────────┐    │
│ │ Integrated browser privacy management (MVP)         │    │
│ └─────────────────────────────────────────────────────┘    │
│ ┌─ Controls ──────────────────────────────────────────┐    │
│ │ [Scan Programs] ... [Hide Options] [Preview] [Clean]│    │
│ └─────────────────────────────────────────────────────┘    │
│ ┌─ Program Table ─────────────────────────────────────┐    │
│ │ Program         │ Present │ Running │ Source        │    │
│ │ Google Chrome   │ yes     │ no      │ registry,...  │    │
│ │ Mozilla Firefox │ no      │ no      │ registry,...  │    │
│ └─────────────────────────────────────────────────────┘    │
│ ┌─ Cleaner Options (collapsible) ─────────────────────┐    │
│ │ [Select All] [Clear All]                             │    │
│ │ ☐ Cache - Delete browser cache                       │    │
│ │ ☐ Cookies - Delete cookies databases                 │    │
│ │ ☐ History - Delete site history and related caches   │    │
│ │ ☐ Session - Delete current and last sessions         │    │
│ │ ☐ Passwords - Delete saved passwords [Warning: ...]  │    │
│ └─────────────────────────────────────────────────────┘    │
│ [Quit]                                                      │
├─────────────────────────────────────────────────────────────┤
│ DEBUG PANEL (collapsible)                                   │
│ ┌─ Variables ──────────────────────────────────────────┐   │
│ │ timestamp: 2025-10-09 14:23:45                       │   │
│ │ app_version: 0.1.0                                   │   │
│ │ python: 3.12.0                                       │   │
│ │ platform: Windows-10-...                             │   │
│ │ [Refresh]                                            │   │
│ └─────────────────────────────────────────────────────┘   │
│ ┌─ Console ───────────────────────────────────────────┐   │
│ │ [ 14:23:45 ] INFO: PrivacyEraser started             │   │
│ │ [ 14:23:45 ] INFO: scan> starting program detection  │   │
│ │ [ 14:23:46 ] INFO: scan> collected 9 rows            │   │
│ │ [ 14:23:46 ] INFO: scan> table updated               │   │
│ │ [Clear]                                              │   │
│ └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Components (✅ Implemented)

### 1. Header
**Location:** Top of window (fixed)

**Elements:**
- Title Label: "PrivacyEraser" (24pt bold)
- Debug Toggle Button: "Show Debug" / "Hide Debug" (right-aligned)

**Behavior:**
- Debug toggle reveals/hides Debug Panel at bottom
- Button text updates based on panel state

### 2. Content Area
**Location:** Main scrollable area

#### 2.1 Subtitle
- Text: "Integrated browser privacy management (MVP)"
- Centered, smaller font

#### 2.2 Controls Frame
**Buttons (left to right):**
1. **Scan Programs** - Trigger browser detection
2. **Hide/Show Options** - Toggle Cleaner Options panel (right side)
3. **Preview** - Dry-run selected cleaners (right-aligned)
4. **Clean** - Execute selected cleaners (right-aligned)

#### 2.3 Program Table (ttk.Treeview)
**Columns:**
- **Program** (220px, left-aligned) - Browser name
- **Present** (90px, center) - "yes" or "no"
- **Running** (90px, center) - "yes" or "no"
- **Source** (180px, left) - Comma-separated detection methods

**Features:**
- Vertical scrollbar
- Row selection (single)
- Click row → load cleaner options

**Data Source:**
```python
rows = collect_programs(probes)  # Returns list[dict[str, str]]
tree.insert("", "end", values=(row["name"], row["present"], row["running"], row["source"]))
```

#### 2.4 Cleaner Options Panel (Collapsible)
**Header:**
- Title: "Cleaner Options" (14pt bold)
- Subtitle: "{Program Name} — {User Data Path}"
- "Hide Options" button (top-right)

**Controls:**
- **Select All** button - Check all cleaner options
- **Clear All** button - Uncheck all cleaner options

**Option Checkboxes:**
- One checkbox per `CleanerOption`
- Format: `☐ {label} - {description} [Warning: {warning}]`
- State: Unchecked by default
- Warnings: Red text for dangerous options (e.g., passwords)

**Loading Logic:**
1. User selects program from table
2. GUI calls `_guess_user_data(program_name)` → user data directory
3. Try load CleanerML from `bleachbit/cleaners/{browser}.xml`
4. Fallback to `chromium_cleaner_options(user_data_dir)` for Chromium browsers
5. Create checkboxes for each option

**Collapsing:**
- Button: "Hide Options" / "Show Options" (in Controls frame)
- State: Visible by default
- Collapse: `pack_forget()` the panel

#### 2.5 Quit Button
- Location: Bottom-center
- Action: `app.destroy()` (close window)

### 3. Debug Panel (Collapsible)
**Location:** Bottom of window (after content)

**Visibility:**
- Hidden by default
- Toggle via "Show Debug" button in header

#### 3.1 Variables Section
**Header:** "Variables" (14pt bold)

**Content:** Key-value pairs
- `timestamp` - Current datetime
- `app_version` - From `privacy_eraser.__version__`
- `python` - Python version
- `platform` - OS and version
- `cwd` - Current working directory
- `venv` - Virtual environment path (if active)

**Controls:**
- **Refresh** button - Update variables snapshot

**Implementation:**
```python
def _collect_variables() -> list[tuple[str, str]]:
    from . import __version__
    return [
        ("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        ("app_version", __version__),
        ("python", sys.version.split()[0]),
        ("platform", platform.platform()),
        ("cwd", os.getcwd()),
        ("venv", os.environ.get("VIRTUAL_ENV", "")),
    ]
```

#### 3.2 Console Section
**Header:** "Console" (14pt bold)

**Content:** Scrollable text widget
- Live stream of loguru messages
- Format: `[ HH:MM:SS ] LEVEL: message`
- Auto-scroll to bottom on new message
- Syntax: Plain text (no colors in GUI sink)

**Controls:**
- **Clear** button - Clear console textbox

**Implementation:**
```python
def append_console(text: str) -> None:
    console_box.configure(state="normal")
    console_box.insert("end", text)
    console_box.see("end")
    console_box.configure(state="disabled")

# Wire to loguru
logger.add(
    lambda msg: append_console(str(msg)),
    level="INFO",
    format="[ {time:HH:mm:ss} ] {level}: {message}",
)
```

---

## User Workflows

### Workflow 1: Scan and Clean
**Goal:** Detect browsers and delete cache

**Steps:**
1. Launch app: `uv run privacy_eraser`
2. Window opens with empty Program Table
3. Click **Scan Programs** button
4. Console logs detection checks
5. Program Table populates with detected browsers
6. Click a browser row (e.g., "Google Chrome")
7. Cleaner Options panel populates with checkboxes
8. Check "Cache" option
9. Click **Preview** button
10. Console logs all matching cache files (up to 50, then "... and N more")
11. Review preview; click **Clean** button
12. Console logs deletion stats: "clean> Cache: deleted 142 items, 53248 bytes"
13. Done; click **Quit** or scan again

### Workflow 2: Debug Inspection
**Goal:** View environment and logs

**Steps:**
1. Launch app
2. Click **Show Debug** button in header
3. Debug Panel slides open at bottom
4. Variables section shows app version, Python version, platform
5. Console section shows live logs (e.g., startup diagnostics)
6. Perform actions (scan, preview, clean)
7. Console updates in real-time with detailed logs
8. Click **Clear** to reset console
9. Click **Refresh** to update variables
10. Click **Hide Debug** to collapse panel

### Workflow 3: Multi-Browser Clean
**Goal:** Clean cache for multiple browsers

**Steps:**
1. Scan programs
2. Select browser #1 (e.g., Chrome)
3. Check desired options
4. Click **Clean**
5. Select browser #2 (e.g., Edge)
6. Cleaner Options panel updates automatically
7. Check desired options
8. Click **Clean**
9. Repeat for more browsers

---

## Widget Reference (CustomTkinter)

### Widgets Used in MVP
- `CTk()` - Main window
- `CTkFrame()` - Container frames
- `CTkLabel()` - Text labels
- `CTkButton()` - Action buttons
- `CTkCheckBox()` - Cleaner option checkboxes
- `CTkTextbox()` - Console and Variables (read-only)
- `ttk.Treeview()` - Program table (from stdlib tkinter)
- `ttk.Scrollbar()` - Table scrollbar

### Styling
```python
# Set theme
ctk.set_appearance_mode("system")  # "light", "dark", or "system"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

# Custom fonts
title_font = ("Segoe UI", 24, "bold")
subtitle_font = ("Segoe UI", 14, "bold")
```

---

## Planned GUI Features (🔜 Not Implemented)

### Schedules Tab
**Location:** New tab in main window (tabview)

**Features:**
- List of scheduled tasks (name, cron, next run)
- CRUD buttons (Add, Edit, Delete)
- Enable/Disable toggle per schedule
- Test button (run once now)

**Add/Edit Dialog:**
- Schedule name
- Frequency (daily/weekly/monthly/idle)
- Time picker
- Browser selector
- Preset selector
- Options: Skip if browser running, Notify before/after

### Quick Clean Presets
**Location:** New "Quick Clean" tab

**Presets:**
- **Quick Clean:** Cookies + Session only (fast, safe)
- **Security Clean:** Cookies + Passwords + Autofill (privacy-focused)
- **Full Clean:** All options (nuclear option)
- **Custom:** User-defined (save current selections as preset)

**Buttons:**
- One button per preset (1-click execution)
- Confirmation dialog for destructive presets

### Statistics Dashboard
**Location:** New "Statistics" tab

**Widgets:**
- Line chart (bytes cleaned over time)
- Pie chart (bytes per browser)
- Summary cards:
  - Total runs
  - Total bytes freed
  - Last run timestamp
  - Next scheduled run

**Export:**
- CSV export button (raw data)
- PNG export button (chart screenshot)

### Settings Panel
**Location:** New "Settings" tab

**Options:**
- Theme selector (light/dark/system)
- Auto-scan on startup (checkbox)
- Show debug panel by default (checkbox)
- Check for updates (checkbox)
- Language selector (en/ko/ja - future)

**Buttons:**
- Save settings
- Reset to defaults

### License Activation Dialog
**Location:** Modal dialog (Help → Enter License)

**Fields:**
- Email (text input)
- License key (text input with paste button)
- Hardware ID (read-only, for support)

**Buttons:**
- Activate (online validation)
- Activate Offline (paste response code)
- Cancel

**Status:**
- Green checkmark: "Licensed to {email} ({tier}) until {date}"
- Red X: "Unlicensed (Free tier)"

### Update Notification Banner
**Location:** Top of window (below header, dismissible)

**Content:**
- Icon (info symbol)
- Text: "Update available: v0.2.0 (Release notes)"
- Buttons: "Update Now", "Remind Later", "Dismiss"

**Behavior:**
- Auto-check on startup (if enabled in settings)
- Download in background
- Prompt to restart after download

---

## Accessibility Considerations (Future)

### Keyboard Navigation
- Tab order: Scan → Preview → Clean → Quit
- Enter key: Activate focused button
- Space key: Toggle focused checkbox
- Escape key: Close dialogs

### Screen Reader Support
- All buttons have accessible labels
- Table announces row count
- Console updates announce new messages (optional)

### High Contrast Mode
- Detect Windows high contrast settings
- Override theme with high-contrast colors
- Increase font sizes (125% scaling)

---

## Error Handling in GUI

### Current Approach
All errors logged to console (visible in Debug panel):

```python
try:
    rows = collect_programs(probes)
except Exception as e:
    logger.error(f"Failed to scan programs: {e}")
```

### Future: Error Dialogs (Planned)
```python
from tkinter import messagebox

try:
    # ... operation ...
except PermissionError:
    messagebox.showerror("Permission Denied", "Cannot delete file (check admin rights)")
except Exception as e:
    messagebox.showerror("Error", f"Unexpected error: {e}")
```

---

## Performance Optimizations

### Current Implementation
- Table updates: Bulk insert (not per-row)
- Checkbox creation: Destroy old widgets before creating new ones
- Console appends: Batch text insertion (not per-character)

### Future Improvements
- Virtual scrolling for large tables (>100 rows)
- Lazy loading of cleaner options (only when panel expanded)
- Background thread for scanning (non-blocking GUI)
- Progress bar for long-running cleans

---

## Theming and Branding

### Current Theme
- **Colors:** CustomTkinter default blue theme
- **Fonts:** Segoe UI (Windows), San Francisco (macOS), system default (Linux)
- **Icons:** None (future: custom app icon, toolbar icons)

### Future Branding
- **Logo:** Privacy shield icon (SVG)
- **Colors:** Blue accent (#1976D2), green success (#4CAF50), red warning (#F44336)
- **Splash Screen:** App logo + version on startup (optional)

---

## Testing GUI (Manual)

### Smoke Tests
- [ ] App launches without errors
- [ ] All buttons visible and clickable
- [ ] Scan populates table
- [ ] Selecting row loads cleaner options
- [ ] Preview logs items to console
- [ ] Clean executes and logs stats
- [ ] Debug panel toggles visibility
- [ ] Console updates in real-time

### Edge Cases
- [ ] Scan with no browsers installed → empty table
- [ ] Select row with no CleanerML → fallback to built-in
- [ ] Clean with all options unchecked → log "0 items"
- [ ] Quit during clean → abort gracefully (future: add abort button)

### Platform Testing
- [ ] Windows 10 (primary)
- [ ] Windows 11
- [ ] Linux (Ubuntu 22.04) - GUI works, detection no-op
- [ ] macOS (experimental) - GUI works, detection no-op

---

## GUI Code Architecture

### Main Entry Point
```python
def run_gui() -> None:
    if USE_CT:
        # CustomTkinter implementation (lines 126-516)
        app = ctk.CTk()
        # ... build UI ...
        app.mainloop()
    else:
        # tkinter fallback (lines 517-731)
        app = tk.Tk()
        # ... build UI (similar structure) ...
        app.mainloop()
```

### Key Functions
- `_configure_logging(append_console)` - Wire loguru sinks
- `_collect_variables()` - Snapshot system info
- `_default_probes()` - Define browser detection probes
- `_guess_user_data(program)` - Map program name to user data directory
- `_populate_cleaners_for(program, user_data)` - Load and display cleaner options
- `run_scan()` - Execute detection and populate table
- `preview_clean()` - Preview selected cleaners
- `execute_clean()` - Execute selected cleaners
- `on_select_program(event)` - Handle table row selection

### Code Duplication
**Issue:** CustomTkinter and tkinter branches have ~80% duplicate code.

**Future Refactoring:**
- Extract common logic into separate functions
- Use adapter pattern for widget creation
- Single UI definition with widget factory

---

## Future UI Enhancements

### Tabs/Pages
- Dashboard (current view)
- Quick Clean (presets)
- Schedules (automated tasks)
- Statistics (charts and reports)
- Settings (preferences)

### Modern Features
- Drag-and-drop file patterns (advanced users)
- System tray icon (minimize to tray)
- Toast notifications (Windows 10/11 native)
- Dark mode toggle (manual override)
- Toolbar with icons (scan, clean, schedule, settings)

### Advanced Options
- Regex file patterns (for power users)
- Custom CleanerML editor (built-in)
- Backup/Restore settings (export/import JSON)
- Multi-language support (i18n)

---

For architecture details, see `.cursor/context/architecture.md`.  
For development workflows, see `.cursor/context/runbook.md`.

