"""Tests for ScheduleExecutor - DEV/PROD mode execution and error handling"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import os

from privacy_eraser.schedule_executor import (
    execute_scenario,
    execute_dev_mode,
    execute_prod_mode,
    _get_browser_files,
    _expand_path,
    _safe_delete,
    _get_file_size,
)
from privacy_eraser.core.schedule_manager import ScheduleScenario
from privacy_eraser.config import AppConfig


# ═══════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════


@pytest.fixture
def sample_scenario():
    """Create a sample scenario for testing"""
    return ScheduleScenario(
        id="test-scenario-id",
        name="Test Clean",
        enabled=True,
        schedule_type="daily",
        time="14:00",
        weekdays=[],
        day_of_month=None,
        browsers=["Chrome", "Firefox"],
        delete_bookmarks=False,
        delete_downloads=True,
        delete_downloads_folder=False,
        created_at="2025-10-22T14:00:00",
        description="Test scenario",
    )


@pytest.fixture
def temp_test_data(tmp_path):
    """Create temporary test data files"""
    browser_dir = tmp_path / "test_browser"
    browser_dir.mkdir()

    # Create some test files
    (browser_dir / "cache.dat").write_text("cache data")
    (browser_dir / "cookies.db").write_text("cookies data")

    return browser_dir


# ═══════════════════════════════════════════════════════════
# DEV Mode Tests
# ═══════════════════════════════════════════════════════════


@patch("privacy_eraser.dev_data_generator.count_test_files")
def test_execute_dev_mode_single_browser(mock_count, sample_scenario):
    """Test DEV mode execution with single browser"""
    sample_scenario.browsers = ["Chrome"]
    mock_count.return_value = 100

    result = execute_dev_mode(sample_scenario)

    assert result["mode"] == "dev"
    assert result["total_files"] == 100
    assert result["browser_counts"]["Chrome"] == 100
    assert result["deleted"] is False
    mock_count.assert_called_once_with("Chrome")


@patch("privacy_eraser.dev_data_generator.count_test_files")
def test_execute_dev_mode_multiple_browsers(mock_count, sample_scenario):
    """Test DEV mode execution with multiple browsers"""
    mock_count.side_effect = [50, 75]  # Chrome, Firefox

    result = execute_dev_mode(sample_scenario)

    assert result["mode"] == "dev"
    assert result["total_files"] == 125
    assert result["browser_counts"]["Chrome"] == 50
    assert result["browser_counts"]["Firefox"] == 75
    assert result["deleted"] is False


@patch("privacy_eraser.dev_data_generator.count_test_files")
def test_execute_dev_mode_no_test_data(mock_count, sample_scenario):
    """Test DEV mode when no test data exists"""
    mock_count.return_value = 0

    result = execute_dev_mode(sample_scenario)

    assert result["total_files"] == 0
    assert result["deleted"] is False


@patch("privacy_eraser.dev_data_generator.count_test_files")
def test_execute_dev_mode_returns_simulation_result(mock_count, sample_scenario):
    """Test DEV mode returns simulation result without deletion"""
    mock_count.return_value = 50

    result = execute_dev_mode(sample_scenario)

    assert "mode" in result
    assert "total_files" in result
    assert "browser_counts" in result
    assert "deleted" in result
    assert result["deleted"] is False


@patch("privacy_eraser.dev_data_generator.count_test_files")
def test_execute_dev_mode_browser_error(mock_count, sample_scenario):
    """Test DEV mode handles browser errors gracefully"""
    # First browser succeeds, second fails
    mock_count.side_effect = [100, Exception("Test error")]

    result = execute_dev_mode(sample_scenario)

    # Should complete with partial data
    assert result["browser_counts"]["Chrome"] == 100
    assert result["browser_counts"]["Firefox"] == 0  # Failed browser


# ═══════════════════════════════════════════════════════════
# PROD Mode Tests
# ═══════════════════════════════════════════════════════════


@patch("privacy_eraser.schedule_executor._get_browser_files")
@patch("privacy_eraser.schedule_executor._safe_delete")
@patch("privacy_eraser.schedule_executor._get_file_size")
def test_execute_prod_mode_single_browser(
    mock_size, mock_delete, mock_get_files, sample_scenario
):
    """Test PROD mode execution with single browser"""
    sample_scenario.browsers = ["Chrome"]

    # Mock files to delete
    test_files = ["/path/to/cache", "/path/to/cookies"]
    mock_get_files.return_value = test_files
    mock_size.return_value = 1024  # 1 KB per file

    result = execute_prod_mode(sample_scenario)

    assert result["mode"] == "prod"
    assert result["total_files"] == 2
    assert result["deleted_files"] == 2
    assert result["deleted_size_mb"] > 0
    assert result["failed_files"] == 0
    assert mock_delete.call_count == 2


@patch("privacy_eraser.schedule_executor._get_browser_files")
@patch("privacy_eraser.schedule_executor._safe_delete")
@patch("privacy_eraser.schedule_executor._get_file_size")
def test_execute_prod_mode_multiple_browsers(
    mock_size, mock_delete, mock_get_files, sample_scenario
):
    """Test PROD mode execution with multiple browsers"""
    # Mock different files for each browser
    mock_get_files.side_effect = [
        ["/chrome/cache", "/chrome/cookies"],  # Chrome
        ["/firefox/cache"],  # Firefox
    ]
    mock_size.return_value = 2048  # 2 KB per file

    result = execute_prod_mode(sample_scenario)

    assert result["total_files"] == 3
    assert result["deleted_files"] == 3
    assert mock_delete.call_count == 3


@patch("privacy_eraser.schedule_executor._get_browser_files")
def test_execute_prod_mode_with_bookmarks(mock_get_files, sample_scenario):
    """Test PROD mode respects delete_bookmarks option"""
    sample_scenario.delete_bookmarks = True

    mock_get_files.return_value = []

    result = execute_prod_mode(sample_scenario)

    # Verify get_cleaner_options was called with delete_bookmarks=True
    assert result["mode"] == "prod"


@patch("privacy_eraser.schedule_executor._get_browser_files")
@patch("privacy_eraser.schedule_executor._safe_delete")
@patch("privacy_eraser.schedule_executor._get_file_size")
def test_execute_prod_mode_deletion_failure(
    mock_size, mock_delete, mock_get_files, sample_scenario
):
    """Test PROD mode handles deletion failures"""
    sample_scenario.browsers = ["Chrome"]

    test_files = ["/path/file1", "/path/file2", "/path/file3"]
    mock_get_files.return_value = test_files
    mock_size.return_value = 1024

    # Second deletion fails
    mock_delete.side_effect = [None, Exception("Permission denied"), None]

    result = execute_prod_mode(sample_scenario)

    assert result["total_files"] == 3
    assert result["deleted_files"] == 2  # 2 succeeded
    assert result["failed_files"] == 1  # 1 failed


@patch("privacy_eraser.schedule_executor._get_browser_files")
@patch("privacy_eraser.schedule_executor._safe_delete")
@patch("privacy_eraser.schedule_executor._get_file_size")
def test_execute_prod_mode_calculates_size(
    mock_size, mock_delete, mock_get_files, sample_scenario
):
    """Test PROD mode calculates deleted size correctly"""
    sample_scenario.browsers = ["Chrome"]

    mock_get_files.return_value = ["/file1", "/file2"]
    mock_size.side_effect = [1024 * 1024, 2 * 1024 * 1024]  # 1 MB, 2 MB

    result = execute_prod_mode(sample_scenario)

    # Should be 3 MB total
    assert result["deleted_size_mb"] == pytest.approx(3.0, rel=0.01)


# ═══════════════════════════════════════════════════════════
# Main execute_scenario Tests
# ═══════════════════════════════════════════════════════════


@patch("privacy_eraser.schedule_executor.execute_dev_mode")
@patch("privacy_eraser.schedule_executor.show_dev_notification")
def test_execute_scenario_dev_mode(mock_notify, mock_exec, sample_scenario, monkeypatch):
    """Test execute_scenario in DEV mode"""
    monkeypatch.setattr(AppConfig, "_dev_mode", True)

    mock_exec.return_value = {
        "mode": "dev",
        "total_files": 100,
        "browser_counts": {"Chrome": 50, "Firefox": 50},
    }

    execute_scenario(sample_scenario)

    mock_exec.assert_called_once_with(sample_scenario)
    mock_notify.assert_called_once()


@patch("privacy_eraser.schedule_executor.execute_prod_mode")
@patch("privacy_eraser.schedule_executor.show_prod_notification")
def test_execute_scenario_prod_mode(mock_notify, mock_exec, sample_scenario, monkeypatch):
    """Test execute_scenario in PROD mode"""
    monkeypatch.setattr(AppConfig, "_dev_mode", False)

    mock_exec.return_value = {
        "mode": "prod",
        "deleted_files": 50,
        "deleted_size_mb": 10.5,
        "duration": 1.5,
    }

    execute_scenario(sample_scenario)

    mock_exec.assert_called_once_with(sample_scenario)
    mock_notify.assert_called_once()


@patch("privacy_eraser.schedule_executor.execute_dev_mode")
@patch("privacy_eraser.schedule_executor.show_error_notification")
def test_execute_scenario_handles_exception(
    mock_error_notify, mock_exec, sample_scenario, monkeypatch
):
    """Test execute_scenario handles exceptions"""
    monkeypatch.setattr(AppConfig, "_dev_mode", True)

    mock_exec.side_effect = Exception("Test error")

    # Should not raise, but show error notification
    execute_scenario(sample_scenario)

    mock_error_notify.assert_called_once()


# ═══════════════════════════════════════════════════════════
# Helper Function Tests
# ═══════════════════════════════════════════════════════════


def test_expand_path_simple(tmp_path):
    """Test _expand_path with simple file"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("test")

    result = _expand_path(str(test_file))

    assert len(result) == 1
    assert str(test_file) in result


def test_expand_path_glob_pattern(tmp_path):
    """Test _expand_path with glob pattern"""
    # Create test files
    (tmp_path / "file1.txt").write_text("test")
    (tmp_path / "file2.txt").write_text("test")

    pattern = str(tmp_path / "*.txt")
    result = _expand_path(pattern)

    assert len(result) == 2


def test_expand_path_nonexistent():
    """Test _expand_path with nonexistent file"""
    result = _expand_path("/nonexistent/file.txt")

    assert len(result) == 0


def test_safe_delete_file(tmp_path):
    """Test _safe_delete with file"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")

    _safe_delete(str(test_file))

    assert not test_file.exists()


def test_safe_delete_directory(tmp_path):
    """Test _safe_delete with directory"""
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    (test_dir / "file.txt").write_text("test")

    _safe_delete(str(test_dir))

    assert not test_dir.exists()


def test_safe_delete_nonexistent():
    """Test _safe_delete with nonexistent path"""
    # Should raise exception
    with pytest.raises(Exception):
        _safe_delete("/nonexistent/file.txt")


def test_get_file_size_file(tmp_path):
    """Test _get_file_size with file"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")

    size = _get_file_size(str(test_file))

    assert size == len("test content")


def test_get_file_size_directory(tmp_path):
    """Test _get_file_size with directory"""
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    (test_dir / "file1.txt").write_text("hello")
    (test_dir / "file2.txt").write_text("world")

    size = _get_file_size(str(test_dir))

    assert size == len("hello") + len("world")


def test_get_file_size_nonexistent():
    """Test _get_file_size with nonexistent path"""
    size = _get_file_size("/nonexistent/file.txt")

    assert size == 0


# ═══════════════════════════════════════════════════════════
# Error Handling Tests
# ═══════════════════════════════════════════════════════════


@patch("privacy_eraser.schedule_executor._get_browser_files")
def test_execute_with_invalid_browser(mock_get_files, sample_scenario):
    """Test execution with invalid browser name"""
    sample_scenario.browsers = ["InvalidBrowser"]

    mock_get_files.return_value = []  # No files found

    result = execute_prod_mode(sample_scenario)

    assert result["total_files"] == 0
    assert result["deleted_files"] == 0


@patch("privacy_eraser.schedule_executor.get_browser_xml_path")
def test_get_browser_files_missing_cleanerml(mock_xml_path):
    """Test _get_browser_files with missing CleanerML"""
    mock_xml_path.return_value = None

    result = _get_browser_files("UnknownBrowser", ["cache"])

    assert len(result) == 0


@patch("privacy_eraser.schedule_executor.get_browser_xml_path")
@patch("privacy_eraser.schedule_executor.load_cleanerml")
def test_get_browser_files_handles_exception(mock_load, mock_xml_path):
    """Test _get_browser_files handles exceptions gracefully"""
    mock_xml_path.return_value = "/path/to/cleaner.xml"
    mock_load.side_effect = Exception("XML parse error")

    # Should not raise, but return empty list
    result = _get_browser_files("Chrome", ["cache"])

    assert len(result) == 0
