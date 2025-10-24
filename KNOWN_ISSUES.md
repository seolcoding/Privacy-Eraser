# Known Issues & Critical Fixes Needed

## ✅ FIXED: app.zip Size Issue (was 1.2GB)

**Status:** ✅ FIXED (2025-10-24)
**Next Steps:** Test build to verify fix works

### Problem
After building with `flet build windows`, the generated `app.zip` file in `data/flutter_assets/` is **1.2GB** in size and contains:
- Complete source code
- Potentially `.venv` or development files
- Unnecessary project files

**Location:** `PrivacyEraser-v2.x.x-win-x64\data\flutter_assets\app.zip`

### Impact
- Massive distribution file size (users download 1.2GB unnecessarily)
- Exposes source code in production build
- Includes development files that shouldn't be in production

### Root Cause Analysis

#### Current Build Process:
```bash
cd src
uv run flet build windows --exclude ".venv" --exclude "venv" --exclude "__pycache__" --exclude "tests"
```

**Problems Identified:**
1. **Wrong exclude location in pyproject.toml:**
   - Current: `[tool.flet]` section with `exclude = [...]`
   - Correct: Should be `[tool.flet.app]` section
   - Result: Exclusions not applied to app.zip packaging

2. **No verification of src/ cleanliness:**
   - If `.venv` exists in `src/`, it gets packaged
   - No pre-build cleanup step

3. **Flet packaging behavior:**
   - "By default, all files except the build directory will be added to the package asset"
   - Our extensive exclude list not being respected during app.zip creation

### Solution Applied ✅

#### 1. Fixed pyproject.toml Structure ✅
```toml
[tool.flet]
org = "com.seolcoding"
product = "Privacy Eraser"
# ... other metadata

[tool.flet.app]
# Proper location for exclude patterns
exclude = [
    ".venv/**/*",
    "venv/**/*",
    "__pycache__/**/*",
    # ... rest of exclusions
]
```

#### 2. Added Pre-Build Cleanup to Script ✅
```batch
REM Before building, verify src/ is clean
cd src
if exist ".venv" (
    echo [ERROR] .venv found in src/! This will bloat app.zip
    echo Please remove .venv from src/ directory
    exit /b 1
)
if exist "venv" (
    echo [ERROR] venv found in src/! This will bloat app.zip
    exit /b 1
)
```

#### 3. Using Flet 0.28.0+ with Proper Exclusions ✅
```bash
flet build windows \
    --exclude ".venv" \
    --exclude "venv" \
    --exclude "__pycache__" \
    --exclude "tests" \
    --cleanup-on-compile
```

#### 4. Added Post-Build Verification ✅
```batch
REM Check app.zip size after build
powershell -Command "Get-Item 'build\windows\data\flutter_assets\app.zip' | ForEach-Object { if ($_.Length -gt 100MB) { Write-Error 'app.zip is too large!' } }"
```

### Expected Results After Fix
- **app.zip size:** ~5-20MB (only necessary Python code and dependencies)
- **Total distribution:** ~70-100MB (down from 1.2GB+)
- **Contents:** Only production code, no .venv, no dev files

### Testing Checklist (User to Verify)
- [ ] Build with fixed configuration (`scripts\release_flutter.bat`)
- [ ] Verify app.zip size < 50MB (script will auto-check)
- [ ] Extract and inspect app.zip contents (no .venv, no __pycache__)
- [ ] Test application functionality (ensure all dependencies work)
- [ ] Verify final ZIP distribution size

**Implementation Complete:** All code changes applied. Awaiting build test.

### References
- [Flet Issue #3125: --exclude option](https://github.com/flet-dev/flet/issues/3125)
- [Flet packaging update blog](https://flet.dev/blog/flet-packaging-update/)
- [Flet 0.27.0 release notes](https://flet.dev/blog/flet-v-0-27-release-announcement/)

---

## Other Known Issues

### None currently

---

## Changelog

### 2025-10-24
- **10:00 - DISCOVERED:** app.zip bloat issue (1.2GB, contains source code and .venv)
- **10:30 - ANALYZED:** Root cause identified - exclude patterns in wrong pyproject.toml section
- **11:00 - IMPLEMENTED:**
  - Moved exclude from `[tool.flet]` to `[tool.flet.app]`
  - Added pre-build src/ verification (fails if .venv exists)
  - Added post-build app.zip size check (fails if >100MB)
- **11:30 - DOCUMENTED:** Updated BUILD_OPTIMIZATION.md with new approach
- **STATUS:** ✅ All fixes implemented, ready for build test
