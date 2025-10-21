@echo off
REM ============================================================================
REM Privacy Eraser - Build & Release Script
REM ============================================================================
REM
REM 로컬에서 빌드하고 GitHub Release를 생성하는 자동화 스크립트
REM
REM Requirements:
REM   - Python 3.12+ with PyInstaller, PySide6, etc.
REM   - gh CLI (GitHub CLI)
REM
REM Usage:
REM   scripts\release.bat [version]
REM   예: scripts\release.bat 1.0.1
REM
REM ============================================================================

setlocal EnableDelayedExpansion

echo.
echo ============================================================
echo  Privacy Eraser - Build ^& Release
echo ============================================================
echo.

REM Change to project root
cd /d "%~dp0\.."

REM ============================================
REM 1. 버전 입력
REM ============================================

set VERSION=%1

if "%VERSION%"=="" (
    echo [1/5] 버전 입력
    echo.
    set /p VERSION="릴리즈 버전을 입력하세요 (예: 1.0.1): "
)

if "%VERSION%"=="" (
    echo [ERROR] 버전이 입력되지 않았습니다.
    exit /b 1
)

REM v 접두사 제거 (입력한 경우)
set VERSION=%VERSION:v=%

echo.
echo 버전: v%VERSION%
echo.

REM 확인 메시지
set /p CONFIRM="v%VERSION%로 릴리즈를 생성하시겠습니까? (y/n): "
if /i not "%CONFIRM%"=="y" (
    echo 취소되었습니다.
    exit /b 0
)

REM ============================================
REM 2. 의존성 확인
REM ============================================

echo.
echo [2/5] 의존성 확인...

REM Python 확인
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python이 설치되지 않았습니다.
    exit /b 1
)

REM gh CLI 확인
gh --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] GitHub CLI(gh)가 설치되지 않았습니다.
    echo          https://cli.github.com/ 에서 설치하세요.
    exit /b 1
)

REM PyInstaller 설치 확인 및 설치
python -c "import PyInstaller" >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller가 설치되지 않았습니다. 설치 중...
    python -m pip install pyinstaller pyside6 qt-material qtawesome loguru --quiet
)

echo 의존성 확인 완료!

REM ============================================
REM 3. 빌드
REM ============================================

echo.
echo [3/5] 빌드 중...
echo.

REM 이전 빌드 정리
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM PyInstaller 실행
python -m PyInstaller PrivacyEraser.spec --log-level WARN

if %errorlevel% neq 0 (
    echo [ERROR] 빌드에 실패했습니다.
    exit /b 1
)

REM 빌드 결과 확인
if not exist dist\PrivacyEraser.exe (
    echo [ERROR] dist\PrivacyEraser.exe가 생성되지 않았습니다.
    exit /b 1
)

REM 파일 크기 표시
for %%A in (dist\PrivacyEraser.exe) do (
    set /a SIZE_MB=%%~zA / 1048576
    echo 빌드 성공! 크기: !SIZE_MB! MB
)

REM ============================================
REM 4. Git 태그 생성 및 푸시
REM ============================================

echo.
echo [4/5] Git 태그 생성...

REM 태그가 이미 존재하는지 확인
git rev-parse v%VERSION% >nul 2>&1
if %errorlevel% equ 0 (
    echo [ERROR] 태그 v%VERSION%가 이미 존재합니다.
    echo          기존 태그를 삭제하려면: git tag -d v%VERSION% ^&^& git push origin :refs/tags/v%VERSION%
    exit /b 1
)

REM 태그 생성
git tag -a v%VERSION% -m "Release v%VERSION%"
if %errorlevel% neq 0 (
    echo [ERROR] 태그 생성에 실패했습니다.
    exit /b 1
)

REM 태그 푸시
git push origin v%VERSION%
if %errorlevel% neq 0 (
    echo [ERROR] 태그 푸시에 실패했습니다.
    echo          로컬 태그 삭제: git tag -d v%VERSION%
    exit /b 1
)

echo 태그 v%VERSION% 생성 및 푸시 완료!

REM ============================================
REM 5. GitHub Release 생성
REM ============================================

echo.
echo [5/5] GitHub Release 생성...
echo.

REM Release 노트 생성
set RELEASE_NOTES=## Privacy Eraser POC v%VERSION%^

^

### 다운로드^

- **Windows**: `PrivacyEraser.exe`^

^

### 주요 기능^

- 🔍 자동 브라우저 감지 (Chrome, Edge, Firefox 등)^

- 🗑️ 원클릭 개인정보 삭제 (캐시, 쿠키, 히스토리, 세션, 비밀번호)^

- 📚 북마크/다운로드 삭제 옵션^

- ↩️ 실행 취소 기능 (백업/복원)^

- 🎨 Material Design UI^

^

### 설치 방법^

1. `PrivacyEraser.exe` 다운로드^

2. Windows SmartScreen 경고 시 "추가 정보" → "실행" 클릭^

3. 실행^

^

### 시스템 요구사항^

- Windows 10/11 (64-bit)^

^

---^

^

🤖 Built locally and released with ❤️

REM GitHub Release 생성
gh release create v%VERSION% dist\PrivacyEraser.exe --title "Privacy Eraser POC v%VERSION%" --notes "%RELEASE_NOTES%"

if %errorlevel% neq 0 (
    echo [ERROR] GitHub Release 생성에 실패했습니다.
    echo          태그는 생성되었으므로 수동으로 릴리즈를 생성하세요.
    exit /b 1
)

REM ============================================
REM 완료
REM ============================================

echo.
echo ============================================================
echo  릴리즈 완료!
echo ============================================================
echo.
echo  버전: v%VERSION%
echo  릴리즈 URL: https://github.com/seolcoding/Privacy-Eraser/releases/tag/v%VERSION%
echo  다운로드: https://github.com/seolcoding/Privacy-Eraser/releases/download/v%VERSION%/PrivacyEraser.exe
echo.
echo ============================================================
echo.

exit /b 0
