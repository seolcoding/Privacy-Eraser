#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI 스크린샷 분석 스크립트

Claude Code가 최신 UI 스크린샷을 분석하여 개선사항을 제안할 수 있도록
컨텍스트를 제공하는 스크립트입니다.

Usage:
    python scripts/analyze_ui_screenshot.py

Output:
    - 최신 스크린샷 경로
    - UI 분석 프롬프트 (Claude Code용)
"""

import sys
from pathlib import Path
from datetime import datetime

# 프로젝트 루트
PROJECT_ROOT = Path(__file__).parent.parent
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"


def find_latest_screenshot() -> Path | None:
    """최신 스크린샷 찾기

    Returns:
        최신 스크린샷 경로 (없으면 None)
    """
    if not SCREENSHOTS_DIR.exists():
        return None

    # latest.png 우선
    latest_path = SCREENSHOTS_DIR / "latest.png"
    if latest_path.exists():
        return latest_path

    # 타임스탬프 파일 검색
    screenshots = list(SCREENSHOTS_DIR.glob("poc_gui_*.png"))
    if not screenshots:
        return None

    # 최신 파일 반환 (파일명 기준)
    screenshots.sort(reverse=True)
    return screenshots[0]


def generate_analysis_prompt(screenshot_path: Path) -> str:
    """UI 분석 프롬프트 생성

    Args:
        screenshot_path: 스크린샷 파일 경로

    Returns:
        Claude Code용 분석 프롬프트
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    prompt = f"""
# Privacy Eraser POC - UI 분석 요청

**스크린샷 경로**: `{screenshot_path.relative_to(PROJECT_ROOT)}`
**분석 시각**: {timestamp}

## 분석 요청사항

다음 관점에서 UI를 분석하고 개선사항을 제안해주세요:

### 1. 시각적 디자인 (Visual Design)
- [ ] 색상 대비 (Contrast): 텍스트와 배경의 가독성
- [ ] 타이포그래피 (Typography): 폰트 크기, 굵기, 위계
- [ ] 간격 (Spacing): 여백, 패딩, 마진의 일관성
- [ ] 정렬 (Alignment): 요소들의 정렬과 균형

### 2. 사용성 (Usability)
- [ ] 버튼 크기: 클릭 영역이 충분한가?
- [ ] 시각적 계층 (Visual Hierarchy): 중요한 요소가 눈에 띄는가?
- [ ] 피드백: 사용자 액션에 대한 시각적 피드백이 명확한가?
- [ ] 일관성: 디자인 패턴이 일관되게 적용되었는가?

### 3. Material Design 가이드라인
- [ ] Elevation: 그림자와 깊이감
- [ ] Ripple Effects: 터치 피드백 (현재는 Qt 제약)
- [ ] 색상 팔레트: Primary, Secondary, Surface 색상 사용
- [ ] 둥근 모서리: Border Radius 일관성

### 4. 레이아웃 (Layout)
- [ ] 그리드 시스템: 4x3 브라우저 카드 레이아웃이 균형있는가?
- [ ] 반응형: 윈도우 크기 조정 시 레이아웃이 깨지지 않는가?
- [ ] 여백 활용: 빈 공간이 효과적으로 사용되었는가?

### 5. 아이콘 & 이미지
- [ ] 아이콘 크기: 48px가 적절한가?
- [ ] 아이콘 일관성: qtawesome 아이콘이 통일감 있는가?
- [ ] 색상 조화: 아이콘 색상이 브라우저 색상과 잘 어울리는가?

## 응답 형식

다음 형식으로 개선사항을 제안해주세요:

1. **현재 상태 요약** (2-3문장)
2. **주요 개선사항** (우선순위별 3-5개)
   - 각 항목마다:
     - 문제점
     - 제안하는 해결책
     - 예상 효과
3. **코드 수정 제안** (필요한 경우)
   - 파일 경로
   - 수정할 부분 (diff 형식 또는 설명)

## 참고 파일

- `src/privacy_eraser/poc/ui/styles.py` - 색상, 타이포그래피, 크기 정의
- `src/privacy_eraser/poc/ui/main_window.py` - 메인 윈도우 레이아웃
- `src/privacy_eraser/poc/ui/browser_card.py` - 브라우저 카드 위젯

---

**참고**: 이 스크린샷은 자동으로 캡처되었습니다 (GUI 로드 1초 후).
"""
    return prompt


def main():
    """메인 함수"""
    print("=" * 70)
    print("🎨 Privacy Eraser POC - UI 분석 스크립트")
    print("=" * 70)
    print()

    # 최신 스크린샷 찾기
    screenshot_path = find_latest_screenshot()

    if not screenshot_path:
        print("❌ 스크린샷을 찾을 수 없습니다.")
        print()
        print("다음 명령어로 POC를 실행하여 스크린샷을 생성하세요:")
        print("  uv run python run_poc.py")
        print("  또는")
        print("  uv run python dev_server.py")
        print()
        sys.exit(1)

    print(f"✅ 최신 스크린샷 발견: {screenshot_path.relative_to(PROJECT_ROOT)}")
    print(f"   파일 크기: {screenshot_path.stat().st_size / 1024:.1f} KB")
    print()

    # 분석 프롬프트 생성
    prompt = generate_analysis_prompt(screenshot_path)

    # 프롬프트 출력
    print("=" * 70)
    print("📋 Claude Code용 분석 프롬프트")
    print("=" * 70)
    print()
    print(prompt)
    print()
    print("=" * 70)
    print("💡 사용 방법:")
    print("   1. 위 프롬프트를 Claude Code에 복사")
    print("   2. 스크린샷 파일을 함께 첨부")
    print("   3. Claude Code가 UI를 분석하고 개선사항 제안")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
