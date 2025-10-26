# Claude Code - 프로젝트 작업 가이드

이 문서는 Claude Code와 함께 작업할 때 사용하는 명령어와 프로세스를 기록합니다.

## 📚 AI 개발 문서 참고 (중요!)

**라이브러리나 프레임워크 사용 시 반드시 `ai-docs/` 디렉토리의 문서를 참고하세요.**

### 주요 참고 문서

- **Flet UI 개발 시**: `ai-docs/flet.md` 필독
- **프로젝트 아키텍처 이해**: `ai-docs/context/architecture.md`
- **테스트 작성**: `ai-docs/context/testing.md`

### 사용 예시

```
# Claude Code에게 명령 시:
"Flet으로 새 다이얼로그 만들어줘 (ai-docs/flet.md 참고)"
"새 기능 추가 시 프로젝트 구조 확인 (ai-docs/context/architecture.md 참고)"
```

**⚠️ 중요**:

- Flet 코드 작성 전에는 **반드시** `ai-docs/flet.md`를 먼저 읽으세요
- 새로운 라이브러리 도입 시 ai-docs에 문서를 추가하세요

---

## 📋 다음 작업 (TODO)

### 1. DEV 모드 경고 메시지 추가 ⏳

**목적**: 개발자가 DEV 모드에서 작업 중임을 명확히 인지하도록 함

**구현 위치**: `src/privacy_eraser/ui/main.py`

**상세 내용**:
- UI 상단 또는 삭제 버튼 근처에 경고 배너 표시
- 메시지: "⚠️ 개발자 모드: 실제 파일이 삭제되지 않습니다"
- 배경색: `AppColors.WARNING` (amber)
- 조건: `AppConfig.is_dev_mode()` 확인

**구현 예시**:
```python
if AppConfig.is_dev_mode():
    ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.INFO_ROUNDED, color=AppColors.WARNING),
            ft.Text("개발자 모드: 실제 파일이 삭제되지 않습니다")
        ]),
        bgcolor=f"{AppColors.WARNING}20",
        padding=8,
        border_radius=6
    )
```

---

### 2. 브라우저 설정 보존 (초기화 방지) 🔧

**문제**: 현재 sync 옵션으로 브라우저 동기화 데이터를 삭제하면 브라우저가 완전히 초기화됨

**목표**: 개인정보만 삭제하고 브라우저 설정(테마, 확장프로그램 설정 등)은 유지

**분석 필요**:
1. CleanerML에서 어떤 파일들이 설정 관련인지 확인
2. `sync` 옵션이 삭제하는 파일 목록 검토
3. Preferences, Local State 파일 중 어떤 키를 보존해야 하는지 확인

**제외해야 할 항목** (예상):
- `Preferences` 파일의 특정 섹션 (테마, UI 설정)
- `Local State` 파일의 프로필 리스트 제외 항목
- 확장프로그램 설정 (`Extension Settings/`)

**구현 방법**:
1. `sync` 옵션을 더 세밀하게 분리
2. JSON 파일 부분 삭제 기능 구현 (특정 키만 삭제)
3. 또는 `sync` 옵션을 제거하고 개별 파일만 삭제

**참고**:
- `src/privacy_eraser/cleaners/google_chrome.xml` - sync 옵션
- `src/privacy_eraser/cleaners/whale.xml` - sync 옵션

---

### 3. 시스템 트레이 기능 구현 🖥️

**목적**: 앱을 최소화해도 백그라운드에서 실행 유지

**구현 사항**:
- 창 닫기 버튼 클릭 시 → 트레이로 최소화
- 트레이 아이콘 더블클릭 → 창 복원
- 트레이 우클릭 메뉴:
  - "열기"
  - "종료"

**Flet 구현**:
```python
def window_event_handler(e):
    if e.data == "close":
        page.window_minimized = True
        # Show tray notification
        page.show_snack_bar(
            ft.SnackBar(content=ft.Text("트레이로 최소화되었습니다"))
        )

page.window_prevent_close = True
page.on_window_event = window_event_handler
```

**참고 문서**: `ai-docs/flet.md` - Window Events 섹션

**추가 기능**:
- 트레이 알림: "Privacy Eraser가 백그라운드에서 실행 중입니다"
- 시작 프로그램 등록 옵션 (선택사항)

---

### 4. 커스텀 앱 아이콘 제작 및 적용 🎨

**현재 문제**: Flet 기본 아이콘 사용 중

**작업 내용**:
1. **아이콘 디자인**
   - 테마: 빗자루 + 자물쇠/방패 조합
   - 색상: 메인 컬러 (#6366F1 Indigo) 기반
   - 크기: 256x256, 128x128, 64x64, 32x32, 16x16

2. **파일 형식**
   - Windows: `.ico` 파일
   - macOS: `.icns` 파일
   - Linux: `.png` 파일

3. **저장 위치**
   - `static/icons/app_icon.ico`
   - `static/icons/app_icon.png`

4. **적용 방법**
   ```python
   # main.py
   page.window_icon = "static/icons/app_icon.png"

   # Flet build 시
   flet build windows --icon static/icons/app_icon.ico
   ```

**디자인 도구**:
- 무료: GIMP, Inkscape
- 온라인: favicon.io, flaticon.com

**참고**:
- Flet 아이콘 설정: `ai-docs/flet.md` 참고

---

### 5. 트레이 간편 예약 메뉴 🕐

**목적**: 트레이 메뉴에서 빠르게 예약 설정

**트레이 우클릭 메뉴 구조**:
```
Privacy Eraser
├── 열기
├── 간편 예약 ▶
│   ├── 10분 후
│   ├── 30분 후
│   ├── 1시간 후
│   ├── 3시간 후
│   └── 예약 취소
├── 예약 목록 보기
└── 종료
```

**구현 방법**:
1. 간편 예약용 임시 스케줄 생성
2. `ScheduleManager`에 one-time 스케줄 추가
3. 기존 간편 예약이 있으면 덮어쓰기

**코드 예시**:
```python
def create_quick_schedule(minutes: int):
    schedule_time = datetime.now() + timedelta(minutes=minutes)

    scenario = ScheduleScenario(
        id="quick_schedule",
        name=f"{minutes}분 후 자동 삭제",
        enabled=True,
        schedule_type="once",
        time=schedule_time.strftime("%H:%M"),
        browsers=get_selected_browsers(),
        delete_bookmarks=False,
        delete_downloads=False,
        created_at=datetime.now().isoformat(),
        description=f"트레이 간편 예약: {minutes}분 후 실행"
    )

    schedule_manager.add_schedule(scenario)
```

**참고 파일**:
- `src/privacy_eraser/core/schedule_manager.py`
- `src/privacy_eraser/schedule_executor.py`

---

### 6. 예약 실행 30초 전 알림 및 취소 옵션 ⏰

**목적**: 사용자가 실수로 예약을 설정했을 경우 마지막 기회 제공

**구현 내용**:

1. **30초 전 알림 표시**
   - 시스템 트레이 알림
   - 앱이 열려있으면 Dialog 표시
   - 메시지: "30초 후 브라우저 데이터가 삭제됩니다"

2. **카운트다운 UI**
   ```python
   ft.AlertDialog(
       title=ft.Text("예약 실행 알림"),
       content=ft.Column([
           ft.Text("30초 후 다음 작업이 실행됩니다:"),
           ft.Text(f"• 브라우저: {', '.join(browsers)}"),
           ft.Text(f"• 삭제 항목: 쿠키, 히스토리, 세션"),
           ft.Text(f"남은 시간: {countdown}초",
                   size=24, weight=ft.FontWeight.BOLD)
       ]),
       actions=[
           ft.TextButton("취소", on_click=cancel_schedule),
           ft.ElevatedButton("지금 실행", on_click=execute_now),
       ]
   )
   ```

3. **취소 기능**
   - "취소" 버튼 클릭 → 예약 비활성화 (삭제하지 않음)
   - "지금 실행" 버튼 → 즉시 실행
   - 30초 경과 → 자동 실행

4. **구현 위치**
   - `src/privacy_eraser/schedule_executor.py`의 `execute_scenario()` 함수 시작 부분
   - 또는 APScheduler의 `before_job` 이벤트 활용

**스케줄러 수정**:
```python
def execute_scenario_with_countdown(scenario: ScheduleScenario):
    # 30초 카운트다운 및 알림
    if not show_countdown_notification(scenario, timeout=30):
        logger.info("User cancelled scheduled execution")
        return

    # 기존 실행 로직
    execute_scenario(scenario)
```

**알림 방법**:
1. Flet Dialog (앱이 실행 중일 때)
2. Windows 알림 (`plyer` 라이브러리 사용)
   ```python
   from plyer import notification
   notification.notify(
       title="Privacy Eraser",
       message="30초 후 브라우저 데이터가 삭제됩니다",
       timeout=30
   )
   ```

---

## 📝 작업 우선순위

| 순위 | 작업 | 예상 시간 | 난이도 |
|------|------|-----------|--------|
| 1 | DEV 모드 경고 메시지 | 10분 | ⭐ |
| 2 | 커스텀 앱 아이콘 | 30분 | ⭐ |
| 3 | 시스템 트레이 기능 | 1시간 | ⭐⭐ |
| 4 | 트레이 간편 예약 메뉴 | 1시간 | ⭐⭐ |
| 5 | 예약 실행 30초 전 알림 | 1.5시간 | ⭐⭐⭐ |
| 6 | 브라우저 설정 보존 | 2시간 | ⭐⭐⭐ |

**권장 작업 순서**: 1 → 2 → 3 → 4 → 5 → 6

---

## 🚀 빌드 & 릴리즈 프로세스

### 두 가지 빌드 방식 비교

| | **Flet Build (Flutter)** ⭐ | **Flet Pack (PyInstaller)** |
|---|---|---|
| **권장도** | 권장 | 선택적 |
| **기반 기술** | Flutter SDK (네이티브) | PyInstaller (Python) |
| **빌드 결과** | ZIP (onedir 폴더) | 단일 EXE 파일 |
| **오탐률** | 낮음 (네이티브 컴파일) | 높음 (셀프-추출 패턴) |
| **빌드 속도** | 중간 (첫 빌드 느림) | 빠름 |
| **실행 성능** | 빠름 | 보통 |
| **설치 요구** | Flutter SDK | PyInstaller |
| **배포 형태** | ZIP 압축 해제 필요 | 단일 파일 실행 |

**⚠️ 중요: Windows Defender 오탐 방지**

- **Flet Build (Flutter)** 방식이 오탐률이 훨씬 낮습니다
- PyInstaller의 셀프-추출 패턴은 바이러스로 오인되기 쉽습니다
- 코드 서명 없이 배포 시 **Flet Build** 강력 권장

---

### 자동 빌드 & 릴리즈 (Flet Build - 권장 ⭐)

**`scripts/release_flutter.bat`** 스크립트를 사용하면 Flutter 빌드부터 릴리즈까지 자동화됩니다.

#### 사용법

```bash
# 버전을 인자로 전달
scripts\release_flutter.bat 2.0.1

# 또는 실행 후 버전 입력
scripts\release_flutter.bat
```

#### 스크립트가 자동으로 수행하는 작업

1. ✅ 버전 입력 (또는 인자로 전달)
2. ✅ 의존성 확인 (Python, Flet, Flutter SDK, gh CLI)
3. ✅ **Flutter 빌드** (Flet Build - 네이티브 컴파일)
4. ✅ ZIP 압축 및 SHA256 해시 생성
5. ✅ Git `latest` 태그 생성 및 푸시
6. ✅ GitHub Release 생성 및 ZIP 업로드

**Requirements:**

- Python 3.12+
- Flet (`pip install flet`)
- Flutter SDK (<https://docs.flutter.dev/get-started/install/windows>)
- uv (`pip install uv` 또는 <https://github.com/astral-sh/uv>)
- GitHub CLI (`gh`) 설치: <https://cli.github.com/>

**주요 특징:**

- 🟢 **낮은 오탐률**: 네이티브 컴파일로 바이러스 오탐 최소화
- 📦 **ZIP 배포**: `PrivacyEraser-v2.0.0-win-x64.zip`
- 🔒 **SHA256 해시**: 무결성 검증 파일 포함
- 🏷️ **`latest` 태그**: 항상 최신 릴리스를 가리킴
- 🚀 **Flutter 기반**: Material Design 3 UI, 빠른 실행 속도

### 수동 빌드만 하기

빌드만 필요한 경우:

```bash
# Flutter 빌드 (권장) - exclude 옵션으로 크기 최적화
uv run flet build windows --exclude test_data .git .venv references .claude .coverage

# PyInstaller 빌드 (오탐 위험)
uv run flet pack main.py --name "PrivacyEraser" --add-data "static/images;static/images"
```

### 빌드 크기 최적화

**문제**: 기본 빌드는 불필요한 파일을 포함하여 크기가 큼 (1.2GB+)

**해결 방법**:

#### 1. pyproject.toml 설정 (권장)

**앱 패키징 제외 설정** (app.zip에서 제외):
```toml
[tool.flet.app]
exclude = [
    ".venv/**/*",
    "venv/**/*",
    "__pycache__/**/*",
    "*.pyc",
    "*.pyo",
    ".git/**/*",
    "references/**/*",
    ".claude/**/*",
    "test_data/**/*",
    "tests/**/*",
    ".coverage",
    ".pytest_cache/**/*",
]
```

**소스 패키징 제외 설정**:
```toml
[tool.flet]
exclude = [
    "test_data",
    ".git",
    ".venv",
    "references",
    ".claude",
    ".coverage",
]
```

#### 2. 빌드 스크립트 최적화

`scripts/release_flutter.bat`에서 자동으로 다음을 수행:
- src/.venv 존재 여부 확인 (있으면 빌드 실패)
- 빌드 후 app.zip 크기 검증 (100MB 초과 시 경고)

#### 3. 예상 크기

- **최적화 전**: ~1.2GB (app.zip에 .venv 포함)
- **최적화 후**: ~70-100MB
  - Flutter 엔진: ~30MB
  - libmpv-2.dll: ~28MB (미디어 지원, 제거 불가)
  - Python 런타임: ~15MB
  - 앱 코드 + 의존성: ~5-20MB

#### 4. FAQ: .venv 제외해도 의존성이 포함되나요?

**A: 네, 정상적으로 포함됩니다!**

**작동 원리:**
1. `flet build`는 `pyproject.toml`의 `[project.dependencies]`를 **직접 읽습니다**
2. 필요한 패키지들을 **독립적으로 수집**하여 번들에 포함합니다
3. `.venv`는 개발 환경일 뿐, 빌드 시에는 참조되지 않습니다

**빌드 흐름:**
```
uv sync (개발 환경 의존성 설치)
    ↓
flet build windows (pyproject.toml 읽기)
    ↓
의존성 독립적으로 수집 (NOT from .venv)
    ↓
앱 번들에 포함
```

**`--exclude ".venv"`의 의미:**
- **소스 코드** 패키징 시 `.venv` 폴더를 제외
- 의존성 번들링과는 무관
- 크기만 줄이고 기능은 동일

#### 5. 빌드 검증 방법

```bash
# app.zip 크기 확인
dir build\windows\data\flutter_assets\app.zip

# app.zip 내용 확인
tar -tzf build\windows\data\flutter_assets\app.zip | findstr ".venv"
# (아무것도 출력되지 않으면 성공)
```

**주의**: `test_data/` 폴더가 src/에 있으면 크기가 크게 증가합니다. 빌드 전에 삭제하거나 exclude 옵션을 사용하세요.

---

## 🧹 BleachBit 통합 및 참조 전략

Privacy Eraser는 BleachBit의 CleanerML 파일과 코어 삭제 로직을 활용합니다.

### BleachBit 소스코드 참조

**위치**: `references/bleachbit/` (참조용, 커밋하지 않음)

```bash
# BleachBit 소스코드 가져오기
git clone https://github.com/bleachbit/bleachbit references/bleachbit
cd references/bleachbit
rm -rf .git  # Git 히스토리 제거
```

**⚠️ 중요**:
- `references/bleachbit/` 폴더는 `.gitignore`에 추가되어 있습니다
- 이 폴더는 참조용으로만 사용하며, 커밋하지 않습니다
- 필요한 파일만 `src/privacy_eraser/` 안에 복사해서 사용합니다
- **빌드 시 포함되지 않음**: src/ 밖에 있어 빌드 사이즈에 영향 없음 (8.3MB 절약)

### 복사된 BleachBit 리소스

#### 1. CleanerML 파일 (브라우저 삭제 규칙)

**위치**: `src/privacy_eraser/cleaners/`

**복사된 파일**:
- `google_chrome.xml` - Chrome, Whale용
- `microsoft_edge.xml` - Edge용
- `firefox.xml` - Firefox용
- `brave.xml` - Brave용
- `opera.xml` - Opera용
- `safari.xml` - Safari용

**경로 설정**: `src/privacy_eraser/ui/core/data_config.py`
```python
CLEANER_XML_MAP = {
    "chrome": _get_cleaner_xml_path("google_chrome.xml"),
    "edge": _get_cleaner_xml_path("microsoft_edge.xml"),
    "firefox": _get_cleaner_xml_path("firefox.xml"),
    "brave": _get_cleaner_xml_path("brave.xml"),
    "opera": _get_cleaner_xml_path("opera.xml"),
    "whale": _get_cleaner_xml_path("google_chrome.xml"),  # Chromium 기반
    "safari": _get_cleaner_xml_path("safari.xml"),
}
```

#### 2. CleanerML Loader (XML 파싱)

**위치**: `src/privacy_eraser/cleanerml_loader.py`

BleachBit의 CleanerML 파서를 경량화하여 복사:
- `load_cleaner_options_from_file(pathname)` - XML 파일을 파싱하여 CleanerOption 리스트 반환
- OS 매칭, 변수 확장, 액션 파싱 기능 포함

#### 3. Cleaning Engine (삭제 로직)

**위치**: `src/privacy_eraser/cleaning.py` (레거시 래퍼)

BleachBit의 삭제 엔진을 래핑:
- `DeleteAction` - 파일/폴더 삭제 액션
- `CleanerOption` - 삭제 옵션 그룹
- `iter_search()` - 파일 검색 헬퍼

### 새 브라우저 추가 방법

1. **BleachBit에서 CleanerML 파일 확인**
   ```bash
   # references/bleachbit/cleaners/ 에서 찾기
   ls references/bleachbit/cleaners/ | grep <browser_name>
   ```

2. **CleanerML 파일 복사**
   ```bash
   cp references/bleachbit/cleaners/<browser_name>.xml src/privacy_eraser/cleaners/
   ```

3. **data_config.py 업데이트**
   ```python
   CLEANER_XML_MAP = {
       # ...
       "<browser_name>": _get_cleaner_xml_path("<browser_name>.xml"),
   }
   ```

### 커스텀 브라우저 XML 작성

Whale처럼 BleachBit에 없는 브라우저는 Chromium 기반 XML을 재사용하거나, 직접 작성할 수 있습니다.

**CleanerML 형식 예시**:
```xml
<cleaner id="whale" os="windows">
  <label>Naver Whale</label>
  <description>Delete Whale browser data</description>

  <option id="cache">
    <label>Cache</label>
    <description>Delete cache files</description>
    <action command="delete" search="walk.files"
            path="%LocalAppData%\Naver\Naver Whale\User Data\Default\Cache"/>
  </option>
</cleaner>
```

### BleachBit 업데이트 시

1. `references/bleachbit/` 폴더 삭제
2. 최신 BleachBit 클론: `git clone https://github.com/bleachbit/bleachbit references/bleachbit`
3. 필요한 XML 파일 재복사
4. 테스트 실행하여 호환성 확인

---

## 🔧 개발 관련 명령어

### Flet UI 실행

```bash
# Flet UI 실행
python -m privacy_eraser.ui.main

# 또는 엔트리포인트 사용
privacy_eraser
privacy_eraser_poc
```

### 의존성 설치

```bash
# uv 사용
uv sync

# 또는 pip 사용
pip install -e .

# 빌드 의존성 포함
uv sync --extra build
# 또는
pip install -e .[build]
```

### 테스트 실행

```bash
# 전체 테스트
pytest

# 커버리지 포함
pytest --cov=privacy_eraser
```

---

## 🎯 Claude Code에게 명령하기

POC 애플리케이션 실행:

```
Flet POC 실행해줘
```

---

## 📝 작업 히스토리

### v2.0.0 (2025-10-21) - Flet UI Migration

- **완전한 UI 프레임워크 전환**: PySide6 → Flet (Flutter for Python)
- **Material Design 3 적용**: 모던하고 세련된 UI
- **한국어 현지화**: 모든 UI 요소 한국어로 변경
- **새로운 기능 추가**:
  - 다운로드 폴더 파일 삭제 옵션 (체크박스)
  - 예약 실행 설정 UI (시간/반복 설정)
  - 클릭 가능한 개발자 링크 (seolcoding.com)
- **브라우저 지원 업데이트**: Chrome, Edge, Firefox, Brave, Opera, Whale, Safari
- **2x4 그리드 레이아웃**: 실제 브라우저 로고 이미지 사용
- **Flet 빌드 스크립트**: scripts/build_flet.bat, scripts/release.bat

### v1.0.0 (2025-10-21) - Initial Release

- 초기 PySide6 기반 릴리즈
- 기본 브라우저 데이터 삭제 기능
- 백업 및 복원 기능
- PyInstaller 빌드 스크립트

---

## 🛠️ 트러블슈팅

### Flet Pack 빌드 실패

- **Flet 설치 확인**: `pip install flet`
- **uv 설치 확인**: `pip install uv` 또는 <https://github.com/astral-sh/uv>
- **Python 버전 확인**: Python 3.12+ 필요
- **빌드 경로 확인**: `dist/PrivacyEraser.exe` (단일 파일)
- **이미지 포함 확인**: `--add-data "static/images;static/images"` 옵션 포함

### 릴리즈 스크립트 오류

- **gh CLI가 없는 경우**: <https://cli.github.com/> 에서 설치
- **`latest` 태그 충돌**: 스크립트가 자동으로 삭제 후 재생성 (--force)
- **gh 인증 실패**: `gh auth login` 으로 GitHub 계정 로그인
- **이전 릴리즈 덮어쓰기**: `latest` 릴리스 자동 삭제 후 재생성

### 의존성 설치 오류

- `uv sync` 실행하여 모든 의존성 설치
- Python 버전 확인: Python 3.12+ 필요

### 한글 깨짐

- Windows 콘솔: `chcp 65001` 실행
- logger 설정: encoding 파라미터 제거 (loguru 기본 사용)
- uv로 항상 실행

### 빌드된 앱에서 이미지 안보임

- `get_resource_path()` 함수 사용 확인 (PyInstaller 경로 처리)
- `--add-data` 옵션으로 이미지 포함 확인
- `static/images/` 폴더 존재 여부 확인
