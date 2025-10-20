# PrivacyEraser Development Roadmap

**Last Updated:** 2025-10-09  
**Current Version:** 0.1.0 (MVP)

---

## Current Status (MVP - Phase 1)

### ✅ Completed Features
- [x] Project scaffolding with uv package manager
- [x] CustomTkinter GUI with tkinter fallback
- [x] Windows browser detection (registry, file, process)
- [x] Core cleaning engine (DeleteAction, CleanerOption)
- [x] Built-in Chromium cleaner options (cache, cookies, history, session, passwords)
- [x] CleanerML loader (BleachBit-compatible XML parser)
- [x] Logging system (loguru + rich + GUI sink)
- [x] Test suite (pytest with 80%+ coverage)
- [x] Debug panel with live console and variable inspection

### 🚧 Current Limitations
- Windows-only detection (no macOS/Linux support)
- Single profile support (Chromium "Default" only)
- No settings persistence (selections lost on restart)
- No scheduling (manual execution only)
- No Firefox built-in options (requires CleanerML)

---

## Phase 2: Settings Persistence & Presets (Next 2-3 weeks)

### Goals
- Persist user selections and preferences
- Quick Clean presets for common scenarios
- Improved UX with saved state

### Tasks
- [ ] Implement SQLite database (`privacy_eraser.db`)
  - [ ] Settings table (theme, auto-scan, etc.)
  - [ ] Presets table (quick clean definitions)
  - [ ] History table (deletion logs)
- [ ] Create `database.py` module with CRUD operations
- [ ] Save/load selected cleaner options per browser
- [ ] Implement Quick Clean presets
  - [ ] Quick Clean (cookies + session)
  - [ ] Security Clean (cookies + passwords + autofill)
  - [ ] Full Clean (all options)
  - [ ] Custom presets (user-defined)
- [ ] Add Settings panel/tab
  - [ ] Theme selector
  - [ ] Auto-scan on startup
  - [ ] Show debug panel default
- [ ] Add Presets tab/panel to GUI
- [ ] Warn if target browser is running before clean

### Success Criteria
- User selections persist across restarts
- One-click Quick Clean execution
- Settings panel functional
- Database migrations work

---

## Phase 3: Scheduling System (3-4 weeks)

### Goals
- Automated cleaning on schedule
- Windows Task Scheduler integration
- Background jobs with APScheduler

### Tasks
- [ ] Install APScheduler dependency
- [ ] Create `scheduler.py` module
  - [ ] Background scheduler setup
  - [ ] Job definitions (clean task)
  - [ ] Cron trigger parsing
- [ ] Implement Windows Task Scheduler bridge
  - [ ] Create scheduled task via `win32com`
  - [ ] Register task on schedule creation
  - [ ] Unregister task on schedule deletion
- [ ] Build Schedules GUI tab
  - [ ] Schedule list (table/treeview)
  - [ ] Add/Edit/Delete schedule dialogs
  - [ ] Enable/Disable toggle per schedule
  - [ ] Test/Run Now button
- [ ] Schedule options
  - [ ] Daily/Weekly/Monthly triggers
  - [ ] Idle-time trigger
  - [ ] Pre-execution browser closure
  - [ ] Post-execution notifications
  - [ ] Battery mode skip option
- [ ] Store schedules in SQLite database
- [ ] Background service mode (optional tray icon)

### Success Criteria
- Scheduled clean runs unattended
- Windows Task Scheduler reflects active schedules
- GUI schedule management works
- Notifications on completion

---

## Phase 4: Auto-Update & License System (2-3 weeks)

### Goals
- Seamless updates from GitHub Releases
- License tiers for monetization
- Professional deployment

### Auto-Update Tasks
- [ ] Add `requests` dependency
- [ ] Create `updater.py` module
  - [ ] GitHub Releases API integration
  - [ ] Version comparison (`packaging` library)
  - [ ] Download installer to temp
  - [ ] SHA256 integrity verification
- [ ] Update notification banner in GUI
- [ ] Background update check (on startup)
- [ ] Silent install option
- [ ] Update history log

### License System Tasks
- [ ] Create `license.py` module
  - [ ] Hardware fingerprint generation
  - [ ] License validation (online/offline)
  - [ ] Tier definitions (Free, Commercial, Enterprise)
- [ ] License activation dialog (GUI)
- [ ] Busan City email whitelist (@busan.go.kr)
- [ ] Educational institution whitelist (.ac.kr, .edu)
- [ ] Encrypted license storage (`license.dat`)
- [ ] Feature gating based on tier
- [ ] License server API (backend - separate project)

### Success Criteria
- App auto-updates on new release
- License activation works
- Free tier fully functional
- Commercial tier unlocks features
- Busan City users get Pro for free

---

## Phase 5: Installer & Distribution (1-2 weeks)

### Goals
- Professional Windows installer
- Automated build pipeline
- Public release preparation

### Tasks
- [ ] PyInstaller configuration
  - [ ] Bundle Python + dependencies
  - [ ] Icon and resources
  - [ ] One-file vs one-directory build
- [ ] Inno Setup installer script
  - [ ] Install directory selection
  - [ ] Start menu shortcuts
  - [ ] Uninstaller
  - [ ] Upgrade detection
- [ ] Code signing certificate (DigiCert)
  - [ ] Sign executable
  - [ ] Sign installer
- [ ] GitHub Actions CI/CD
  - [ ] Build on tag push
  - [ ] Run tests
  - [ ] Create installer
  - [ ] Upload to GitHub Releases
- [ ] Release checklist automation
- [ ] Website/landing page (optional)

### Success Criteria
- Installer builds automatically
- Signed executables (no SmartScreen warnings)
- GitHub Releases workflow complete
- Installation tested on clean VM

---

## Phase 6: macOS/Linux Support (4-6 weeks)

### Goals
- Cross-platform browser detection
- Platform-specific cleaning logic
- Unified codebase

### Tasks
- [ ] Create `detect_macos.py` module
  - [ ] `.app` bundle detection
  - [ ] plist file parsing
  - [ ] Process detection (cross-platform psutil)
- [ ] Create `detect_linux.py` module
  - [ ] `.desktop` file parsing
  - [ ] XDG config directory support
  - [ ] Process detection
- [ ] macOS browser paths
  - [ ] Safari (`~/Library/Safari/`)
  - [ ] Chrome (`~/Library/Application Support/Google/Chrome/`)
  - [ ] Firefox (`~/Library/Application Support/Firefox/`)
- [ ] Linux browser paths
  - [ ] Chrome (`~/.config/google-chrome/`)
  - [ ] Firefox (`~/.mozilla/firefox/`)
  - [ ] Chromium (`~/.config/chromium/`)
- [ ] Platform abstraction layer
  - [ ] Unified detection interface
  - [ ] Platform-specific implementations
- [ ] Test on macOS and Linux VMs
- [ ] Update CleanerML loader for Unix paths

### Success Criteria
- GUI launches on macOS/Linux
- Browser detection works
- Cleaning engine functional
- Tests pass on all platforms

---

## Phase 7: Advanced Features (Future)

### Statistics & Reporting
- [ ] Statistics tab with charts
- [ ] Bytes cleaned over time (line chart)
- [ ] Bytes per browser (pie chart)
- [ ] CSV/JSON export
- [ ] Scheduled reports (email - optional)

### Advanced CleanerML
- [ ] Registry deletion (`winreg.delete`)
- [ ] JSON modification (`command="json"`)
- [ ] INI modification (`command="ini"`)
- [ ] Shell command execution (`command="shell"`)
- [ ] Variable expansion enhancements

### Security Enhancements
- [ ] Secure deletion (DoD 5220.22-M wipe)
- [ ] Process termination with confirmation
- [ ] Whitelist/blacklist for protected paths
- [ ] Recycle bin integration (undo delete)
- [ ] Sandbox mode (dry-run with detailed preview)

### UX Improvements
- [ ] System tray icon (minimize to tray)
- [ ] Toast notifications (Windows 10/11)
- [ ] Dark mode toggle (manual override)
- [ ] Multi-language support (i18n)
  - [ ] English (default)
  - [ ] Korean
  - [ ] Japanese
- [ ] Drag-and-drop custom file patterns
- [ ] Custom CleanerML editor (built-in)

### Enterprise Features
- [ ] Central management console (web-based)
- [ ] Policy-based deployment
- [ ] Group policy (GPO) integration
- [ ] Silent install with preset config
- [ ] Audit logs and compliance reports

---

## Version Milestones

### v0.1.0 (Current - MVP)
- Core cleaning engine
- Windows detection
- Basic GUI
- Test coverage

### v0.2.0 (Phase 2)
- Settings persistence
- Quick Clean presets
- Improved UX

### v0.3.0 (Phase 3)
- Scheduling system
- Windows Task Scheduler integration
- Background mode

### v0.4.0 (Phase 4)
- Auto-update
- License system
- Commercial readiness

### v1.0.0 (Phase 5)
- Installer
- Code signing
- Public release

### v1.1.0 (Phase 6)
- macOS support
- Linux support
- Cross-platform

### v2.0.0 (Phase 7)
- Statistics dashboard
- Advanced features
- Enterprise edition

---

## Risk Mitigation

### Technical Risks
- **Risk:** Windows API changes break detection
  - **Mitigation:** Version-specific detection logic, fallbacks
- **Risk:** Antivirus flags installer as malware
  - **Mitigation:** Code signing, whitelist with AV vendors
- **Risk:** Browser updates change data paths
  - **Mitigation:** CleanerML allows community updates

### Business Risks
- **Risk:** Low user adoption
  - **Mitigation:** Busan City partnership, free tier, local marketing
- **Risk:** License piracy
  - **Mitigation:** Online validation, hardware binding, reasonable pricing
- **Risk:** Competitor dominance (CCleaner)
  - **Mitigation:** Korean market focus, modern UI, Whale browser support

---

## Success Metrics

### Phase 2 Goals
- 100% settings persistence (no data loss on restart)
- <0.5s preset execution time

### Phase 3 Goals
- 95%+ scheduled task success rate
- <10s schedule creation time

### Phase 4 Goals
- 90%+ update success rate
- <1% license activation failures

### Phase 5 Goals
- <5% installer failures
- 0 SmartScreen warnings (signed)

### Phase 6 Goals
- Feature parity across platforms
- <10% platform-specific bugs

---

## Community & Open Source

### Open Source Strategy
- [ ] Publish source code to GitHub (GPL-3.0 or MIT)
- [ ] Accept community contributions (CleanerML, translations)
- [ ] Maintain CHANGELOG.md
- [ ] CONTRIBUTING.md guidelines
- [ ] Issue templates (bug, feature request)
- [ ] PR review process

### Documentation
- [x] README.md (quickstart)
- [x] Architecture docs
- [x] Testing guide
- [ ] User manual (PDF/web)
- [ ] FAQ
- [ ] Video tutorials (YouTube)

---

## Next Actions (Immediate)

1. **Complete MVP polish** (1 week)
   - Fix any remaining MVP bugs
   - Improve error messages
   - Add more CleanerML mappings (Vivaldi, Whale)

2. **Start Phase 2** (Settings Persistence)
   - Design database schema
   - Implement `database.py` module
   - Add Settings panel to GUI

3. **Marketing preparation**
   - Draft Busan City partnership proposal
   - Create demo video
   - Prepare website copy

---

For detailed implementation plans, see:
- `TODO.md` - Current task list
- `docs/01_CORE_FEATURES.md` - Feature specifications
- `.cursor/context/architecture.md` - Technical architecture

