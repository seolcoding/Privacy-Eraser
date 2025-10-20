# Path Migration Guide: Unicode → ASCII

**Issue:** The current project path `D:\설\priv` contains Korean characters ("설") which cause Unicode encoding issues with:
- PowerShell commands
- Python virtual environments
- File system tools
- Some development tools

**Solution:** Migrate to ASCII-only path `D:\seol\priv`

## Manual Migration Steps

### Option 1: File Explorer (Recommended)

1. **Open File Explorer** and navigate to `D:\`
2. **Rename** the folder `설` to `seol`
3. **Verify** the new path is `D:\seol\priv`

### Option 2: Command Prompt (Alternative)

Open Command Prompt (cmd.exe) as Administrator and run:
```cmd
cd /d D:\
ren "설" seol
```

### Option 3: PowerShell with Unicode Support

If you have PowerShell 7+ with proper Unicode support:
```powershell
cd D:\
Rename-Item -Path "설" -NewName "seol"
```

## After Migration

### 1. Update Working Directory
```bash
cd "D:\seol\priv"
```

### 2. Recreate Virtual Environment
```bash
# Remove old venv (if it exists)
rm -rf .venv

# Create new venv
uv venv

# Install dependencies
uv sync
```

### 3. Run Tests
```bash
uv run pytest -q
```

### 4. Test GUI
```bash
uv run privacy_eraser
```

## Verification

After migration, verify these work:
- [ ] `uv sync` - Dependencies install
- [ ] `uv run pytest` - Tests pass
- [ ] `uv run privacy_eraser` - GUI launches
- [ ] No Unicode errors in terminal

## Benefits of ASCII Path

- ✅ Compatible with all tools and environments
- ✅ No encoding issues in virtual environments
- ✅ Works with all command-line tools
- ✅ Compatible with CI/CD systems
- ✅ No issues with Python imports

## Files That Need Manual Copy

If migration fails, these key files need to be copied manually:

### Core Files
- `pyproject.toml` - Project configuration
- `readme.md` - Updated documentation
- `TODO.md` - Task list
- `uv.lock` - Dependency lock file

### New Core Engine
- `src/privacy_eraser/core/` - Entire directory
  - `__init__.py`
  - `file_utils.py`
  - `windows_utils.py`
  - `cleaner_engine.py`

### Updated Files
- `src/privacy_eraser/cleaning.py` - Refactored to wrappers
- `CLEANUP_GUIDE.md` - Cleanup instructions
- `REFACTORING_COMPLETE.md` - Completion summary

### Documentation
- All files in `docs/` directory
- `CLEANUP_GUIDE.md`
- `REFACTORING_COMPLETE.md`
- `PATH_MIGRATION_GUIDE.md` (this file)

## Git Considerations

If you're using git:
1. **Before migration:** Commit all changes
2. **After migration:** The new location won't be a git repo
3. **To restore git:** Copy `.git` folder from old location to new location

## Alternative: Create New Repository

If migration is complex:
1. Create new directory `D:\seol\priv`
2. Copy all files manually
3. Initialize new git repo: `git init`
4. Add all files: `git add .`
5. Commit: `git commit -m "feat: migrate to ASCII path and integrate BleachBit core"`

## Support

If you encounter issues:
1. Check this guide first
2. Verify all files copied correctly
3. Recreate virtual environment
4. Run tests to verify functionality

---

**Status:** Ready for manual migration  
**Priority:** High (required for proper development environment)
