# Claude Code - 프로젝트 작업 가이드

이 문서는 Claude Code와 함께 작업할 때 사용하는 명령어와 프로세스를 기록합니다.

## 📚 AI 개발 문서 참고 (중요!)

**라이브러리나 프레임워크 사용 시 반드시 `ai-docs/` 디렉토리의 문서를 참고하세요.**

### 주요 참고 문서

- **프로젝트 아키텍처 이해**: `ai-docs/context/architecture.md`
- **테스트 작성**: `ai-docs/context/testing.md`

### 사용 예시

```
# Claude Code에게 명령 시:
"새 기능 추가 시 프로젝트 구조 확인 (ai-docs/context/architecture.md 참고)"
```

**⚠️ 중요**:
- 새로운 라이브러리 도입 시 ai-docs에 문서를 추가하세요

## 🚀 빌드 & 릴리즈 프로세스

**Note**: 빌드 스크립트는 현재 deprecated 폴더로 이동되었습니다. Flet 기반 UI로 전환 중입니다.

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

### 2025-10-21 (Latest)
- PySide6 제거 및 Flet UI로 전환
- 기존 PySide6 코드 및 문서 deprecated로 이동
- pyproject.toml 의존성 정리

### v1.0.0 (2025-10-21)
- 초기 프로덕션 릴리즈
- 로컬 빌드 & 릴리즈 자동화 스크립트 (scripts/release.bat)
- 실행 취소 기능 구현
- 스크린샷 자동 캡처
- 한글 로그 출력 수정

---

## 🛠️ 트러블슈팅

### 의존성 설치 오류
- `uv sync` 실행하여 모든 의존성 설치
- Python 버전 확인: Python 3.12+ 필요

### 한글 깨짐
- Windows 콘솔: `chcp 65001` 실행
- logger 설정: encoding 파라미터 제거 (loguru 기본 사용)
- uv로 항상 실행