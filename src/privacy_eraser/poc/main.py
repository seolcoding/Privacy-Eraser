"""Privacy Eraser POC - 메인 진입점"""

import sys
import os
from PySide6.QtWidgets import QApplication
from loguru import logger

from privacy_eraser.poc.ui.main_window import MainWindow
from privacy_eraser.poc.ui.styles import get_stylesheet


def setup_logger() -> None:
    """로거 설정"""
    # Windows 콘솔 UTF-8 설정
    if os.name == 'nt':
        os.system('chcp 65001 > nul')
        try:
            sys.stderr.reconfigure(encoding='utf-8')
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    logger.remove()  # 기본 핸들러 제거
    logger.add(
        sys.stderr,
        format="<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO"
        # Note: loguru automatically uses sys.stderr's encoding (already configured as UTF-8 above)
    )


def main() -> None:
    """메인 함수"""
    # 로거 설정
    setup_logger()
    logger.info("Privacy Eraser POC 시작")

    # Qt 애플리케이션 생성
    app = QApplication(sys.argv)

    # 글로벌 스타일시트 적용
    app.setStyleSheet(get_stylesheet())

    # 메인 윈도우 생성 및 표시
    window = MainWindow()
    window.show()

    logger.info("UI 시작됨")

    # 애플리케이션 루프 시작
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
