#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Privacy Eraser GUI 대화형 테스트 스크립트
==========================================

이 스크립트는 GUI 컴포넌트를 단계별로 테스트합니다.
"""

import sys
import os
from pathlib import Path

# Windows 콘솔 UTF-8 설정
if os.name == 'nt':
    os.system('chcp 65001 > nul')
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# 프로젝트 경로 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from PySide6.QtWidgets import QApplication
from loguru import logger


def test_browser_detection():
    """브라우저 감지 테스트"""
    print("\n" + "="*60)
    print("1️⃣  브라우저 감지 테스트")
    print("="*60)

    from privacy_eraser.detect_windows import detect_browsers

    browsers = detect_browsers()
    print(f"\n✅ {len(browsers)}개 브라우저 감지됨:")

    for browser in browsers:
        name = browser.get("name", "Unknown")
        present = browser.get("present", "no")
        status = "✅ 설치됨" if present == "yes" else "❌ 미설치"
        print(f"  - {name}: {status}")

    return browsers


def test_browser_card_widget():
    """브라우저 카드 위젯 테스트"""
    print("\n" + "="*60)
    print("2️⃣  브라우저 카드 위젯 테스트")
    print("="*60)

    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    from privacy_eraser.poc.ui.browser_card import BrowserCard
    from privacy_eraser.poc.core.browser_info import BrowserInfo

    # 테스트 브라우저 생성
    test_browser = BrowserInfo(
        name="Chrome",
        icon="🌐",
        color="#4285F4",
        installed=True
    )

    card = BrowserCard(test_browser)
    print(f"\n✅ BrowserCard 생성 성공")
    print(f"  - 브라우저: {card.browser_info.name}")
    print(f"  - 선택 상태: {card.is_selected}")
    print(f"  - 아이콘: {card.browser_info.icon}")

    # 선택 토글 테스트
    card.checkbox.setChecked(False)
    print(f"  - 토글 후: {card.is_selected}")

    return card


def test_progress_dialog():
    """진행 다이얼로그 테스트"""
    print("\n" + "="*60)
    print("3️⃣  진행 다이얼로그 테스트")
    print("="*60)

    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    from privacy_eraser.poc.ui.progress_dialog import ProgressDialog
    from privacy_eraser.poc.core.browser_info import CleaningStats

    dialog = ProgressDialog()
    dialog.set_total_files(100)
    dialog.set_total_size(100 * 1024 * 1024)  # 100 MB

    print(f"\n✅ ProgressDialog 생성 성공")
    print(f"  - 전체 파일: {dialog.total_files}")
    print(f"  - 전체 크기: {dialog.total_size / 1024 / 1024:.2f} MB")

    # 진행 시뮬레이션
    for i in range(10):
        file_path = f"/mock/cache/file_{i}"
        file_size = 10 * 1024 * 1024  # 10 MB
        dialog.update_progress(file_path, file_size)

    print(f"  - 삭제된 파일: {dialog.deleted_files}")
    print(f"  - 진행률: {dialog.progress_bar.value()}%")

    # 완료 시뮬레이션
    stats = CleaningStats(
        total_files=100,
        deleted_files=100,
        failed_files=0,
        total_size=100 * 1024 * 1024,
        deleted_size=100 * 1024 * 1024,
        duration=5.5,
        errors=[]
    )
    dialog.show_completion(stats)
    print(f"  - 완료 상태: {stats.success_rate}% 성공")

    return dialog


def test_main_window_ui():
    """메인 윈도우 UI 테스트"""
    print("\n" + "="*60)
    print("4️⃣  메인 윈도우 UI 테스트")
    print("="*60)

    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    from privacy_eraser.poc.ui.main_window import MainWindow

    # 자동 감지 없이 생성
    window = MainWindow(auto_detect=False)

    print(f"\n✅ MainWindow 생성 성공")
    print(f"  - 윈도우 제목: {window.windowTitle()}")
    print(f"  - 크기: {window.width()}x{window.height()}")
    print(f"  - 북마크 삭제 옵션: {window.delete_bookmarks}")

    # 모의 브라우저 추가
    from privacy_eraser.poc.core.browser_info import BrowserInfo

    mock_browsers = [
        BrowserInfo(name="Chrome", icon="🌐", color="#4285F4", installed=True),
        BrowserInfo(name="Firefox", icon="🦊", color="#FF7139", installed=True),
        BrowserInfo(name="Edge", icon="🌐", color="#0078D4", installed=True),
    ]

    window.on_browsers_detected(mock_browsers)

    print(f"  - 감지된 브라우저: {len(window.browser_cards)}개")
    for name in window.browser_cards:
        print(f"    • {name}")

    return window


def test_full_app_launch():
    """전체 앱 실행 테스트 (실제 GUI 표시)"""
    print("\n" + "="*60)
    print("5️⃣  전체 앱 실행 테스트 (GUI 표시)")
    print("="*60)
    print("\n🚀 POC GUI를 실행합니다...")
    print("   (창을 닫으면 테스트가 종료됩니다)\n")

    from privacy_eraser.poc.main import main

    try:
        main()
    except SystemExit:
        print("\n✅ GUI 정상 종료")


def main():
    """메인 테스트 함수"""
    print("\n")
    print("🛡️  Privacy Eraser GUI 대화형 테스트")
    print("="*60)

    try:
        # 1. 브라우저 감지 테스트
        browsers = test_browser_detection()

        # 2. 위젯 테스트
        test_browser_card_widget()

        # 3. 다이얼로그 테스트
        test_progress_dialog()

        # 4. 메인 윈도우 테스트
        test_main_window_ui()

        # 5. 전체 앱 실행 (선택 사항)
        print("\n" + "="*60)
        response = input("\n전체 GUI를 실행하시겠습니까? (y/N): ")

        if response.lower() == 'y':
            test_full_app_launch()
        else:
            print("\n✅ 모든 테스트 완료!")

    except Exception as e:
        print(f"\n❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
