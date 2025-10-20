# Testing Guide for PrivacyEraser

## Test Philosophy
- **Safety First:** All tests run in isolated sandbox; NEVER touch real user data
- **Cross-Platform:** Tests should pass on Windows, Linux, macOS (with platform-specific skips)
- **Fast:** MVP test suite runs in <5 seconds
- **Comprehensive:** Cover all public APIs and edge cases

## Test Structure

### Test Files
- `tests/conftest.py` - Shared fixtures (sandbox, seed_walk_tree, make_glob_files)
- `tests/test_cleaning_actions.py` - DeleteAction, iter_search, CleanerOption
- `tests/test_cleaning_chromium.py` - Chromium built-in cleaner options
- `tests/test_cleanerml_loader.py` - CleanerML XML parsing
- `tests/test_detect_windows.py` - Windows-only detection (skipped on other platforms)

### Coverage (as of 2025-10-09)
- `cleaning.py`: ~90% (core engine fully tested)
- `cleanerml_loader.py`: ~85% (OS filtering, var expansion, delete actions)
- `detect_windows.py`: ~70% (Windows-only, partial mock coverage)
- `gui.py`: Minimal (manual testing only)
- `diagnostics.py`: Not tested (placeholder)

## Key Fixtures

### `sandbox` (from conftest.py)
**Purpose:** Isolated temporary directory with safe environment variables

**Usage:**
```python
def test_example(sandbox: Path):
    # sandbox is a clean tmp directory
    # Environment variables are patched:
    # - LOCALAPPDATA, APPDATA, TMP, TEMP, HOME all point inside sandbox
    target = sandbox / "test.txt"
    target.write_text("hello")
    assert target.exists()
    # Automatic cleanup after test
```

**Environment Variables Set:**
- `LOCALAPPDATA` → `{sandbox}/LOCALAPPDATA`
- `APPDATA` → `{sandbox}/APPDATA`
- `TMP`, `TEMP` → `{sandbox}/LOCALAPPDATA/Temp`
- `HOME` → `{sandbox}/HOME`
- `USERNAME` → `testuser`

### `seed_walk_tree` (from conftest.py)
**Purpose:** Create directory trees with files for walk tests

**Usage:**
```python
def test_walk(sandbox: Path, seed_walk_tree):
    base = sandbox / "tree"
    count = seed_walk_tree(base, {
        "": ("file1.txt", "file2.txt"),          # root of base
        "subdir": ("nested.log",),               # base/subdir/nested.log
        "subdir/deep": ("deep.dat",),            # base/subdir/deep/deep.dat
    })
    assert count == 4
    assert (base / "file1.txt").exists()
    assert (base / "subdir" / "nested.log").exists()
```

### `make_glob_files` (from conftest.py)
**Purpose:** Create files matching glob patterns

**Usage:**
```python
def test_glob(sandbox: Path, make_glob_files):
    created = make_glob_files(sandbox, {
        "logs/*.log": 3,      # creates logs/file0.log, logs/file1.log, logs/file2.log
        "cache/*.cache": 2,   # creates cache/file0.cache, cache/file1.cache
    })
    assert len(created) == 5
```

## Writing Tests

### Basic Test Template
```python
from pathlib import Path
from privacy_eraser.cleaning import DeleteAction

def test_my_feature(sandbox: Path):
    # 1. Setup: create test files
    target = sandbox / "data" / "test.txt"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(b"x" * 100)
    
    # 2. Execute: run the code under test
    action = DeleteAction("file", str(target))
    preview = action.preview()
    
    # 3. Assert: verify results
    assert len(preview) == 1
    count, bytes_deleted = action.execute()
    assert count == 1
    assert bytes_deleted == 100
    assert not target.exists()
```

### Testing CleanerML Loader
```python
def test_cleanerml_parsing(sandbox: Path):
    xml_content = """
    <cleaner os="windows">
      <var name="TMP">
        <value os="windows">%TEMP%</value>
      </var>
      <option id="temp">
        <label>Temp Files</label>
        <description>Delete temp files</description>
        <action command="delete" search="glob" path="$$TMP$$\\*.tmp" />
      </option>
    </cleaner>
    """
    xml_file = sandbox / "test.xml"
    xml_file.write_text(xml_content)
    
    options = load_cleaner_options_from_file(str(xml_file))
    assert len(options) == 1
    assert options[0].id == "temp"
    assert options[0].label == "Temp Files"
```

### Testing Windows-Only Code
```python
import os
import pytest

pytestmark = pytest.mark.skipif(os.name != "nt", reason="Windows-only tests")

def test_registry_detection(monkeypatch):
    from privacy_eraser import detect_windows as dw
    
    if dw.winreg is None:
        pytest.skip("winreg not available")
    
    # Mock winreg.OpenKey
    class FakeKey:
        pass
    
    def fake_open_key(hive, subkey):
        if subkey == "SOFTWARE\\TestApp":
            return FakeKey()
        raise FileNotFoundError
    
    monkeypatch.setattr(dw.winreg, "OpenKey", fake_open_key)
    assert dw.registry_key_exists("HKLM\\SOFTWARE\\TestApp") is True
    assert dw.registry_key_exists("HKLM\\SOFTWARE\\Missing") is False
```

## Running Tests

### Basic Commands
```bash
# Run all tests
uv run -m pytest -q

# Verbose output
uv run -m pytest -v

# Stop on first failure
uv run -m pytest -x

# Run specific file
uv run -m pytest tests/test_cleaning.py

# Run specific test
uv run -m pytest tests/test_cleaning.py::test_delete_action_deletes_files_and_dirs -v
```

### Coverage
```bash
# Coverage report in terminal
uv run -m pytest --cov=privacy_eraser --cov-report=term-missing

# HTML coverage report
uv run -m pytest --cov=privacy_eraser --cov-report=html
# Open htmlcov/index.html

# Coverage for specific module
uv run -m pytest --cov=privacy_eraser.cleaning tests/test_cleaning_*.py
```

### Debugging Tests
```bash
# Show print/log output
uv run -m pytest -s

# Drop into debugger on failure
uv run -m pytest --pdb

# Full traceback
uv run -m pytest --tb=long
```

## Test Best Practices

### ✅ DO
- Use `sandbox` fixture for all file operations
- Use `monkeypatch` for environment variables
- Test both preview and execute for DeleteAction/CleanerOption
- Test edge cases: empty directories, missing files, permission errors (where safe)
- Assert specific values, not just `> 0`

### ❌ DON'T
- Access real user directories (`C:\Users\...`, `/home/...`)
- Hardcode absolute paths
- Modify files outside `sandbox` or `tmp_path`
- Skip cleanup (fixtures handle this)
- Test GUI interactively in automated tests (manual testing only for now)

## Platform-Specific Testing

### Windows-Only Tests
Use `pytestmark` at module level:
```python
import os
import pytest

pytestmark = pytest.mark.skipif(os.name != "nt", reason="Windows-only detection tests")
```

### Cross-Platform Tests
Ensure paths use `os.path.join()` or `Path /` operator (NOT hardcoded `\\` or `/`).

## Test Data Patterns

### Small Files (for speed)
```python
# 3-byte files are enough for existence checks
target.write_bytes(b"xyz")
```

### Realistic Sizes (for byte count validation)
```python
# Create 1MB file
target.write_bytes(b"x" * (1024 * 1024))
count, bytes_deleted = action.execute()
assert bytes_deleted == 1024 * 1024
```

## Mocking Guidelines

### Prefer Fixtures Over Mocks
- Use `sandbox` for real file operations (safer, more realistic)
- Mock only external dependencies (winreg, psutil, network)

### Example: Mocking psutil
```python
def test_process_detection(monkeypatch):
    class FakeProcess:
        def name(self):
            return "chrome.exe"
        def username(self):
            return "testuser"
    
    def fake_iter():
        return [FakeProcess()]
    
    import psutil
    monkeypatch.setattr(psutil, "process_iter", fake_iter)
    # Now test is_process_running_windows()
```

## Coverage Goals
- **Critical modules (cleaning, cleanerml_loader):** >90%
- **Platform-specific (detect_windows):** >70% (Windows only)
- **GUI:** Manual testing (automated GUI testing future work)
- **Overall project:** >80%

## CI/CD (Future)
When GitHub Actions is set up:
```yaml
- name: Run tests
  run: |
    uv sync --extra test
    uv run -m pytest --cov=privacy_eraser --cov-report=xml
- name: Upload coverage
  uses: codecov/codecov-action@v3
```

## Adding New Tests

### Checklist
1. Identify module and function to test
2. Create test file: `tests/test_<module>.py`
3. Import function/class under test
4. Write test using `sandbox` fixture
5. Run test: `uv run -m pytest tests/test_<module>.py -v`
6. Verify coverage: `uv run -m pytest --cov=privacy_eraser.<module>`
7. Commit test with implementation

### Test Naming
- File: `test_<module>.py`
- Function: `test_<feature>_<scenario>()`
- Examples:
  - `test_delete_action_deletes_files_and_dirs()`
  - `test_cleanerml_os_filtering_skips_non_matching()`
  - `test_chromium_options_preview_and_execute()`

