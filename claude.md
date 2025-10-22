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
# Flutter 빌드 (권장)
uv run flet build windows

# PyInstaller 빌드 (오탐 위험)
uv run flet pack main.py --name "PrivacyEraser" --add-data "static/images;static/images"
```

---

## 🧹 BleachBit 통합 및 참조 전략

Privacy Eraser는 BleachBit의 CleanerML 파일과 코어 삭제 로직을 활용합니다.

### BleachBit 소스코드 참조

**위치**: `src/bleachbit/` (참조용, 커밋하지 않음)

```bash
# BleachBit 소스코드 가져오기
cd src
git clone https://github.com/bleachbit/bleachbit
cd bleachbit
rm -rf .git  # Git 히스토리 제거
```

**⚠️ 중요**:
- `src/bleachbit/` 폴더는 `.gitignore`에 추가되어 있습니다
- 이 폴더는 참조용으로만 사용하며, 커밋하지 않습니다
- 필요한 파일만 `src/privacy_eraser/` 안에 복사해서 사용합니다

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
   # src/bleachbit/cleaners/ 에서 찾기
   ls src/bleachbit/cleaners/ | grep <browser_name>
   ```

2. **CleanerML 파일 복사**
   ```bash
   cp src/bleachbit/cleaners/<browser_name>.xml src/privacy_eraser/cleaners/
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

1. `src/bleachbit/` 폴더 삭제
2. 최신 BleachBit 클론
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
