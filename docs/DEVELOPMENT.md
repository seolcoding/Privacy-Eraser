# Privacy Eraser - Development Guide

개발 가이드 및 BleachBit 통합 전략입니다.

---

## 🧹 BleachBit 통합 전략

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

---

## 🆕 새 브라우저 추가 방법

### 1. BleachBit에서 CleanerML 파일 확인

```bash
# references/bleachbit/cleaners/ 에서 찾기
ls references/bleachbit/cleaners/ | grep <browser_name>
```

### 2. CleanerML 파일 복사

```bash
cp references/bleachbit/cleaners/<browser_name>.xml src/privacy_eraser/cleaners/
```

### 3. data_config.py 업데이트

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

## 🔧 개발 명령어

### 앱 실행

```bash
# Flet UI 실행
python -m privacy_eraser.ui.main

# 또는 엔트리포인트 사용
privacy_eraser
```

### 의존성 관리

```bash
# uv 사용 (권장)
uv sync

# 또는 pip 사용
pip install -e .

# 빌드 의존성 포함
uv sync --extra build
```

### 테스트

```bash
# 전체 테스트
uv run pytest

# 커버리지 포함
uv run pytest --cov=privacy_eraser

# 특정 테스트만
uv run pytest tests/test_cleaning.py
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

### 의존성 설치 오류

- `uv sync` 실행하여 모든 의존성 설치
- Python 버전 확인: Python 3.12+ 필요

### 한글 깨짐

- Windows 콘솔: `chcp 65001` 실행
- logger 설정: encoding 파라미터 제거 (loguru 기본 사용)
- uv로 항상 실행

### DEV 모드

DEV 모드에서는 실제 파일이 삭제되지 않고 `test_data/` 디렉토리의 더미 파일만 삭제됩니다.

**활성화 방법**:
```python
# config.py
AppConfig.set_dev_mode(True)

# 또는 환경변수
export PRIVACY_ERASER_DEV_MODE=true  # Linux/Mac
set PRIVACY_ERASER_DEV_MODE=true  # Windows
```

**확인 방법**:
```python
from privacy_eraser.config import AppConfig
print(f"DEV 모드: {AppConfig.is_dev_mode()}")
```

---

## 📚 참고 문서

- **아키텍처**: `ai-docs/context/architecture.md`
- **테스트**: `ai-docs/context/testing.md`
- **Flet 가이드**: `ai-docs/flet.md`
- **빌드**: `docs/BUILD.md`
- **TODO**: `docs/TODO.md`
