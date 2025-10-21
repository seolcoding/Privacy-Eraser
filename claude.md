# Claude Code - 프로젝트 작업 가이드

이 문서는 Claude Code와 함께 작업할 때 사용하는 명령어와 프로세스를 기록합니다.

## 📚 AI 개발 문서 참고 (중요!)

**라이브러리나 프레임워크 사용 시 반드시 `ai-docs/` 디렉토리의 문서를 참고하세요.**

### 주요 참고 문서

- **PySide6 UI 개발 시**: `ai-docs/pyside.md`, `ai-docs/pyside_examples.md` 필독
- **프로젝트 아키텍처 이해**: `ai-docs/context/architecture.md`
- **테스트 작성**: `ai-docs/context/testing.md`

### 사용 예시

```
# Claude Code에게 명령 시:
"PySide6로 설정 다이얼로그를 만들어줘 (ai-docs/pyside.md 참고)"
"새 기능 추가 시 프로젝트 구조 확인 (ai-docs/context/architecture.md 참고)"
```

**⚠️ 중요**:
- PySide6 코드 작성 전에는 **반드시** `ai-docs/pyside.md`를 먼저 읽으세요
- 예제가 필요하면 `ai-docs/pyside_examples.md`에서 유사한 코드를 찾으세요
- 새로운 라이브러리 도입 시 ai-docs에 문서를 추가하세요

## 🚀 빌드 & 릴리즈 프로세스

### 자동 빌드 & 릴리즈 (권장 ⭐)

**`scripts/release.bat`** 스크립트를 사용하면 빌드부터 릴리즈까지 자동화됩니다.

#### 사용법

```bash
# 버전을 인자로 전달
scripts\release.bat 1.0.2

# 또는 실행 후 버전 입력
scripts\release.bat
```

#### 스크립트가 자동으로 수행하는 작업

1. ✅ 버전 입력 (또는 인자로 전달)
2. ✅ 의존성 확인 (Python, gh CLI, PyInstaller)
3. ✅ 빌드 실행 (PyInstaller)
4. ✅ Git 태그 생성 및 푸시
5. ✅ GitHub Release 생성 및 EXE 업로드

**Requirements:**
- Python 3.12+
- GitHub CLI (`gh`) 설치: https://cli.github.com/

---

### 수동 빌드만 하기

빌드만 필요한 경우:

```bash
# EXE 빌드만 실행
scripts\build_exe.bat

# 또는 직접 PyInstaller 실행
python -m PyInstaller PrivacyEraser.spec
```

---

## 🔧 개발 관련 명령어

### POC 개발 서버 실행

```bash
# Hot reload 개발 서버
python dev_server.py

# 또는 직접 실행
python -m privacy_eraser.poc.main
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

다음번에 빌드 & 릴리즈가 필요할 때:

```
버전 1.0.2로 빌드하고 릴리즈해줘
```

또는

```
릴리즈 스크립트 실행해줘 (버전: 1.0.2)
```

Claude Code가 자동으로 `scripts/release.bat 1.0.2`를 실행하여:
1. ✅ 빌드 (PyInstaller)
2. ✅ 태그 생성 및 푸시
3. ✅ GitHub Release 생성 및 업로드

를 순차적으로 진행합니다.

---

## 📝 작업 히스토리

### v1.0.0 (2025-10-21)
- 초기 프로덕션 릴리즈
- 로컬 빌드 & 릴리즈 자동화 스크립트 (scripts/release.bat)
- 실행 취소 기능 구현
- 스크린샷 자동 캡처
- 한글 로그 출력 수정

---

## 🛠️ 트러블슈팅

### PyInstaller 빌드 실패
- PySide6가 설치되지 않은 경우: `pip install pyside6 qt-material qtawesome`
- 경로 문제: `SPECPATH` 사용 (PrivacyEraser.spec 참조)

### 릴리즈 스크립트 오류
- **gh CLI가 없는 경우**: https://cli.github.com/ 에서 설치
- **태그가 이미 존재**: `git tag -d v1.0.1 && git push origin :refs/tags/v1.0.1` 로 삭제 후 재시도
- **gh 인증 실패**: `gh auth login` 으로 GitHub 계정 로그인

### 한글 깨짐
- Windows 콘솔: `chcp 65001` 실행
- logger 설정: encoding 파라미터 제거 (loguru 기본 사용)
