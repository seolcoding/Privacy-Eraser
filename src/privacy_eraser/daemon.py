"""
Privacy Eraser Daemon Module
============================

백그라운드에서 지속적으로 동작하는 데몬 프로세스 관리 모듈.
시스템 트레이 아이콘, 스케줄러, 단일 인스턴스 관리 등을 담당합니다.
"""

from __future__ import annotations

import os
import sys
import time
import threading
import socket
import json
from typing import Optional, Dict, Any
from pathlib import Path

from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMessageBox
from PySide6.QtCore import Qt, QTimer, QThread, Signal, QObject, QMutex, QWaitCondition
from PySide6.QtGui import QIcon, QAction

try:
    import qtawesome as qta
    HAS_QT_AWESOME = True
except ImportError:
    HAS_QT_AWESOME = False

from loguru import logger

from .settings_db import init_settings_db, load_setting, save_setting
from .app_state import app_state


class SingleInstanceChecker:
    """단일 인스턴스 실행을 보장하는 클래스"""

    def __init__(self, app_name: str = "PrivacyEraser"):
        self.app_name = app_name
        self.lock_socket = None
        self.lock_file = Path.home() / f".{app_name.lower()}_lock"

    def is_running(self) -> bool:
        """다른 인스턴스가 실행 중인지 확인"""
        try:
            # 소켓을 통한 중복 실행 검사
            self.lock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.lock_socket.bind(('127.0.0.1', 0))  # 임의의 포트 할당
            return False
        except OSError:
            # 소켓 바인딩 실패 = 이미 실행 중
            return True

    def cleanup(self):
        """잠금 파일 정리"""
        try:
            if self.lock_socket:
                self.lock_socket.close()
            if self.lock_file.exists():
                self.lock_file.unlink()
        except Exception:
            pass


class DaemonSignals(QObject):
    """데몬과 GUI 간 통신을 위한 시그널"""
    tray_icon_clicked = Signal()
    exit_requested = Signal()
    gui_requested = Signal()
    clean_now_requested = Signal()
    status_updated = Signal(str)  # 상태 메시지 전달


class BackgroundScheduler(QThread):
    """백그라운드 스케줄러 스레드"""

    def __init__(self):
        super().__init__()
        self.running = False
        self.check_interval = 60  # 1분마다 체크

    def run(self):
        """스케줄 체크 루프"""
        self.running = True
        logger.info("Background scheduler started")

        while self.running:
            try:
                # 스케줄 체크 로직 (추후 구현)
                self._check_schedules()
                time.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                time.sleep(30)  # 오류 발생 시 30초 대기

    def _check_schedules(self):
        """스케줄 확인 및 실행"""
        # TODO: 실제 스케줄 확인 로직 구현
        pass

    def stop(self):
        """스케줄러 중지"""
        self.running = False
        self.wait()


class PrivacyEraserDaemon:
    """Privacy Eraser 데몬 메인 클래스"""

    def __init__(self):
        self.app: Optional[QApplication] = None
        self.tray_icon: Optional[QSystemTrayIcon] = None
        self.main_window = None
        self.signals = DaemonSignals()
        self.scheduler = BackgroundScheduler()
        self.single_instance = SingleInstanceChecker()

        # 상태 관리
        self.is_gui_visible = False
        self.is_background_mode = True

    def initialize(self) -> bool:
        """데몬 초기화"""
        try:
            # 단일 인스턴스 검사
            if self.single_instance.is_running():
                logger.warning("Another instance is already running")
                QMessageBox.warning(
                    None,
                    "Privacy Eraser",
                    "Privacy Eraser가 이미 실행 중입니다.\n시스템 트레이에서 확인하세요."
                )
                return False

            # 설정 초기화
            init_settings_db()

            # 앱 상태 로드
            self._load_app_state()

            # Qt 애플리케이션 생성
            self.app = QApplication(sys.argv) if not QApplication.instance() else QApplication.instance()

            # Material Design 테마 적용
            self._apply_theme()

            # 시스템 트레이 설정
            if not self._setup_system_tray():
                logger.error("Failed to setup system tray")
                return False

            # 스케줄러 시작
            self.scheduler.start()

            # 시그널 연결
            self._connect_signals()

            logger.info("Privacy Eraser daemon initialized successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize daemon: {e}")
            return False

    def _load_app_state(self):
        """앱 상태 로드"""
        try:
            app_state.ui_mode = load_setting("ui_mode", "easy")
            app_state.appearance_mode = load_setting("appearance_mode", "dark")
            app_state.debug_enabled = load_setting("debug_enabled", "false") == "true"
        except Exception as e:
            logger.warning(f"Failed to load app state: {e}")

    def _apply_theme(self):
        """테마 적용"""
        try:
            from qt_material import apply_stylesheet
            appearance_mode = load_setting("appearance_mode", "dark")
            if appearance_mode == "dark":
                apply_stylesheet(self.app, theme='dark_blue.xml')
            else:
                apply_stylesheet(self.app, theme='light_blue.xml')
        except ImportError:
            logger.warning("qt-material not available, using default theme")

    def _setup_system_tray(self) -> bool:
        """시스템 트레이 아이콘 설정"""
        try:
            # 트레이 아이콘 생성
            if HAS_QT_AWESOME:
                tray_icon = QIcon(qta.icon('fa5s.shield-alt').pixmap(32, 32))
            else:
                tray_icon = QIcon()  # 기본 아이콘

            self.tray_icon = QSystemTrayIcon(tray_icon, self.app)

            # 트레이 메뉴 생성
            tray_menu = QMenu()

            # GUI 열기/숨기기
            self.toggle_gui_action = QAction("UI 열기", self.app)
            self.toggle_gui_action.triggered.connect(self._toggle_gui)
            tray_menu.addAction(self.toggle_gui_action)

            tray_menu.addSeparator()

            # 지금 정리 실행
            clean_now_action = QAction("지금 정리 실행", self.app)
            clean_now_action.triggered.connect(self._clean_now)
            tray_menu.addAction(clean_now_action)

            tray_menu.addSeparator()

            # 종료
            quit_action = QAction("종료", self.app)
            quit_action.triggered.connect(self._quit_application)
            tray_menu.addAction(quit_action)

            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.setToolTip("Privacy Eraser - 브라우저 개인정보 정리")

            # 트레이 아이콘 클릭 시그널 연결
            self.tray_icon.activated.connect(self._on_tray_activated)

            # 트레이 아이콘 표시
            self.tray_icon.show()

            logger.info("System tray setup completed")
            return True

        except Exception as e:
            logger.error(f"Failed to setup system tray: {e}")
            return False

    def _connect_signals(self):
        """시그널 연결"""
        self.signals.tray_icon_clicked.connect(self._on_tray_clicked)
        self.signals.exit_requested.connect(self._quit_application)
        self.signals.gui_requested.connect(self._show_gui)
        self.signals.clean_now_requested.connect(self._clean_now)

    def _toggle_gui(self):
        """GUI 표시/숨기기 토글"""
        if self.is_gui_visible:
            self._hide_gui()
        else:
            self._show_gui()

    def _show_gui(self):
        """메인 GUI 표시"""
        if self.main_window is None:
            from .gui import MainWindow
            self.main_window = MainWindow()

        self.main_window.show()
        self.main_window.raise_()
        self.main_window.activateWindow()
        self.is_gui_visible = True

        # 트레이 메뉴 업데이트
        if hasattr(self, 'toggle_gui_action'):
            self.toggle_gui_action.setText("UI 숨기기")

        logger.info("GUI shown")

    def _hide_gui(self):
        """메인 GUI 숨기기"""
        if self.main_window:
            self.main_window.hide()
        self.is_gui_visible = False

        # 트레이 메뉴 업데이트
        if hasattr(self, 'toggle_gui_action'):
            self.toggle_gui_action.setText("UI 열기")

        logger.info("GUI hidden")

    def _clean_now(self):
        """즉시 정리 실행"""
        logger.info("Clean now requested from tray")
        # TODO: 정리 실행 로직 구현
        self.signals.status_updated.emit("정리 작업을 시작합니다...")

    def _quit_application(self):
        """애플리케이션 종료"""
        logger.info("Application exit requested")

        # 정리 작업 중지
        if self.scheduler.isRunning():
            self.scheduler.stop()

        # 단일 인스턴스 잠금 해제
        self.single_instance.cleanup()

        # GUI 숨기기
        self._hide_gui()

        # 트레이 아이콘 숨기기
        if self.tray_icon:
            self.tray_icon.hide()

        # 애플리케이션 종료
        if self.app:
            self.app.quit()

    def _on_tray_activated(self, reason):
        """트레이 아이콘 활성화 처리"""
        if reason == QSystemTrayIcon.DoubleClick:
            self._toggle_gui()
        elif reason == QSystemTrayIcon.MiddleClick:
            self._clean_now()

    def _on_tray_clicked(self):
        """트레이 클릭 처리"""
        self._toggle_gui()

    def run_background_mode(self):
        """백그라운드 모드로 실행"""
        if not self.initialize():
            return False

        self._hide_gui()  # GUI 숨기고 백그라운드로 실행
        logger.info("Running in background mode")

        # 이벤트 루프 실행
        if self.app:
            return self.app.exec()

        return False

    def run_gui_mode(self):
        """GUI 모드로 실행"""
        if not self.initialize():
            return False

        self._show_gui()
        logger.info("Running in GUI mode")

        # 이벤트 루프 실행
        if self.app:
            return self.app.exec()

        return False


# 전역 데몬 인스턴스
_daemon_instance = None
_daemon_mutex = threading.Lock()


def get_daemon() -> PrivacyEraserDaemon:
    """전역 데몬 인스턴스 반환"""
    global _daemon_instance
    with _daemon_mutex:
        if _daemon_instance is None:
            _daemon_instance = PrivacyEraserDaemon()
        return _daemon_instance


def run_background_daemon() -> int:
    """백그라운드 데몬 실행"""
    daemon = get_daemon()
    return daemon.run_background_mode()


def run_gui_daemon() -> int:
    """GUI 데몬 실행"""
    daemon = get_daemon()
    return daemon.run_gui_mode()


__all__ = [
    "PrivacyEraserDaemon",
    "get_daemon",
    "run_background_daemon",
    "run_gui_daemon",
    "SingleInstanceChecker"
]
