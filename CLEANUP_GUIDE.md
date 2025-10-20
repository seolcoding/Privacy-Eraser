# Repository Cleanup Guide

This document describes the repository cleanup performed on 2025-10-20.

## ✅ Completed Actions

### 1. Created Core Engine (`src/privacy_eraser/core/`)
Extracted and adapted BleachBit core logic into modular components:
- `file_utils.py` - File operations, whitelist protection, safe deletion
- `windows_utils.py` - Registry operations, process detection, locked file handling
- `cleaner_engine.py` - Cleaning orchestration, action types, progress reporting

### 2. Updated Existing Modules
- `cleaning.py` - Now provides backward-compatible wrappers around core engine
- Maintained API compatibility for existing code

### 3. Deleted Obsolete Files
- `main.py` - Replaced by `src/privacy_eraser/__main__.py`
- `privacy_eraser.zip` - Old archive removed
- `test_gui_manual.py` - Replaced by proper test suite
- `verify_refactor.py` - Refactor verification complete

### 4. Updated Documentation
- `readme.md` - Reflects new architecture and v1.0.0 features
- `pyproject.toml` - Version bumped to 1.0.0, description updated

## 📋 Manual Cleanup Required

Due to PowerShell path encoding issues, the following items need manual relocation:

### Move to `reference/bleachbit_original/`:
```
bleachbit/              → reference/bleachbit_original/bleachbit/
```
The entire BleachBit source directory should be archived for reference.

### Move to `reference/deprecated/`:
```
새 폴더/                → reference/deprecated/old_experiments/
```
Contains old experimental code and examples.

### Move to `docs/`:
```
00.OVERVIEW.md          → docs/00.OVERVIEW.md
01.CORE_FEATURES.md     → docs/01_CORE_FEATURES.md (rename for consistency)
spec.md                 → docs/00_SPEC.md (rename for clarity)
REFACTORING_SUMMARY.md  → docs/REFACTORING_HISTORY.md
PYSIDE6_REFACTOR_SUMMARY.md → docs/PYSIDE6_REFACTOR.md
```

### Optional Cleanup:
```
privacy_eraser.zip      → (already deleted)
reference/bleachbit_original/ → (keep as-is if BleachBit was successfully moved)
reference/deprecated/   → (keep as-is)
```

## 🏗️ New Structure

```
priv/
├── src/
│   └── privacy_eraser/
│       ├── core/                 # ✨ NEW: BleachBit-inspired core engine
│       │   ├── __init__.py
│       │   ├── file_utils.py
│       │   ├── windows_utils.py
│       │   └── cleaner_engine.py
│       ├── gui*.py               # PySide6 frontend modules
│       ├── app_state.py
│       ├── settings_db.py
│       ├── detect_windows.py
│       ├── cleanerml_loader.py
│       └── cleaning.py           # Legacy compatibility wrappers
├── tests/
├── docs/                         # All documentation
├── reference/                    # ✨ NEW: Archived code
│   ├── bleachbit_original/      # BleachBit source (reference)
│   └── deprecated/              # Old implementations
├── pyproject.toml
├── readme.md
├── TODO.md
└── uv.lock
```

## 🎯 Key Improvements

1. **Modular Core Engine**: Separated business logic from UI
2. **PySide6 Only**: Removed all deprecated GUI frameworks
3. **BleachBit Integration**: Adopted battle-tested cleaning logic
4. **Clean Architecture**: Clear separation of concerns
5. **Type Safety**: Full type hints throughout core modules
6. **Testability**: Core logic can be tested independently

## 🚀 Next Steps

1. Manually move files as described above
2. Run tests to verify nothing broke: `uv run pytest`
3. Test GUI: `uv run privacy_eraser`
4. Commit changes: `git add . && git commit -m "feat: integrate BleachBit core and clean repository"`
5. Consider adding integration tests for core engine

## 📝 Notes

- All deleted files are recoverable from git history if needed
- The `reference/` directory is gitignored by default - update `.gitignore` if you want to track it
- BleachBit source is kept for reference and GPL compliance (attribution)

