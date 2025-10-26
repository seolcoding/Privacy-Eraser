# Claude Code - Privacy Eraser 개발 가이드

> 이 문서는 Claude Code와 함께 Privacy Eraser를 개발할 때 참고하는 핵심 가이드입니다.

---

## 📌 프로젝트 개요

**Privacy Eraser**는 브라우저 개인정보 자동 삭제 도구입니다.

- **UI**: Flet (Flutter for Python) + Material Design 3
- **언어**: Python 3.12+
- **패키지 관리**: uv
- **지원 브라우저**: Chrome, Edge, Firefox, Brave, Opera, Whale, Safari
- **주요 기능**: 원클릭 삭제, 백업/복원, 예약 실행

---

## 🎯 핵심 개발 규칙

### 1. 패키지 관리
- **항상 `uv` 사용**: `uv sync`, `uv run`, `uv add`
- pip 사용 금지 (uv로 통일)

### 2. 코드 스타일
- **Flet 참조 필수**: UI 개발 시 `docs/flet.md` 먼저 읽기
- **타입 힌트 사용**: 모든 함수에 타입 힌트 추가
- **Docstring**: 공개 API에 docstring 작성

### 3. 테스트
- **테스트 필수**: 새 기능 추가 시 테스트 함께 작성
- **sandbox fixture 사용**: 실제 사용자 데이터 절대 접근 금지
- 테스트 가이드: `docs/TESTING.md`

### 4. 커밋 규칙
- **Conventional Commits** 형식 사용
- 예: `feat:`, `fix:`, `docs:`, `refactor:`
- 항상 마지막에 Claude Code 서명 포함

---

## 📚 참조 문서

### 핵심 문서 (자주 참조)
- **Flet UI 개발**: `docs/flet.md` ⭐ (11k 라인 종합 가이드)
- **프로젝트 아키텍처**: `docs/ARCHITECTURE.md`
- **빌드 & 릴리즈**: `docs/BUILD.md`
- **TODO 목록**: `docs/TODO.md`

### 개발 참고
- **개발 가이드**: `docs/DEVELOPMENT.md` (BleachBit 통합, 새 브라우저 추가)
- **테스트 가이드**: `docs/TESTING.md`
- **운영 가이드**: `docs/runbook.md`

---

## ⚡ 자주 쓰는 명령어

### 앱 실행
```bash
# UI 실행 (개발 모드)
python -m privacy_eraser.ui.main

# 또는
privacy_eraser
```

### 의존성 관리
```bash
# 의존성 설치
uv sync

# 새 패키지 추가
uv add <package>

# 빌드 의존성 포함
uv sync --extra build
```

### 테스트
```bash
# 전체 테스트
uv run pytest

# 커버리지
uv run pytest --cov=privacy_eraser
```

### 빌드 & 릴리즈
```bash
# 빌드만 (로컬 테스트용)
uv run flet build windows

# 빌드 + GitHub 릴리즈 (자동화)
scripts\release_flutter.bat 2.0.5
```

---

## 🔍 프로젝트 구조 (핵심만)

```
Privacy-Eraser/
├── src/privacy_eraser/
│   ├── ui/                # Flet UI
│   │   ├── main.py        # 엔트리포인트
│   │   └── core/          # 핵심 로직 (브라우저 감지, 스케줄, 백업)
│   ├── scheduler.py       # APScheduler 통합
│   ├── cleaning.py        # 삭제 엔진
│   ├── cleanerml_loader.py # BleachBit XML 파서
│   └── cleaners/          # CleanerML 파일들
├── static/images/         # 브라우저 로고
├── docs/                  # 📚 모든 문서 (통합됨)
├── tests/                 # 테스트
└── scripts/               # 빌드 스크립트
```

---

## 💡 AI에게 도움 요청하기

### 새 기능 추가
```
docs/TODO.md 확인 후 우선순위 1번 작업 구현해줘
(ai-docs/flet.md 참고)
```

### 빌드 문제
```
빌드 크기가 너무 커, docs/BUILD.md 참고해서 최적화해줘
```

### 새 브라우저 추가
```
Vivaldi 브라우저 지원 추가해줘
(docs/DEVELOPMENT.md의 "새 브라우저 추가 방법" 참고)
```

---

## 🚨 중요 사항

### DEV 모드
- 개발 중에는 **항상 DEV 모드** 사용
- `AppConfig.is_dev_mode()` 확인
- DEV 모드에서는 실제 파일 삭제 안됨 (test_data만 사용)

### Flet UI 개발
- **반드시 `docs/flet.md` 먼저 읽기**
- Material Design 3 가이드라인 준수
- `AppColors` 클래스 사용 (일관된 색상)

### 빌드
- **Flet Build (Flutter) 권장** (PyInstaller는 오탐 위험)
- `pyproject.toml`의 exclude 설정 확인
- 빌드 전 src/.venv 삭제 또는 제외

---

## 📖 더 알아보기

- **TODO 목록**: `docs/TODO.md` - 다음 작업 확인
- **빌드 가이드**: `docs/BUILD.md` - 릴리즈 프로세스
- **개발 가이드**: `docs/DEVELOPMENT.md` - BleachBit, 트러블슈팅
- **아키텍처**: `docs/ARCHITECTURE.md` - 전체 시스템 구조
- **Flet 마스터 가이드**: `docs/flet.md` - 11k 라인 종합 참조

---

**Last Updated**: 2025-10-27
**Version**: 2.0.x (Flet-based)
