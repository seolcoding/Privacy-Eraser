# Build Size Optimization Guide

## Problem
`.venv` and development files were being included in the Flet build, causing unnecessarily large distribution files.

## Solutions Applied

### 1. Enhanced `pyproject.toml` Exclude Configuration
Updated `[tool.flet]` exclude list to comprehensively exclude:
- Virtual environments (`.venv`, `venv`)
- Python cache files (`__pycache__`, `*.pyc`, `*.pyo`, `*.pyd`)
- Version control files (`.git`)
- Editor/IDE configurations
- Documentation files
- Test files
- Build artifacts
- Development scripts

**Key Pattern Changes:**
```toml
exclude = [
    ".venv/**/*",      # Recursive exclusion
    "venv/**/*",
    "__pycache__/**/*",
    # ... (see pyproject.toml for full list)
]
```

### 2. Build Script Optimization
Updated `scripts/release_flutter.bat` to explicitly exclude directories:
```bash
uv run flet build windows --exclude ".venv" --exclude "venv" --exclude "__pycache__" --exclude "tests"
```

### 3. Build from `src/` Directory
Building from `src/` directory ensures only application code is packaged, not root-level development files.

## Expected Size Reduction

### Before Optimization
- Build typically includes:
  - `.venv` directory (~100-500MB depending on dependencies)
  - `__pycache__` files
  - Development tools and scripts
  - Documentation files

### After Optimization
- Excludes all development files
- Only includes:
  - Application source code (`src/privacy_eraser`)
  - Static assets (`static/`)
  - Required runtime dependencies (minimal)

**Estimated reduction: 50-80% smaller distribution**

## Additional Optimization Tips

### 1. Dependency Audit
Review dependencies in `pyproject.toml`:
```toml
dependencies = [
    "flet>=0.28.0",          # ~30MB (Flutter engine)
    "pillow>=10.0.0",        # ~3MB (image processing)
    "loguru>=0.7.2",         # ~1MB (logging)
    "psutil>=5.9.8",         # ~500KB (system info)
    "pyinstaller>=6.16.0",   # Development only? Consider moving to [project.optional-dependencies]
    "apscheduler>=3.10.0",   # ~500KB (scheduling)
    "winotify>=1.1.0",       # ~200KB (Windows notifications)
]
```

**Recommendation:** Move `pyinstaller` to `[project.optional-dependencies.build]` if not needed at runtime.

### 2. Flet Size Contributors
- **libmpv-2.dll** (~28MB): Included for audio/video support
  - Not needed if app doesn't use audio/video
  - Currently can't be excluded (Flet limitation)

### 3. Image Optimization
Static assets are small (~55KB total), no optimization needed.

### 4. Verify Build Contents
After building, check what's included:
```bash
# Windows
dir /s build\windows
```

Look for unexpected files:
- `.venv`, `venv` folders
- `__pycache__` directories
- `.py` test files
- Documentation files

## Build Command Reference

### Standard Build (with optimizations)
```bash
cd src
uv run flet build windows --exclude ".venv" --exclude "venv" --exclude "__pycache__" --exclude "tests"
```

### Full Release (automated)
```bash
scripts\release_flutter.bat 2.0.0
```

**New in v2.1.0+:**
- Automated src/ directory verification (fails if .venv detected)
- Post-build app.zip size validation (<100MB check)
- [tool.flet.app] exclude configuration for proper app.zip packaging

## FAQ: Common Concerns

### Q: ".venv 제외하면 라이브러리가 포함되지 않나요?"

**A: 아닙니다! Flet 빌드는 `.venv`를 사용하지 않습니다.**

**작동 원리:**
1. `flet build` 명령어는 `pyproject.toml`의 `[project.dependencies]`를 **직접 읽습니다**
2. 필요한 패키지들을 **독립적으로 수집**하여 번들에 포함합니다
3. `.venv`는 개발 환경일 뿐, 빌드 시에는 참조되지 않습니다

**증거 (Flet 공식 문서):**
> "The packaging installs all dependencies 'as is' from requirements.txt or pyproject.toml"
>
> "Site packages are now copied in an unpacked state directly into the application bundle" (Flet 0.27.0+)

**빌드 흐름:**
```
uv sync (개발 환경에 의존성 설치)
    ↓
flet build windows (pyproject.toml 읽기)
    ↓
의존성을 독립적으로 수집 (NOT from .venv)
    ↓
앱 번들에 포함
```

**`--exclude ".venv"`의 의미:**
- **소스 코드** 패키징 시 `.venv` 폴더를 제외
- 의존성 번들링과는 무관
- 크기만 줄이고 기능은 동일

### Q: "그럼 .venv가 없어도 빌드가 가능한가요?"

**A: 이론적으로는 가능하지만, 실제로는:**
- `uv sync`로 개발 환경을 먼저 준비합니다 (line 87)
- `flet build`가 pyproject.toml을 읽을 때 올바른 환경이 필요합니다
- `.venv`는 빌드 **도구** 실행을 위해 필요하지만, **결과물**에는 포함되지 않습니다

**결론:** `.venv`를 exclude해도 앱은 정상 작동합니다!

## Troubleshooting

### Issue: `.venv` still included
**Check:**
1. Ensure building from `src/` directory (not root)
2. Verify no `.venv` exists in `src/` folder
3. Check `pyproject.toml` exclude patterns

### Issue: Build too large (>100MB)
**Common causes:**
1. libmpv-2.dll (28MB) - unavoidable if using Flet
2. Flutter engine (~30MB) - required for Flet
3. Python runtime (~15MB) - required
4. Dependencies - audit and minimize

**Expected minimum size:** ~70-80MB for Flet Windows app

## References
- [Flet Build Documentation](https://flet.dev/docs/reference/cli/build/)
- [Flet Issue #2319: Reduce app size](https://github.com/flet-dev/flet/discussions/2319)
- [Flet Issue #4620: How to reduce the size of exe packaging](https://github.com/flet-dev/flet/issues/4620)

## Changelog

### 2025-10-24 (Critical Update)
- **FIXED:** app.zip bloat issue (1.2GB → expected 5-20MB)
  - Moved exclude patterns from `[tool.flet]` to `[tool.flet.app]` section
  - Added pre-build verification: fails if src/.venv exists
  - Added post-build validation: fails if app.zip >100MB
  - See KNOWN_ISSUES.md for details
- Enhanced `pyproject.toml` exclude patterns (recursive exclusion)
- Added explicit `--exclude` flags to build script
- Documented optimization strategy and expected results
