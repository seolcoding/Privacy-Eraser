@echo off
REM ============================================================
REM Privacy Eraser - Flet Pack Build Script (Single File)
REM ============================================================
REM Builds a single executable using flet pack (PyInstaller)
REM ============================================================

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo Privacy Eraser - Flet Pack Build (Single File)
echo ============================================================
echo.

REM Check if Python is available
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is missing. Please install Python 3.12+
    pause
    exit /b 1
)

REM Check if Flet is installed
python -c "import flet" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Flet is missing. Installing...
    pip install flet
)

REM Clean previous builds
echo.
echo [1/3] Cleaning previous builds...
if exist "dist" (
    rmdir /s /q "dist"
    echo     - Removed dist directory
)

REM Build with Flet Pack
echo.
echo [2/3] Building with flet pack...
echo.

REM Flet pack command with image resources
uv run flet pack main.py ^
    --name "PrivacyEraser" ^
    --product-name "Privacy Eraser" ^
    --product-version "2.0.0" ^
    --file-description "Privacy Eraser - Browser Data Cleaner" ^
    --copyright "Copyright (C) 2025 seolcoding.com" ^
    --add-data "static/images;static/images"

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

REM Check if executable was created
echo.
echo [3/3] Verifying build...

if exist "dist\PrivacyEraser.exe" (
    echo.
    echo ============================================================
    echo BUILD SUCCESSFUL!
    echo ============================================================
    echo.
    echo Executable location: dist\PrivacyEraser.exe
    echo.

    REM Get file size
    for %%A in ("dist\PrivacyEraser.exe") do (
        set SIZE=%%~zA
        set /a SIZE_MB=!SIZE! / 1048576
        echo File size: !SIZE_MB! MB
    )
    echo.
) else (
    echo.
    echo [ERROR] Executable is missing!
    echo Build may have failed silently.
    pause
    exit /b 1
)

echo Build completed successfully!
echo.
pause
