# PrivacyEraser TODO List

**Last Updated:** 2025-10-09  
**Current Sprint:** MVP Polish + Phase 2 Planning

---

## Legend
- ✅ Completed
- 🚧 In Progress
- 📋 Todo (Planned)
- ⏸️ Blocked/Deferred
- ❌ Cancelled

---

## 🔥 Immediate Priorities (This Week)

### MVP Bug Fixes & Polish
- 📋 Add more browser probes to `_default_probes()`
  - Vivaldi (complete mapping)
  - Waterfox
  - LibreWolf
- 📋 Improve error handling in cleaning engine
  - Catch and log permission errors gracefully
  - Show user-friendly messages for common errors
- 📋 Add file count/size calculation before clean
  - Show total items and bytes in preview
  - Confirm before destructive operations (passwords)
- 📋 Map additional CleanerML files in GUI
  - `vivaldi.xml`
  - `librewolf.xml`
  - `waterfox.xml`
- 📋 Test on Windows 11 (currently only tested on Windows 10)

### Documentation
- ✅ Create `.cursor/` directory structure
- ✅ Write `.cursor/rules`
- ✅ Write `.cursor/context/architecture.md`
- ✅ Write `.cursor/context/runbook.md`
- ✅ Write `.cursor/context/testing.md`
- ✅ Update `readme.md` with current features
- ✅ Update `docs/01_CORE_FEATURES.md`
- ✅ Update `docs/02_TECHNICAL_ARCHITECTURE.md`
- ✅ Update `docs/05_GUI_DESIGN.md`
- ✅ Create `docs/ROADMAP.md`
- ✅ Create `TODO.md` (this file)

---

## 📦 Phase 2: Settings Persistence & Presets (Next 2-3 weeks)

### Database Setup
- 📋 Design SQLite schema
  - `settings` table (key-value pairs)
  - `presets` table (preset definitions)
  - `history` table (deletion logs)
  - `browser_selections` table (last selected options per browser)
- 📋 Create `src/privacy_eraser/database.py` module
  - Database initialization
  - CRUD operations (save_setting, load_setting, etc.)
  - Migration support (future versions)
- 📋 Add database tests (`tests/test_database.py`)

### Settings Persistence
- 📋 Implement settings save/load
  - Theme preference
  - Auto-scan on startup
  - Show debug panel default
  - Window size/position
- 📋 Save selected cleaner options per browser
  - Remember last selections for each browser
  - Auto-select on next run (optional)
- 📋 Add Settings panel/tab to GUI
  - Theme selector (light/dark/system)
  - Auto-scan checkbox
  - Debug panel checkbox
  - Save/Reset buttons

### Quick Clean Presets
- 📋 Define preset structure (JSON format)
- 📋 Implement built-in presets
  - Quick Clean (cookies + session)
  - Security Clean (cookies + passwords + autofill)
  - Full Clean (all options)
- 📋 Add Presets tab/panel to GUI
  - List of presets
  - One-click execution per preset
  - Confirmation dialog for destructive presets
- 📋 Allow custom preset creation
  - Save current selections as preset
  - Edit/Delete custom presets
- 📋 Store presets in database

### UX Improvements
- 📋 Add confirmation dialogs
  - Before cleaning (with item count/size)
  - Before deleting passwords
- 📋 Warn if browser is running
  - Check process before clean
  - Offer to close browser (advanced)
- 📋 Show progress indicators
  - Indeterminate progress bar during scan
  - Determinate progress bar during clean (optional)

---

## 📅 Phase 3: Scheduling System (Future - 3-4 weeks)

### Scheduler Module
- 📋 Add `apscheduler` dependency to `pyproject.toml`
- 📋 Create `src/privacy_eraser/scheduler.py` module
  - BackgroundScheduler setup
  - Job definitions
  - Cron trigger parsing
- 📋 Implement schedule CRUD operations
  - Create schedule
  - Edit schedule
  - Delete schedule
  - Enable/Disable schedule

### Windows Task Scheduler Integration
- 📋 Add `pywin32` dependency
- 📋 Implement Windows Task Scheduler bridge
  - Create scheduled task via COM API
  - Register task on schedule creation
  - Unregister task on deletion
- 📋 Handle elevated permissions (admin required)

### Schedules GUI
- 📋 Add Schedules tab to main window
- 📋 Schedule list (Treeview with columns: name, trigger, next run, enabled)
- 📋 Add Schedule dialog
  - Name input
  - Frequency selector (daily/weekly/monthly)
  - Time picker
  - Browser selector
  - Preset selector
  - Options (skip if running, notify)
- 📋 Edit/Delete schedule buttons
- 📋 Test/Run Now button

### Background Mode
- 📋 System tray icon (minimize to tray)
- 📋 Tray context menu (Open, Schedules, Quit)
- 📋 Tray notifications (next run, completion)

---

## 🔄 Phase 4: Auto-Update & License (Future - 2-3 weeks)

### Auto-Update
- 📋 Add `requests` and `packaging` dependencies
- 📋 Create `src/privacy_eraser/updater.py` module
  - GitHub Releases API client
  - Version comparison
  - Download installer
  - SHA256 verification
- 📋 Update notification banner in GUI
- 📋 Background update check on startup
- 📋 Silent install option

### License System
- 📋 Create `src/privacy_eraser/license.py` module
  - Hardware fingerprint generation
  - License validation (online/offline)
  - Tier definitions
- 📋 License activation dialog (GUI)
- 📋 Email whitelists (Busan City, education)
- 📋 Encrypted license storage
- 📋 Feature gating (Pro features)

---

## 🛠️ Technical Debt & Refactoring

### Code Quality
- 📋 Refactor `gui.py` (currently 730+ lines)
  - Extract CustomTkinter and tkinter common logic
  - Move `_default_probes()` to separate config file
  - Move `_guess_user_data()` to `detect_windows.py`
- 📋 Add type hints to all functions (currently ~80% coverage)
- 📋 Add docstrings to public APIs
- 📋 Run linter (ruff or pylint)
  - Fix all warnings
  - Add to CI pipeline

### Testing
- 📋 Increase coverage to >90%
  - Add GUI integration tests (optional)
  - Test error paths
  - Test edge cases (empty directories, permission errors)
- 📋 Add GitHub Actions CI
  - Run tests on push
  - Upload coverage to Codecov
  - Matrix testing (Windows 10/11)

### Performance
- 📋 Profile cleaning operations
  - Optimize slow paths
  - Benchmark large cleanups (>10k files)
- 📋 Add parallel scanning (thread pool for multiple browsers)
- 📋 Lazy-load CleanerML (only when needed)

---

## 🐛 Known Bugs

### High Priority
- None currently

### Medium Priority
- 📋 CleanerML loader doesn't handle malformed XML gracefully
  - Add try/except and log errors
- 📋 Console textbox doesn't limit size (memory leak on long sessions)
  - Add max line limit (e.g., 1000 lines)
  - Auto-trim old logs

### Low Priority
- 📋 Window doesn't remember size/position on restart
  - Will be fixed in Phase 2 (settings persistence)

---

## 📚 Documentation TODOs

- 📋 Write user manual (Markdown or PDF)
  - Getting started
  - Feature walkthrough
  - FAQ
  - Troubleshooting
- 📋 Create video tutorial (YouTube)
  - Installation
  - Basic usage (scan + clean)
  - Scheduling (future)
- 📋 Add CHANGELOG.md
  - Follow Keep a Changelog format
  - Semantic versioning
- 📋 Add CONTRIBUTING.md
  - Code style guide
  - PR process
  - CleanerML contribution guide

---

## 🎨 Design & UX TODOs

- 📋 Create app icon (.ico for Windows)
  - Privacy shield design
  - Multiple sizes (16x16 to 256x256)
- 📋 Add toolbar icons (optional)
  - Scan icon
  - Clean icon
  - Schedule icon
- 📋 Improve button layout
  - More consistent spacing
  - Better visual hierarchy
- 📋 Add loading animations
  - Spinner during scan
  - Progress bar during clean

---

## 🚀 Marketing & Distribution TODOs

- 📋 Draft Busan City partnership proposal
  - Value proposition
  - Deployment plan
  - Support commitment
- 📋 Create landing page (GitHub Pages or custom)
  - Features showcase
  - Screenshots
  - Download link
  - Documentation link
- 📋 Prepare demo video
  - 2-3 minutes
  - Professional narration
  - Showcase key features
- 📋 Write press release (for local launch)
- 📋 Create social media accounts
  - Twitter/X
  - YouTube (for tutorials)

---

## ⏸️ Deferred (Future Consideration)

- ⏸️ Browser extension integration (communicate with running browsers)
- ⏸️ Cloud sync (settings across devices)
- ⏸️ Mobile app (iOS/Android) - remote trigger
- ⏸️ AI-based smart cleaning (predict what to clean)
- ⏸️ Network drive cleaning (UNC paths)
- ⏸️ Portable mode (USB stick, no installation)

---

## ❌ Cancelled

- ❌ Native Linux GUI (GTK) - Decided to use CustomTkinter cross-platform instead

---

## Current Sprint Plan (Week of 2025-10-09)

### Monday-Tuesday
- ✅ Update all documentation
- ✅ Create .cursor/ context files
- 📋 Fix CleanerML loader error handling
- 📋 Add Vivaldi/Waterfox/LibreWolf probes

### Wednesday-Thursday
- 📋 Design SQLite database schema
- 📋 Start implementing `database.py` module
- 📋 Write database tests

### Friday
- 📋 Add Settings panel to GUI (basic)
- 📋 Implement save/load for theme setting
- 📋 Sprint review and planning for next week

---

## Notes

- All file paths are relative to project root
- Use `uv` for all dependency management
- Test on Windows before committing
- Keep git commits small and focused
- Update this TODO.md as tasks progress

---

**Next Review:** 2025-10-16

