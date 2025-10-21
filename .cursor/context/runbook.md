# PrivacyEraser Development Runbook

## Quick Start

### Initial Setup
```bash
# Clone repository
git clone <repo-url>
cd privacy_eraser

# Create virtual environment and install dependencies
uv venv
uv sync

# Verify installation
uv run privacy_eraser
```

### Running the Application
```bash
# Standard run
uv run privacy_eraser

# Direct module invocation
uv run python -m privacy_eraser

# From installed script (after uv sync)
uv run privacy_eraser
```

## Development Commands

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
# Open htmlcov/index.html in browser
```

### Installing Test Dependencies
```bash
# Install with test extras
uv sync --extra test

# Or use the group syntax
uv sync -e test
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

## Platform-Specific Notes

### Windows
- Primary development platform
- Full feature set available (registry detection, process checks)
- CustomTkinter works natively

### Linux/macOS
- GUI works (CustomTkinter or tkinter fallback)
- Detection module (`detect_windows.py`) is no-op (imports guarded)
- Cleaning engine works for local file operations
- Windows-only tests are automatically skipped

## Debugging

### Enable Debug Panel
1. Run application: `uv run privacy_eraser`
2. Click "Show Debug" button in top-right
3. View:
   - Variables: app version, Python version, platform, paths
   - Console: live loguru output

### Increase Log Verbosity
Edit `src/privacy_eraser/gui.py`:
```python
logger.add(..., level="DEBUG")  # Change from "INFO"
```

### Test-Specific Debugging
```bash
# Show print statements in tests
uv run -m pytest -s

# Run single test with full output
uv run -m pytest tests/test_cleaning.py::test_name -vv -s

# Drop into debugger on failure
uv run -m pytest --pdb
```

## Common Tasks

### Adding a New Cleaner Option (Built-in)
1. Edit `src/privacy_eraser/cleaning.py`
2. Add `CleanerOption` to `chromium_cleaner_options()` function
3. Define `DeleteAction` list with appropriate search modes
4. Write test in `tests/test_cleaning_chromium.py`

### Adding CleanerML Support for New Browser
1. Obtain or create CleanerML XML file in `bleachbit/cleaners/`
2. Update `xml_map` in `src/privacy_eraser/gui.py` `_populate_cleaners_for()`
3. Add `ProgramProbe` in `_default_probes()` in `gui.py`
4. Test detection and cleaning manually

### Adding New Detection Probe
1. Edit `src/privacy_eraser/gui.py` → `_default_probes()`
2. Create `ProgramProbe` with:
   - `registry_keys` (HKCU/HKLM paths)
   - `file_patterns` (with %ENVVAR% expansion)
   - `process_names` (executable names)
3. Update `_guess_user_data()` mapping if Chromium-like
4. Test on Windows with browser installed

## Troubleshooting

### "Module not found" errors
```bash
# Ensure dependencies are installed
uv sync
uv sync --extra test
```

### GUI doesn't launch
- Check Python version: `python --version` (must be 3.12+)
- Verify CustomTkinter installed: `uv pip list | grep customtkinter`
- Check for import errors in console output

### Tests fail with path errors
- Tests should use `sandbox` fixture from `conftest.py`
- Never hardcode absolute paths
- Use `monkeypatch.setenv()` for environment variables

### CleanerML not loading
- Verify XML file exists: `bleachbit/cleaners/<browser>.xml`
- Check file path in logs (Debug panel)
- Ensure `<cleaner os="windows">` matches current platform
- Validate XML syntax

## Performance Profiling

### Memory Usage
```python
import tracemalloc
tracemalloc.start()
# ... run code ...
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
for stat in top_stats[:10]:
    print(stat)
```

### Execution Time
```bash
# Profile the application
uv run python -m cProfile -o profile.stats -m privacy_eraser

# Analyze with snakeviz (install separately)
snakeviz profile.stats
```

## Release Checklist (Future)
- [ ] All tests pass: `uv run -m pytest`
- [ ] Coverage >80%: `uv run -m pytest --cov`
- [ ] Version bumped in `src/privacy_eraser/__init__.py`
- [ ] CHANGELOG.md updated
- [ ] Tag release: `git tag v0.x.0`
- [ ] Build installer (PyInstaller - TBD)
- [ ] Test installer on clean Windows VM
- [ ] Upload to GitHub Releases

## Environment Variables (for testing)
Tests automatically set these via `sandbox` fixture:
- `LOCALAPPDATA` → sandbox/LOCALAPPDATA
- `APPDATA` → sandbox/APPDATA
- `TMP` / `TEMP` → sandbox/LOCALAPPDATA/Temp
- `HOME` → sandbox/HOME
- `USERNAME` → testuser

Do NOT set these manually in production code; use `os.path.expandvars()`.

