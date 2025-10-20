#!/usr/bin/env python3
"""
Privacy Eraser 실행 스크립트
=========================

Privacy Eraser를 다양한 모드로 실행할 수 있는 통합 실행 스크립트입니다.
"""

import sys
import os
import argparse
from pathlib import Path

# 프로젝트 루트 경로 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

def print_banner():
    """프로그램 배너 출력"""
    print("🛡️  Privacy Eraser - 브라우저 개인정보 정리 도구")
    print("=" * 60)
    print("버전: 1.0.0 | 프레임워크: PySide6 + Material Design")
    print("=" * 60)

def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(
        description="Privacy Eraser - 브라우저 개인정보 정리 도구",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
실행 모드:
  gui         그래픽 사용자 인터페이스 모드 (기본값)
  background  백그라운드 데몬 모드로 실행 (시스템 트레이)
  daemon      백그라운드 데몬 모드 (동의어)
  test        테스트 모드 실행

예시:
  python run_privacy_eraser.py              # GUI 모드 실행
  python run_privacy_eraser.py --mode background  # 백그라운드 모드
  python run_privacy_eraser.py --debug       # 디버그 모드
  python run_privacy_eraser.py --test        # 테스트 실행
        """
    )

    parser.add_argument(
        "--mode", "-m",
        choices=["gui", "background", "daemon", "test"],
        default="gui",
        help="실행 모드 선택 (기본값: gui)"
    )

    parser.add_argument(
        "--debug", "-d",
        action="store_true",
        help="디버그 모드 활성화"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="상세 로그 출력"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="Privacy Eraser 1.0.0"
    )

    args = parser.parse_args()

    # 배너 출력
    print_banner()

    # 로깅 설정
    if args.debug or args.verbose:
        print("🔧 디버그 모드 활성화")

    try:
        if args.mode == "test":
            # 테스트 모드 실행
            print("🧪 테스트 모드 실행 중...")
            from test_comprehensive import main as test_main
            success = test_main()

            if success:
                print("✅ 모든 테스트가 성공적으로 완료되었습니다!")
                return 0
            else:
                print("❌ 일부 테스트에서 실패가 발생했습니다.")
                return 1

        elif args.mode in ["background", "daemon"]:
            # 백그라운드 데몬 모드 실행
            print("🔄 백그라운드 데몬 모드로 시작 중...")

            try:
                from privacy_eraser.daemon import run_background_daemon
                exit_code = run_background_daemon()

                if exit_code == 0:
                    print("✅ 백그라운드 데몬이 성공적으로 시작되었습니다.")
                    print("💡 시스템 트레이에서 Privacy Eraser를 확인하세요.")
                else:
                    print(f"❌ 백그라운드 데몬 시작 실패 (코드: {exit_code})")

                return exit_code

            except ImportError as e:
                print(f"❌ 백그라운드 모듈 로드 실패: {e}")
                print("💡 GUI 모드로 실행하려면 --mode gui 옵션을 사용하세요.")
                return 1

        else:
            # GUI 모드 실행 (기본값)
            print("🖼️  그래픽 사용자 인터페이스 모드로 시작 중...")

            try:
                from privacy_eraser.gui import run_gui
                exit_code = run_gui()

                if exit_code == 0:
                    print("✅ GUI가 성공적으로 실행되었습니다.")
                else:
                    print(f"❌ GUI 실행 실패 (코드: {exit_code})")

                return exit_code

            except ImportError as e:
                print(f"❌ GUI 모듈 로드 실패: {e}")
                print("💡 필요한 의존성을 설치했는지 확인하세요.")
                print("   uv run uv add PySide6 qt-material qtawesome")
                return 1

    except KeyboardInterrupt:
        print("\n\n🛑 사용자에 의해 실행이 중단되었습니다.")
        return 0

    except Exception as e:
        print(f"❌ 예상치 못한 오류 발생: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1

def show_help():
    """도움말 표시"""
    print_banner()
    print("사용법: python run_privacy_eraser.py [옵션]")
    print()
    print("필수 의존성:")
    print("  - PySide6 (GUI 프레임워크)")
    print("  - qt-material (Material Design 테마)")
    print("  - qtawesome (아이콘 라이브러리)")
    print("  - APScheduler (스케줄링)")
    print()
    print("설치 명령:")
    print("  uv run uv add PySide6 qt-material qtawesome APScheduler")
    print()
    print("자세한 도움말:")
    print("  python run_privacy_eraser.py --help")

if __name__ == "__main__":
    # 의존성 확인
    required_modules = [
        'PySide6',
        'qt_material',
        'qtawesome',
        'apscheduler',
        'loguru'
    ]

    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)

    if missing_modules:
        print("⚠️  필요한 의존성이 설치되지 않았습니다:")
        for module in missing_modules:
            print(f"  - {module}")
        print()
        print("다음 명령어로 설치하세요:")
        print("  uv run uv add PySide6 qt-material qtawesome APScheduler loguru")
        print()
        show_help()
        sys.exit(1)

    # 메인 실행
    sys.exit(main())
