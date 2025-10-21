"""Schedule Manager - CRUD operations for cleaning schedules"""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, asdict
from loguru import logger
import uuid


@dataclass
class ScheduleScenario:
    """예약 시나리오 데이터 모델"""

    id: str
    name: str
    enabled: bool
    schedule_type: str  # once, hourly, daily, weekly, monthly
    time: str  # HH:MM format
    weekdays: list[int]  # 0=일요일, 1=월요일, ..., 6=토요일 (weekly용)
    day_of_month: Optional[int]  # 1-31 (monthly용)
    browsers: list[str]
    delete_bookmarks: bool
    delete_downloads: bool
    delete_downloads_folder: bool
    created_at: str
    last_run: Optional[str] = None
    description: str = ""

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "ScheduleScenario":
        """Create from dictionary"""
        return cls(**data)


class ScheduleManager:
    """예약 시나리오 관리 클래스"""

    def __init__(self, storage_path: Optional[Path] = None):
        """Initialize schedule manager

        Args:
            storage_path: JSON 파일 저장 경로 (기본: 사용자 홈/.privacy_eraser/schedules.json)
        """
        if storage_path is None:
            storage_path = Path.home() / ".privacy_eraser" / "schedules.json"

        self.storage_path = storage_path
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

        # 파일이 없으면 초기화
        if not self.storage_path.exists():
            self._save_schedules([])

    def _load_schedules(self) -> list[ScheduleScenario]:
        """Load schedules from JSON file"""
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [ScheduleScenario.from_dict(item) for item in data]
        except Exception as e:
            logger.error(f"Failed to load schedules: {e}")
            return []

    def _save_schedules(self, schedules: list[ScheduleScenario]):
        """Save schedules to JSON file"""
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(
                    [s.to_dict() for s in schedules], f, ensure_ascii=False, indent=2
                )
        except Exception as e:
            logger.error(f"Failed to save schedules: {e}")

    def create_schedule(
        self,
        name: str,
        schedule_type: str,
        time: str,
        browsers: list[str],
        weekdays: list[int] | None = None,
        day_of_month: int | None = None,
        delete_bookmarks: bool = False,
        delete_downloads: bool = False,
        delete_downloads_folder: bool = False,
        description: str = "",
    ) -> ScheduleScenario:
        """Create new schedule scenario

        Args:
            name: 시나리오 이름
            schedule_type: once, hourly, daily, weekly, monthly
            time: HH:MM 형식
            browsers: 브라우저 목록
            weekdays: 주별 반복 시 요일 목록 (0=일, 6=토)
            day_of_month: 월별 반복 시 날짜 (1-31)
            delete_bookmarks: 북마크 삭제 여부
            delete_downloads: 다운로드 기록 삭제 여부
            delete_downloads_folder: 다운로드 파일 삭제 여부
            description: 설명

        Returns:
            ScheduleScenario: 생성된 시나리오
        """
        scenario = ScheduleScenario(
            id=str(uuid.uuid4()),
            name=name,
            enabled=True,
            schedule_type=schedule_type,
            time=time,
            weekdays=weekdays or [],
            day_of_month=day_of_month,
            browsers=browsers,
            delete_bookmarks=delete_bookmarks,
            delete_downloads=delete_downloads,
            delete_downloads_folder=delete_downloads_folder,
            created_at=datetime.now().isoformat(),
            description=description,
        )

        schedules = self._load_schedules()
        schedules.append(scenario)
        self._save_schedules(schedules)

        logger.info(f"Created schedule: {name} ({scenario.id})")
        return scenario

    def get_all_schedules(self) -> list[ScheduleScenario]:
        """Get all schedules"""
        return self._load_schedules()

    def get_schedule(self, schedule_id: str) -> Optional[ScheduleScenario]:
        """Get schedule by ID"""
        schedules = self._load_schedules()
        for schedule in schedules:
            if schedule.id == schedule_id:
                return schedule
        return None

    def update_schedule(
        self, schedule_id: str, **kwargs
    ) -> Optional[ScheduleScenario]:
        """Update schedule

        Args:
            schedule_id: 시나리오 ID
            **kwargs: 업데이트할 필드 (name, enabled, schedule_type, time, etc.)

        Returns:
            ScheduleScenario: 업데이트된 시나리오 또는 None
        """
        schedules = self._load_schedules()

        for i, schedule in enumerate(schedules):
            if schedule.id == schedule_id:
                # Update fields
                for key, value in kwargs.items():
                    if hasattr(schedule, key):
                        setattr(schedule, key, value)

                schedules[i] = schedule
                self._save_schedules(schedules)

                logger.info(f"Updated schedule: {schedule.name} ({schedule_id})")
                return schedule

        logger.warning(f"Schedule not found: {schedule_id}")
        return None

    def delete_schedule(self, schedule_id: str) -> bool:
        """Delete schedule

        Args:
            schedule_id: 시나리오 ID

        Returns:
            bool: 삭제 성공 여부
        """
        schedules = self._load_schedules()
        original_count = len(schedules)

        schedules = [s for s in schedules if s.id != schedule_id]

        if len(schedules) < original_count:
            self._save_schedules(schedules)
            logger.info(f"Deleted schedule: {schedule_id}")
            return True

        logger.warning(f"Schedule not found: {schedule_id}")
        return False

    def toggle_schedule(self, schedule_id: str) -> Optional[ScheduleScenario]:
        """Toggle schedule enabled state

        Args:
            schedule_id: 시나리오 ID

        Returns:
            ScheduleScenario: 업데이트된 시나리오 또는 None
        """
        schedule = self.get_schedule(schedule_id)
        if schedule:
            return self.update_schedule(schedule_id, enabled=not schedule.enabled)
        return None

    def get_active_schedules(self) -> list[ScheduleScenario]:
        """Get only enabled schedules"""
        return [s for s in self._load_schedules() if s.enabled]

    def mark_as_run(self, schedule_id: str):
        """Mark schedule as run (update last_run timestamp)

        Args:
            schedule_id: 시나리오 ID
        """
        self.update_schedule(schedule_id, last_run=datetime.now().isoformat())
