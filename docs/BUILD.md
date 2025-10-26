# Privacy Eraser - Build & Release Guide

빌드 및 릴리즈 프로세스 가이드입니다.

---

## 🚀 빌드 방식 비교

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

## 자동 빌드 & 릴리즈 (권장 ⭐)

`scripts/release_flutter.bat` 스크립트를 사용하면 Flutter 빌드부터 GitHub 릴리즈까지 자동화됩니다.

### 사용법

```bash
# 버전을 인자로 전달
scripts\release_flutter.bat 2.0.1

# 또는 실행 후 버전 입력
scripts\release_flutter.bat
```

### 스크립트가 수행하는 작업

1. ✅ 버전 입력 (또는 인자로 전달)
2. ✅ 의존성 확인 (Python, Flet, Flutter SDK, gh CLI)
3. ✅ **Flutter 빌드** (Flet Build - 네이티브 컴파일)
4. ✅ ZIP 압축 및 SHA256 해시 생성
5. ✅ Git `latest` 태그 생성 및 푸시
6. ✅ GitHub Release 생성 및 ZIP 업로드

### Requirements

- Python 3.12+
- Flet (`pip install flet`)
- Flutter SDK (https://docs.flutter.dev/get-started/install/windows)
- uv (`pip install uv` 또는 https://github.com/astral-sh/uv)
- GitHub CLI (`gh`) 설치: https://cli.github.com/

### 주요 특징

- 🟢 **낮은 오탐률**: 네이티브 컴파일로 바이러스 오탐 최소화
- 📦 **ZIP 배포**: `PrivacyEraser-v2.0.0-win-x64.zip`
- 🔒 **SHA256 해시**: 무결성 검증 파일 포함
- 🏷️ **`latest` 태그**: 항상 최신 릴리스를 가리킴
- 🚀 **Flutter 기반**: Material Design 3 UI, 빠른 실행 속도

---

## 수동 빌드

빌드만 필요한 경우:

```bash
# Flutter 빌드 (권장) - exclude 옵션으로 크기 최적화
uv run flet build windows --exclude test_data .git .venv references .claude .coverage

# PyInstaller 빌드 (오탐 위험)
uv run flet pack main.py --name "PrivacyEraser" --add-data "static/images;static/images"
```

---

## 빌드 크기 최적화

**문제**: 기본 빌드는 불필요한 파일을 포함하여 크기가 큼 (1.2GB+)

### 1. pyproject.toml 설정 (권장)

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

### 2. 빌드 스크립트 최적화

`scripts/release_flutter.bat`에서 자동으로 다음을 수행:
- src/.venv 존재 여부 확인 (있으면 빌드 실패)
- 빌드 후 app.zip 크기 검증 (100MB 초과 시 경고)

### 3. 예상 크기

- **최적화 전**: ~1.2GB (app.zip에 .venv 포함)
- **최적화 후**: ~70-100MB
  - Flutter 엔진: ~30MB
  - libmpv-2.dll: ~28MB (미디어 지원, 제거 불가)
  - Python 런타임: ~15MB
  - 앱 코드 + 의존성: ~5-20MB

### 4. FAQ: .venv 제외해도 의존성이 포함되나요?

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

### 5. 빌드 검증 방법

```bash
# app.zip 크기 확인
dir build\windows\data\flutter_assets\app.zip

# app.zip 내용 확인
tar -tzf build\windows\data\flutter_assets\app.zip | findstr ".venv"
# (아무것도 출력되지 않으면 성공)
```

**주의**: `test_data/` 폴더가 src/에 있으면 크기가 크게 증가합니다. 빌드 전에 삭제하거나 exclude 옵션을 사용하세요.

---

## 트러블슈팅

### Flet Pack 빌드 실패

- **Flet 설치 확인**: `pip install flet`
- **uv 설치 확인**: `pip install uv` 또는 https://github.com/astral-sh/uv
- **Python 버전 확인**: Python 3.12+ 필요
- **빌드 경로 확인**: `dist/PrivacyEraser.exe` (단일 파일)
- **이미지 포함 확인**: `--add-data "static/images;static/images"` 옵션 포함

### 릴리즈 스크립트 오류

- **gh CLI가 없는 경우**: https://cli.github.com/ 에서 설치
- **`latest` 태그 충돌**: 스크립트가 자동으로 삭제 후 재생성 (--force)
- **gh 인증 실패**: `gh auth login` 으로 GitHub 계정 로그인
- **이전 릴리즈 덮어쓰기**: `latest` 릴리스 자동 삭제 후 재생성

### 빌드된 앱에서 이미지 안보임

- `get_resource_path()` 함수 사용 확인 (PyInstaller 경로 처리)
- `--add-data` 옵션으로 이미지 포함 확인
- `static/images/` 폴더 존재 여부 확인
