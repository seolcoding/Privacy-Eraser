@echo off
REM ============================================================
REM Privacy Eraser - Flet Web Build Script
REM ============================================================
REM Builds a web app (no Visual Studio required)
REM ============================================================

echo.
echo ============================================================
echo Privacy Eraser - Flet Web Build Script
echo ============================================================
echo.

REM Clean previous builds
echo [1/2] Cleaning previous builds...
if exist "build\web" (
    rmdir /s /q "build\web"
    echo     - Removed build\web directory
)

REM Build web version
echo.
echo [2/2] Building Flet web app...
echo.

uv run flet build web

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
echo Web app location: build\web\
echo Open index.html in a browser to test
echo.
pause
