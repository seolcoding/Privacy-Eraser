from __future__ import annotations

import sys
import argparse
from loguru import logger

from .daemon import run_gui_daemon, run_background_daemon


def main() -> None:
    """Privacy Eraser 메인 함수"""
    parser = argparse.ArgumentParser(description="Privacy Eraser - 브라우저 개인정보 정리 도구")
    parser.add_argument(
        "--mode",
        choices=["gui", "background", "daemon"],
        default="gui",
        help="실행 모드 선택 (기본값: gui)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="디버그 모드 활성화"
    )

    args = parser.parse_args()

    # 로깅 설정
    if args.debug:
        logger.remove()
        logger.add(
            sys.stderr,
            level="DEBUG",
            format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        )
        logger.info("Debug mode enabled")

    try:
        if args.mode in ["background", "daemon"]:
            logger.info("Starting Privacy Eraser in background mode")
            exit_code = run_background_daemon()
        else:
            logger.info("Starting Privacy Eraser in GUI mode")
            exit_code = run_gui_daemon()

        sys.exit(exit_code)

    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
