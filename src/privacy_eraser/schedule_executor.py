"""Schedule Executor

Executes scheduled cleaning scenarios in DEV or PROD mode.
"""

import time
import os
from pathlib import Path
from loguru import logger

from privacy_eraser.config import AppConfig
from privacy_eraser.core.schedule_manager import ScheduleScenario
from privacy_eraser.notification_manager import (
    show_dev_notification,
    show_prod_notification,
    show_error_notification,
)


# ═══════════════════════════════════════════════════════════
# Main Execution Function
# ═══════════════════════════════════════════════════════════


def execute_scenario(scenario: ScheduleScenario):
    """Execute a scheduled cleaning scenario

    Args:
        scenario: ScheduleScenario object

    This function is called by APScheduler when a schedule is triggered.
    """
    logger.info(f"[SCHEDULE] Executing scenario: {scenario.name}")

    try:
        if AppConfig.is_dev_mode():
            result = execute_dev_mode(scenario)
            show_dev_notification(
                scenario_name=scenario.name,
                browsers=scenario.browsers,
                file_count=result["total_files"],
            )
        else:
            result = execute_prod_mode(scenario)
            show_prod_notification(
                scenario_name=scenario.name,
                browsers=scenario.browsers,
                deleted_files=result["deleted_files"],
                deleted_size_mb=result["deleted_size_mb"],
                duration=result["duration"],
            )

        logger.success(f"[SCHEDULE] Scenario completed: {scenario.name}")

    except Exception as e:
        logger.error(f"[SCHEDULE] Scenario failed: {scenario.name} - {e}")
        show_error_notification(scenario.name, str(e))


# ═══════════════════════════════════════════════════════════
# DEV Mode Execution (Simulation)
# ═══════════════════════════════════════════════════════════


def execute_dev_mode(scenario: ScheduleScenario) -> dict:
    """Execute scenario in DEV mode (simulation only, no deletion)

    Args:
        scenario: ScheduleScenario object

    Returns:
        dict with statistics (no actual deletion)
    """
    logger.info(f"[DEV] Simulating scenario: {scenario.name}")

    # Count test data files (no deletion)
    from privacy_eraser.dev_data_generator import count_test_files

    total_files = 0
    browser_counts = {}

    for browser in scenario.browsers:
        try:
            count = count_test_files(browser)
            browser_counts[browser] = count
            total_files += count
            logger.info(f"[DEV] {browser}: {count} files (simulated)")
        except Exception as e:
            logger.warning(f"[DEV] Failed to count files for {browser}: {e}")
            browser_counts[browser] = 0

    result = {
        "mode": "dev",
        "browsers": scenario.browsers,
        "total_files": total_files,
        "browser_counts": browser_counts,
        "deleted": False,
    }

    logger.info(f"[DEV] Simulation complete: {total_files} files (no deletion)")

    return result


# ═══════════════════════════════════════════════════════════
# PROD Mode Execution (Actual Deletion)
# ═══════════════════════════════════════════════════════════


def execute_prod_mode(scenario: ScheduleScenario) -> dict:
    """Execute scenario in PROD mode (actual file deletion)

    Args:
        scenario: ScheduleScenario object

    Returns:
        dict with deletion statistics
    """
    logger.info(f"[PROD] Executing scenario: {scenario.name}")

    start_time = time.time()

    # Use the same logic as FletCleanerWorker but synchronously
    from privacy_eraser.ui.core.data_config import get_cleaner_options, get_browser_xml_path
    from privacy_eraser.cleanerml_loader import load_cleanerml
    import glob as glob_module

    total_files = 0
    deleted_files = 0
    deleted_size = 0
    failed_files = 0

    options = get_cleaner_options(
        scenario.delete_bookmarks,
        scenario.delete_downloads,
    )

    # Collect files to delete
    files_to_delete = []

    for browser in scenario.browsers:
        try:
            browser_files = _get_browser_files(browser, options)
            files_to_delete.extend(browser_files)
            logger.info(f"[PROD] {browser}: {len(browser_files)} files to delete")
        except Exception as e:
            logger.warning(f"[PROD] Failed to collect files for {browser}: {e}")

    total_files = len(files_to_delete)
    logger.info(f"[PROD] Total files to delete: {total_files}")

    # Delete files
    for file_path in files_to_delete:
        try:
            file_size = _get_file_size(file_path) if os.path.exists(file_path) else 0
            _safe_delete(file_path)
            deleted_files += 1
            deleted_size += file_size
        except Exception as e:
            failed_files += 1
            logger.warning(f"[PROD] Failed to delete {file_path}: {e}")

    duration = time.time() - start_time
    deleted_size_mb = deleted_size / (1024 * 1024)

    result = {
        "mode": "prod",
        "browsers": scenario.browsers,
        "total_files": total_files,
        "deleted_files": deleted_files,
        "deleted_size_mb": deleted_size_mb,
        "failed_files": failed_files,
        "duration": duration,
    }

    logger.info(
        f"[PROD] Deletion complete: {deleted_files}/{total_files} files, "
        f"{deleted_size_mb:.1f} MB, {duration:.1f}s"
    )

    return result


# ═══════════════════════════════════════════════════════════
# Helper Functions
# ═══════════════════════════════════════════════════════════


def _get_browser_files(browser_name: str, options: list[str]) -> list[str]:
    """Get files for specific browser"""
    from privacy_eraser.ui.core.data_config import get_browser_xml_path
    from privacy_eraser.cleanerml_loader import load_cleanerml
    import glob as glob_module

    files = []

    try:
        xml_path = get_browser_xml_path(browser_name)
        if not xml_path:
            logger.warning(f"CleanerML path not found: {browser_name}")
            return files

        cleaner_def = load_cleanerml(xml_path)

        for option in options:
            try:
                actions = cleaner_def.get_actions(option)
                for action in actions:
                    expanded = _expand_path(action.path)
                    files.extend(expanded)
            except Exception as e:
                logger.debug(f"Failed to process option {option}: {e}")

    except Exception as e:
        logger.warning(f"Failed to load CleanerML for {browser_name}: {e}")

    return files


def _expand_path(path: str) -> list[str]:
    """Expand environment variables and glob patterns"""
    import glob as glob_module

    expanded_files = []

    try:
        expanded = os.path.expandvars(path)

        if "*" in expanded or "?" in expanded:
            matched = glob_module.glob(expanded, recursive=True)
            expanded_files.extend(matched)
        else:
            if os.path.exists(expanded):
                expanded_files.append(expanded)

    except Exception as e:
        logger.debug(f"Failed to expand path {path}: {e}")

    return expanded_files


def _safe_delete(path: str):
    """Safely delete file or directory"""
    try:
        if os.path.isdir(path):
            import shutil
            shutil.rmtree(path, ignore_errors=True)
        else:
            os.remove(path)
    except Exception as e:
        logger.warning(f"Failed to delete {path}: {e}")
        raise


def _get_file_size(path: str) -> int:
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
