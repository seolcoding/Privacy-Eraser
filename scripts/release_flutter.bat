@echo off
REM ============================================================
REM Privacy Eraser - Flet Build & Release Script (Flutter)
REM ============================================================

REM CRITICAL: Set UTF-8 to see error messages (suppress emoji errors with file redirect)
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
REM Automates the entire release process:
REM 1. Build with Flutter SDK (flet build windows)
REM 2. Create ZIP archive
REM 3. Create Git tag
REM 4. Push to GitHub
REM 5. Create GitHub Release with ZIP
REM ============================================================
REM Advantages over PyInstaller:
REM - Native Flutter compilation (lower false-positive rate)
REM - Better performance
REM - Modern app structure
REM ============================================================

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo Privacy Eraser - Build ^& Release (Flet/Flutter)
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
echo Build Method: Flet Build (Flutter SDK)
echo Note: Product info from pyproject.toml
echo.

REM ============================================================
REM Step 1: Check dependencies
REM ============================================================
echo [Step 1/6] Checking dependencies...
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
REM Step 2: Build with Flet Build (Flutter)
REM ============================================================
echo [Step 2/6] Building with Flet Build (Flutter)...
echo.

REM Ensure all dependencies are installed (including flet-cli)
echo   Installing dependencies with uv...
uv sync --all-extras
if %errorlevel% neq 0 (
    echo [ERROR] Failed to sync dependencies!
    pause
    exit /b 1
)
echo   [OK] Dependencies synced

REM Clean previous builds (COMPLETE clean to avoid cache issues)
REM CRITICAL: Delete entire build/ and src/build/, not just subdirectories
REM Otherwise Flet may reuse cached app.zip (786MB bloat!)
echo   [CLEAN] Removing all build artifacts...
if exist "build" rmdir /s /q "build"
if exist "src\build" rmdir /s /q "src\build"
if exist ".flet" rmdir /s /q ".flet"
if exist "src\test_data" rmdir /s /q "src\test_data"
echo   [OK] Clean build environment ready (test_data removed)

REM ============================================================
REM CRITICAL: Verify project root is clean before build
REM ============================================================
REM If .venv or venv exists in project, it might be packaged (potential bloat!)
REM See: KNOWN_ISSUES.md for details
echo   [CHECK] Verifying project directory is clean...

if exist ".venv" (
    echo [WARNING] .venv directory found in project root
    echo This is okay if pyproject.toml excludes it (should be excluded by default^)
    echo Continuing with build...
)

if exist "venv" (
    echo [WARNING] venv directory found in project root
    echo This is okay if pyproject.toml excludes it (should be excluded by default^)
    echo Continuing with build...
)

echo   [OK] Project directory check complete

REM Build with Flet Build (Flutter-based, uses pyproject.toml settings)
REM Build from project root (main.py is in root)
REM Uses root's pyproject.toml and .venv automatically
REM FIXED: exclude patterns now in [tool.flet.app] section of pyproject.toml
REM   This ensures exclusions are applied to app.zip packaging
echo   [INFO] Running Flet build (output logged to build_flet.log)...
uv run flet build windows > build_flet.log 2>&1

if %errorlevel% neq 0 (
    echo [ERROR] Build failed! Check build_flet.log for details
    echo.
    echo Last 20 lines of log:
    powershell -Command "Get-Content build_flet.log -Tail 20"
    pause
    exit /b 1
)

REM Verify build output exists
if not exist "build\windows" (
    echo [ERROR] Build directory is missing!
    pause
    exit /b 1
)

echo   [OK] Build successful (Flutter/onedir)
echo.

REM ============================================================
REM Step 3: Create ZIP archive
REM ============================================================
echo [Step 3/5] Creating ZIP archive...
echo.

set ZIP_NAME=PrivacyEraser-v%VERSION%-win-x64.zip

REM Delete old ZIP if exists
if exist "%ZIP_NAME%" del /f "%ZIP_NAME%"

REM Create ZIP using PowerShell
powershell -Command "Compress-Archive -Path 'build\windows\*' -DestinationPath '%ZIP_NAME%' -Force"

if %errorlevel% neq 0 (
    echo [ERROR] ZIP creation failed!
    pause
    exit /b 1
)

REM Verify ZIP exists
if not exist "%ZIP_NAME%" (
    echo [ERROR] ZIP file is missing!
    pause
    exit /b 1
)

REM Calculate SHA256 hash
powershell -Command "Get-FileHash '%ZIP_NAME%' -Algorithm SHA256 | ForEach-Object { \"$($_.Hash)  %ZIP_NAME%\" } | Out-File '%ZIP_NAME%.sha256' -Encoding ascii"

REM ============================================================
REM CRITICAL: Verify final ZIP size (must be under 200MB)
REM ============================================================
echo   [CHECK] Verifying distribution size...

REM Get ZIP size in MB
for %%A in ("%ZIP_NAME%") do set ZIP_SIZE=%%~zA
if not defined ZIP_SIZE set ZIP_SIZE=0
set /a ZIP_SIZE_MB=%ZIP_SIZE% / 1048576

echo   Distribution size: %ZIP_SIZE_MB% MB
echo   Maximum allowed: 200 MB

if !ZIP_SIZE_MB! GTR 200 (
    echo.
    echo ============================================================
    echo [ERROR] Distribution ZIP is too large! (%ZIP_SIZE_MB% MB^)
    echo Maximum allowed: 200 MB
    echo.
    echo This indicates build optimization failed.
    echo Check KNOWN_ISSUES.md for troubleshooting.
    echo ============================================================
    pause
    exit /b 1
)

echo   [OK] Distribution size is acceptable
echo   [OK] ZIP created: %ZIP_NAME% (%ZIP_SIZE_MB% MB)
echo   [OK] Hash file: %ZIP_NAME%.sha256
echo.

REM ============================================================
REM Step 4: Create and push Git tag (always "latest")
REM ============================================================
echo [Step 4/5] Creating Git tag...
echo.

REM Delete existing "latest" tag (locally and remotely)
git tag -d "latest" 2>nul
git push origin ":refs/tags/latest" 2>nul
echo   [OK] Old "latest" tag deleted

REM Create new "latest" tag
git tag -a "latest" -m "Release v%VERSION% - Flet Build (Flutter)"
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
REM Step 5: Create GitHub Release
REM ============================================================
echo [Step 5/5] Creating GitHub Release...
echo.

REM Delete existing "latest" release if it exists
gh release delete "latest" --yes 2>nul
echo   [OK] Old "latest" release deleted (if existed)

REM Check if RELEASE_NOTES.md exists
if not exist "RELEASE_NOTES.md" (
    echo [ERROR] RELEASE_NOTES.md not found!
    pause
    exit /b 1
)
echo   [OK] RELEASE_NOTES.md found

REM Create release with gh CLI (using RELEASE_NOTES.md)
REM Use --target main to specify the branch (avoids timing issues)
gh release create "latest" ^
    "%ZIP_NAME%" ^
    "%ZIP_NAME%.sha256" ^
    --title "Privacy Eraser v%VERSION%" ^
    --notes-file "RELEASE_NOTES.md" ^
    --target main

if %errorlevel% neq 0 (
    echo [ERROR] Failed to create GitHub release!
    pause
    exit /b 1
)

echo   [OK] GitHub Release created
echo.

REM ============================================================
REM Release Complete
REM ============================================================
echo ============================================================
echo RELEASE COMPLETED SUCCESSFULLY!
echo ============================================================
echo.
echo Version: %VERSION%
echo Tag: latest (always points to newest)
echo Build Method: Flet Build (Flutter SDK)
echo Package: %ZIP_NAME%
echo Hash: %ZIP_NAME%.sha256
echo Framework: Flet (Flutter for Python)
echo.
echo Download: https://github.com/seolcoding/Privacy-Eraser/releases/latest
echo.
echo ============================================================
echo.

pause
