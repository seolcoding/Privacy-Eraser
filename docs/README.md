# Privacy Eraser - Documentation

Privacy Eraser 프로젝트의 모든 문서가 이 디렉토리에 통합되어 있습니다.

---

## 📚 문서 구조

### 핵심 문서

| 문서 | 설명 | 용도 |
|------|------|------|
| **flet.md** | Flet 프레임워크 종합 가이드 (11k+ 라인) | UI 개발 시 필수 참조 |
| **ARCHITECTURE.md** | 시스템 아키텍처 설명 | 프로젝트 구조 이해 |
| **TODO.md** | 다음 작업 목록 | 개발 우선순위 확인 |
| **BUILD.md** | 빌드 & 릴리즈 가이드 | 배포 프로세스 |
| **DEVELOPMENT.md** | 개발 가이드 | BleachBit 통합, 트러블슈팅 |

### 참조 문서

| 문서 | 설명 |
|------|------|
| **TESTING.md** | 테스트 작성 가이드 |
| **runbook.md** | 운영 가이드 (uv 명령어) |
| **mcp.json** | Model Context Protocol 설정 |
| **rules** | AI 코딩 규칙 |

### 아카이브

| 디렉토리 | 설명 |
|----------|------|
| **archive/** | 히스토리 문서 보관 (proposal, cursor.md) |

---

## 🎯 문서 찾기

### UI 개발 중
→ **flet.md** 참조

### 새 기능 추가 전
→ **ARCHITECTURE.md**로 구조 파악 → **TODO.md**로 우선순위 확인

### 빌드 & 릴리즈
→ **BUILD.md**

### 새 브라우저 추가
→ **DEVELOPMENT.md** (BleachBit 통합 섹션)

### 테스트 작성
→ **TESTING.md**

### 문제 해결
→ **DEVELOPMENT.md** (트러블슈팅 섹션) 또는 **BUILD.md** (빌드 문제)

---

## 📖 문서 관리 원칙

1. **단일 진실의 원천**: 중복 없이 한 곳에만 기록
2. **최신 유지**: 코드 변경 시 관련 문서도 함께 업데이트
3. **명확한 분리**:
   - 사용자 문서 → RELEASE_NOTES.md (루트)
   - 개발자 문서 → docs/
   - AI 가이드 → CLAUDE.md (루트, 간결)

4. **참조 링크**: 중복 대신 다른 문서 참조

---

## 🔄 문서 업데이트 시

### 새 문서 추가
1. 해당 주제에 맞는 기존 문서 확인
2. 통합 가능하면 기존 문서에 섹션 추가
3. 독립 문서가 필요하면 이 README에 추가

### 구조 변경
1. ARCHITECTURE.md 업데이트
2. 관련 문서들 확인 및 링크 수정
3. CLAUDE.md 참조 링크 확인

### 아카이브
1. 더 이상 필요 없는 문서는 archive/로 이동
2. archive/README.md에 기록

---

## 📝 최근 업데이트

### 2025-10-27
- **통합**: ai-docs/ → docs/ (문서 중앙화)
- **분리**: CLAUDE.md에서 상세 내용 분리 (TODO, BUILD, DEVELOPMENT)
- **간결화**: CLAUDE.md 613줄 → 172줄
- **정리**: 17개 → 12개 활성 문서 (29% 감소)

---

**Tip**: CLAUDE.md에서 필요한 문서 바로 찾기!
