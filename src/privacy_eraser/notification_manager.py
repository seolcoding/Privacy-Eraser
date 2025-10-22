"""Windows Toast Notification Manager

Handles system notifications for scheduled task execution.
"""

import os
import sys
from pathlib import Path
from loguru import logger

try:
    from winotify import Notification, audio
    WINOTIFY_AVAILABLE = True
except ImportError:
    WINOTIFY_AVAILABLE = False
    logger.warning("winotify not available, notifications disabled")


# ═══════════════════════════════════════════════════════════
# Icon Path Helper
# ═══════════════════════════════════════════════════════════


def get_icon_path() -> str:
    """Get application icon path"""
    try:
        # PyInstaller path
        base_path = sys._MEIPASS
    except Exception:
        # Development path
        base_path = Path(__file__).parent.parent.parent

    icon_path = Path(base_path) / "static" / "images" / "app_icon.ico"

    # Fallback: use Chrome icon if app icon doesn't exist
    if not icon_path.exists():
        icon_path = Path(base_path) / "static" / "images" / "chrome.png"

    if icon_path.exists():
        return str(icon_path)

    return ""  # No icon


# ═══════════════════════════════════════════════════════════
# Notification Functions
# ═══════════════════════════════════════════════════════════


def show_dev_notification(scenario_name: str, browsers: list[str], file_count: int):
    """Show DEV mode notification (simulation)

    Args:
        scenario_name: Name of the schedule scenario
        browsers: List of browser names
        file_count: Total number of files (simulated)
    """
    if not WINOTIFY_AVAILABLE:
        logger.info(f"[DEV] Would show notification: {scenario_name} - {file_count} files")
        return

    try:
        browsers_text = ", ".join(browsers)

        toast = Notification(
            app_id="Privacy Eraser",
            title="🔔 [DEV] 예약 실행 시뮬레이션",
            msg=f"{browsers_text}\n{file_count}개 파일 (삭제 안됨)\n\n시나리오: {scenario_name}",
            icon=get_icon_path(),
        )

        toast.set_audio(audio.Default, loop=False)
        toast.show()

        logger.info(f"[DEV] Notification shown: {scenario_name} - {file_count} files")

    except Exception as e:
        logger.error(f"Failed to show DEV notification: {e}")


def show_prod_notification(
    scenario_name: str,
    browsers: list[str],
    deleted_files: int,
    deleted_size_mb: float,
    duration: float
):
    """Show PROD mode notification (actual deletion stats)

    Args:
        scenario_name: Name of the schedule scenario
        browsers: List of browser names
        deleted_files: Number of deleted files
        deleted_size_mb: Total size deleted in MB
        duration: Execution time in seconds
    """
    if not WINOTIFY_AVAILABLE:
        logger.info(
            f"[PROD] Would show notification: {scenario_name} - "
            f"{deleted_files} files, {deleted_size_mb:.1f} MB"
        )
        return

    try:
        browsers_text = ", ".join(browsers)

        toast = Notification(
            app_id="Privacy Eraser",
            title="✅ 정리 완료",
            msg=(
                f"{browsers_text}\n"
                f"{deleted_files}개 파일 ({deleted_size_mb:.1f} MB) 삭제\n\n"
                f"시나리오: {scenario_name}\n"
                f"소요시간: {duration:.1f}초"
            ),
            icon=get_icon_path(),
        )

        toast.set_audio(audio.Default, loop=False)
        toast.show()

        logger.info(
            f"[PROD] Notification shown: {scenario_name} - "
            f"{deleted_files} files, {deleted_size_mb:.1f} MB"
        )

    except Exception as e:
        logger.error(f"Failed to show PROD notification: {e}")


def show_error_notification(scenario_name: str, error_message: str):
    """Show error notification

    Args:
        scenario_name: Name of the schedule scenario
        error_message: Error message
    """
    if not WINOTIFY_AVAILABLE:
        logger.error(f"[ERROR] {scenario_name}: {error_message}")
        return

    try:
        toast = Notification(
            app_id="Privacy Eraser",
            title="⚠️ 예약 실행 실패",
            msg=f"시나리오: {scenario_name}\n\n오류: {error_message}",
            icon=get_icon_path(),
        )

        toast.set_audio(audio.Default, loop=False)
        toast.show()

        logger.error(f"Error notification shown: {scenario_name} - {error_message}")

    except Exception as e:
        logger.error(f"Failed to show error notification: {e}")
