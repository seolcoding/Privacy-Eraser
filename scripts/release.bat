@echo off
REM ============================================================
REM Privacy Eraser - Flet Pack & Release Script
REM ============================================================
REM Automates the entire release process:
REM 1. Build single-file executable with Flet Pack
REM 2. Create Git tag
REM 3. Push to GitHub
REM 4. Create GitHub Release with executable
REM ============================================================

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo Privacy Eraser - Build ^& Release Automation (Flet Pack)
echo ============================================================
echo.

REM Get version number from argument or prompt
set VERSION=%1
if "%VERSION%"=="" (
    set /p VERSION="Enter version number (e.g., 2.0.0): "
)

if "%VERSION%"=="" (
    echo [ERROR] Version number is required!
    pause
    exit /b 1
)

echo Version: %VERSION%
echo Tag: latest (always points to newest release)
echo.

REM ============================================================
REM Step 1: Check dependencies
REM ============================================================
echo [Step 1/5] Checking dependencies...
echo.

REM Check Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is missing. Please install Python 3.12+
    pause
    exit /b 1
)
echo   [OK] Python found

REM Check Flet
python -c "import flet" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Flet is missing. Installing...
    pip install flet
)
echo   [OK] Flet available

REM Check GitHub CLI
where gh >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] GitHub CLI ^(gh^) is missing!
    echo Please install from: https://cli.github.com/
    pause
    exit /b 1
)
echo   [OK] GitHub CLI found

echo.

REM ============================================================
REM Step 2: Build single-file executable with Flet Pack
REM ============================================================
echo [Step 2/5] Building single-file executable with Flet Pack...
echo.

REM Clean previous builds
if exist "dist" rmdir /s /q "dist"

REM Build with Flet Pack (PyInstaller-based, single file)
uv run flet pack main.py ^
    --name "PrivacyEraser" ^
    --product-name "Privacy Eraser" ^
    --product-version "%VERSION%" ^
    --file-description "Privacy Eraser - Browser Data Cleaner" ^
    --copyright "Copyright (C) 2025 seolcoding.com" ^
    --add-data "static/images;static/images"

if %errorlevel% neq 0 (
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

REM Verify executable exists
if not exist "dist\PrivacyEraser.exe" (
    echo [ERROR] Executable is missing!
    pause
    exit /b 1
)

echo   [OK] Build successful (single file)
echo.

REM ============================================================
REM Step 3: Create and push Git tag (always "latest")
REM ============================================================
echo [Step 3/5] Creating Git tag...
echo.

REM Delete existing "latest" tag (locally and remotely)
git tag -d "latest" 2>nul
git push origin ":refs/tags/latest" 2>nul
echo   [OK] Old "latest" tag deleted

REM Create new "latest" tag
git tag -a "latest" -m "Release v%VERSION% - Flet UI (Flutter)"
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create tag!
    pause
    exit /b 1
)
echo   [OK] Tag created: latest (v%VERSION%)

REM Push tag to GitHub (force update)
git push origin "latest" --force
if %errorlevel% neq 0 (
    echo [ERROR] Failed to push tag!
    pause
    exit /b 1
)
echo   [OK] Tag pushed to GitHub
echo.

REM ============================================================
REM Step 4: Create GitHub Release
REM ============================================================
echo [Step 4/5] Creating GitHub Release...
echo.

REM Delete existing "latest" release if it exists
gh release delete "latest" --yes 2>nul
echo   [OK] Old "latest" release deleted (if existed)

REM Create release notes
set RELEASE_NOTES=Privacy Eraser v%VERSION%^

^

Flet (Flutter for Python) UI with Material Design 3^

^

**Features:**^

- Modern Flet/Flutter-based UI framework^

- Single-file executable (no installation)^

- Browser privacy data cleaning^

- Backup and restore functionality^

- Schedule execution (UI ready)^

- Download folder deletion option^

^

🤖 Generated with [Claude Code](https://claude.com/claude-code)

REM Create release with gh CLI
gh release create "latest" ^
    "dist\PrivacyEraser.exe" ^
    --title "Privacy Eraser v%VERSION%" ^
    --notes "%RELEASE_NOTES%"

if %errorlevel% neq 0 (
    echo [ERROR] Failed to create GitHub release!
    pause
    exit /b 1
)

echo   [OK] GitHub Release created
echo.

REM ============================================================
REM Step 5: Summary
REM ============================================================
echo ============================================================
echo RELEASE COMPLETED SUCCESSFULLY!
echo ============================================================
echo.
echo Version: %VERSION%
echo Tag: latest (always points to newest)
echo Executable: dist\PrivacyEraser.exe (single file)
echo Framework: Flet (Flutter for Python)
echo.
echo GitHub Release: https://github.com/yourusername/Privacy-Eraser/releases/latest
echo.
echo ============================================================
echo.

pause
