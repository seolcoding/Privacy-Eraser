@echo off
REM ============================================================
REM Quick Release Script - Manual GitHub Release
REM ============================================================
REM Compresses build\windows and uploads to GitHub Release
REM ============================================================

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo Quick Release - Upload build\windows to GitHub
echo ============================================================
echo.

REM Get version number from argument or prompt
set VERSION=%1
if "%VERSION%"=="" (
    set /p VERSION="Enter version number (e.g., 2.0.6-test): "
)

if "%VERSION%"=="" (
    echo [ERROR] Version number is required!
    pause
    exit /b 1
)

echo Version: %VERSION%
echo Tag: latest
echo.

REM ============================================================
REM Step 1: Verify build directory exists
REM ============================================================
echo [Step 1/4] Verifying build directory...
echo.

if not exist "build\windows" (
    echo [ERROR] build\windows directory not found!
    echo Please run the build first: uv run flet build windows
    pause
    exit /b 1
)
echo   [OK] build\windows found
echo.

REM ============================================================
REM Step 2: Create ZIP archive
REM ============================================================
echo [Step 2/4] Creating ZIP archive...
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

REM Get ZIP size
for %%A in ("%ZIP_NAME%") do set ZIP_SIZE=%%~zA
set /a ZIP_SIZE_MB=%ZIP_SIZE% / 1048576

echo   [OK] ZIP created: %ZIP_NAME% (%ZIP_SIZE_MB% MB)
echo   [OK] Hash file: %ZIP_NAME%.sha256
echo.

REM ============================================================
REM Step 3: Create Git tag
REM ============================================================
echo [Step 3/4] Creating Git tag...
echo.

REM Delete existing "latest" tag (locally and remotely)
git tag -d "latest" 2>nul
git push origin ":refs/tags/latest" 2>nul
echo   [OK] Old "latest" tag deleted

REM Create new "latest" tag
git tag -a "latest" -m "Release v%VERSION%"
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
echo [Step 4/4] Creating GitHub Release...
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

REM Create release with gh CLI
gh release create "latest" ^
    "%ZIP_NAME%" ^
    "%ZIP_NAME%.sha256" ^
    --title "Privacy Eraser v%VERSION%" ^
    --notes-file "RELEASE_NOTES.md"

if %errorlevel% neq 0 (
    echo [ERROR] Failed to create GitHub release!
    pause
    exit /b 1
)

echo   [OK] GitHub Release created
echo.

REM ============================================================
REM Summary
REM ============================================================
echo ============================================================
echo RELEASE COMPLETED SUCCESSFULLY!
echo ============================================================
echo.
echo Version: %VERSION%
echo Tag: latest
echo Package: %ZIP_NAME% (%ZIP_SIZE_MB% MB)
echo Hash: %ZIP_NAME%.sha256
echo.
echo Download: https://github.com/seolcoding/Privacy-Eraser/releases/latest
echo.
echo ============================================================
echo.

pause
