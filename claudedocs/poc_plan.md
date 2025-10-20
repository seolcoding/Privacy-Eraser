# Privacy Eraser POC - 상세 설계 문서

## 📋 프로젝트 개요

### 목표
심사위원 시연용 **극도로 단순한 원클릭 개인정보 삭제 프로그램** 개발
- **핵심 가치**: 시각적 임팩트 최대화 (파일 삭제 과정의 실시간 시각화)
- **사용자 경험**: 한 번의 클릭으로 모든 브라우저의 개인정보 삭제
- **신뢰성**: 기존 BleachBit 기반 코어 로직 재사용으로 안정성 확보

### 핵심 원칙
1. **극도의 단순함**: 설정 화면 없음, 최소한의 UI 요소
2. **시각적 피드백**: 삭제되는 모든 파일을 실시간으로 표시
3. **신뢰감**: Material Design + 프로페셔널한 애니메이션
4. **속도**: 빠른 시작 시간, 반응성 있는 UI

---

## 🎨 UI 와이어프레임

### 메인 윈도우 (800x700px)

```
┌─────────────────────────────────────────────────────────────┐
│  🛡️  Privacy Eraser POC                            [_][□][×] │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  감지된 브라우저를 선택하세요                                      │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   🌐 Chrome │  │   🌐 Edge   │  │  🦊 Firefox │          │
│  │             │  │             │  │             │          │
│  │     [✓]     │  │     [ ]     │  │     [✓]     │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │  🦁 Brave   │  │   🅾️ Opera  │  │   🐋 Whale  │          │
│  │             │  │             │  │             │          │
│  │     [✓]     │  │     [ ]     │  │     [✓]     │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐                           │
│  │ 🎨 Vivaldi  │  │ (미감지)     │                           │
│  │             │  │             │                           │
│  │     [✓]     │  │             │                           │
│  └─────────────┘  └─────────────┘                           │
│                                                               │
│                                                               │
│  옵션                                                          │
│  ┌─────────────────────────────────────────────────────┐     │
│  │ 북마크도 삭제하기  [────○]  (기본: 유지)               │     │
│  └─────────────────────────────────────────────────────┘     │
│                                                               │
│  삭제 대상: 로그인 데이터, 히스토리, 쿠키, 세션, 비밀번호             │
│                                                               │
│              ┌─────────────────────────┐                     │
│              │  🗑️  개인정보 지우기     │                     │
│              └─────────────────────────┘                     │
│                    (Primary Button)                          │
└─────────────────────────────────────────────────────────────┘
```

### 삭제 진행 팝업 (600x500px)

```
┌─────────────────────────────────────────────────┐
│  개인정보 삭제 중...                     [×]     │
├─────────────────────────────────────────────────┤
│                                                 │
│  💚 개인정보가 안전하게 삭제되고 있습니다            │
│                                                 │
│  삭제된 파일: 1,247 / 1,850                      │
│  삭제된 용량: 124.5 MB / 189.2 MB                │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ ████████████████░░░░░░░░░ 67%          │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  삭제 중인 파일들:                               │
│  ┌─────────────────────────────────────────┐   │
│  │ C:\Users\...\Chrome\Cache\f_000123      │   │
│  │ C:\Users\...\Chrome\Cache\f_000124      │   │
│  │ C:\Users\...\Chrome\Cookies              │   │
│  │ C:\Users\...\Chrome\History              │   │
│  │ C:\Users\...\Firefox\cache2\entries\...  │   │
│  │ C:\Users\...\Firefox\cookies.sqlite      │   │
│  │ C:\Users\...\Brave\Session Storage\...   │   │
│  │ ... (스크롤 리스트)                        │   │
│  │                                          │   │
│  │                                          │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  현재: C:\Users\...\Chrome\Cache\f_000125       │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 🎨 Material Design 스펙

### 색상 팔레트

```python
# Primary Colors
PRIMARY = "#5E35B1"           # Deep Purple 600
PRIMARY_LIGHT = "#9162E4"     # Deep Purple 300
PRIMARY_DARK = "#280680"      # Deep Purple 900

# Secondary Colors
SECONDARY = "#00BFA5"         # Teal A700
SECONDARY_LIGHT = "#5DF2D6"   # Teal A200
SECONDARY_DARK = "#008E76"    # Teal A900

# Background & Surface
BACKGROUND = "#FAFAFA"        # Grey 50
SURFACE = "#FFFFFF"           # White
SURFACE_VARIANT = "#F5F5F5"   # Grey 100

# Text Colors
TEXT_PRIMARY = "#212121"      # Grey 900
TEXT_SECONDARY = "#757575"    # Grey 600
TEXT_HINT = "#BDBDBD"         # Grey 400

# Status Colors
SUCCESS = "#4CAF50"           # Green 500
WARNING = "#FF9800"           # Orange 500
ERROR = "#F44336"             # Red 500

# Card Shadow
SHADOW_1 = "rgba(0, 0, 0, 0.05)"  # Elevation 1
SHADOW_2 = "rgba(0, 0, 0, 0.10)"  # Elevation 2
SHADOW_4 = "rgba(0, 0, 0, 0.15)"  # Elevation 4
```

### 타이포그래피

```python
# Font Family
FONT_FAMILY = "Segoe UI, Roboto, sans-serif"

# Font Sizes
TITLE = 24          # Main window title
HEADING = 18        # Section headings
BODY = 14           # Normal text
CAPTION = 12        # Secondary info
BUTTON = 16         # Button text (uppercase)

# Font Weights
WEIGHT_LIGHT = 300
WEIGHT_REGULAR = 400
WEIGHT_MEDIUM = 500
WEIGHT_BOLD = 700

# Line Heights
LINE_HEIGHT_TIGHT = 1.2
LINE_HEIGHT_NORMAL = 1.5
LINE_HEIGHT_LOOSE = 1.8
```

### Spacing System

```python
# Based on 8px grid
SPACING_XS = 4
SPACING_SM = 8
SPACING_MD = 16
SPACING_LG = 24
SPACING_XL = 32
SPACING_XXL = 48

# Card & Component Sizes
CARD_WIDTH = 150
CARD_HEIGHT = 180
CARD_RADIUS = 12
BUTTON_HEIGHT = 48
BUTTON_RADIUS = 24
INPUT_HEIGHT = 40
```

### Elevation (그림자)

```css
/* Elevation Level 1 - 브라우저 카드 (기본 상태) */
box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);

/* Elevation Level 2 - 브라우저 카드 (호버 상태) */
box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);

/* Elevation Level 4 - 메인 버튼 */
box-shadow: 0 10px 20px rgba(0,0,0,0.19), 0 6px 6px rgba(0,0,0,0.23);

/* Elevation Level 8 - 팝업 다이얼로그 */
box-shadow: 0 19px 38px rgba(0,0,0,0.30), 0 15px 12px rgba(0,0,0,0.22);
```

### 애니메이션 타이밍

```python
# Duration (milliseconds)
DURATION_FAST = 150        # 버튼 호버, 체크박스 토글
DURATION_NORMAL = 250      # 카드 호버, 페이드인
DURATION_SLOW = 400        # 다이얼로그 오픈/클로즈
DURATION_VERY_SLOW = 800   # 페이지 전환

# Easing Functions
EASE_STANDARD = "cubic-bezier(0.4, 0.0, 0.2, 1)"      # 표준 전환
EASE_DECELERATE = "cubic-bezier(0.0, 0.0, 0.2, 1)"   # 시작 빠름
EASE_ACCELERATE = "cubic-bezier(0.4, 0.0, 1, 1)"     # 끝 빠름
EASE_BOUNCE = "cubic-bezier(0.68, -0.55, 0.265, 1.55)"  # 바운스 효과
```

---

## 🧩 컴포넌트 상세 명세

### 1. 메인 윈도우 (MainWindow)

**파일**: `src/privacy_eraser/poc/ui/main_window.py`

#### 책임
- 브라우저 감지 및 카드 그리드 렌더링
- 북마크 토글 상태 관리
- 삭제 버튼 클릭 시 워커 스레드 시작 및 진행 팝업 표시

#### 속성
```python
class MainWindow(QMainWindow):
    def __init__(self):
        self.detected_browsers: List[BrowserInfo] = []
        self.browser_cards: Dict[str, BrowserCard] = {}
        self.delete_bookmarks: bool = False
        self.cleaner_worker: Optional[CleanerWorker] = None
        self.progress_dialog: Optional[ProgressDialog] = None
```

#### 메서드
```python
def setup_ui(self) -> None:
    """UI 레이아웃 초기화"""

def detect_browsers(self) -> None:
    """브라우저 감지 (별도 스레드)"""

def on_browsers_detected(self, browsers: List[BrowserInfo]) -> None:
    """브라우저 감지 완료 시 UI 업데이트"""

def on_clean_clicked(self) -> None:
    """삭제 버튼 클릭 핸들러"""

def start_cleaning(self, selected_browsers: List[str]) -> None:
    """워커 스레드 시작 및 진행 팝업 표시"""

def on_cleaning_finished(self, stats: CleaningStats) -> None:
    """삭제 완료 시 결과 표시"""
```

#### 레이아웃
- QVBoxLayout (메인 레이아웃)
  - QLabel (제목: "감지된 브라우저를 선택하세요")
  - QGridLayout (브라우저 카드 그리드, 3열)
  - QWidget (옵션 영역)
    - QHBoxLayout
      - QLabel ("북마크도 삭제하기")
      - QCheckBox (북마크 토글)
  - QLabel (삭제 대상 안내 텍스트)
  - QPushButton (메인 삭제 버튼)

---

### 2. 브라우저 카드 (BrowserCard)

**파일**: `src/privacy_eraser/poc/ui/browser_card.py`

#### 책임
- 브라우저 아이콘 + 이름 + 체크박스 표시
- 호버 효과 (Elevation 1 → 2)
- 선택 상태 관리

#### 속성
```python
class BrowserCard(QWidget):
    # 시그널
    selection_changed = Signal(str, bool)  # (browser_name, is_selected)

    def __init__(self, browser_info: BrowserInfo):
        self.browser_info: BrowserInfo = browser_info
        self.is_selected: bool = True  # 기본: 모두 선택
        self.is_hovered: bool = False
```

#### 메서드
```python
def setup_ui(self) -> None:
    """카드 UI 초기화"""

def enterEvent(self, event: QEvent) -> None:
    """마우스 호버 시 그림자 증가"""

def leaveEvent(self, event: QEvent) -> None:
    """마우스 떠날 때 그림자 복원"""

def on_checkbox_toggled(self, checked: bool) -> None:
    """체크박스 토글 시 시그널 발생"""
```

#### 스타일
```css
/* 기본 상태 */
BrowserCard {
    background-color: #FFFFFF;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.12);
}

/* 호버 상태 */
BrowserCard:hover {
    box-shadow: 0 3px 6px rgba(0,0,0,0.16);
    transform: translateY(-2px);
    transition: all 250ms cubic-bezier(0.4, 0.0, 0.2, 1);
}

/* 선택 상태 */
BrowserCard[selected=true] {
    border: 2px solid #5E35B1;
}
```

#### 아이콘 매핑
```python
BROWSER_ICONS = {
    "chrome": "🌐",
    "edge": "🌐",
    "firefox": "🦊",
    "brave": "🦁",
    "opera": "🅾️",
    "whale": "🐋",
    "vivaldi": "🎨",
    "librewolf": "🦊",
}

BROWSER_COLORS = {
    "chrome": "#4285F4",
    "edge": "#0078D4",
    "firefox": "#FF7139",
    "brave": "#FB542B",
    "opera": "#FF1B2D",
    "whale": "#3B5998",
    "vivaldi": "#EF3939",
    "librewolf": "#00539F",
}
```

---

### 3. 삭제 진행 팝업 (ProgressDialog)

**파일**: `src/privacy_eraser/poc/ui/progress_dialog.py`

#### 책임
- 실시간 파일 삭제 리스트 표시 (모든 파일 경로)
- 프로그레스 바 업데이트
- 카운터 애니메이션 (삭제된 파일/용량)
- 상태 메시지 표시

#### 속성
```python
class ProgressDialog(QDialog):
    def __init__(self, total_files: int, total_size: int):
        self.total_files: int = total_files
        self.total_size: int = total_size
        self.deleted_files: int = 0
        self.deleted_size: int = 0

        # UI 요소
        self.status_label: QLabel
        self.counter_label: QLabel
        self.size_label: QLabel
        self.progress_bar: QProgressBar
        self.file_list: QListWidget
        self.current_file_label: QLabel
```

#### 메서드
```python
def setup_ui(self) -> None:
    """팝업 UI 초기화"""

def update_progress(self, file_path: str, file_size: int) -> None:
    """파일 삭제 시 실시간 업데이트"""

def add_file_to_list(self, file_path: str) -> None:
    """리스트에 파일 경로 추가 (페이드인 애니메이션)"""

def animate_counter(self, target_count: int) -> None:
    """카운터 숫자 증가 애니메이션"""

def on_finished(self, success: bool, error: Optional[str]) -> None:
    """삭제 완료 시 처리"""
```

#### 레이아웃
- QVBoxLayout
  - QLabel (상태 메시지: "💚 개인정보가 안전하게...")
  - QLabel (카운터: "삭제된 파일: X / Y")
  - QLabel (용량: "삭제된 용량: X MB / Y MB")
  - QProgressBar (진행률)
  - QLabel ("삭제 중인 파일들:")
  - QListWidget (파일 리스트, 자동 스크롤)
  - QLabel (현재 파일: "현재: ...")

#### 애니메이션
```python
# 파일 추가 시 페이드인 애니메이션
def add_file_with_animation(self, file_path: str) -> None:
    item = QListWidgetItem(file_path)
    self.file_list.addItem(item)

    # 페이드인 효과
    opacity_effect = QGraphicsOpacityEffect()
    item.setData(Qt.UserRole, opacity_effect)

    animation = QPropertyAnimation(opacity_effect, b"opacity")
    animation.setDuration(250)
    animation.setStartValue(0.0)
    animation.setEndValue(1.0)
    animation.setEasingCurve(QEasingCurve.OutCubic)
    animation.start()

    # 자동 스크롤
    self.file_list.scrollToBottom()
```

---

## 🔄 데이터 플로우

### 브라우저 감지 플로우

```
MainWindow.__init__()
    ↓
detect_browsers() (별도 스레드)
    ↓
DetectorWorker.run()
    → detect_windows.detect_browsers()
    → BrowserInfo 리스트 생성
    ↓
signal: browsers_detected(List[BrowserInfo])
    ↓
on_browsers_detected()
    → BrowserCard 생성
    → 그리드에 추가
    → 애니메이션 적용
```

### 삭제 프로세스 플로우

```
on_clean_clicked()
    ↓
선택된 브라우저 검증
    ↓
ProgressDialog 생성 및 표시
    ↓
CleanerWorker 스레드 시작
    ↓
┌───────────────────────────────────┐
│ CleanerWorker.run() (별도 스레드)   │
│                                   │
│ 1. 브라우저별 삭제 대상 파일 수집    │
│    → CleanerML 파싱               │
│    → 경로 확장 (%LOCALAPPDATA% 등) │
│    → 북마크 필터링 (옵션에 따라)     │
│                                   │
│ 2. 파일 삭제 시작                  │
│    for each file:                │
│        → file_utils.safe_delete() │
│        → signal: progress_updated │
│            (file_path, file_size) │
│                                   │
│ 3. 완료                           │
│    → signal: cleaning_finished   │
│       (CleaningStats)            │
└───────────────────────────────────┘
    ↓
ProgressDialog.update_progress()
    → 리스트에 파일 추가 (애니메이션)
    → 카운터 업데이트
    → 프로그레스 바 업데이트
    ↓
cleaning_finished()
    → 결과 다이얼로그 표시
    → 통계 정보 (삭제된 파일/용량)
```

### Qt Signal/Slot 연결

```python
# 브라우저 감지
detector_worker.browsers_detected.connect(self.on_browsers_detected)

# 브라우저 카드 선택
browser_card.selection_changed.connect(self.on_browser_selection_changed)

# 삭제 진행
cleaner_worker.progress_updated.connect(progress_dialog.update_progress)
cleaner_worker.cleaning_finished.connect(self.on_cleaning_finished)
```

---

## 🗑️ 삭제 대상 정의

### CleanerML 옵션 매핑

**파일**: `src/privacy_eraser/poc/core/data_config.py`

```python
# 기본 삭제 대상 (북마크 제외)
DEFAULT_CLEANER_OPTIONS = [
    "cache",           # 캐시 파일
    "cookies",         # 쿠키
    "history",         # 브라우징 히스토리
    "session",         # 세션 데이터
    "passwords",       # 저장된 비밀번호
    "form_history",    # 자동완성 데이터
]

# 북마크 옵션 (토글 활성화 시 추가)
BOOKMARK_OPTIONS = [
    "bookmarks",       # 북마크
    "favicons",        # 파비콘
]

# 제외할 옵션 (항상 보존)
EXCLUDE_OPTIONS = [
    "extensions",      # 확장 프로그램
    "settings",        # 브라우저 설정
]
```

### 브라우저별 CleanerML 파일 매핑

```python
CLEANER_XML_MAP = {
    "chrome": "bleachbit/cleaners/chrome.xml",
    "edge": "bleachbit/cleaners/chrome.xml",  # Chromium 기반
    "firefox": "bleachbit/cleaners/firefox.xml",
    "brave": "bleachbit/cleaners/brave.xml",
    "opera": "bleachbit/cleaners/opera.xml",
    "whale": "bleachbit/cleaners/chrome.xml",  # Chromium 기반
    "vivaldi": "bleachbit/cleaners/chrome.xml",  # Chromium 기반
    "librewolf": "bleachbit/cleaners/firefox.xml",  # Firefox 기반
}
```

---

## 🔧 코어 모듈 재사용 전략

### 1. 브라우저 감지 (`detect_windows.py`)

**재사용 방법**:
```python
from privacy_eraser.detect_windows import detect_browsers

# POC용 래퍼
def detect_browsers_for_poc() -> List[BrowserInfo]:
    """POC용으로 간소화된 브라우저 감지"""
    detected = detect_browsers()

    # BrowserInfo 변환
    return [
        BrowserInfo(
            name=browser["name"],
            icon=BROWSER_ICONS.get(browser["name"].lower(), "🌐"),
            color=BROWSER_COLORS.get(browser["name"].lower(), "#666666"),
            installed=browser["present"] == "yes",
        )
        for browser in detected
    ]
```

### 2. 파일 삭제 (`core/file_utils.py`)

**재사용 방법**:
```python
from privacy_eraser.core.file_utils import safe_delete, calculate_size

class CleanerWorker(QThread):
    progress_updated = Signal(str, int)  # (file_path, file_size)

    def run(self):
        for file_path in files_to_delete:
            try:
                file_size = calculate_size(file_path)
                safe_delete(file_path)

                # UI 업데이트 시그널
                self.progress_updated.emit(file_path, file_size)

            except Exception as e:
                logger.warning(f"삭제 실패: {file_path} - {e}")
```

### 3. CleanerML 파싱 (`cleanerml_loader.py`)

**재사용 방법**:
```python
from privacy_eraser.cleanerml_loader import load_cleanerml

def get_files_to_delete(
    browser_name: str,
    options: List[str],
    delete_bookmarks: bool
) -> List[str]:
    """브라우저별 삭제 대상 파일 리스트 생성"""

    # CleanerML 로드
    xml_path = CLEANER_XML_MAP[browser_name.lower()]
    cleaner_def = load_cleanerml(xml_path)

    # 옵션 필터링
    if not delete_bookmarks:
        options = [opt for opt in options if opt not in BOOKMARK_OPTIONS]

    # 파일 경로 확장
    files = []
    for option in options:
        actions = cleaner_def.get_actions(option)
        for action in actions:
            expanded_paths = expand_path(action.path)
            files.extend(expanded_paths)

    return files
```

### 4. Windows 유틸리티 (`core/windows_utils.py`)

**재사용 방법**:
```python
from privacy_eraser.core.windows_utils import is_process_running

def check_browser_running(browser_name: str) -> bool:
    """브라우저 실행 여부 확인"""
    process_names = {
        "chrome": "chrome.exe",
        "edge": "msedge.exe",
        "firefox": "firefox.exe",
        # ...
    }

    process = process_names.get(browser_name.lower())
    if process:
        return is_process_running(process)
    return False
```

---

## 🧵 워커 스레드 구조

### CleanerWorker (QThread)

**파일**: `src/privacy_eraser/poc/core/poc_cleaner.py`

```python
from PySide6.QtCore import QThread, Signal
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class CleaningStats:
    """삭제 작업 통계"""
    total_files: int
    deleted_files: int
    failed_files: int
    total_size: int
    deleted_size: int
    duration: float  # seconds
    errors: List[str]

class CleanerWorker(QThread):
    """별도 스레드에서 파일 삭제 작업 수행"""

    # 시그널
    started = Signal()  # 작업 시작
    progress_updated = Signal(str, int)  # (file_path, file_size)
    cleaning_finished = Signal(CleaningStats)  # 작업 완료
    error_occurred = Signal(str)  # 에러 발생

    def __init__(
        self,
        browsers: List[str],
        delete_bookmarks: bool,
        parent=None
    ):
        super().__init__(parent)
        self.browsers = browsers
        self.delete_bookmarks = delete_bookmarks
        self.is_cancelled = False

    def run(self):
        """메인 삭제 로직"""
        self.started.emit()

        start_time = time.time()
        stats = CleaningStats(
            total_files=0,
            deleted_files=0,
            failed_files=0,
            total_size=0,
            deleted_size=0,
            duration=0,
            errors=[]
        )

        try:
            # 1. 삭제 대상 파일 수집
            all_files = []
            for browser in self.browsers:
                files = get_files_to_delete(
                    browser,
                    DEFAULT_CLEANER_OPTIONS,
                    self.delete_bookmarks
                )
                all_files.extend(files)

            stats.total_files = len(all_files)
            stats.total_size = sum(
                calculate_size(f) for f in all_files if os.path.exists(f)
            )

            # 2. 파일 삭제
            for file_path in all_files:
                if self.is_cancelled:
                    break

                try:
                    file_size = calculate_size(file_path) if os.path.exists(file_path) else 0
                    safe_delete(file_path)

                    stats.deleted_files += 1
                    stats.deleted_size += file_size

                    # UI 업데이트
                    self.progress_updated.emit(file_path, file_size)

                    # 너무 빠른 삭제는 시각적으로 보이지 않으므로 지연 추가
                    time.sleep(0.01)

                except Exception as e:
                    stats.failed_files += 1
                    stats.errors.append(f"{file_path}: {str(e)}")
                    logger.warning(f"삭제 실패: {file_path} - {e}")

            stats.duration = time.time() - start_time
            self.cleaning_finished.emit(stats)

        except Exception as e:
            self.error_occurred.emit(str(e))
            logger.error(f"삭제 작업 실패: {e}")

    def cancel(self):
        """작업 취소"""
        self.is_cancelled = True
```

---

## ✅ 테스트 계획

### 단위 테스트

**파일**: `tests/test_poc_ui.py`

```python
def test_browser_card_creation():
    """브라우저 카드 생성 테스트"""
    browser_info = BrowserInfo(
        name="Chrome",
        icon="🌐",
        color="#4285F4",
        installed=True
    )
    card = BrowserCard(browser_info)
    assert card.is_selected is True
    assert card.browser_info.name == "Chrome"

def test_browser_card_selection():
    """브라우저 카드 선택 테스트"""
    # ...

def test_progress_dialog_updates():
    """진행 팝업 업데이트 테스트"""
    # ...

def test_cleaner_worker(sandbox):
    """CleanerWorker 스레드 테스트"""
    # sandbox 환경에서 파일 생성
    # CleanerWorker 실행
    # 결과 검증
```

### 통합 테스트 (샌드박스)

```python
def test_full_cleaning_flow(sandbox, qtbot):
    """전체 삭제 플로우 테스트"""
    # 1. 메인 윈도우 생성
    window = MainWindow()
    window.show()
    qtbot.addWidget(window)

    # 2. 브라우저 감지 대기
    with qtbot.waitSignal(window.detector_worker.browsers_detected, timeout=5000):
        pass

    # 3. 브라우저 선택
    # ...

    # 4. 삭제 버튼 클릭
    qtbot.mouseClick(window.clean_button, Qt.LeftButton)

    # 5. 진행 팝업 표시 확인
    # ...

    # 6. 삭제 완료 대기
    with qtbot.waitSignal(window.cleaner_worker.cleaning_finished, timeout=30000):
        pass

    # 7. 결과 검증
    # ...
```

### 시각적 테스트 체크리스트

**수동 테스트 항목**:
- [ ] 브라우저 카드 호버 시 그림자 증가
- [ ] 브라우저 카드 클릭 시 체크박스 토글
- [ ] 북마크 토글 스위치 애니메이션
- [ ] 메인 버튼 호버 효과
- [ ] 진행 팝업 오픈 애니메이션
- [ ] 파일 리스트 실시간 업데이트 (페이드인)
- [ ] 프로그레스 바 부드러운 증가
- [ ] 카운터 숫자 증가 애니메이션
- [ ] 완료 다이얼로그 표시

---

## 📁 파일 구조

```
src/privacy_eraser/poc/
├── __init__.py
├── main.py                        # POC 진입점
│
├── ui/
│   ├── __init__.py
│   ├── main_window.py             # 메인 윈도우
│   ├── browser_card.py            # 브라우저 카드 위젯
│   ├── progress_dialog.py         # 삭제 진행 팝업
│   └── styles.py                  # Material Design 스타일시트
│
├── core/
│   ├── __init__.py
│   ├── poc_cleaner.py             # CleanerWorker 스레드
│   ├── data_config.py             # 삭제 대상 정의
│   └── browser_info.py            # BrowserInfo 데이터 클래스
│
└── tests/
    ├── __init__.py
    ├── test_poc_ui.py             # UI 컴포넌트 테스트
    └── test_poc_cleaner.py        # 코어 로직 테스트
```

### 의존성 다이어그램

```
main.py
    ↓
MainWindow ───────┬─→ BrowserCard (여러 개)
    │             │
    ├─→ DetectorWorker ─→ detect_windows.py (기존)
    │
    ├─→ ProgressDialog
    │       ↓
    └─→ CleanerWorker ─┬─→ file_utils.py (기존)
                        ├─→ cleanerml_loader.py (기존)
                        └─→ windows_utils.py (기존)
```

---

## 🛠️ 기술 스택

### 프레임워크 및 라이브러리
- **PySide6**: Qt6 Python 바인딩 (MIT 라이선스)
- **loguru**: 로깅
- **pytest**: 테스트 프레임워크
- **pytest-qt**: Qt 테스트 유틸리티

### 기존 모듈 재사용
- `detect_windows.py`: 브라우저 감지
- `core/file_utils.py`: 파일 삭제
- `core/windows_utils.py`: Windows 유틸리티
- `cleanerml_loader.py`: CleanerML 파싱
- `bleachbit/cleaners/*.xml`: 브라우저별 정의

### 새로 구현할 모듈
- `poc/ui/*`: Material Design UI 컴포넌트
- `poc/core/poc_cleaner.py`: 워커 스레드
- `poc/core/data_config.py`: POC용 설정

---

## 📝 구현 순서

### Phase 1: 기본 구조 (2시간)
1. 브랜치 생성: `feature/poc-redesign`
2. 디렉토리 구조 생성
3. `BrowserInfo` 데이터 클래스 작성
4. `data_config.py` 작성 (삭제 대상 정의)

### Phase 2: Material Design 스타일 (1시간)
1. `styles.py` 작성
   - 색상 팔레트
   - 타이포그래피
   - 애니메이션 타이밍
   - QSS 스타일시트

### Phase 3: UI 컴포넌트 (4시간)
1. `BrowserCard` 구현
   - 기본 레이아웃
   - 호버 효과
   - 선택 상태 관리
2. `MainWindow` 구현
   - 브라우저 카드 그리드
   - 북마크 토글
   - 메인 버튼
3. `ProgressDialog` 구현
   - 파일 리스트
   - 프로그레스 바
   - 카운터 애니메이션

### Phase 4: 코어 로직 통합 (3시간)
1. `CleanerWorker` 구현
   - 파일 수집
   - 삭제 로직
   - 시그널/슬롯 연결
2. 기존 모듈 래핑
   - 브라우저 감지 래퍼
   - 파일 삭제 래퍼

### Phase 5: 테스트 (2시간)
1. 단위 테스트 작성
2. 통합 테스트 작성
3. 샌드박스 테스트
4. 실제 데이터 테스트 (주의!)

### Phase 6: 마무리 (1시간)
1. 진입점 (`main.py`) 작성
2. `pyproject.toml` 업데이트
3. 문서화 (README, 사용법)
4. 커밋 및 PR

**총 예상 시간**: 13시간

---

## 🎯 핵심 목표 재확인

1. ✅ **극도의 단순함**: 설정 없음, 원클릭 삭제
2. ✅ **시각적 임팩트**: 실시간 파일 리스트, 애니메이션
3. ✅ **신뢰감**: Material Design, 프로페셔널 UI
4. ✅ **안정성**: 기존 검증된 코어 로직 재사용

---

## 📌 주의사항

1. **UI 스레드 블로킹 방지**: 모든 I/O 작업은 워커 스레드에서
2. **에러 핸들링**: 파일 삭제 실패 시에도 계속 진행
3. **테스트 격리**: 실제 브라우저 데이터 건드리지 않도록 샌드박스 사용
4. **성능**: 파일이 너무 빠르게 삭제되면 `time.sleep(0.01)` 추가
5. **접근성**: 키보드 네비게이션, 고대비 모드 지원

---

## 🚀 다음 단계

1. **브랜치 생성**: `git checkout -b feature/poc-redesign`
2. **디렉토리 구조 생성**: `mkdir -p src/privacy_eraser/poc/{ui,core,tests}`
3. **스타일시트 작성**: `styles.py` 먼저 구현
4. **컴포넌트 구현**: BrowserCard → MainWindow → ProgressDialog
5. **코어 통합**: CleanerWorker + 기존 모듈 연결
6. **테스트 및 검증**

**Let's build something amazing! 🎨**
