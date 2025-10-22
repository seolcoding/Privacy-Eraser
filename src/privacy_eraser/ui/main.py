"""Privacy Eraser - Flet UI Version

Modern, beautiful UI built with Flet (Flutter for Python).
Clean Material Design 3 aesthetic with smooth animations.
"""

import flet as ft
from loguru import logger
import threading
import time
from pathlib import Path
from datetime import datetime
import webbrowser

import os
import sys
import glob
import subprocess

from privacy_eraser.detect_windows import detect_browsers
from privacy_eraser.ui.core.browser_info import BrowserInfo, CleaningStats
from privacy_eraser.ui.core.data_config import (
    get_browser_icon,
    get_browser_color,
    get_browser_display_name,
    get_browser_xml_path,
    get_cleaner_options,
    BROWSER_PROCESSES,
)
from privacy_eraser.ui.core.backup_manager import BackupManager
from privacy_eraser.core.schedule_manager import ScheduleManager, ScheduleScenario
from privacy_eraser.config import AppConfig


# ═════════════════════════════════════════════════════════════
# Resource Path Helper
# ═════════════════════════════════════════════════════════════


def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# ═════════════════════════════════════════════════════════════
# Design Tokens (Material Design 3)
# ═════════════════════════════════════════════════════════════


class AppColors:
    """Color palette"""

    BACKGROUND = "#FAFAFA"
    SURFACE = "#FFFFFF"
    PRIMARY = "#2563EB"
    DANGER = "#DC2626"
    WARNING = "#F59E0B"  # Amber/Orange for warnings
    SUCCESS = "#059669"
    TEXT_PRIMARY = "#1A1A1A"
    TEXT_SECONDARY = "#666666"
    TEXT_HINT = "#999999"
    BORDER = "#E5E5E5"
    BORDER_HOVER = "#CCCCCC"
    BORDER_SELECTED = "#2563EB"


# ═════════════════════════════════════════════════════════════
# Browser Process Management
# ═════════════════════════════════════════════════════════════


def check_running_browsers(browsers: list[str]) -> list[str]:
    """Check which browsers are currently running

    Args:
        browsers: List of browser names to check

    Returns:
        List of running browser names
    """
    running = []

    try:
        # Get list of running processes (Windows)
        result = subprocess.run(
            ['tasklist', '/FO', 'CSV', '/NH'],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        if result.returncode == 0:
            running_processes = result.stdout.lower()

            for browser in browsers:
                browser_lower = browser.lower()
                if browser_lower in BROWSER_PROCESSES:
                    process_names = BROWSER_PROCESSES[browser_lower]
                    for process_name in process_names:
                        if process_name.lower() in running_processes:
                            running.append(browser)
                            break  # Found one process for this browser
    except Exception as e:
        logger.warning(f"Failed to check running browsers: {e}")

    return running


def kill_browser_processes(browsers: list[str]) -> tuple[int, list[str]]:
    """Gracefully terminate browser processes

    Args:
        browsers: List of browser names to terminate

    Returns:
        Tuple of (killed_count, failed_browsers)
    """
    killed_count = 0
    failed = []

    for browser in browsers:
        browser_lower = browser.lower()
        if browser_lower not in BROWSER_PROCESSES:
            continue

        process_names = BROWSER_PROCESSES[browser_lower]
        browser_killed = False

        for process_name in process_names:
            try:
                # Try graceful shutdown first (without /F flag)
                result = subprocess.run(
                    ['taskkill', '/IM', process_name],
                    capture_output=True,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    timeout=5
                )

                if result.returncode == 0:
                    logger.info(f"Gracefully terminated browser process: {process_name}")
                    browser_killed = True
                    killed_count += 1
            except subprocess.TimeoutExpired:
                # If graceful shutdown times out, force kill
                try:
                    logger.info(f"Graceful shutdown timed out, forcing kill: {process_name}")
                    result = subprocess.run(
                        ['taskkill', '/F', '/IM', process_name],
                        capture_output=True,
                        text=True,
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
                    if result.returncode == 0:
                        browser_killed = True
                        killed_count += 1
                except Exception as e:
                    logger.warning(f"Failed to force kill {process_name}: {e}")
            except Exception as e:
                logger.warning(f"Failed to terminate {process_name}: {e}")

        if not browser_killed:
            failed.append(browser)

    return killed_count, failed


# ═════════════════════════════════════════════════════════════
# Cleaner Worker (Thread-based for Flet)
# ═════════════════════════════════════════════════════════════


class FletCleanerWorker(threading.Thread):
    """Thread-based cleaner worker for Flet (no Qt dependency)"""

    def __init__(
        self,
        browsers: list[str],
        delete_bookmarks: bool = False,
        delete_downloads: bool = False,
        on_started=None,
        on_progress=None,
        on_finished=None,
        on_error=None,
        on_browser_counts=None,  # NEW: callback for browser file counts
    ):
        super().__init__(daemon=True)
        self.browsers = browsers
        self.delete_bookmarks = delete_bookmarks
        self.delete_downloads = delete_downloads
        self.is_cancelled = False
        self.backup_manager = BackupManager()

        # Callbacks
        self.on_started = on_started
        self.on_progress = on_progress
        self.on_finished = on_finished
        self.on_error = on_error
        self.on_browser_counts = on_browser_counts  # NEW

    def run(self):
        """Main cleaning logic"""
        if self.on_started:
            self.on_started()

        start_time = time.time()
        stats = CleaningStats(
            total_files=0,
            deleted_files=0,
            failed_files=0,
            total_size=0,
            deleted_size=0,
            duration=0,
            errors=[],
        )

        try:
            # Collect files (with browser counts)
            all_files, browser_file_counts = self._collect_files_with_counts()
            stats.total_files = len(all_files)
            stats.total_size = sum(
                self._get_file_size(f) for f in all_files if os.path.exists(f)
            )

            # Notify browser counts
            if self.on_browser_counts:
                self.on_browser_counts(browser_file_counts)

            logger.info(
                f"삭제 대상: {stats.total_files} 파일, {stats.total_size / (1024 * 1024):.1f} MB"
            )

            # Delete files
            for file_path in all_files:
                if self.is_cancelled:
                    logger.info("삭제 작업 취소됨")
                    break

                try:
                    file_size = (
                        self._get_file_size(file_path)
                        if os.path.exists(file_path)
                        else 0
                    )
                    self._safe_delete(file_path)

                    stats.deleted_files += 1
                    stats.deleted_size += file_size

                    if self.on_progress:
                        self.on_progress(file_path, file_size)

                    time.sleep(0.001)

                except Exception as e:
                    stats.failed_files += 1
                    error_msg = f"{file_path}: {str(e)}"
                    stats.errors.append(error_msg)
                    logger.warning(f"삭제 실패: {error_msg}")

            stats.duration = time.time() - start_time
            logger.info(f"삭제 완료: {stats.deleted_files}/{stats.total_files} 파일")

            if self.on_finished:
                self.on_finished(stats)

        except Exception as e:
            logger.error(f"삭제 작업 실패: {e}")
            if self.on_error:
                self.on_error(str(e))

    def _collect_files_with_counts(self) -> tuple[list[str], dict[str, int]]:
        """Collect files to delete and return browser file counts"""
        # 개발 모드: test_data 폴더의 더미 파일 사용
        if AppConfig.is_dev_mode():
            logger.info("[DEV] Development mode: Using test data")
            return self._collect_dev_files_with_counts()

        # 프로덕션 모드: 실제 브라우저 파일 수집
        files = []
        browser_counts = {}
        options = get_cleaner_options(self.delete_bookmarks, self.delete_downloads)

        for browser in self.browsers:
            try:
                browser_files = self._get_browser_files(browser, options)
                files.extend(browser_files)
                browser_counts[browser] = len(browser_files)
                logger.info(f"{browser}: {len(browser_files)} 파일 수집됨")
            except Exception as e:
                logger.warning(f"{browser} 파일 수집 실패: {e}")
                browser_counts[browser] = 0

        # 중복 제거
        unique_files = list(dict.fromkeys(files))  # 순서 보존하면서 중복 제거
        if len(unique_files) < len(files):
            logger.info(f"중복 제거: {len(files)} -> {len(unique_files)} 파일")

        return unique_files, browser_counts

    def _collect_files_to_delete(self) -> list[str]:
        """Backward compatibility wrapper"""
        files, _ = self._collect_files_with_counts()
        return files

    def _collect_dev_files_with_counts(self) -> tuple[list[str], dict[str, int]]:
        """Collect dummy files from test_data directory (development mode)"""
        from privacy_eraser.config import TEST_DATA_DIR

        files = []
        browser_counts = {}

        for browser in self.browsers:
            browser_dir = TEST_DATA_DIR / browser.lower()

            if not browser_dir.exists():
                logger.warning(f"[WARN] Test data not found for {browser}: {browser_dir}")
                browser_counts[browser] = 0
                continue

            # Collect all files in browser directory
            browser_files = []
            for file_path in browser_dir.rglob("*"):
                if file_path.is_file():
                    browser_files.append(str(file_path))

            files.extend(browser_files)
            browser_counts[browser] = len(browser_files)

            logger.info(f"[DEV] {browser}: {len(browser_files)} test files collected")

        return files, browser_counts

    def _collect_dev_files(self) -> list[str]:
        """Backward compatibility wrapper"""
        files, _ = self._collect_dev_files_with_counts()
        return files

    def _get_browser_files(self, browser_name: str, options: list[str]) -> list[str]:
        """Get files for specific browser"""
        files = []

        try:
            xml_path = get_browser_xml_path(browser_name)
            if not xml_path:
                logger.warning(f"CleanerML 경로 없음: {browser_name}")
                return files

            from privacy_eraser.cleanerml_loader import load_cleaner_options_from_file

            cleaner_options = load_cleaner_options_from_file(xml_path)

            for option_id in options:
                try:
                    # Find matching CleanerOption by ID
                    matching_option = next((opt for opt in cleaner_options if opt.id == option_id), None)
                    if matching_option:
                        for action in matching_option.actions:
                            expanded = self._expand_path(action.path)
                            files.extend(expanded)
                except Exception as e:
                    logger.debug(f"옵션 {option_id} 처리 실패: {e}")

        except Exception as e:
            logger.warning(f"{browser_name} CleanerML 처리 실패: {e}")

        return files

    def _expand_path(self, path: str) -> list[str]:
        """Expand environment variables and glob patterns"""
        expanded_files = []

        try:
            # Normalize path separators for Windows (/ -> \)
            normalized_path = path.replace('/', os.sep)

            # Expand environment variables
            expanded = os.path.expandvars(normalized_path)

            # Normalize path (resolve .., ., remove duplicate separators)
            expanded = os.path.normpath(expanded)

            if "*" in expanded or "?" in expanded:
                # Glob pattern matching
                matched = glob.glob(expanded, recursive=True)
                expanded_files.extend(matched)
            else:
                # Direct file/directory check
                if os.path.exists(expanded):
                    expanded_files.append(expanded)

        except Exception as e:
            logger.debug(f"경로 확장 실패 {path}: {e}")

        return expanded_files

    def _safe_delete(self, path: str):
        """Safely delete file or directory"""
        try:
            if os.path.isdir(path):
                import shutil
                shutil.rmtree(path, ignore_errors=True)
            else:
                os.remove(path)
        except Exception as e:
            logger.debug(f"삭제 실패 {path}: {e}")
            raise

    def _get_file_size(self, path: str) -> int:
        """Get file size in bytes"""
        try:
            if os.path.isfile(path):
                return os.path.getsize(path)
            elif os.path.isdir(path):
                total = 0
                for dirpath, dirnames, filenames in os.walk(path):
                    for filename in filenames:
                        filepath = os.path.join(dirpath, filename)
                        try:
                            total += os.path.getsize(filepath)
                        except (OSError, IOError):
                            pass
                return total
        except (OSError, IOError):
            pass
        return 0


# ═════════════════════════════════════════════════════════════
# Browser Card Component
# ═════════════════════════════════════════════════════════════


class BrowserCard(ft.Container):
    """Material Design 3 browser card with selection state"""

    def __init__(self, browser_info: BrowserInfo, on_click_callback):
        self.browser_info = browser_info
        self.selected = browser_info.installed
        self.on_click_callback = on_click_callback

        # Icon image mapping (브라우저별 이미지 파일)
        icon_image_map = {
            "chrome": get_resource_path("static/images/chrome.png"),
            "edge": get_resource_path("static/images/edge.png"),
            "firefox": get_resource_path("static/images/firefox.png"),
            "brave": get_resource_path("static/images/brave.svg"),
            "opera": get_resource_path("static/images/opera logo.png"),
            "whale": get_resource_path("static/images/whale.jpg"),
            "safari": get_resource_path("static/images/safari.png"),
        }

        # 브라우저 이름 소문자로 변환하여 매칭
        browser_key = browser_info.name.lower()
        icon_src = icon_image_map.get(browser_key, get_resource_path("static/images/chrome.png"))

        # Card content (아이콘을 이미지로 교체)
        content = ft.Column(
            [
                ft.Image(
                    src=icon_src,
                    width=38,  # 48 → 38 (80%)
                    height=38,  # 48 → 38 (80%)
                    fit=ft.ImageFit.CONTAIN,
                    opacity=1.0 if browser_info.installed else 0.4,
                ),
                ft.Text(
                    browser_info.name,
                    size=11,  # 13 → 11 (80%)
                    weight=ft.FontWeight.W_500,
                    color=AppColors.TEXT_PRIMARY,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5,  # 6 → 5
        )

        super().__init__(
            content=content,
            width=128,  # 160 → 128 (80%)
            height=80,  # 100 → 80 (80%)
            bgcolor=self._get_bg_color(),
            border=ft.border.all(2, self._get_border_color()),
            border_radius=8,  # 10 → 8 (80%)
            padding=10,  # 12 → 10 (80%)
            ink=True if browser_info.installed else False,
            on_click=self._handle_click if browser_info.installed else None,
            tooltip="이 브라우저는 설치되지 않았습니다."
            if not browser_info.installed
            else None,
        )

    def _get_bg_color(self):
        if not self.browser_info.installed:
            return "#F9F9F9"
        return "#EFF6FF" if self.selected else AppColors.SURFACE

    def _get_border_color(self):
        if not self.browser_info.installed:
            return AppColors.BORDER
        return AppColors.BORDER_SELECTED if self.selected else AppColors.BORDER

    def _handle_click(self, e):
        if not self.browser_info.installed:
            return

        self.selected = not self.selected
        self.bgcolor = self._get_bg_color()
        self.border = ft.border.all(2, self._get_border_color())
        self.update()

        # Notify parent
        self.on_click_callback(self.browser_info.name, self.selected)


# ═════════════════════════════════════════════════════════════
# Main Application
# ═════════════════════════════════════════════════════════════


def main(page: ft.Page):
    """Main Flet application"""

    # ─────────────────────────────────────────────────────────
    # Page Configuration (Fixed: 1920x1080의 절반)
    # ─────────────────────────────────────────────────────────

    page.title = "Privacy Eraser"
    page.window.width = 720  # 4:3 비율 (540 * 4/3)
    page.window.height = 540
    page.window.resizable = False  # 크기 고정
    page.padding = 24
    page.bgcolor = AppColors.BACKGROUND
    page.theme_mode = ft.ThemeMode.LIGHT

    # Set custom app icon
    icon_path = get_resource_path("static/icons/app_icon.png")
    if os.path.exists(icon_path):
        page.window.icon = icon_path

    # ─────────────────────────────────────────────────────────
    # Scheduler Initialization
    # ─────────────────────────────────────────────────────────

    from privacy_eraser.scheduler import get_scheduler

    scheduler = get_scheduler()
    scheduler.start()
    logger.info("Background scheduler started")

    # Cleanup on app close
    def on_disconnect(e):
        """Cleanup when app closes"""
        try:
            scheduler.stop()
            logger.info("Background scheduler stopped")
        except Exception as ex:
            logger.error(f"Failed to stop scheduler: {ex}")

    page.on_disconnect = on_disconnect

    # ─────────────────────────────────────────────────────────
    # State
    # ─────────────────────────────────────────────────────────

    detected_browsers = []
    browser_cards_dict = {}
    selected_browsers = {}
    delete_bookmarks = False
    delete_downloads = False
    delete_downloads_folder = False

    # ─────────────────────────────────────────────────────────
    # UI Components
    # ─────────────────────────────────────────────────────────

    # Dev mode toggle switch
    def on_dev_mode_toggle(e):
        """Toggle development mode"""
        new_state = AppConfig.toggle_dev_mode()
        dev_mode_text.value = "DEV" if new_state else "PROD"
        dev_mode_text.color = "#059669" if new_state else AppColors.TEXT_HINT
        logger.info(f"Mode switched to: {'Development' if new_state else 'Production'}")

        # Toggle warning banner visibility
        dev_warning_banner.visible = new_state
        dev_warning_banner.update()

        # DEV 모드로 전환 시 더미 데이터 삭제 후 재생성
        if new_state:
            def generate_test_data_async():
                """Background thread to regenerate test data"""
                try:
                    from privacy_eraser.dev_data_generator import (
                        clean_test_data,
                        generate_all_test_data,
                    )

                    # 기존 테스트 데이터 삭제
                    logger.info("[DEV] Cleaning existing test data...")
                    clean_test_data()

                    # 새로운 테스트 데이터 생성 (force=True로 항상 재생성)
                    logger.info("[DEV] Regenerating test data...")
                    result = generate_all_test_data(force=True)

                    if not result["skipped"]:
                        logger.success(
                            f"[DEV] Test data regenerated: {result['total_files']} files "
                            f"({result['total_size_mb']:.1f} MB)"
                        )
                except Exception as ex:
                    logger.error(f"[DEV] Failed to regenerate test data: {ex}")

            # 백그라운드에서 생성 (UI 블로킹 방지)
            threading.Thread(target=generate_test_data_async, daemon=True).start()
        else:
            # PROD 모드로 전환 시 테스트 데이터 정리
            def clean_test_data_async():
                """Background thread to clean test data"""
                try:
                    from privacy_eraser.dev_data_generator import clean_test_data

                    logger.info("[PROD] Cleaning test data...")
                    clean_test_data()
                    logger.success("[PROD] Test data cleaned")
                except Exception as ex:
                    logger.error(f"[PROD] Failed to clean test data: {ex}")

            # 백그라운드에서 정리 (UI 블로킹 방지)
            threading.Thread(target=clean_test_data_async, daemon=True).start()

        page.update()

    dev_mode_switch = ft.Switch(
        value=AppConfig.is_dev_mode(),
        active_color="#059669",
        width=40,
        height=20,
        on_change=on_dev_mode_toggle,
    )

    dev_mode_text = ft.Text(
        "DEV" if AppConfig.is_dev_mode() else "PROD",
        size=10,
        weight=ft.FontWeight.W_600,
        color="#059669" if AppConfig.is_dev_mode() else AppColors.TEXT_HINT,
    )

    dev_mode_container = ft.Row(
        [
            dev_mode_text,
            dev_mode_switch,
        ],
        spacing=6,
        alignment=ft.MainAxisAlignment.END,
    )

    # Title with dev mode toggle
    title_row = ft.Row(
        [
            ft.Text(
                "Privacy Eraser",
                size=20,
                weight=ft.FontWeight.BOLD,
                color=AppColors.TEXT_PRIMARY,
            ),
            ft.Container(expand=True),  # Spacer
            dev_mode_container,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    # Subtitle
    subtitle = ft.Text(
        "삭제할 브라우저를 선택하세요 (설치된 브라우저만 활성화됨)",
        size=13,  # 14 → 13
        color=AppColors.TEXT_SECONDARY,
    )

    # DEV mode warning banner
    dev_warning_banner = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.INFO_ROUNDED, color=AppColors.WARNING, size=18),
                ft.Text(
                    "개발자 모드: 실제 파일이 삭제되지 않습니다",
                    size=12,
                    weight=ft.FontWeight.W_500,
                    color=AppColors.TEXT_PRIMARY,
                ),
            ],
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        bgcolor=f"{AppColors.WARNING}20",  # 20% opacity
        padding=ft.padding.symmetric(vertical=8, horizontal=12),
        border_radius=6,
        visible=AppConfig.is_dev_mode(),  # Only show in DEV mode
    )

    # Browser cards container (2x4 그리드)
    browser_grid = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=12,
    )

    # Loading indicator
    loading = ft.ProgressRing()
    loading_container = ft.Container(
        content=ft.Column(
            [
                loading,
                ft.Text(
                    "브라우저 검색 중...", size=13, color=AppColors.TEXT_SECONDARY
                ),  # 14 → 13
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,  # 16 → 12
        ),
        padding=24,  # 32 → 24
        alignment=ft.alignment.center,
    )

    # Options checkboxes
    bookmark_checkbox = ft.Checkbox(
        label="북마크 삭제",
        value=False,
        on_change=lambda e: on_bookmark_toggle(e.control.value),
    )

    downloads_checkbox = ft.Checkbox(
        label="다운로드 기록 삭제",
        value=False,
        on_change=lambda e: on_downloads_toggle(e.control.value),
    )

    delete_downloads_folder_checkbox = ft.Checkbox(
        label="[주의] 다운로드 파일 삭제",
        value=False,
        on_change=lambda e: on_delete_downloads_folder_toggle(e.control.value),
    )

    options_row = ft.Row(
        [bookmark_checkbox, downloads_checkbox, delete_downloads_folder_checkbox],
        spacing=20,  # 24 → 20
        alignment=ft.MainAxisAlignment.CENTER,  # 가운데 정렬
    )

    # Info text
    info_text = ft.Text(
        "캐시, 쿠키, 방문기록, 세션, 저장된 비밀번호가 삭제됩니다",
        size=11,  # 12 → 11
        color=AppColors.TEXT_HINT,
    )

    # Buttons (크기 조정)
    undo_button = ft.OutlinedButton(
        "실행 취소",
        width=120,  # 140 → 120
        height=38,  # 44 → 38
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=19),  # 22 → 19
        ),
        on_click=lambda e: show_undo_dialog(),
    )

    delete_button = ft.ElevatedButton(
        "삭제하기",
        width=120,  # 140 → 120
        height=38,  # 44 → 38
        style=ft.ButtonStyle(
            bgcolor=AppColors.DANGER,
            color="#FFFFFF",
            shape=ft.RoundedRectangleBorder(radius=19),  # 22 → 19
        ),
        on_click=lambda e: start_cleaning(),
    )

    # 실행 예약 버튼
    schedule_button = ft.ElevatedButton(
        "실행 예약",
        width=120,
        height=38,
        style=ft.ButtonStyle(
            bgcolor="#059669",  # 초록색 계열
            color="#FFFFFF",
            shape=ft.RoundedRectangleBorder(radius=19),
        ),
        on_click=lambda e: (logger.info("[DEBUG] 실행 예약 버튼 클릭됨"), show_schedule_dialog()),
    )

    # 버튼 레이아웃 (1행에 3개)
    buttons_row = ft.Row(
        [undo_button, schedule_button, delete_button],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=12,
    )

    # Footer (clickable link)
    footer = ft.Row(
        [
            ft.Text(
                "developed by 설코딩 (",
                size=10,
                color=AppColors.TEXT_HINT,
            ),
            ft.Container(
                content=ft.Text(
                    "seolcoding.com",
                    size=10,
                    color=AppColors.PRIMARY,
                    weight=ft.FontWeight.W_500,
                ),
                on_click=lambda _: webbrowser.open("https://seolcoding.com"),
                ink=True,
            ),
            ft.Text(
                ")",
                size=10,
                color=AppColors.TEXT_HINT,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=0,
    )

    # ─────────────────────────────────────────────────────────
    # Event Handlers
    # ─────────────────────────────────────────────────────────

    def on_browser_clicked(browser_name: str, is_selected: bool):
        """Handle browser card selection"""
        nonlocal selected_browsers
        selected_browsers[browser_name] = is_selected
        logger.info(f"{browser_name}: {'selected' if is_selected else 'unselected'}")

    def on_bookmark_toggle(value: bool):
        """Toggle bookmark deletion"""
        nonlocal delete_bookmarks
        delete_bookmarks = value
        logger.info(f"Delete bookmarks: {delete_bookmarks}")

    def on_downloads_toggle(value: bool):
        """Toggle downloads deletion"""
        nonlocal delete_downloads
        delete_downloads = value
        logger.info(f"Delete downloads: {delete_downloads}")

    def on_delete_downloads_folder_toggle(value: bool):
        """Toggle downloads folder deletion"""
        nonlocal delete_downloads_folder
        delete_downloads_folder = value
        logger.info(f"Delete downloads folder: {delete_downloads_folder}")

    def detect_browsers_async():
        """Detect browsers in background thread"""
        nonlocal detected_browsers, browser_cards_dict, selected_browsers

        try:
            # Detect browsers
            browsers_raw = detect_browsers()
            browsers = []

            for browser in browsers_raw:
                browser_name = browser.get("name", "Unknown").lower()
                icon = get_browser_icon(browser_name)
                color = get_browser_color(browser_name)

                browser_info = BrowserInfo(
                    name=browser.get("name", "Unknown"),
                    icon=icon,
                    color=color,
                    installed=browser.get("present") == "yes",
                )
                browsers.append(browser_info)

            detected_browsers = browsers

            # Create browser cards (2x4 grid: 2 rows, 4 columns)
            browser_grid.controls.clear()

            # 브라우저를 2행으로 나누기
            browsers_to_show = browsers[:8]  # Max 8 browsers (2x4)

            # 첫 번째 행 (4개)
            if len(browsers_to_show) > 0:
                row1 = ft.Row(
                    spacing=12,
                    alignment=ft.MainAxisAlignment.CENTER,
                )
                for browser_info in browsers_to_show[:4]:
                    card = BrowserCard(browser_info, on_browser_clicked)
                    browser_cards_dict[browser_info.name] = card
                    selected_browsers[browser_info.name] = browser_info.installed
                    row1.controls.append(card)
                browser_grid.controls.append(row1)

            # 두 번째 행 (4개)
            if len(browsers_to_show) > 4:
                row2 = ft.Row(
                    spacing=12,
                    alignment=ft.MainAxisAlignment.CENTER,
                )
                for browser_info in browsers_to_show[4:8]:
                    card = BrowserCard(browser_info, on_browser_clicked)
                    browser_cards_dict[browser_info.name] = card
                    selected_browsers[browser_info.name] = browser_info.installed
                    row2.controls.append(card)
                browser_grid.controls.append(row2)

            # Replace loading with grid
            main_column.controls[3] = browser_grid

            logger.info(f"Detected {len(browsers)} browsers")
            page.update()

        except Exception as e:
            logger.error(f"Browser detection failed: {e}")
            error_text = ft.Text(
                f"Error detecting browsers: {e}", color=AppColors.DANGER, size=14
            )
            main_column.controls[3] = error_text
            page.update()

    def show_undo_dialog():
        """Show undo/restore dialog - Coming Soon"""

        # 개발 중 안내 대화상자
        coming_soon_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                [
                    ft.Icon(ft.Icons.CONSTRUCTION, color="#F59E0B", size=24),
                    ft.Text(
                        "기능 개발 중",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                    ),
                ],
                spacing=8,
            ),
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text(
                                        "실행 취소 기능",
                                        size=14,
                                        weight=ft.FontWeight.BOLD,
                                        color=AppColors.TEXT_PRIMARY,
                                    ),
                                    ft.Text(
                                        "이 기능은 현재 개발 중입니다.",
                                        size=12,
                                        color=AppColors.TEXT_SECONDARY,
                                    ),
                                ],
                                spacing=4,
                            ),
                            bgcolor="#FEF3C7",
                            padding=12,
                            border_radius=8,
                        ),
                        ft.Container(height=12),
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.INFO_OUTLINE, color=AppColors.PRIMARY, size=20),
                                ft.Text(
                                    "추후 업데이트 예정",
                                    size=11,
                                    color=AppColors.TEXT_SECONDARY,
                                ),
                            ],
                            spacing=8,
                        ),
                        ft.Container(height=8),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Icon(ft.Icons.LOCK, color=AppColors.DANGER, size=18),
                                            ft.Text(
                                                "관리자 전용 기능",
                                                size=11,
                                                weight=ft.FontWeight.W_600,
                                                color=AppColors.DANGER,
                                            ),
                                        ],
                                        spacing=6,
                                    ),
                                    ft.Text(
                                        "실행 취소는 관리자만 사용할 수 있으며\n암호로 보호됩니다.",
                                        size=10,
                                        color=AppColors.TEXT_HINT,
                                        italic=True,
                                    ),
                                ],
                                spacing=4,
                            ),
                            bgcolor="#FEE2E2",
                            padding=10,
                            border_radius=6,
                        ),
                    ],
                    spacing=4,
                ),
                width=280,
            ),
            actions=[
                ft.ElevatedButton(
                    "확인",
                    width=float('inf'),
                    height=40,
                    bgcolor=AppColors.PRIMARY,
                    color="#FFFFFF",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                    on_click=lambda e: close_dialog(coming_soon_dialog),
                ),
            ],
            actions_padding=ft.padding.only(left=24, right=24, bottom=16),
        )

        page.open(coming_soon_dialog)

    def restore_backup(backup_dir: Path):
        """Restore selected backup"""
        # Show progress
        progress_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("복원 중..."),
            content=ft.Column(
                [ft.ProgressRing(), ft.Text("백업 복원 중...", size=14)],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=16,
            ),
        )
        page.open(progress_dialog)

        # Restore in background
        def do_restore():
            backup_manager = BackupManager()
            success = backup_manager.restore_backup(backup_dir)

            # Close progress, show result
            result_dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("복원 완료" if success else "복원 실패"),
                content=ft.Text(
                    "백업이 성공적으로 복원되었습니다!"
                    if success
                    else "백업 복원에 실패했습니다."
                ),
                actions=[
                    ft.TextButton(
                        "확인", on_click=lambda e: close_dialog(result_dialog)
                    )
                ],
            )
            page.open(result_dialog)

        threading.Thread(target=do_restore, daemon=True).start()

    def close_dialog(dialog):
        """Close dialog"""
        page.close(dialog)  # 올바른 Flet 문법 사용

    def start_cleaning():
        """Start cleaning process"""
        selected = [name for name, sel in selected_browsers.items() if sel]

        if not selected:
            # No browsers selected
            warning_dialog = ft.AlertDialog(
                title=ft.Text("브라우저 미선택"),
                content=ft.Text("삭제할 브라우저를 최소 하나 이상 선택해주세요."),
                actions=[
                    ft.TextButton(
                        "확인", on_click=lambda e: close_dialog(warning_dialog)
                    )
                ],
            )
            page.open(warning_dialog)
            return

        # Show confirmation dialog
        show_confirm_delete_dialog(selected)

    def show_confirm_delete_dialog(selected_browsers_list: list[str]):
        """Show confirmation dialog before deletion"""

        # 브라우저 아이콘 매핑
        icon_image_map = {
            "chrome": get_resource_path("static/images/chrome.png"),
            "edge": get_resource_path("static/images/edge.png"),
            "firefox": get_resource_path("static/images/firefox.png"),
            "brave": get_resource_path("static/images/brave.svg"),
            "opera": get_resource_path("static/images/opera logo.png"),
            "whale": get_resource_path("static/images/whale.jpg"),
            "safari": get_resource_path("static/images/safari.png"),
        }

        # 브라우저 카드 생성 (작은 크기)
        browser_cards = []
        for browser_name in selected_browsers_list:
            browser_key = browser_name.lower()
            icon_src = icon_image_map.get(browser_key, icon_image_map.get("chrome"))

            card = ft.Container(
                content=ft.Column(
                    [
                        ft.Image(
                            src=icon_src,
                            width=24,  # 32 → 24
                            height=24,  # 32 → 24
                            fit=ft.ImageFit.CONTAIN,
                        ),
                        ft.Text(
                            browser_name,
                            size=9,  # 10 → 9
                            weight=ft.FontWeight.W_500,
                            color=AppColors.TEXT_PRIMARY,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    spacing=3,  # 4 → 3
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                width=48,  # 64 → 48
                height=48,  # 64 → 48
                bgcolor="#EFF6FF",
                border=ft.border.all(1.5, AppColors.BORDER_SELECTED),  # 2 → 1.5
                border_radius=6,  # 8 → 6
                padding=6,  # 8 → 6
            )
            browser_cards.append(card)

        # 브라우저 카드 Row (1줄로 표시)
        browser_cards_row = ft.Row(
            browser_cards,
            spacing=6,  # 8 → 6
            wrap=False,  # wrap 비활성화 (1줄 고정)
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # 삭제될 항목 목록
        delete_items = [
            "✓ 캐시",
            "✓ 쿠키",
            "✓ 방문기록",
            "✓ 세션",
            "✓ 비밀번호",
        ]

        # 선택적 항목 추가
        if delete_bookmarks:
            delete_items.append("✓ 북마크")
        if delete_downloads:
            delete_items.append("✓ DL기록")
        if delete_downloads_folder:
            delete_items.append("⚠️ DL파일")

        # 삭제될 항목을 2줄로 나누기
        items_per_row = (len(delete_items) + 1) // 2  # 반올림하여 2줄로 나누기
        delete_items_row1 = delete_items[:items_per_row]
        delete_items_row2 = delete_items[items_per_row:]

        # 첫 번째 줄
        items_row1 = ft.Row(
            [
                ft.Text(
                    item,
                    size=10,
                    color=AppColors.DANGER if "⚠️" in item else AppColors.TEXT_SECONDARY,
                )
                for item in delete_items_row1
            ],
            spacing=12,
            wrap=True,
        )

        # 두 번째 줄
        items_row2 = ft.Row(
            [
                ft.Text(
                    item,
                    size=10,
                    color=AppColors.DANGER if "⚠️" in item else AppColors.TEXT_SECONDARY,
                )
                for item in delete_items_row2
            ],
            spacing=12,
            wrap=True,
        )

        # 컨텐츠 구성 (10% 여백 증가)
        content_column = ft.Column(
            [
                # ⚠️ 브라우저 종료 경고
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=AppColors.WARNING, size=16),
                            ft.Text(
                                "선택한 브라우저가 종료됩니다",
                                size=10,
                                weight=ft.FontWeight.W_500,
                                color=AppColors.WARNING,
                            ),
                        ],
                        spacing=6,
                        tight=True,
                    ),
                    bgcolor=f"{AppColors.WARNING}15",  # 15% opacity
                    padding=8,
                    border_radius=6,
                    margin=ft.margin.only(bottom=10),
                ),
                ft.Text(
                    "다음 브라우저의 데이터가 삭제됩니다:",
                    size=11,
                    weight=ft.FontWeight.W_500,
                    color=AppColors.TEXT_PRIMARY,
                ),
                ft.Container(height=5),  # 4 → 5 (+25%)
                browser_cards_row,
                ft.Container(height=7),  # 6 → 7 (+17%)
                ft.Text(
                    "삭제될 항목:",
                    size=11,
                    weight=ft.FontWeight.W_500,
                    color=AppColors.TEXT_PRIMARY,
                ),
                ft.Container(height=3),  # 2 → 3 (+50%)
                items_row1,
                items_row2,
                ft.Container(height=9),  # 8 → 9 (+12.5%)
                # 취소 버튼 (전체 너비, 테두리)
                ft.OutlinedButton(
                    "취소",
                    width=float('inf'),  # 가로 전체
                    height=38,  # 36 → 38 (+5.5%)
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                    on_click=lambda e: close_dialog(confirm_dialog),
                ),
                ft.Container(height=5),  # 4 → 5 (+25%)
                # 삭제하기 버튼 (가로 전체)
                ft.ElevatedButton(
                    "삭제하기",
                    width=float('inf'),  # 가로 전체
                    height=42,  # 40 → 42 (+5%)
                    bgcolor=AppColors.DANGER,
                    color="#FFFFFF",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                    on_click=lambda e: confirm_and_start_cleaning(
                        confirm_dialog, selected_browsers_list
                    ),
                ),
            ],
            spacing=0,
            tight=True,  # 내용물에 맞게 자동 조절
        )

        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                "데이터 삭제 확인",
                size=14,
                weight=ft.FontWeight.BOLD,
            ),
            content=ft.Container(
                content=content_column,
                width=320,  # 너비 고정
            ),
            content_padding=ft.padding.only(left=20, right=20, top=12, bottom=18),  # 10 → 12, 16 → 18
            title_padding=ft.padding.only(left=20, right=20, top=18, bottom=10),  # 16 → 18, 8 → 10
            actions=[],  # 버튼을 content 안에 포함시킴
            actions_padding=0,  # actions 패딩 제거
        )

        page.open(confirm_dialog)

    def confirm_and_start_cleaning(dialog, selected_browsers_list: list[str]):
        """Confirmed - close dialog, kill browser processes, and start cleaning"""
        close_dialog(dialog)
        logger.info(f"User confirmed deletion for: {', '.join(selected_browsers_list)}")

        # Check and kill running browser processes
        running_browsers = check_running_browsers(selected_browsers_list)
        if running_browsers:
            logger.info(f"Killing running browsers: {', '.join(running_browsers)}")
            killed_count, failed = kill_browser_processes(running_browsers)

            if killed_count > 0:
                logger.info(f"Successfully killed {killed_count} browser process(es)")
            if failed:
                logger.warning(f"Failed to kill browsers: {', '.join(failed)}")

            # Wait a moment for processes to fully terminate
            time.sleep(0.5)

        show_progress_dialog(selected_browsers_list)

    def show_schedule_dialog():
        """예약 관리 다이얼로그 (왼쪽: 폼, 오른쪽: 리스트)"""
        schedule_manager = ScheduleManager()

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 브라우저 칩 클래스
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        class BrowserChip:
            def __init__(self, name, icon_src, selected=True):
                self.name = name
                self.icon_src = icon_src
                self.selected = selected

                self.container = ft.Container(
                    content=ft.Image(
                        src=icon_src,
                        width=20,
                        height=20,
                        fit=ft.ImageFit.CONTAIN,
                        opacity=1.0 if selected else 0.4,
                    ),
                    width=36,
                    height=36,
                    bgcolor=AppColors.SURFACE,
                    border=ft.border.all(
                        2,
                        AppColors.BORDER_SELECTED if selected else AppColors.BORDER
                    ),
                    border_radius=8,
                    padding=6,
                    on_click=self.toggle,
                    tooltip=name,
                )

            def toggle(self, e):
                self.selected = not self.selected
                self.container.border = ft.border.all(
                    2,
                    AppColors.BORDER_SELECTED if self.selected else AppColors.BORDER
                )
                self.container.content.opacity = 1.0 if self.selected else 0.4
                page.update()

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 왼쪽: 폼 영역
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        # 편집 모드 추적
        editing_scenario_id = None

        # 폼 필드 (80% 크기)
        name_field = ft.TextField(
            label="시나리오 이름",
            hint_text="예: 주말 정리",
            width=280,
            text_size=12,
        )

        description_field = ft.TextField(
            label="설명 (선택사항)",
            hint_text="시나리오 설명",
            width=280,
            multiline=True,
            max_lines=2,
            text_size=12,
        )

        schedule_type_dropdown = ft.Dropdown(
            label="반복 주기",
            width=120,  # 280 → 120 (한 줄에 배치)
            value="daily",
            text_size=12,
            options=[
                ft.dropdown.Option("once", "일회성"),
                ft.dropdown.Option("hourly", "매시간"),
                ft.dropdown.Option("daily", "매일"),
                ft.dropdown.Option("weekly", "매주"),
                ft.dropdown.Option("monthly", "매월"),
            ],
        )

        hour_field = ft.TextField(
            label="시간",
            value="14",
            width=64,
            keyboard_type=ft.KeyboardType.NUMBER,
            hint_text="0-23",
            text_size=12,
        )

        minute_field = ft.TextField(
            label="분",
            value="0",
            width=64,
            keyboard_type=ft.KeyboardType.NUMBER,
            hint_text="0-59",
            text_size=12,
        )

        # 반복주기, 시간, 분을 한 줄에 배치
        schedule_time_row = ft.Row(
            [
                schedule_type_dropdown,
                hour_field,
                ft.Text(":", size=20, weight=ft.FontWeight.BOLD),
                minute_field,
            ],
            spacing=8,
        )

        # 요일 선택 (weekly용, 80% 크기)
        weekday_checkboxes = []
        weekday_names = ["일", "월", "화", "수", "목", "금", "토"]
        for i, day_name in enumerate(weekday_names):
            cb = ft.Checkbox(
                label=day_name,
                value=False,
                data=i,  # 0=일요일, 6=토요일
                label_style=ft.TextStyle(size=11),
            )
            weekday_checkboxes.append(cb)

        weekday_row = ft.Row(
            weekday_checkboxes,
            spacing=8,
            wrap=True,
            visible=False,  # 기본 숨김
        )

        # 날짜 선택 (monthly용)
        day_of_month_field = ft.TextField(
            label="날짜",
            value="1",
            width=80,
            keyboard_type=ft.KeyboardType.NUMBER,
            hint_text="1-31",
            text_size=12,
            visible=False,  # 기본 숨김
        )

        # 스케줄 타입 변경 시 조건부 UI 업데이트
        def on_schedule_type_change(e):
            is_weekly = schedule_type_dropdown.value == "weekly"
            is_monthly = schedule_type_dropdown.value == "monthly"

            weekday_row.visible = is_weekly
            day_of_month_field.visible = is_monthly
            page.update()

        schedule_type_dropdown.on_change = on_schedule_type_change

        # 브라우저 아이콘 매핑
        icon_image_map = {
            "chrome": get_resource_path("static/images/chrome.png"),
            "edge": get_resource_path("static/images/edge.png"),
            "firefox": get_resource_path("static/images/firefox.png"),
            "brave": get_resource_path("static/images/brave.svg"),
            "opera": get_resource_path("static/images/opera logo.png"),
            "whale": get_resource_path("static/images/whale.jpg"),
            "safari": get_resource_path("static/images/safari.png"),
        }

        # 브라우저 칩 생성
        browser_chips = []
        for browser_name in selected_browsers.keys():
            browser_key = browser_name.lower()
            icon_src = icon_image_map.get(browser_key, icon_image_map["chrome"])
            chip = BrowserChip(browser_name, icon_src, selected=True)
            browser_chips.append(chip)

        browser_chips_row = ft.Row(
            [chip.container for chip in browser_chips],
            wrap=True,
            spacing=8,
            run_spacing=8,
        )

        # 옵션 칩 스타일 (한 줄에 3개)
        class OptionChip:
            def __init__(self, label, initial_value):
                self.label = label
                self.value = initial_value

                self.container = ft.Container(
                    content=ft.Text(
                        label,
                        size=10,
                        color="#FFFFFF" if initial_value else AppColors.TEXT_SECONDARY,
                        weight=ft.FontWeight.W_500,
                    ),
                    bgcolor=AppColors.PRIMARY if initial_value else AppColors.SURFACE,
                    border=ft.border.all(1, AppColors.BORDER if not initial_value else AppColors.PRIMARY),
                    border_radius=12,
                    padding=ft.padding.symmetric(horizontal=10, vertical=4),
                    on_click=self.toggle,
                    ink=True,
                )

            def toggle(self, e):
                self.value = not self.value
                self.container.bgcolor = AppColors.PRIMARY if self.value else AppColors.SURFACE
                self.container.border = ft.border.all(
                    1, AppColors.PRIMARY if self.value else AppColors.BORDER
                )
                self.container.content.color = "#FFFFFF" if self.value else AppColors.TEXT_SECONDARY
                page.update()

        opt_bookmarks = OptionChip("북마크", delete_bookmarks)
        opt_downloads = OptionChip("DL기록", delete_downloads)
        opt_downloads_folder = OptionChip("DL파일", delete_downloads_folder)

        options_row = ft.Row(
            [opt_bookmarks.container, opt_downloads.container, opt_downloads_folder.container],
            spacing=6,
        )

        # 폼 저장 버튼
        def save_scenario(e):
            nonlocal editing_scenario_id

            # 검증
            if not name_field.value or not name_field.value.strip():
                show_error("시나리오 이름을 입력해주세요.")
                return

            try:
                hour = int(hour_field.value)
                minute = int(minute_field.value)
                if not (0 <= hour <= 23) or not (0 <= minute <= 59):
                    raise ValueError()
            except:
                show_error("시간 형식이 올바르지 않습니다. (시간: 0-23, 분: 0-59)")
                return

            selected_browser_list = [chip.name for chip in browser_chips if chip.selected]
            if not selected_browser_list:
                show_error("최소 하나의 브라우저를 선택해주세요.")
                return

            # 주별/월별 검증
            weekdays_list = None
            day_of_month_val = None

            if schedule_type_dropdown.value == "weekly":
                weekdays_list = [cb.data for cb in weekday_checkboxes if cb.value]
                if not weekdays_list:
                    show_error("최소 하나의 요일을 선택해주세요.")
                    return

            if schedule_type_dropdown.value == "monthly":
                try:
                    day_of_month_val = int(day_of_month_field.value)
                    if not (1 <= day_of_month_val <= 31):
                        raise ValueError()
                except:
                    show_error("날짜는 1-31 사이여야 합니다.")
                    return

            # 시나리오 생성 or 업데이트
            time_str = f"{hour:02d}:{minute:02d}"

            if editing_scenario_id:
                # 업데이트
                schedule_manager.update_schedule(
                    editing_scenario_id,
                    name=name_field.value.strip(),
                    description=description_field.value.strip() if description_field.value else "",
                    schedule_type=schedule_type_dropdown.value,
                    time=time_str,
                    weekdays=weekdays_list or [],
                    day_of_month=day_of_month_val,
                    browsers=selected_browser_list,
                    delete_bookmarks=opt_bookmarks.value,
                    delete_downloads=opt_downloads.value,
                    delete_downloads_folder=opt_downloads_folder.value,
                )
                logger.info(f"Updated scenario: {editing_scenario_id}")
            else:
                # 생성
                schedule_manager.create_schedule(
                    name=name_field.value.strip(),
                    description=description_field.value.strip() if description_field.value else "",
                    schedule_type=schedule_type_dropdown.value,
                    time=time_str,
                    weekdays=weekdays_list,
                    day_of_month=day_of_month_val,
                    browsers=selected_browser_list,
                    delete_bookmarks=opt_bookmarks.value,
                    delete_downloads=opt_downloads.value,
                    delete_downloads_folder=opt_downloads_folder.value,
                )
                logger.info(f"Created new scenario: {name_field.value}")

            # 폼 리셋 & 리스트 새로고침
            reset_form()
            refresh_scenario_list()

        def reset_form():
            nonlocal editing_scenario_id
            editing_scenario_id = None

            name_field.value = ""
            description_field.value = ""
            schedule_type_dropdown.value = "daily"
            hour_field.value = "14"
            minute_field.value = "0"

            for cb in weekday_checkboxes:
                cb.value = False
            weekday_row.visible = False

            day_of_month_field.value = "1"
            day_of_month_field.visible = False

            for chip in browser_chips:
                chip.selected = True
                chip.container.border = ft.border.all(2, AppColors.BORDER_SELECTED)
                chip.container.content.opacity = 1.0

            opt_bookmarks.value = delete_bookmarks
            opt_downloads.value = delete_downloads
            opt_downloads_folder.value = delete_downloads_folder

            save_button.text = "저장"
            cancel_button.visible = False

            page.update()

        def show_error(message: str):
            error_dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("입력 오류"),
                content=ft.Text(message),
                actions=[
                    ft.TextButton("확인", on_click=lambda e: close_dialog(error_dialog))
                ],
            )
            page.open(error_dialog)

        save_button = ft.ElevatedButton(
            "저장",
            icon=ft.Icons.SAVE,
            on_click=save_scenario,
        )

        cancel_button = ft.OutlinedButton(
            "취소",
            icon=ft.Icons.CANCEL,
            on_click=lambda e: reset_form(),
            visible=False,
        )

        # Fast Mode 토글 (DEV 전용) - 저장 버튼과 같은 줄
        from privacy_eraser.scheduler import is_fast_mode, set_fast_mode

        def on_fast_mode_toggle(e):
            """Toggle Fast Mode"""
            new_state = e.control.value
            set_fast_mode(new_state)

            # 스케줄러 다시 로드
            scheduler.reload_schedules()

            logger.info(f"Fast Mode: {'enabled' if new_state else 'disabled'}")

            # 사용자 알림
            page.snack_bar = ft.SnackBar(
                content=ft.Text(
                    f"Fast Mode {'활성화' if new_state else '비활성화'} - 스케줄 갱신됨"
                ),
                bgcolor=AppColors.SUCCESS,
            )
            page.snack_bar.open = True
            page.update()

        fast_mode_toggle = ft.Container(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.SPEED, color="#F59E0B", size=14),
                    ft.Text(
                        "Fast",
                        size=10,
                        weight=ft.FontWeight.W_500,
                        color=AppColors.TEXT_HINT,
                    ),
                    ft.Switch(
                        value=is_fast_mode(),
                        active_color="#F59E0B",
                        width=32,
                        height=16,
                        on_change=on_fast_mode_toggle,
                    ),
                ],
                spacing=4,
            ),
            visible=AppConfig.is_dev_mode(),  # DEV 모드에서만 표시
        )

        form_buttons = ft.Row(
            [
                save_button,
                cancel_button,
                ft.Container(expand=True),  # Spacer
                fast_mode_toggle,  # Fast Mode 토글 우측 정렬
            ],
            spacing=12,
            alignment=ft.MainAxisAlignment.START,
        )

        # 폼 필드 영역 (스크롤 가능)
        form_fields = ft.Column(
            [
                name_field,
                description_field,
                ft.Container(height=6),
                schedule_time_row,  # 반복주기, 시간, 분 한 줄에
                weekday_row,
                day_of_month_field,
                ft.Container(height=6),
                ft.Text("브라우저 선택", size=11, weight=ft.FontWeight.W_600),
                browser_chips_row,
                ft.Container(height=6),
                ft.Text("옵션", size=11, weight=ft.FontWeight.W_600),
                options_row,
            ],
            spacing=6,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

        # 폼 전체 (제목 + 스크롤 영역 + 고정 버튼)
        form_column = ft.Column(
            [
                ft.Text("시나리오 설정", size=13, weight=ft.FontWeight.BOLD),
                ft.Divider(height=1, color=AppColors.BORDER),
                form_fields,
                ft.Divider(height=1, color=AppColors.BORDER),
                form_buttons,
            ],
            spacing=6,
            width=310,
        )

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 오른쪽: 리스트 영역
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        scenario_list_column = ft.Column(
            spacing=8,
            scroll=ft.ScrollMode.AUTO,
        )

        def format_schedule_info(scenario: ScheduleScenario) -> str:
            """스케줄 정보를 문자열로 포맷"""
            type_map = {
                "once": "일회성",
                "hourly": "매시간",
                "daily": "매일",
                "weekly": "매주",
                "monthly": "매월",
            }

            schedule_str = f"{type_map.get(scenario.schedule_type, scenario.schedule_type)} {scenario.time}"

            if scenario.schedule_type == "weekly" and scenario.weekdays:
                weekday_names_kr = ["일", "월", "화", "수", "목", "금", "토"]
                days_str = ", ".join([weekday_names_kr[d] for d in sorted(scenario.weekdays)])
                schedule_str += f" ({days_str})"

            if scenario.schedule_type == "monthly" and scenario.day_of_month:
                schedule_str += f" (매월 {scenario.day_of_month}일)"

            return schedule_str

        def create_scenario_card(scenario: ScheduleScenario):
            """시나리오 카드 생성"""

            # 토글 스위치 (70% 크기)
            toggle_switch = ft.Switch(
                value=scenario.enabled,
                width=28,  # 기본 40 * 0.7 = 28
                height=14,  # 기본 20 * 0.7 = 14
                on_change=lambda e: toggle_scenario(scenario.id, e.control.value),
            )

            # 지금 실행 버튼
            def run_now(e):
                """시나리오를 즉시 실행"""
                import threading
                from privacy_eraser.schedule_executor import execute_scenario

                logger.info(f"[TEST] Running scenario now: {scenario.name}")

                def run_in_background():
                    execute_scenario(scenario)

                threading.Thread(target=run_in_background, daemon=True).start()

                # 사용자 알림
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"'{scenario.name}' 실행 중... 알림을 확인하세요."),
                    bgcolor=AppColors.SUCCESS,
                )
                page.snack_bar.open = True
                page.update()

            run_now_btn = ft.IconButton(
                icon=ft.Icons.PLAY_ARROW,
                icon_size=18,
                icon_color=AppColors.SUCCESS,
                tooltip="지금 실행",
                on_click=run_now,
            )

            # 편집 버튼
            edit_btn = ft.IconButton(
                icon=ft.Icons.EDIT,
                icon_size=18,
                tooltip="편집",
                on_click=lambda e: edit_scenario(scenario),
            )

            # 삭제 버튼
            delete_btn = ft.IconButton(
                icon=ft.Icons.DELETE,
                icon_size=18,
                icon_color=AppColors.DANGER,
                tooltip="삭제",
                on_click=lambda e: confirm_delete_scenario(scenario),
            )

            # 카드 내용 (새 레이아웃: 제목→설명→버튼들)
            card_content = ft.Container(
                content=ft.Column(
                    [
                        # 첫 줄: 제목
                        ft.Text(
                            scenario.name,
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=AppColors.TEXT_PRIMARY,
                        ),
                        # 둘째 줄: 스케줄 정보
                        ft.Text(
                            format_schedule_info(scenario),
                            size=12,
                            color=AppColors.TEXT_SECONDARY,
                        ),
                        # 셋째 줄: 브라우저 (전체 가로 크기)
                        ft.Text(
                            f"브라우저: {', '.join(scenario.browsers)}",
                            size=11,
                            color=AppColors.TEXT_HINT,
                        ),
                        # 넷째 줄: 토글 | 실행 | 수정 | 삭제
                        ft.Row(
                            [
                                toggle_switch,
                                run_now_btn,
                                edit_btn,
                                delete_btn,
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=4,
                        ),
                    ],
                    spacing=4,
                ),
                bgcolor=AppColors.SURFACE if scenario.enabled else "#F9F9F9",
                border=ft.border.all(
                    1,
                    AppColors.BORDER_SELECTED if scenario.enabled else AppColors.BORDER
                ),
                border_radius=8,
                padding=12,
            )

            return card_content

        def refresh_scenario_list():
            """시나리오 리스트 새로고침"""
            scenarios = schedule_manager.get_all_schedules()
            scenario_list_column.controls.clear()

            if not scenarios:
                scenario_list_column.controls.append(
                    ft.Container(
                        content=ft.Text(
                            "등록된 시나리오가 없습니다.\n왼쪽에서 새 시나리오를 만드세요.",
                            size=13,
                            color=AppColors.TEXT_HINT,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        padding=32,
                        alignment=ft.alignment.center,
                    )
                )
            else:
                for scenario in scenarios:
                    scenario_list_column.controls.append(create_scenario_card(scenario))

            page.update()

        def toggle_scenario(scenario_id: str, new_value: bool):
            """시나리오 활성화/비활성화"""
            schedule_manager.update_schedule(scenario_id, enabled=new_value)
            logger.info(f"Toggled scenario {scenario_id}: {new_value}")
            refresh_scenario_list()

        def edit_scenario(scenario: ScheduleScenario):
            """시나리오 편집"""
            nonlocal editing_scenario_id
            editing_scenario_id = scenario.id

            # 폼에 값 채우기
            name_field.value = scenario.name
            description_field.value = scenario.description or ""
            schedule_type_dropdown.value = scenario.schedule_type

            hour, minute = scenario.time.split(":")
            hour_field.value = str(int(hour))
            minute_field.value = str(int(minute))

            # 조건부 UI 표시
            weekday_row.visible = scenario.schedule_type == "weekly"
            day_of_month_field.visible = scenario.schedule_type == "monthly"

            # 요일 설정
            if scenario.schedule_type == "weekly":
                for cb in weekday_checkboxes:
                    cb.value = cb.data in scenario.weekdays

            # 날짜 설정
            if scenario.schedule_type == "monthly" and scenario.day_of_month:
                day_of_month_field.value = str(scenario.day_of_month)

            # 브라우저 설정
            for chip in browser_chips:
                chip.selected = chip.name in scenario.browsers
                chip.container.border = ft.border.all(
                    2,
                    AppColors.BORDER_SELECTED if chip.selected else AppColors.BORDER
                )
                chip.container.content.opacity = 1.0 if chip.selected else 0.4

            # 옵션 설정
            opt_bookmarks.value = scenario.delete_bookmarks
            opt_downloads.value = scenario.delete_downloads
            opt_downloads_folder.value = scenario.delete_downloads_folder

            # 버튼 변경
            save_button.text = "수정"
            cancel_button.visible = True

            page.update()
            logger.info(f"Editing scenario: {scenario.name}")

        def confirm_delete_scenario(scenario: ScheduleScenario):
            """시나리오 삭제 확인"""
            confirm_dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("시나리오 삭제"),
                content=ft.Text(f"'{scenario.name}' 시나리오를 삭제하시겠습니까?"),
                actions=[
                    ft.TextButton("취소", on_click=lambda e: close_dialog(confirm_dialog)),
                    ft.ElevatedButton(
                        "삭제",
                        bgcolor=AppColors.DANGER,
                        color="#FFFFFF",
                        on_click=lambda e: delete_scenario(scenario.id, confirm_dialog),
                    ),
                ],
            )
            page.open(confirm_dialog)

        def delete_scenario(scenario_id: str, confirm_dialog):
            """시나리오 삭제"""
            success = schedule_manager.delete_schedule(scenario_id)
            close_dialog(confirm_dialog)

            if success:
                logger.info(f"Deleted scenario: {scenario_id}")
                refresh_scenario_list()
            else:
                show_error("시나리오 삭제에 실패했습니다.")

        # 리스트 영역 전체
        list_container = ft.Container(
            content=ft.Column(
                [
                    ft.Text("등록된 시나리오", size=16, weight=ft.FontWeight.BOLD),
                    ft.Divider(height=1, color=AppColors.BORDER),
                    scenario_list_column,
                ],
                spacing=8,
            ),
            expand=True,
        )

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # 다이얼로그 레이아웃 (왼쪽/오른쪽 분할)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        dialog_content = ft.Row(
            [
                ft.Container(
                    content=form_column,
                    padding=16,
                ),
                ft.VerticalDivider(width=1, color=AppColors.BORDER),
                ft.Container(
                    content=list_container,
                    padding=16,
                    expand=True,
                ),
            ],
            spacing=0,
            expand=True,
        )

        schedule_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("예약 관리", size=18, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=dialog_content,
                width=900,
                height=550,  # 580 → 550 (Fast Mode 토글이 제목줄로 이동)
            ),
            actions=[
                ft.TextButton(
                    "닫기",
                    on_click=lambda e: close_dialog(schedule_dialog),
                ),
            ],
        )

        # 초기 리스트 로드
        refresh_scenario_list()

        # 다이얼로그 표시
        page.open(schedule_dialog)
        logger.info("Schedule management dialog opened")

    def show_progress_dialog(selected_browsers_list: list[str]):
        """Show progress dialog with detailed progress tracking"""

        # 브라우저 아이콘 매핑
        icon_image_map = {
            "chrome": get_resource_path("static/images/chrome.png"),
            "edge": get_resource_path("static/images/edge.png"),
            "firefox": get_resource_path("static/images/firefox.png"),
            "brave": get_resource_path("static/images/brave.svg"),
            "opera": get_resource_path("static/images/opera logo.png"),
            "whale": get_resource_path("static/images/whale.jpg"),
            "safari": get_resource_path("static/images/safari.png"),
        }

        # 브라우저별 진행 상태 추적 (배경색 채우기 방식)
        browser_progress = {}
        for browser in selected_browsers_list:
            # 브라우저 아이콘
            browser_key = browser.lower()
            icon_src = icon_image_map.get(browser_key, icon_image_map.get("chrome"))

            # 진행 배경 Container (동적으로 width 변경)
            progress_bg = ft.Container(
                width=0,  # 초기값 0
                height=70,
                bgcolor="#E3F2FD",  # 연한 파란색
                border_radius=8,
            )

            # 브라우저 아이콘
            browser_icon = ft.Image(
                src=icon_src,
                width=32,
                height=32,
                fit=ft.ImageFit.CONTAIN,
            )

            # 브라우저 이름과 진행률 텍스트
            name_text = ft.Text(
                browser,
                size=12,
                weight=ft.FontWeight.BOLD,
                color=AppColors.TEXT_PRIMARY,
            )
            progress_text = ft.Text(
                "0/0 (0%)",
                size=11,
                color=AppColors.TEXT_SECONDARY,
            )

            # Stack으로 배경 + 텍스트 겹치기
            card = ft.Container(
                content=ft.Stack(
                    [
                        progress_bg,  # 배경 (진행률에 따라 늘어남)
                        ft.Container(
                            content=ft.Row(
                                [
                                    browser_icon,
                                    ft.Column(
                                        [name_text, progress_text],
                                        spacing=2,
                                    ),
                                ],
                                spacing=10,
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            padding=12,
                        ),
                    ]
                ),
                width=230,
                height=70,
                bgcolor="#F9F9F9",  # 기본 배경
                border=ft.border.all(1, AppColors.BORDER),
                border_radius=8,
            )

            browser_progress[browser] = {
                "total": 0,
                "current": 0,
                "progress_bg": progress_bg,  # 배경 Container
                "name_text": name_text,
                "progress_text": progress_text,
                "card": card,
            }

        # Grid 레이아웃 (2열)
        browser_cards_rows = []
        for i in range(0, len(selected_browsers_list), 2):
            row_browsers = selected_browsers_list[i:i+2]
            row = ft.Row(
                [browser_progress[b]["card"] for b in row_browsers],
                spacing=12,
                alignment=ft.MainAxisAlignment.CENTER,
            )
            browser_cards_rows.append(row)

        browser_progress_column = ft.Column(
            browser_cards_rows,
            spacing=8,
        )

        # 실시간 파일 목록 (최대 100개 표시)
        file_list_column = ft.ListView(
            spacing=2,
            height=150,
            auto_scroll=True,
        )

        # 전체 진행 상태
        overall_progress_bar = ft.ProgressBar(width=450, value=0)
        overall_text = ft.Text("준비 중...", size=13, weight=ft.FontWeight.W_500)

        progress_content = ft.Container(
            content=ft.Column(
                [
                    overall_text,
                    overall_progress_bar,
                    ft.Divider(height=1, color=AppColors.BORDER),
                    ft.Text("브라우저별 진행 상황", size=12, weight=ft.FontWeight.W_600),
                    browser_progress_column,
                    ft.Divider(height=1, color=AppColors.BORDER),
                    ft.Text("삭제된 파일 (최근 100개)", size=12, weight=ft.FontWeight.W_600),
                    ft.Container(
                        content=file_list_column,
                        bgcolor="#F9F9F9",
                        border=ft.border.all(1, AppColors.BORDER),
                        border_radius=4,
                        padding=8,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.START,
                spacing=12,
                scroll=ft.ScrollMode.AUTO,
            ),
            width=500,
            height=450,
        )

        progress_dialog = ft.AlertDialog(
            title=ft.Text("개인정보 삭제 중"),
            content=progress_content,
            modal=True,
        )

        page.open(progress_dialog)

        # 브라우저별 파일 카운트 초기화 (작업 시작 전)
        total_files_count = 0
        deleted_files_count = 0

        # Callbacks for cleaner worker
        def on_started():
            """Called when cleaning starts"""
            pass

        def on_browser_counts(counts: dict[str, int]):
            """Called when browser file counts are ready"""
            nonlocal total_files_count

            # 브라우저별 total 설정
            for browser, count in counts.items():
                if browser in browser_progress:
                    browser_progress[browser]["total"] = count
                    browser_progress[browser]["progress_text"].value = f"0/{count} (0%)"

            # 전체 파일 개수
            total_files_count = sum(counts.values())
            overall_text.value = f"전체: 0/{total_files_count} 파일 (0%)"

            page.update()
            logger.info(f"Browser counts: {counts}, Total: {total_files_count}")

        def on_progress(file_path: str, file_size: int):
            """Called for each deleted file"""
            nonlocal deleted_files_count

            deleted_files_count += 1

            # 파일이 속한 브라우저 찾기
            file_browser = None
            for browser in selected_browsers_list:
                if browser.lower() in file_path.lower():
                    file_browser = browser
                    break

            # 브라우저별 진행률 업데이트 (배경색 채우기)
            if file_browser and file_browser in browser_progress:
                bp = browser_progress[file_browser]
                bp["current"] += 1

                if bp["total"] > 0:
                    progress_value = bp["current"] / bp["total"]
                    # 배경 Container의 width를 조절 (230px 카드 전체 너비)
                    bp["progress_bg"].width = 230 * progress_value
                    bp["progress_text"].value = f"{bp['current']}/{bp['total']} ({progress_value*100:.0f}%)"

            # 전체 진행률 업데이트
            if total_files_count > 0:
                overall_progress = deleted_files_count / total_files_count
                overall_progress_bar.value = overall_progress
                overall_text.value = f"전체: {deleted_files_count}/{total_files_count} 파일 ({overall_progress*100:.0f}%)"

            # 파일 목록에 추가 (최근 100개만 유지)
            file_name = Path(file_path).name

            # 최대 100개만 유지 (먼저 체크)
            if len(file_list_column.controls) >= 100:
                file_list_column.controls.pop(0)

            file_list_column.controls.append(
                ft.Text(
                    f"[OK] {file_name}",
                    size=10,
                    color=AppColors.TEXT_SECONDARY,
                )
            )

            # 맨 아래로 스크롤 (명시적으로)
            try:
                file_list_column.scroll_to(offset=-1, duration=100)
            except:
                pass  # 스크롤 실패 시 무시

            page.update()

        def on_finished(stats: CleaningStats):
            """Called when cleaning finishes"""
            # 통계 화면으로 전환
            overall_progress_bar.value = 1.0
            overall_text.value = "[완료] 삭제 완료!"
            overall_text.color = AppColors.SUCCESS
            overall_text.size = 16

            # 브라우저별 통계 카드 생성 (Grid 레이아웃)
            browser_stats_cards = []

            for browser in selected_browsers_list:
                bp = browser_progress[browser]

                # 브라우저 아이콘
                browser_key = browser.lower()
                icon_src = icon_image_map.get(browser_key, icon_image_map.get("chrome"))

                browser_icon = ft.Image(
                    src=icon_src,
                    width=24,  # 28 → 24
                    height=24,  # 28 → 24
                    fit=ft.ImageFit.CONTAIN,
                )

                card = ft.Container(
                    content=ft.Column(
                        [
                            browser_icon,
                            ft.Text(
                                browser,
                                size=11,  # 12 → 11
                                weight=ft.FontWeight.BOLD,
                                color=AppColors.TEXT_PRIMARY,
                            ),
                            ft.Text(
                                f"{bp['current']}개",  # "파일" 제거
                                size=10,  # 11 → 10
                                color=AppColors.TEXT_SECONDARY,
                            ),
                        ],
                        spacing=3,  # 4 → 3
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    width=96,  # 120 → 96 (80%)
                    height=76,  # 95 → 76 (80%)
                    bgcolor="#E3F2FD",  # 연한 파란색
                    border=ft.border.all(1, AppColors.BORDER_SELECTED),
                    border_radius=8,
                    padding=10,  # 12 → 10
                    alignment=ft.alignment.center,
                )
                browser_stats_cards.append(card)

            # Grid 레이아웃 (3열)
            stats_rows = []
            for i in range(0, len(browser_stats_cards), 3):
                row_cards = browser_stats_cards[i:i+3]
                row = ft.Row(
                    row_cards,
                    spacing=12,
                    alignment=ft.MainAxisAlignment.CENTER,
                )
                stats_rows.append(row)

            # UI를 통계 화면으로 교체
            progress_content.content.controls.clear()
            progress_content.content.controls.extend([
                ft.Row(
                    [
                        overall_text,
                        ft.Text(
                            f"소요시간: {stats.duration:.1f}초",
                            size=13,
                            color=AppColors.TEXT_SECONDARY,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(height=1, color=AppColors.BORDER),
                ft.Text(
                    f"총 {stats.deleted_files}개 파일 ({stats.deleted_size_mb:.1f} MB) 삭제됨",
                    size=14,
                    weight=ft.FontWeight.W_500,
                ),
                ft.Divider(height=1, color=AppColors.BORDER),
                ft.Text("브라우저별 상세", size=13, weight=ft.FontWeight.W_600),
                ft.Column(stats_rows, spacing=8),
            ])

            # Add close button
            progress_dialog.actions = [
                ft.TextButton("닫기", on_click=lambda e: close_dialog(progress_dialog))
            ]

            page.update()

        def on_error(error: str):
            """Called when error occurs"""
            overall_text.value = f"오류 발생: {error}"
            overall_text.color = AppColors.DANGER
            progress_dialog.actions = [
                ft.TextButton("닫기", on_click=lambda e: close_dialog(progress_dialog))
            ]
            page.update()

        # Start cleaner worker with callbacks
        cleaner_worker = FletCleanerWorker(
            browsers=selected_browsers_list,
            delete_bookmarks=delete_bookmarks,
            delete_downloads=delete_downloads,
            on_started=on_started,
            on_browser_counts=on_browser_counts,
            on_progress=on_progress,
            on_finished=on_finished,
            on_error=on_error,
        )

        # Start worker
        cleaner_worker.start()

    # ─────────────────────────────────────────────────────────
    # Main Layout
    # ─────────────────────────────────────────────────────────

    main_column = ft.Column(
        [
            title_row,
            subtitle,
            dev_warning_banner,  # DEV mode warning
            ft.Container(height=12),  # Spacing (16 → 12)
            loading_container,  # Will be replaced with browser_grid
            ft.Container(height=20),  # Spacing (32 → 20)
            ft.Text(
                "Options",
                size=13,
                weight=ft.FontWeight.W_600,
                color=AppColors.TEXT_SECONDARY,
            ),  # 14 → 13
            options_row,
            info_text,
            ft.Container(expand=True),  # Spacer
            buttons_row,
            ft.Container(height=12),  # Spacing (16 → 12)
            footer,
        ],
        spacing=6,  # 8 → 6
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # 가운데 정렬
    )

    page.add(main_column)

    # ─────────────────────────────────────────────────────────
    # Initialize: Detect browsers
    # ─────────────────────────────────────────────────────────

    threading.Thread(target=detect_browsers_async, daemon=True).start()


# ═════════════════════════════════════════════════════════════
# Entry Point
# ═════════════════════════════════════════════════════════════


def main_entry():
    """Entry point for script"""
    logger.info("Privacy Eraser (Flet) starting...")
    ft.app(target=main)


if __name__ == "__main__":
    main_entry()
