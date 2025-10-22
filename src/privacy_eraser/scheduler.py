"""Background Scheduler for Privacy Eraser

Manages scheduled cleaning tasks using APScheduler.
"""

from datetime import datetime, timedelta
from loguru import logger

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger

from privacy_eraser.config import AppConfig
from privacy_eraser.core.schedule_manager import ScheduleManager, ScheduleScenario
from privacy_eraser.schedule_executor import execute_scenario


# ═══════════════════════════════════════════════════════════
# Global Scheduler Instance
# ═══════════════════════════════════════════════════════════

_scheduler_instance = None
_fast_mode_enabled = False


def get_scheduler():
    """Get global scheduler instance"""
    global _scheduler_instance
    if _scheduler_instance is None:
        _scheduler_instance = PrivacyEraserScheduler()
    return _scheduler_instance


def set_fast_mode(enabled: bool):
    """Set Fast Mode (DEV only, time acceleration)"""
    global _fast_mode_enabled
    _fast_mode_enabled = enabled
    logger.info(f"Fast Mode: {'enabled' if enabled else 'disabled'}")


def is_fast_mode() -> bool:
    """Check if Fast Mode is enabled"""
    return _fast_mode_enabled and AppConfig.is_dev_mode()


# ═══════════════════════════════════════════════════════════
# Scheduler Class
# ═══════════════════════════════════════════════════════════


class PrivacyEraserScheduler:
    """Background scheduler for Privacy Eraser"""

    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.schedule_manager = ScheduleManager()
        self._running = False

    def start(self):
        """Start the scheduler"""
        if self._running:
            logger.warning("Scheduler already running")
            return

        try:
            self.scheduler.start()
            self._running = True
            logger.info("Scheduler started")

            # Load all enabled schedules
            self.load_all_schedules()

        except Exception as e:
            logger.error(f"Failed to start scheduler: {e}")

    def stop(self):
        """Stop the scheduler"""
        if not self._running:
            return

        try:
            self.scheduler.shutdown(wait=False)
            self._running = False
            logger.info("Scheduler stopped")
        except Exception as e:
            logger.error(f"Failed to stop scheduler: {e}")

    def load_all_schedules(self):
        """Load all enabled schedules from ScheduleManager"""
        scenarios = self.schedule_manager.get_all_schedules()

        for scenario in scenarios:
            if scenario.enabled:
                try:
                    self.add_schedule(scenario)
                    logger.info(f"Loaded schedule: {scenario.name}")
                except Exception as e:
                    logger.error(f"Failed to load schedule {scenario.name}: {e}")

    def add_schedule(self, scenario: ScheduleScenario):
        """Add or update a schedule

        Args:
            scenario: ScheduleScenario object
        """
        try:
            trigger = self._create_trigger(scenario)

            self.scheduler.add_job(
                func=execute_scenario,
                trigger=trigger,
                id=scenario.id,
                args=[scenario],
                replace_existing=True,
                name=scenario.name,
            )

            # Get next run time
            job = self.scheduler.get_job(scenario.id)
            next_run = job.next_run_time if job else None

            logger.info(
                f"Schedule added: {scenario.name} "
                f"(next run: {next_run.strftime('%Y-%m-%d %H:%M:%S') if next_run else 'N/A'})"
            )

        except Exception as e:
            logger.error(f"Failed to add schedule {scenario.name}: {e}")
            raise

    def remove_schedule(self, scenario_id: str):
        """Remove a schedule

        Args:
            scenario_id: Scenario ID
        """
        try:
            self.scheduler.remove_job(scenario_id)
            logger.info(f"Schedule removed: {scenario_id}")
        except Exception as e:
            logger.warning(f"Failed to remove schedule {scenario_id}: {e}")

    def reload_schedules(self):
        """Reload all schedules (useful after updates)"""
        logger.info("Reloading all schedules...")

        # Remove all jobs
        self.scheduler.remove_all_jobs()

        # Reload from ScheduleManager
        self.load_all_schedules()

    def get_next_run_time(self, scenario_id: str) -> datetime | None:
        """Get next run time for a scenario

        Args:
            scenario_id: Scenario ID

        Returns:
            Next run time or None
        """
        try:
            job = self.scheduler.get_job(scenario_id)
            return job.next_run_time if job else None
        except Exception:
            return None

    def _create_trigger(self, scenario: ScheduleScenario):
        """Create APScheduler trigger based on scenario type

        Args:
            scenario: ScheduleScenario object

        Returns:
            APScheduler trigger
        """
        # Parse time
        hour, minute = map(int, scenario.time.split(":"))

        # Fast Mode: time acceleration for DEV mode
        if is_fast_mode():
            return self._create_fast_mode_trigger(scenario, hour, minute)

        # Normal Mode
        if scenario.schedule_type == "once":
            # Run once at specified time (today or tomorrow)
            run_time = datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
            if run_time < datetime.now():
                run_time += timedelta(days=1)  # Tomorrow
            return DateTrigger(run_date=run_time)

        elif scenario.schedule_type == "hourly":
            return IntervalTrigger(hours=1, start_date=datetime.now())

        elif scenario.schedule_type == "daily":
            return CronTrigger(hour=hour, minute=minute)

        elif scenario.schedule_type == "weekly":
            # weekdays: 0=Monday, 6=Sunday (APScheduler format)
            # scenario.weekdays: 0=Sunday, 6=Saturday (our format)
            # Convert: our Sunday(0) -> APScheduler Sunday(6)
            apscheduler_weekdays = []
            for day in scenario.weekdays:
                if day == 0:  # Sunday
                    apscheduler_weekdays.append(6)
                else:
                    apscheduler_weekdays.append(day - 1)

            day_of_week = ",".join(map(str, sorted(apscheduler_weekdays)))
            return CronTrigger(day_of_week=day_of_week, hour=hour, minute=minute)

        elif scenario.schedule_type == "monthly":
            return CronTrigger(day=scenario.day_of_month, hour=hour, minute=minute)

        else:
            raise ValueError(f"Unknown schedule type: {scenario.schedule_type}")

    def _create_fast_mode_trigger(self, scenario: ScheduleScenario, hour: int, minute: int):
        """Create Fast Mode trigger (DEV only, time acceleration)

        Args:
            scenario: ScheduleScenario object
            hour: Hour
            minute: Minute

        Returns:
            APScheduler trigger with accelerated time
        """
        logger.info(f"[FAST MODE] Creating accelerated trigger for: {scenario.name}")

        if scenario.schedule_type == "once":
            # Run after 10 seconds
            run_time = datetime.now() + timedelta(seconds=10)
            return DateTrigger(run_date=run_time)

        elif scenario.schedule_type == "hourly":
            # Every 10 seconds instead of every hour
            return IntervalTrigger(seconds=10, start_date=datetime.now())

        elif scenario.schedule_type == "daily":
            # Every 1 minute instead of every day
            return IntervalTrigger(minutes=1, start_date=datetime.now())

        elif scenario.schedule_type == "weekly":
            # Every 5 minutes instead of every week
            return IntervalTrigger(minutes=5, start_date=datetime.now())

        elif scenario.schedule_type == "monthly":
            # Every 10 minutes instead of every month
            return IntervalTrigger(minutes=10, start_date=datetime.now())

        else:
            raise ValueError(f"Unknown schedule type: {scenario.schedule_type}")
