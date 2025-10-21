@echo off
REM ============================================================
REM Privacy Eraser - PyInstaller Build Script
REM ============================================================
REM Builds standalone EXE without Visual Studio
REM ============================================================

echo.
echo ============================================================
echo Privacy Eraser - PyInstaller Build
echo ============================================================
echo.

REM Install PyInstaller if needed
python -c "import PyInstaller" >nul 2>&1
if %errorlevel% neq 0 (
    echo [1/3] Installing PyInstaller...
    pip install pyinstaller
)

REM Clean previous builds
echo [2/3] Cleaning previous builds...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

REM Build with PyInstaller
echo [3/3] Building with PyInstaller...
echo.

pyinstaller ^
    --name "PrivacyEraser" ^
    --onefile ^
    --windowed ^
    --add-data "static;static" ^
    --add-data "bleachbit;bleachbit" ^
    --hidden-import "flet" ^
    --hidden-import "flet.core" ^
    --hidden-import "flet_desktop" ^
    main.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

echo.
echo ============================================================
echo BUILD SUCCESSFUL!
echo ============================================================
echo.
echo Executable: dist\PrivacyEraser.exe
echo.
pause
