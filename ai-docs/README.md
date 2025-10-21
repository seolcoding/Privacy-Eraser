# AI 개발 문서 (AI Development Documentation)

이 디렉토리는 AI 개발 도구(Claude Code, Cursor 등)가 참고할 문서들을 포함합니다.

## 📚 주요 문서

### PySide6 관련 (⭐ 중요)

- **pyside.md** - PySide6 핵심 가이드 및 베스트 프랙티스
- **pyside_examples.md** - PySide6 예제 코드 모음 (대규모 참고 자료)

### 프로젝트 컨텍스트

- **context/architecture.md** - 프로젝트 아키텍처 설명
- **context/runbook.md** - 운영 가이드
- **context/testing.md** - 테스트 전략 및 가이드

### 기타

- **cursor.md** - Cursor IDE 설정 및 사용법
- **mcp.json** - Model Context Protocol 설정
- **rules** - AI 코딩 규칙

## 🤖 AI에게

**라이브러리 사용 시 반드시 이 문서들을 참고하세요:**

1. **PySide6 UI 개발 시** → `pyside.md`, `pyside_examples.md` 필독
2. **프로젝트 아키텍처 이해 시** → `context/architecture.md` 참고
3. **테스트 작성 시** → `context/testing.md` 참고

### 사용 방법

```
# AI에게 명령 예시:
"PySide6로 새 다이얼로그를 만들어줘 (ai-docs/pyside.md 참고)"
"프로젝트 구조 설명해줘 (ai-docs/context/architecture.md 참고)"
```

## 📝 문서 업데이트

새로운 라이브러리나 패턴을 도입할 때:

1. 관련 문서를 이 디렉토리에 추가
2. README.md 업데이트
3. claude.md에 참고 안내 추가

---

**Note**: 이 디렉토리는 AI 도구 전용입니다. 사람이 읽는 문서는 `docs/` 디렉토리를 사용하세요.
