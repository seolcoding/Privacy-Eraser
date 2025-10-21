# Claude Code - 프로젝트 작업 가이드

이 문서는 Claude Code와 함께 작업할 때 사용하는 명령어와 프로세스를 기록합니다.

## 🚀 빌드 & 릴리즈 프로세스

### 로컬 빌드 후 수동 릴리즈 (권장)

빠르고 확실한 방법입니다. GitHub Actions보다 빠르며 빌드 결과를 즉시 확인할 수 있습니다.

#### 1단계: 로컬 빌드

```bash
# Windows 환경에서 EXE 빌드
python -m pip install pyinstaller pyside6 qt-material qtawesome loguru
rm -rf build dist
python -m PyInstaller PrivacyEraser.spec

# 빌드 결과 확인
ls -lh dist/PrivacyEraser.exe
```

**빌드 스크립트 사용 (옵션)**
```bash
# uv가 설치된 경우
scripts\build_exe.bat
```

#### 2단계: 버전 태그 생성

```bash
# 태그 생성 (예: v1.0.1)
git tag -a v1.0.1 -m "Release v1.0.1 - 설명"

# 태그 푸시
git push origin v1.0.1
```

#### 3단계: GitHub Release 생성 및 파일 업로드

```bash
gh release create v1.0.1 dist/PrivacyEraser.exe \
  --title "Privacy Eraser POC v1.0.1" \
  --notes "## Privacy Eraser POC v1.0.1

### 다운로드
- **Windows**: \`PrivacyEraser.exe\` (234MB)

### 주요 기능
- 🔍 자동 브라우저 감지 (Chrome, Edge, Firefox 등)
- 🗑️ 원클릭 개인정보 삭제 (캐시, 쿠키, 히스토리, 세션, 비밀번호)
- 📚 북마크/다운로드 삭제 옵션
- ↩️ 실행 취소 기능 (백업/복원)
- 🎨 Material Design UI

### 설치 방법
1. \`PrivacyEraser.exe\` 다운로드
2. Windows SmartScreen 경고 시 \"추가 정보\" → \"실행\" 클릭
3. 실행

### 시스템 요구사항
- Windows 10/11 (64-bit)

---

🤖 Built locally and released manually"
```

#### 단축 명령 (한 줄로 실행)

```bash
# 빌드 → 태그 → 릴리즈 (버전 수정 필요)
python -m PyInstaller PrivacyEraser.spec && \
  git tag -a v1.0.1 -m "Release v1.0.1" && \
  git push origin v1.0.1 && \
  gh release create v1.0.1 dist/PrivacyEraser.exe \
    --title "Privacy Eraser POC v1.0.1" \
    --notes "릴리즈 노트 내용..."
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

## 📦 GitHub Actions (자동화)

현재는 권한 문제로 인해 로컬 빌드를 권장하지만, 워크플로우는 다음과 같이 작동합니다:

**트리거:**
- `main` 브랜치 push
- `feature/poc-production-ready` 브랜치 push
- `v*.*.*` 태그 push
- 수동 트리거 (workflow_dispatch)

**주의사항:**
- GitHub Actions에 `permissions: contents: write` 설정 필요
- 빌드 시간: 약 5-10분 소요

---

## 🎯 Claude Code에게 명령하기

다음번에 빌드 & 릴리즈가 필요할 때:

```
버전 v1.0.2로 빌드하고 릴리즈해줘
```

Claude Code가 자동으로:
1. 로컬 빌드 실행
2. 버전 태그 생성
3. GitHub Release 생성
4. EXE 파일 업로드

를 순차적으로 진행합니다.

---

## 📝 작업 히스토리

### v1.0.0 (2025-10-21)
- 초기 프로덕션 릴리즈
- GitHub Actions 자동화 추가 (권한 문제로 로컬 빌드 사용)
- 실행 취소 기능 구현
- 스크린샷 자동 캡처
- 한글 로그 출력 수정

---

## 🛠️ 트러블슈팅

### PyInstaller 빌드 실패
- PySide6가 설치되지 않은 경우: `pip install pyside6 qt-material qtawesome`
- 경로 문제: `SPECPATH` 사용 (PrivacyEraser.spec 참조)

### GitHub Release 403 에러
- 워크플로우에 `permissions: contents: write` 추가
- 또는 로컬 빌드 후 `gh release create` 사용

### 한글 깨짐
- Windows 콘솔: `chcp 65001` 실행
- logger 설정: encoding 파라미터 제거 (loguru 기본 사용)
