"""Tests for Scheduler - APScheduler integration for Privacy Eraser"""

import pytest
from datetime import datetime, timedelta, timezone
from pathlib import Path
import time

from privacy_eraser.scheduler import (
    PrivacyEraserScheduler,
    get_scheduler,
    set_fast_mode,
    is_fast_mode,
)
from privacy_eraser.core.schedule_manager import ScheduleManager, ScheduleScenario
from privacy_eraser.config import AppConfig


# Helper function for timezone-aware datetime (KST)
def now_tz():
    """Get current time as timezone-aware datetime (KST)"""
    kst = timezone(timedelta(hours=9))
    return datetime.now(kst)


# ═══════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════


@pytest.fixture
def temp_storage(tmp_path):
    """Create temporary storage path"""
    return tmp_path / "test_schedules.json"


@pytest.fixture
def schedule_manager(temp_storage):
    """Create ScheduleManager with temp storage"""
    return ScheduleManager(storage_path=temp_storage)


@pytest.fixture
def scheduler(schedule_manager, monkeypatch):
    """Create fresh scheduler instance for each test"""
    # Create new scheduler instance
    sched = PrivacyEraserScheduler()
    sched.schedule_manager = schedule_manager  # Use our temp storage

    # Reset fast mode for each test
    set_fast_mode(False)

    yield sched

    # Cleanup
    if sched._running:
        sched.stop()


@pytest.fixture
def sample_scenario(schedule_manager):
    """Create a sample scenario for testing"""
    return schedule_manager.create_schedule(
        name="Test Daily Clean",
        schedule_type="daily",
        time="14:00",
        browsers=["Chrome", "Firefox"],
        delete_bookmarks=False,
        delete_downloads=True,
    )


# ═══════════════════════════════════════════════════════════
# Scheduler Lifecycle Tests
# ═══════════════════════════════════════════════════════════


def test_scheduler_start(scheduler):
    """Test starting the scheduler"""
    assert scheduler._running is False

    scheduler.start()

    assert scheduler._running is True
    assert scheduler.scheduler.running is True


def test_scheduler_stop(scheduler):
    """Test stopping the scheduler"""
    scheduler.start()
    assert scheduler._running is True

    scheduler.stop()

    assert scheduler._running is False


def test_scheduler_start_already_running(scheduler):
    """Test starting scheduler that's already running"""
    scheduler.start()
    assert scheduler._running is True

    # Should not raise error
    scheduler.start()
    assert scheduler._running is True


def test_scheduler_stop_not_running(scheduler):
    """Test stopping scheduler that's not running"""
    assert scheduler._running is False

    # Should not raise error
    scheduler.stop()
    assert scheduler._running is False


# ═══════════════════════════════════════════════════════════
# Schedule Registration Tests
# ═══════════════════════════════════════════════════════════


def test_add_schedule_once(scheduler, schedule_manager):
    """Test adding a once schedule"""
    scenario = schedule_manager.create_schedule(
        name="Once Clean",
        schedule_type="once",
        time="15:30",
        browsers=["Chrome"],
    )

    scheduler.start()
    scheduler.add_schedule(scenario)

    # Verify job was added
    job = scheduler.scheduler.get_job(scenario.id)
    assert job is not None
    assert job.name == "Once Clean"


def test_add_schedule_hourly(scheduler, schedule_manager):
    """Test adding an hourly schedule"""
    scenario = schedule_manager.create_schedule(
        name="Hourly Clean",
        schedule_type="hourly",
        time="00:00",  # Not used for hourly
        browsers=["Firefox"],
    )

    scheduler.start()
    scheduler.add_schedule(scenario)

    job = scheduler.scheduler.get_job(scenario.id)
    assert job is not None
    assert job.name == "Hourly Clean"


def test_add_schedule_daily(scheduler, sample_scenario):
    """Test adding a daily schedule"""
    scheduler.start()
    scheduler.add_schedule(sample_scenario)

    job = scheduler.scheduler.get_job(sample_scenario.id)
    assert job is not None
    assert job.name == "Test Daily Clean"


def test_add_schedule_weekly(scheduler, schedule_manager):
    """Test adding a weekly schedule with multiple days"""
    scenario = schedule_manager.create_schedule(
        name="Weekly Clean",
        schedule_type="weekly",
        time="10:00",
        weekdays=[1, 3, 5],  # Mon, Wed, Fri
        browsers=["Chrome", "Edge"],
    )

    scheduler.start()
    scheduler.add_schedule(scenario)

    job = scheduler.scheduler.get_job(scenario.id)
    assert job is not None
    assert job.name == "Weekly Clean"


def test_add_schedule_monthly(scheduler, schedule_manager):
    """Test adding a monthly schedule"""
    scenario = schedule_manager.create_schedule(
        name="Monthly Clean",
        schedule_type="monthly",
        time="09:00",
        day_of_month=1,
        browsers=["Firefox"],
    )

    scheduler.start()
    scheduler.add_schedule(scenario)

    job = scheduler.scheduler.get_job(scenario.id)
    assert job is not None
    assert job.name == "Monthly Clean"


def test_add_schedule_replace_existing(scheduler, sample_scenario):
    """Test replacing an existing schedule"""
    scheduler.start()
    scheduler.add_schedule(sample_scenario)

    # Modify and add again
    sample_scenario.time = "18:00"
    scheduler.add_schedule(sample_scenario)

    # Should still have only one job
    jobs = scheduler.scheduler.get_jobs()
    matching_jobs = [j for j in jobs if j.id == sample_scenario.id]
    assert len(matching_jobs) == 1


# ═══════════════════════════════════════════════════════════
# Trigger Creation Tests
# ═══════════════════════════════════════════════════════════


def test_trigger_creation_once_tomorrow(scheduler, schedule_manager):
    """Test once trigger schedules for tomorrow if time has passed"""
    # Create a schedule for time that's already passed today
    past_time = (now_tz() - timedelta(hours=1)).strftime("%H:%M")

    scenario = schedule_manager.create_schedule(
        name="Past Time Once",
        schedule_type="once",
        time=past_time,
        browsers=["Chrome"],
    )

    scheduler.start()
    scheduler.add_schedule(scenario)

    next_run = scheduler.get_next_run_time(scenario.id)
    assert next_run is not None

    # Should be scheduled for tomorrow
    assert next_run > now_tz()
    assert next_run.date() >= (now_tz() + timedelta(days=1)).date()


def test_trigger_creation_daily_cron(scheduler, sample_scenario):
    """Test daily trigger creates cron schedule"""
    scheduler.start()
    scheduler.add_schedule(sample_scenario)

    next_run = scheduler.get_next_run_time(sample_scenario.id)
    assert next_run is not None

    # Should be scheduled for today or tomorrow at 14:00
    assert next_run.hour == 14
    assert next_run.minute == 0


def test_trigger_creation_weekly_cron(scheduler, schedule_manager):
    """Test weekly trigger with correct weekday mapping"""
    # Our format: 0=Sunday, 6=Saturday
    # APScheduler format: 0=Monday, 6=Sunday

    scenario = schedule_manager.create_schedule(
        name="Sunday Clean",
        schedule_type="weekly",
        time="10:00",
        weekdays=[0],  # Sunday in our format
        browsers=["Chrome"],
    )

    scheduler.start()
    scheduler.add_schedule(scenario)

    next_run = scheduler.get_next_run_time(scenario.id)
    assert next_run is not None

    # Should be scheduled for a Sunday (weekday() == 6)
    assert next_run.weekday() == 6


def test_weekday_conversion_multiple_days(scheduler, schedule_manager):
    """Test weekday conversion for multiple days"""
    scenario = schedule_manager.create_schedule(
        name="Weekday Clean",
        schedule_type="weekly",
        time="12:00",
        weekdays=[1, 2, 3, 4, 5],  # Mon-Fri in our format
        browsers=["Firefox"],
    )

    scheduler.start()
    scheduler.add_schedule(scenario)

    next_run = scheduler.get_next_run_time(scenario.id)
    assert next_run is not None

    # Should be scheduled for a weekday (0-4 in Python weekday)
    assert 0 <= next_run.weekday() <= 4


def test_trigger_creation_monthly_cron(scheduler, schedule_manager):
    """Test monthly trigger with day_of_month"""
    scenario = schedule_manager.create_schedule(
        name="Monthly Report",
        schedule_type="monthly",
        time="08:00",
        day_of_month=15,
        browsers=["Edge"],
    )

    scheduler.start()
    scheduler.add_schedule(scenario)

    next_run = scheduler.get_next_run_time(scenario.id)
    assert next_run is not None

    # Should be scheduled for 15th of current or next month
    assert next_run.day == 15
    assert next_run.hour == 8
    assert next_run.minute == 0


# ═══════════════════════════════════════════════════════════
# Fast Mode Tests
# ═══════════════════════════════════════════════════════════


def test_fast_mode_disabled_by_default():
    """Test fast mode is disabled by default"""
    set_fast_mode(False)
    assert is_fast_mode() is False


def test_fast_mode_enable(monkeypatch):
    """Test enabling fast mode in dev mode"""
    monkeypatch.setattr(AppConfig, "_dev_mode", True)

    set_fast_mode(True)
    assert is_fast_mode() is True


def test_fast_mode_requires_dev_mode(monkeypatch):
    """Test fast mode requires dev mode to be enabled"""
    monkeypatch.setattr(AppConfig, "_dev_mode", False)

    set_fast_mode(True)

    # Should not be enabled in prod mode
    assert is_fast_mode() is False


def test_fast_mode_once_trigger(scheduler, schedule_manager, monkeypatch):
    """Test fast mode creates accelerated once trigger"""
    monkeypatch.setattr(AppConfig, "_dev_mode", True)
    set_fast_mode(True)

    scenario = schedule_manager.create_schedule(
        name="Fast Once",
        schedule_type="once",
        time="14:00",
        browsers=["Chrome"],
    )

    scheduler.start()
    scheduler.add_schedule(scenario)

    next_run = scheduler.get_next_run_time(scenario.id)
    assert next_run is not None

    # Should run within 10 seconds
    time_until_run = (next_run - now_tz()).total_seconds()
    assert 0 <= time_until_run <= 15  # Allow some margin


def test_fast_mode_hourly_trigger(scheduler, schedule_manager, monkeypatch):
    """Test fast mode hourly runs every 10 seconds"""
    monkeypatch.setattr(AppConfig, "_dev_mode", True)
    set_fast_mode(True)

    scenario = schedule_manager.create_schedule(
        name="Fast Hourly",
        schedule_type="hourly",
        time="00:00",
        browsers=["Firefox"],
    )

    scheduler.start()
    scheduler.add_schedule(scenario)

    next_run = scheduler.get_next_run_time(scenario.id)
    assert next_run is not None

    # Should run within 10 seconds (may be negative if already executed)
    time_until_run = (next_run - now_tz()).total_seconds()
    assert abs(time_until_run) <= 15  # Allow execution or near-future


def test_fast_mode_daily_trigger(scheduler, schedule_manager, monkeypatch):
    """Test fast mode daily runs every minute"""
    monkeypatch.setattr(AppConfig, "_dev_mode", True)
    set_fast_mode(True)

    scenario = schedule_manager.create_schedule(
        name="Fast Daily",
        schedule_type="daily",
        time="14:00",
        browsers=["Edge"],
    )

    scheduler.start()
    scheduler.add_schedule(scenario)

    next_run = scheduler.get_next_run_time(scenario.id)
    assert next_run is not None

    # Should run within a minute
    time_until_run = (next_run - now_tz()).total_seconds()
    assert 0 <= time_until_run <= 65


# ═══════════════════════════════════════════════════════════
# Schedule Management Tests
# ═══════════════════════════════════════════════════════════


def test_remove_schedule(scheduler, sample_scenario):
    """Test removing a schedule"""
    scheduler.start()
    scheduler.add_schedule(sample_scenario)

    # Verify it was added
    assert scheduler.scheduler.get_job(sample_scenario.id) is not None

    scheduler.remove_schedule(sample_scenario.id)

    # Verify it was removed
    assert scheduler.scheduler.get_job(sample_scenario.id) is None


def test_remove_nonexistent_schedule(scheduler):
    """Test removing a nonexistent schedule"""
    scheduler.start()

    # Should not raise error
    scheduler.remove_schedule("nonexistent-id")


def test_reload_schedules(scheduler, schedule_manager):
    """Test reloading all schedules"""
    # Create multiple schedules
    s1 = schedule_manager.create_schedule(
        name="Clean 1",
        schedule_type="daily",
        time="10:00",
        browsers=["Chrome"],
    )
    s2 = schedule_manager.create_schedule(
        name="Clean 2",
        schedule_type="weekly",
        time="12:00",
        weekdays=[1, 3],
        browsers=["Firefox"],
    )

    scheduler.start()
    scheduler.load_all_schedules()

    # Verify both were loaded
    jobs = scheduler.scheduler.get_jobs()
    assert len(jobs) == 2

    # Disable one scenario
    schedule_manager.update_schedule(s1.id, enabled=False)

    # Reload
    scheduler.reload_schedules()

    # Should only have one job now
    jobs = scheduler.scheduler.get_jobs()
    assert len(jobs) == 1
    assert jobs[0].id == s2.id


def test_load_only_enabled_schedules(scheduler, schedule_manager):
    """Test loading only enabled schedules"""
    # Create enabled schedule
    s1 = schedule_manager.create_schedule(
        name="Enabled",
        schedule_type="daily",
        time="10:00",
        browsers=["Chrome"],
    )

    # Create disabled schedule
    s2 = schedule_manager.create_schedule(
        name="Disabled",
        schedule_type="daily",
        time="12:00",
        browsers=["Firefox"],
    )
    schedule_manager.update_schedule(s2.id, enabled=False)

    scheduler.start()
    scheduler.load_all_schedules()

    # Should only load enabled schedule
    jobs = scheduler.scheduler.get_jobs()
    assert len(jobs) == 1
    assert jobs[0].id == s1.id


def test_get_next_run_time(scheduler, sample_scenario):
    """Test getting next run time for a schedule"""
    scheduler.start()
    scheduler.add_schedule(sample_scenario)

    next_run = scheduler.get_next_run_time(sample_scenario.id)

    assert next_run is not None
    assert isinstance(next_run, datetime)
    assert next_run > now_tz()


def test_get_next_run_time_nonexistent(scheduler):
    """Test getting next run time for nonexistent schedule"""
    scheduler.start()

    next_run = scheduler.get_next_run_time("nonexistent-id")

    assert next_run is None


def test_multiple_schedules_coexist(scheduler, schedule_manager):
    """Test multiple schedules can coexist"""
    schedules = []
    for i in range(5):
        scenario = schedule_manager.create_schedule(
            name=f"Clean {i}",
            schedule_type="daily",
            time=f"{10 + i}:00",
            browsers=["Chrome"],
        )
        schedules.append(scenario)

    scheduler.start()
    for scenario in schedules:
        scheduler.add_schedule(scenario)

    jobs = scheduler.scheduler.get_jobs()
    assert len(jobs) == 5

    # Verify all have next run times
    for scenario in schedules:
        next_run = scheduler.get_next_run_time(scenario.id)
        assert next_run is not None


# ═══════════════════════════════════════════════════════════
# Global Scheduler Tests
# ═══════════════════════════════════════════════════════════


def test_get_scheduler_singleton():
    """Test get_scheduler() returns singleton instance"""
    scheduler1 = get_scheduler()
    scheduler2 = get_scheduler()

    assert scheduler1 is scheduler2
