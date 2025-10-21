@echo off
REM ============================================================================
REM Privacy Eraser POC - Local Build Script
REM ============================================================================
REM
REM Builds a single-file Windows executable using PyInstaller
REM
REM Requirements:
REM   - uv package manager installed
REM   - pyinstaller dependency installed (uv sync --extra build)
REM
REM Usage:
REM   scripts\build_exe.bat
REM
REM Output:
REM   dist\PrivacyEraser.exe
REM ============================================================================

echo.
echo ============================================================
echo  Privacy Eraser POC - Build Script
echo ============================================================
echo.

REM Change to project root
cd /d "%~dp0\.."

REM Check if uv is installed
where uv >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] uv not found. Please install uv first:
    echo         https://github.com/astral-sh/uv
    exit /b 1
)

REM Install build dependencies
echo [1/4] Installing build dependencies...
uv sync --extra build
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    exit /b 1
)

REM Clean previous build
echo.
echo [2/4] Cleaning previous build...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Run PyInstaller
echo.
echo [3/4] Building executable with PyInstaller...
uv run pyinstaller build_spec.py
if %errorlevel% neq 0 (
    echo [ERROR] PyInstaller build failed
    exit /b 1
)

REM Verify output
echo.
echo [4/4] Verifying build...
if exist dist\PrivacyEraser.exe (
    echo.
    echo ============================================================
    echo  BUILD SUCCESSFUL!
    echo ============================================================
    echo.
    echo  Output: dist\PrivacyEraser.exe
    for %%A in (dist\PrivacyEraser.exe) do echo  Size:   %%~zA bytes (%%~zA / 1048576 = ~%%~zA MB)
    echo.
    echo  You can now run: dist\PrivacyEraser.exe
    echo ============================================================
    echo.
) else (
    echo [ERROR] Build output not found: dist\PrivacyEraser.exe
    exit /b 1
)

exit /b 0
