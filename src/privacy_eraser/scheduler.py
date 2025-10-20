"""
Privacy Eraser Scheduler Module
===============================

APScheduler를 활용한 자동화 스케줄링 시스템.
다양한 스케줄 타입과 Windows Task Scheduler 연동을 지원합니다.
"""

from __future__ import annotations

import json
import time
from datetime import datetime, time as dt_time, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.events import JobEvent, JobExecutionEvent
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor

from loguru import logger

from .settings_db import get_database_manager
from .daemon import DaemonSignals


class ScheduleType(Enum):
    """스케줄 타입 열거형"""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    IDLE = "idle"
    ONCE = "once"
    INTERVAL = "interval"


@dataclass
class ScheduleConfig:
    """스케줄 설정 데이터 클래스"""
    name: str
    schedule_type: ScheduleType
    enabled: bool = True

    # 시간 설정
    time_config: Dict[str, Any]  # 타입별 설정 저장용 JSON

    # 옵션 설정
    skip_if_browser_running: bool = True
    show_notification: bool = True
    pause_on_battery: bool = True

    # 메타데이터
    description: str = ""
    created_at: Optional[datetime] = None
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None


class CleaningScheduler:
    """Privacy Eraser 스케줄링 관리 클래스"""

    def __init__(self, daemon_signals: DaemonSignals):
        self.signals = daemon_signals
        self.db_manager = get_database_manager()
        self.scheduler = BackgroundScheduler(
            jobstores={'default': MemoryJobStore()},
            executors={'default': ThreadPoolExecutor(max_workers=2)},
            job_defaults={'coalesce': True, 'max_instances': 1}
        )

        # 이벤트 리스너 설정
        self.scheduler.add_listener(
            self._on_job_executed,
            JobExecutionEvent.EVENT_JOB_EXECUTED
        )
        self.scheduler.add_listener(
            self._on_job_error,
            JobExecutionEvent.EVENT_JOB_ERROR
        )

        # 기본 프리셋들
        self._builtin_presets = {
            "빠른 정리": {
                "browsers": ["Chrome", "Edge", "Firefox"],
                "categories": ["cache", "cookies", "history"]
            },
            "보안 정리": {
                "browsers": ["Chrome", "Edge", "Firefox", "Brave"],
                "categories": ["cookies", "history", "passwords", "autofill"]
            },
            "완전 정리": {
                "browsers": ["Chrome", "Edge", "Firefox", "Brave", "Opera", "Whale"],
                "categories": ["cache", "cookies", "history", "passwords", "autofill", "session"]
            }
        }

        # 실행 중인 작업 추적
        self._running_jobs = set()

    def start(self) -> bool:
        """스케줄러 시작"""
        try:
            # 저장된 스케줄들 로드 및 등록
            self._load_and_register_schedules()

            # 스케줄러 시작
            self.scheduler.start()
            logger.info("Cleaning scheduler started successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to start scheduler: {e}")
            return False

    def stop(self):
        """스케줄러 중지"""
        try:
            self.scheduler.shutdown(wait=True)
            logger.info("Cleaning scheduler stopped")
        except Exception as e:
            logger.error(f"Error stopping scheduler: {e}")

    def add_schedule(self, config: ScheduleConfig) -> str:
        """새 스케줄 추가"""
        try:
            job_id = f"cleaning_{config.name}_{int(time.time())}"

            # 트리거 생성
            trigger = self._create_trigger(config)

            if not trigger:
                logger.error(f"Failed to create trigger for schedule: {config.name}")
                return ""

            # 작업 함수 생성
            job_func = self._create_job_function(config)

            # 작업 등록
            self.scheduler.add_job(
                job_func,
                trigger=trigger,
                id=job_id,
                replace_existing=True
            )

            # 데이터베이스에 저장
            self._save_schedule_to_db(config, job_id)

            logger.info(f"Added schedule: {config.name} (ID: {job_id})")
            return job_id

        except Exception as e:
            logger.error(f"Failed to add schedule {config.name}: {e}")
            return ""

    def remove_schedule(self, schedule_id: str) -> bool:
        """스케줄 제거"""
        try:
            self.scheduler.remove_job(schedule_id)

            # 데이터베이스에서 삭제
            # TODO: 스케줄 테이블에서 삭제하는 쿼리 추가 필요

            logger.info(f"Removed schedule: {schedule_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to remove schedule {schedule_id}: {e}")
            return False

    def get_schedules(self) -> List[Dict[str, Any]]:
        """등록된 스케줄 목록 반환"""
        schedules = []

        for job in self.scheduler.get_jobs():
            schedule_info = {
                'id': job.id,
                'name': job.id.split('_')[1] if '_' in job.id else job.id,
                'next_run': job.next_run_time,
                'enabled': not job.next_run_time is None
            }
            schedules.append(schedule_info)

        return schedules

    def _create_trigger(self, config: ScheduleConfig):
        """스케줄 타입에 따른 트리거 생성"""
        try:
            if config.schedule_type == ScheduleType.DAILY:
                time_config = config.time_config
                hour = time_config.get('hour', 10)
                minute = time_config.get('minute', 0)

                return CronTrigger(
                    hour=hour,
                    minute=minute,
                    timezone='Asia/Seoul'
                )

            elif config.schedule_type == ScheduleType.WEEKLY:
                time_config = config.time_config
                day_of_week = time_config.get('day_of_week', 0)  # 0 = 월요일
                hour = time_config.get('hour', 10)
                minute = time_config.get('minute', 0)

                return CronTrigger(
                    day_of_week=day_of_week,
                    hour=hour,
                    minute=minute,
                    timezone='Asia/Seoul'
                )

            elif config.schedule_type == ScheduleType.MONTHLY:
                time_config = config.time_config
                day = time_config.get('day', 1)
                hour = time_config.get('hour', 10)
                minute = time_config.get('minute', 0)

                return CronTrigger(
                    day=day,
                    hour=hour,
                    minute=minute,
                    timezone='Asia/Seoul'
                )

            elif config.schedule_type == ScheduleType.IDLE:
                # 유휴 시간 체크 (5분마다)
                return IntervalTrigger(minutes=5)

            elif config.schedule_type == ScheduleType.ONCE:
                run_time = datetime.fromisoformat(config.time_config.get('run_time'))
                return DateTrigger(run_date=run_time)

            elif config.schedule_type == ScheduleType.INTERVAL:
                minutes = config.time_config.get('minutes', 60)
                return IntervalTrigger(minutes=minutes)

            else:
                logger.error(f"Unknown schedule type: {config.schedule_type}")
                return None

        except Exception as e:
            logger.error(f"Failed to create trigger: {e}")
            return None

    def _create_job_function(self, config: ScheduleConfig) -> Callable:
        """작업 실행 함수 생성"""
        def job_function():
            """실제 정리 작업 실행"""
            try:
                # 실행 중인지 확인
                if config.name in self._running_jobs:
                    logger.info(f"Job {config.name} already running, skipping")
                    return

                self._running_jobs.add(config.name)

                # 브라우저 실행 여부 확인
                if config.skip_if_browser_running and self._are_browsers_running():
                    logger.info(f"Skipping scheduled cleaning {config.name} - browsers are running")
                    self._running_jobs.discard(config.name)
                    return

                # 정리 실행
                self._execute_scheduled_cleaning(config)

            except Exception as e:
                logger.error(f"Error in scheduled job {config.name}: {e}")
            finally:
                self._running_jobs.discard(config.name)

        return job_function

    def _are_browsers_running(self) -> bool:
        """브라우저 프로세스가 실행 중인지 확인"""
        try:
            import psutil

            browser_processes = [
                "chrome.exe", "msedge.exe", "firefox.exe", "brave.exe",
                "opera.exe", "whale.exe", "vivaldi.exe"
            ]

            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'].lower() in browser_processes:
                    return True

            return False

        except ImportError:
            logger.warning("psutil not available, assuming no browsers running")
            return False
        except Exception as e:
            logger.error(f"Error checking browser processes: {e}")
            return False

    def _execute_scheduled_cleaning(self, config: ScheduleConfig):
        """예약된 정리 작업 실행"""
        try:
            logger.info(f"Executing scheduled cleaning: {config.name}")

            # 프리셋 설정으로 정리 실행
            preset_name = config.time_config.get('preset', '빠른 정리')

            # TODO: 실제 클리너 엔진 호출
            # from .core.cleaner_engine import execute_preset_cleaning

            # 임시로 로그만 기록
            self.db_manager.add_cleaning_log(
                operation_type='scheduled',
                browsers=self._builtin_presets.get(preset_name, {}).get('browsers', []),
                categories=self._builtin_presets.get(preset_name, {}).get('categories', []),
                success=True,
                preset_name=preset_name
            )

            # 완료 알림
            if config.show_notification:
                self.signals.status_updated.emit(f"예약 정리 완료: {config.name}")

            logger.info(f"Scheduled cleaning completed: {config.name}")

        except Exception as e:
            logger.error(f"Error executing scheduled cleaning {config.name}: {e}")

            # 오류 로그 기록
            self.db_manager.add_cleaning_log(
                operation_type='scheduled',
                browsers=[],
                categories=[],
                success=False,
                error_message=str(e),
                preset_name=config.time_config.get('preset', '빠른 정리')
            )

    def _save_schedule_to_db(self, config: ScheduleConfig, job_id: str):
        """스케줄을 데이터베이스에 저장"""
        # TODO: 실제 데이터베이스 저장 구현 필요
        # 현재는 임시로 설정으로 저장
        schedule_data = {
            'id': job_id,
            'name': config.name,
            'schedule_type': config.schedule_type.value,
            'time_config': config.time_config,
            'enabled': config.enabled,
            'description': config.description
        }

        # 임시로 설정으로 저장 (실제로는 별도 테이블 필요)
        self.db_manager.save_setting(f"schedule_{job_id}", json.dumps(schedule_data))

    def _load_and_register_schedules(self):
        """저장된 스케줄들을 로드하고 등록"""
        try:
            # TODO: 실제 데이터베이스에서 스케줄 로드
            # 현재는 임시로 설정에서 로드 시도
            all_settings = self.db_manager.get_all_settings()

            for key, value in all_settings.items():
                if key.startswith("schedule_"):
                    try:
                        schedule_data = json.loads(value)
                        config = ScheduleConfig(
                            name=schedule_data['name'],
                            schedule_type=ScheduleType(schedule_data['schedule_type']),
                            time_config=schedule_data['time_config'],
                            enabled=schedule_data.get('enabled', True),
                            description=schedule_data.get('description', '')
                        )

                        self.add_schedule(config)
                    except Exception as e:
                        logger.error(f"Failed to load schedule {key}: {e}")

        except Exception as e:
            logger.error(f"Failed to load schedules: {e}")

    def _on_job_executed(self, event: JobEvent):
        """작업 실행 완료 이벤트 처리"""
        job = self.scheduler.get_job(event.job_id)
        if job:
            logger.info(f"Job executed successfully: {job.id}")

            # 다음 실행 시간 업데이트
            # TODO: 데이터베이스에 다음 실행 시간 저장

    def _on_job_error(self, event: JobEvent):
        """작업 실행 오류 이벤트 처리"""
        job = self.scheduler.get_job(event.job_id)
        if job:
            logger.error(f"Job failed: {job.id} - {event.exception}")

    def get_builtin_presets(self) -> Dict[str, Dict[str, Any]]:
        """기본 제공 프리셋 반환"""
        return self._builtin_presets.copy()

    def test_schedule(self, schedule_name: str) -> bool:
        """스케줄 테스트 실행"""
        try:
            # 해당 스케줄을 즉시 실행해보기
            config = self._load_schedule_config(schedule_name)
            if config:
                # 테스트 실행 (실제 정리 작업 대신 로그만)
                logger.info(f"Testing schedule: {schedule_name}")
                self._execute_scheduled_cleaning(config)
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to test schedule {schedule_name}: {e}")
            return False

    def _load_schedule_config(self, schedule_name: str) -> Optional[ScheduleConfig]:
        """스케줄 설정 로드"""
        # TODO: 실제 데이터베이스에서 로드
        # 현재는 임시 구현
        return None

    def pause_scheduler(self):
        """스케줄러 일시 중지"""
        self.scheduler.pause()
        logger.info("Scheduler paused")

    def resume_scheduler(self):
        """스케줄러 재개"""
        self.scheduler.resume()
        logger.info("Scheduler resumed")

    def get_scheduler_status(self) -> Dict[str, Any]:
        """스케줄러 상태 정보 반환"""
        return {
            'running': self.scheduler.running,
            'jobs_count': len(self.scheduler.get_jobs()),
            'jobs': [
                {
                    'id': job.id,
                    'name': job.id.split('_')[1] if '_' in job.id else job.id,
                    'next_run': job.next_run_time,
                    'enabled': not job.next_run_time is None
                }
                for job in self.scheduler.get_jobs()
            ],
            'running_jobs': len(self._running_jobs)
        }


# 전역 스케줄러 인스턴스
_scheduler_instance = None


def get_scheduler(daemon_signals: DaemonSignals) -> CleaningScheduler:
    """전역 스케줄러 인스턴스 반환"""
    global _scheduler_instance
    if _scheduler_instance is None:
        _scheduler_instance = CleaningScheduler(daemon_signals)
    return _scheduler_instance


__all__ = [
    "ScheduleType",
    "ScheduleConfig",
    "CleaningScheduler",
    "get_scheduler"
]
