@echo off
REM ============================================================
REM Privacy Eraser - Flet Build Script
REM ============================================================
REM Builds a standalone executable using Flet build command
REM ============================================================

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo Privacy Eraser - Flet Build Script
echo ============================================================
echo.

REM Check if Python is available
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is missing. Please install Python 3.12+
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set PYTHON_VERSION=%%v
echo Python version: %PYTHON_VERSION%

REM Check if Flet is installed
python -c "import flet" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Flet is missing. Installing...
    pip install flet
)

REM Clean previous builds
echo.
echo [1/3] Cleaning previous builds...
if exist "build" (
    rmdir /s /q "build"
    echo     - Removed build directory
)
if exist "dist" (
    rmdir /s /q "dist"
    echo     - Removed dist directory
)

REM Build with Flet
echo.
echo [2/3] Building Flet app...
echo.

REM Flet build command for Windows
flet build windows ^
    --project "Privacy Eraser" ^
    --description "Privacy management tool with Flet UI" ^
    --product-name "Privacy Eraser" ^
    --product-version "2.0.0" ^
    --copyright "Copyright (c) 2025 seolcoding.com" ^
    --build-name "2.0.0" ^
    --build-number 1

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

REM Check if executable was created
echo.
echo [3/3] Verifying build...

if exist "build\windows\PrivacyEraser.exe" (
    echo.
    echo ============================================================
    echo BUILD SUCCESSFUL!
    echo ============================================================
    echo.
    echo Executable location: build\windows\PrivacyEraser.exe
    echo.

    REM Get file size
    for %%A in ("build\windows\PrivacyEraser.exe") do (
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
