# Privacy Eraser - PySimpleGUI POC

FreeSimpleGUI를 사용한 심플한 브라우저 개인정보 삭제 도구 POC 버전입니다.

## 특징

- **심플한 UI**: PySimpleGUI 무료 버전(FreeSimpleGUI) 사용
- **POC 컨셉**: 최소한의 기능으로 빠르게 구현
- **동일한 기능**: PySide6 버전과 동일한 브라우저 삭제 기능
- **무료**: 완전 무료 라이브러리만 사용

## 설치

```bash
# FreeSimpleGUI 설치 (무료 버전)
pip install FreeSimpleGUI

# 또는 프로젝트 의존성 설치
pip install -e .
```

## 실행

```bash
# 프로젝트 루트에서 실행
python run_psg_poc.py

# 또는 직접 모듈 실행
python -m privacy_eraser.psg_poc.main
```

## 구조

```
src/privacy_eraser/psg_poc/
├── __init__.py
├── main.py              # 메인 앱 (이벤트 루프)
├── gui.py               # GUI 레이아웃 및 다이얼로그
├── cleaner_helper.py    # 동기 삭제 헬퍼 함수
└── README.md            # 이 파일
```

## 주요 기능

1. **브라우저 감지**: Chrome, Edge, Firefox, Brave, Opera, Vivaldi
2. **선택적 삭제**: 브라우저별 선택 가능
3. **옵션**:
   - 북마크 삭제
   - 다운로드 파일 삭제
   - 기본: 캐시, 쿠키, 히스토리, 세션, 비밀번호
4. **백업 및 복원**: 자동 백업 및 실행 취소 기능

## PySide6 버전과 차이점

| 기능 | PySide6 버전 | PySimpleGUI 버전 |
|------|--------------|------------------|
| UI 프레임워크 | PySide6 (Qt) | FreeSimpleGUI |
| 비동기 처리 | QThread | 동기 처리 |
| 스타일링 | Qt Stylesheet | 테마 기반 |
| 복잡도 | 높음 | 낮음 |
| 기능 | 완전 | 심플 |

## 왜 PySimpleGUI POC인가?

1. **빠른 프로토타이핑**: PySide6보다 간단한 코드
2. **낮은 진입장벽**: Qt 지식 불필요
3. **무료**: FreeSimpleGUI는 완전 무료
4. **POC 검증**: 핵심 기능만 빠르게 구현

## 개발자

developed with ❤️ by 설코딩 (seolcoding.com)
