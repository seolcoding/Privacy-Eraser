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

## 🚀 빌드 & 릴리즈 프로세스 (Flet)

### 자동 빌드 & 릴리즈 (권장 ⭐)

**`scripts/release.bat`** 스크립트를 사용하면 빌드부터 릴리즈까지 자동화됩니다.

#### 사용법

```bash
# 버전을 인자로 전달
scripts\release.bat 2.0.0

# 또는 실행 후 버전 입력
scripts\release.bat
```

#### 스크립트가 자동으로 수행하는 작업

1. ✅ 버전 입력 (또는 인자로 전달)
2. ✅ 의존성 확인 (Python, Flet, gh CLI)
3. ✅ Flet 빌드 실행
4. ✅ Git 태그 생성 및 푸시
5. ✅ GitHub Release 생성 및 EXE 업로드

**Requirements:**
- Python 3.12+
- Flet (`pip install flet`)
- GitHub CLI (`gh`) 설치: https://cli.github.com/

---

### 수동 빌드만 하기

빌드만 필요한 경우:

```bash
# Flet 빌드 실행
scripts\build_flet.bat

# 또는 직접 Flet 명령어 실행
flet build windows
```

---

## 🔧 개발 관련 명령어

### POC 개발 서버 실행

```bash
# Flet POC 실행
python -m privacy_eraser.poc.flet_main

# 또는 엔트리포인트 사용
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

### Flet 빌드 실패
- Flet 설치 확인: `pip install flet`
- Python 버전 확인: Python 3.12+ 필요
- 빌드 경로 확인: `build/windows/PrivacyEraser.exe`

### 릴리즈 스크립트 오류
- **gh CLI가 없는 경우**: https://cli.github.com/ 에서 설치
- **태그가 이미 존재**: 스크립트가 자동으로 덮어쓰기 여부 물어봄
- **gh 인증 실패**: `gh auth login` 으로 GitHub 계정 로그인

### 의존성 설치 오류
- `uv sync` 실행하여 모든 의존성 설치
- Python 버전 확인: Python 3.12+ 필요

### 한글 깨짐
- Windows 콘솔: `chcp 65001` 실행
- logger 설정: encoding 파라미터 제거 (loguru 기본 사용)
- uv로 항상 실행

### Flet 앱 실행 오류
- 이미지 파일 경로 확인: `static/images/` 폴더 존재 여부
- 브라우저 로고 파일 확인: chrome.png, edge.png 등