@echo off
REM ============================================================
REM Privacy Eraser - Flet Build & Release Script
REM ============================================================
REM Automates the entire release process:
REM 1. Build executable with Flet
REM 2. Create Git tag
REM 3. Push to GitHub
REM 4. Create GitHub Release with executable
REM ============================================================

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo Privacy Eraser - Build ^& Release Automation (Flet)
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

REM Check Flet and Flet CLI
python -c "import flet" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Flet is missing. Installing...
    pip install flet
)
python -c "import flet_cli" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Flet CLI is missing. Installing...
    pip install flet-cli
)
echo   [OK] Flet and Flet CLI available

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
REM Step 2: Build executable with Flet
REM ============================================================
echo [Step 2/5] Building executable with Flet...
echo.

REM Clean previous builds
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

REM Build with Flet CLI
REM All metadata is configured in pyproject.toml
python -m flet_cli build windows

if %errorlevel% neq 0 (
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

REM Verify executable exists
if not exist "build\windows\PrivacyEraser.exe" (
    echo [ERROR] Executable is missing!
    pause
    exit /b 1
)

echo   [OK] Build successful
echo.

REM ============================================================
REM Step 3: Create and push Git tag
REM ============================================================
echo [Step 3/5] Creating Git tag...
echo.

REM Check if tag already exists
git rev-parse "v%VERSION%" >nul 2>&1
if %errorlevel% equ 0 (
    echo [WARNING] Tag v%VERSION% already exists!
    set /p OVERWRITE="Overwrite tag? (y/n): "
    if /i "!OVERWRITE!"=="y" (
        git tag -d "v%VERSION%"
        git push origin ":refs/tags/v%VERSION%" 2>nul
        echo   [OK] Old tag deleted
    ) else (
        echo [ABORT] Tag already exists
        pause
        exit /b 1
    )
)

REM Create new tag
git tag -a "v%VERSION%" -m "Release v%VERSION% - Flet UI"
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create tag!
    pause
    exit /b 1
)
echo   [OK] Tag created: v%VERSION%

REM Push tag to GitHub
git push origin "v%VERSION%"
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

REM Create release notes
set RELEASE_NOTES=Release v%VERSION%^

^

Flet-based UI with Material Design 3.^

^

Features:^

- Modern Flet UI framework^

- Browser privacy data cleaning^

- Backup and restore functionality^

- Schedule execution (UI ready)^

- Download folder deletion option^

^

🤖 Generated with [Claude Code](https://claude.com/claude-code)

REM Create release with gh CLI
gh release create "v%VERSION%" ^
    "build\windows\PrivacyEraser.exe" ^
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
echo Tag: v%VERSION%
echo Executable: build\windows\PrivacyEraser.exe
echo.
echo GitHub Release: https://github.com/yourusername/Privacy-Eraser/releases/tag/v%VERSION%
echo.
echo ============================================================
echo.

pause
