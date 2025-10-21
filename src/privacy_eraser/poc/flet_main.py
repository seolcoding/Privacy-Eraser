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
import glob

from privacy_eraser.detect_windows import detect_browsers
from privacy_eraser.poc.core.browser_info import BrowserInfo, CleaningStats
from privacy_eraser.poc.core.data_config import (
    get_browser_icon,
    get_browser_color,
    get_browser_display_name,
    get_browser_xml_path,
    get_cleaner_options,
)
from privacy_eraser.poc.core.backup_manager import BackupManager


# ═════════════════════════════════════════════════════════════
# Design Tokens (Material Design 3)
# ═════════════════════════════════════════════════════════════


class AppColors:
    """Color palette"""

    BACKGROUND = "#FAFAFA"
    SURFACE = "#FFFFFF"
    PRIMARY = "#2563EB"
    DANGER = "#DC2626"
    SUCCESS = "#059669"
    TEXT_PRIMARY = "#1A1A1A"
    TEXT_SECONDARY = "#666666"
    TEXT_HINT = "#999999"
    BORDER = "#E5E5E5"
    BORDER_HOVER = "#CCCCCC"
    BORDER_SELECTED = "#2563EB"


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
            # Collect files
            all_files = self._collect_files_to_delete()
            stats.total_files = len(all_files)
            stats.total_size = sum(
                self._get_file_size(f) for f in all_files if os.path.exists(f)
            )

            logger.info(
                f"삭제 대상: {stats.total_files} 파일, {stats.total_size / (1024 * 1024):.1f} MB"
            )

            # Create backup
            existing_files = [Path(f) for f in all_files if os.path.exists(f)]
            if existing_files:
                backup_dir = self.backup_manager.create_backup(
                    files_to_backup=existing_files,
                    browsers=self.browsers,
                    delete_bookmarks=self.delete_bookmarks,
                    delete_downloads=self.delete_downloads,
                )
                if backup_dir:
                    logger.info(f"백업 생성 완료: {backup_dir}")

                # Cleanup old backups
                deleted = self.backup_manager.cleanup_old_backups()
                if deleted > 0:
                    logger.info(f"{deleted}개 오래된 백업 정리됨")

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

    def _collect_files_to_delete(self) -> list[str]:
        """Collect files to delete"""
        files = []
        options = get_cleaner_options(self.delete_bookmarks, self.delete_downloads)

        for browser in self.browsers:
            try:
                browser_files = self._get_browser_files(browser, options)
                files.extend(browser_files)
                logger.info(f"{browser}: {len(browser_files)} 파일 수집됨")
            except Exception as e:
                logger.warning(f"{browser} 파일 수집 실패: {e}")

        return files

    def _get_browser_files(self, browser_name: str, options: list[str]) -> list[str]:
        """Get files for specific browser"""
        files = []

        try:
            xml_path = get_browser_xml_path(browser_name)
            if not xml_path:
                logger.warning(f"CleanerML 경로 없음: {browser_name}")
                return files

            from privacy_eraser.cleanerml_loader import load_cleanerml

            cleaner_def = load_cleanerml(xml_path)

            for option in options:
                try:
                    actions = cleaner_def.get_actions(option)
                    for action in actions:
                        expanded = self._expand_path(action.path)
                        files.extend(expanded)
                except Exception as e:
                    logger.debug(f"옵션 {option} 처리 실패: {e}")

        except Exception as e:
            logger.warning(f"{browser_name} CleanerML 처리 실패: {e}")

        return files

    def _expand_path(self, path: str) -> list[str]:
        """Expand environment variables and glob patterns"""
        expanded_files = []

        try:
            expanded = os.path.expandvars(path)

            if "*" in expanded or "?" in expanded:
                matched = glob.glob(expanded, recursive=True)
                expanded_files.extend(matched)
            else:
                if os.path.exists(expanded):
                    expanded_files.append(expanded)

        except Exception as e:
            logger.debug(f"경로 확장 실패 {path}: {e}")

        return expanded_files

    def _safe_delete(self, path: str):
        """Safely delete file or directory"""
        try:
            from privacy_eraser.core.file_utils import safe_delete

            safe_delete(path)
        except Exception:
            try:
                if os.path.isdir(path):
                    import shutil

                    shutil.rmtree(path, ignore_errors=True)
                else:
                    os.remove(path)
            except Exception as retry_error:
                logger.warning(f"파일 삭제 재시도 실패 {path}: {retry_error}")
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
            "chrome": "static/images/chrome.png",
            "edge": "static/images/edge.png",
            "firefox": "static/images/firefox.png",
            "brave": "static/images/brave.svg",
            "opera": "static/images/opera logo.png",
            "whale": "static/images/whale.jpg",
            "safari": "static/images/safari.png",
        }

        # 브라우저 이름 소문자로 변환하여 매칭
        browser_key = browser_info.name.lower()
        icon_src = icon_image_map.get(browser_key, "static/images/chrome.png")

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

    # Title (크기 조정)
    title = ft.Text(
        "Privacy Eraser",
        size=20,  # 24 → 20 (0.83배)
        weight=ft.FontWeight.BOLD,
        color=AppColors.TEXT_PRIMARY,
    )

    # Subtitle
    subtitle = ft.Text(
        "삭제할 브라우저를 선택하세요 (설치된 브라우저만 활성화됨)",
        size=13,  # 14 → 13
        color=AppColors.TEXT_SECONDARY,
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
        label="⚠️ 다운로드 파일 삭제",
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
        on_click=lambda e: show_schedule_dialog(),
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
                "developed with ❤️ by 설코딩 (",
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
        """Show undo/restore dialog"""
        backup_manager = BackupManager()
        backups = backup_manager.list_backups()

        if not backups:
            # No backups available
            no_backup_dialog = ft.AlertDialog(
                title=ft.Text("백업 없음"),
                content=ft.Text("복원 가능한 백업이 없습니다."),
                actions=[
                    ft.TextButton(
                        "확인", on_click=lambda e: close_dialog(no_backup_dialog)
                    )
                ],
            )
            page.dialog = no_backup_dialog
            no_backup_dialog.open = True
            page.update()
            return

        # Create backup list
        backup_items = []
        for backup_dir, metadata in backups[:5]:  # Show latest 5
            backup_items.append(
                ft.ListTile(
                    title=ft.Text(metadata.display_name),
                    subtitle=ft.Text(
                        f"{', '.join(metadata.browsers)} • {metadata.files_count}개 파일 • "
                        f"{metadata.total_size / (1024 * 1024):.1f} MB"
                    ),
                    on_click=lambda e, bd=backup_dir: restore_backup(bd),
                )
            )

        undo_dialog = ft.AlertDialog(
            title=ft.Text("백업 복원"),
            content=ft.Column(backup_items, height=300, scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("취소", on_click=lambda e: close_dialog(undo_dialog))
            ],
        )

        page.dialog = undo_dialog
        undo_dialog.open = True
        page.update()

    def restore_backup(backup_dir: Path):
        """Restore selected backup"""
        page.dialog.open = False
        page.update()

        # Show progress
        progress_dialog = ft.AlertDialog(
            title=ft.Text("복원 중..."),
            content=ft.Column(
                [ft.ProgressRing(), ft.Text("백업 복원 중...", size=14)],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=16,
            ),
        )
        page.dialog = progress_dialog
        progress_dialog.open = True
        page.update()

        # Restore in background
        def do_restore():
            backup_manager = BackupManager()
            success = backup_manager.restore_backup(backup_dir)

            # Close progress, show result
            page.dialog.open = False

            result_dialog = ft.AlertDialog(
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
            page.dialog = result_dialog
            result_dialog.open = True
            page.update()

        threading.Thread(target=do_restore, daemon=True).start()

    def close_dialog(dialog):
        """Close dialog"""
        dialog.open = False
        page.update()

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
            page.dialog = warning_dialog
            warning_dialog.open = True
            page.update()
            return

        logger.info(f"Starting deletion for: {', '.join(selected)}")
        show_progress_dialog(selected)

    def show_schedule_dialog():
        """예약 실행 설정 다이얼로그"""
        # 시간 선택 필드
        hour_field = ft.TextField(
            label="시간 (0-23)",
            value="0",
            width=100,
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        minute_field = ft.TextField(
            label="분 (0-59)",
            value="0",
            width=100,
            keyboard_type=ft.KeyboardType.NUMBER,
        )

        # 반복 설정
        repeat_dropdown = ft.Dropdown(
            label="반복",
            width=150,
            value="once",
            options=[
                ft.dropdown.Option("once", "일회성"),
                ft.dropdown.Option("daily", "매일"),
                ft.dropdown.Option("weekly", "매주"),
            ],
        )

        # 브라우저 선택 체크박스
        schedule_checkboxes = []
        for browser_name in selected_browsers.keys():
            cb = ft.Checkbox(label=browser_name, value=True)
            schedule_checkboxes.append(cb)

        schedule_dialog = ft.AlertDialog(
            title=ft.Text("예약 실행 설정"),
            content=ft.Column(
                [
                    ft.Text("실행 시간", weight=ft.FontWeight.BOLD),
                    ft.Row([hour_field, ft.Text(":"), minute_field], spacing=8),
                    ft.Container(height=16),
                    repeat_dropdown,
                    ft.Container(height=16),
                    ft.Text("삭제할 브라우저", weight=ft.FontWeight.BOLD),
                    ft.Column(schedule_checkboxes, spacing=8),
                ],
                tight=True,
                width=400,
                height=400,
                scroll=ft.ScrollMode.AUTO,
            ),
            actions=[
                ft.TextButton("취소", on_click=lambda e: close_dialog(schedule_dialog)),
                ft.ElevatedButton(
                    "예약하기",
                    on_click=lambda e: create_schedule(
                        hour_field.value,
                        minute_field.value,
                        repeat_dropdown.value,
                        schedule_checkboxes,
                        schedule_dialog,
                    ),
                ),
            ],
        )
        page.dialog = schedule_dialog
        schedule_dialog.open = True
        page.update()

    def create_schedule(hour, minute, repeat_type, checkboxes, dialog):
        """예약 작업 생성"""
        try:
            selected_for_schedule = [cb.label for cb in checkboxes if cb.value]

            if not selected_for_schedule:
                error_dialog = ft.AlertDialog(
                    title=ft.Text("브라우저 미선택"),
                    content=ft.Text("최소 하나의 브라우저를 선택해주세요."),
                    actions=[
                        ft.TextButton(
                            "확인", on_click=lambda e: close_dialog(error_dialog)
                        )
                    ],
                )
                page.dialog = error_dialog
                error_dialog.open = True
                page.update()
                return

            dialog.open = False

            # 예약 정보 표시
            result_dialog = ft.AlertDialog(
                title=ft.Text("예약 완료"),
                content=ft.Text(
                    f"✅ 예약이 설정되었습니다.\n\n"
                    f"시간: {hour}:{minute}\n"
                    f"반복: {repeat_type}\n"
                    f"브라우저: {', '.join(selected_for_schedule)}\n\n"
                    f"(실제 예약 기능은 구현 예정)"
                ),
                actions=[
                    ft.TextButton(
                        "확인", on_click=lambda e: close_dialog(result_dialog)
                    )
                ],
            )
            page.dialog = result_dialog
            result_dialog.open = True
            page.update()

        except Exception as e:
            error_dialog = ft.AlertDialog(
                title=ft.Text("오류 발생"),
                content=ft.Text(f"예약 설정 중 오류가 발생했습니다:\n{str(e)}"),
                actions=[
                    ft.TextButton("확인", on_click=lambda e: close_dialog(error_dialog))
                ],
            )
            page.dialog = error_dialog
            error_dialog.open = True
            page.update()

    def show_progress_dialog(selected_browsers_list: list[str]):
        """Show progress dialog and start cleaning"""

        # Progress components
        progress_bar = ft.ProgressBar(width=400, value=0)
        progress_text = ft.Text("시작 중...", size=14)
        stats_text = ft.Text("", size=12, color=AppColors.TEXT_SECONDARY)

        progress_content = ft.Column(
            [progress_bar, progress_text, stats_text],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=16,
            width=450,
        )

        progress_dialog = ft.AlertDialog(
            title=ft.Text("개인정보 삭제 중"), content=progress_content, modal=True
        )

        page.dialog = progress_dialog
        progress_dialog.open = True
        page.update()

        # Callbacks for cleaner worker
        def on_progress(file_path: str, file_size: int):
            progress_text.value = f"삭제 중: {Path(file_path).name}"
            page.update()

        def on_finished(stats: CleaningStats):
            # Show completion
            progress_bar.value = 1.0
            progress_text.value = "삭제 완료!"
            stats_text.value = (
                f"✅ 삭제 완료: {stats.deleted_files}/{stats.total_files}개 파일 "
                f"({stats.deleted_size_mb:.1f} MB)\n"
                f"⏱️ 소요 시간: {stats.duration:.1f}초"
            )

            # Add close button
            progress_dialog.actions = [
                ft.TextButton("닫기", on_click=lambda e: close_dialog(progress_dialog))
            ]

            page.update()

        def on_error(error: str):
            progress_text.value = f"오류 발생: {error}"
            progress_text.color = AppColors.DANGER
            progress_dialog.actions = [
                ft.TextButton("닫기", on_click=lambda e: close_dialog(progress_dialog))
            ]
            page.update()

        # Start cleaner worker with callbacks
        cleaner_worker = FletCleanerWorker(
            browsers=selected_browsers_list,
            delete_bookmarks=delete_bookmarks,
            delete_downloads=delete_downloads,
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
            title,
            subtitle,
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
