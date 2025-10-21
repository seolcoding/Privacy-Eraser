"""백업/복원 관리 모듈

사용자가 삭제한 파일을 백업하고 복원할 수 있는 기능을 제공합니다.
"""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from loguru import logger


# 백업 디렉토리 (사용자 홈 디렉토리)
BACKUP_ROOT = Path.home() / ".privacy_eraser" / "backups"


class BackupMetadata:
    """백업 메타데이터"""

    def __init__(
        self,
        timestamp: str,
        browsers: list[str],
        delete_bookmarks: bool,
        delete_downloads: bool,
        files_count: int,
        total_size: int,
    ):
        self.timestamp = timestamp
        self.browsers = browsers
        self.delete_bookmarks = delete_bookmarks
        self.delete_downloads = delete_downloads
        self.files_count = files_count
        self.total_size = total_size

    def to_dict(self) -> dict:
        """딕셔너리로 변환"""
        return {
            "timestamp": self.timestamp,
            "browsers": self.browsers,
            "delete_bookmarks": self.delete_bookmarks,
            "delete_downloads": self.delete_downloads,
            "files_count": self.files_count,
            "total_size": self.total_size,
        }

    @classmethod
    def from_dict(cls, data: dict) -> BackupMetadata:
        """딕셔너리에서 생성"""
        return cls(
            timestamp=data["timestamp"],
            browsers=data["browsers"],
            delete_bookmarks=data.get("delete_bookmarks", False),
            delete_downloads=data.get("delete_downloads", False),
            files_count=data.get("files_count", 0),
            total_size=data.get("total_size", 0),
        )

    @property
    def display_name(self) -> str:
        """표시 이름"""
        dt = datetime.fromisoformat(self.timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S")


class BackupManager:
    """백업 관리자

    - 파일 백업 (삭제 전 복사)
    - 백업 목록 조회
    - 백업 복원
    - 오래된 백업 자동 정리
    """

    def __init__(self, retention_days: int = 7, max_backups: int = 5):
        """백업 관리자 초기화

        Args:
            retention_days: 백업 보관 일수 (기본 7일)
            max_backups: 최대 백업 개수 (기본 5개)
        """
        self.retention_days = retention_days
        self.max_backups = max_backups
        self.backup_root = BACKUP_ROOT
        self.backup_root.mkdir(parents=True, exist_ok=True)

    def create_backup(
        self,
        files_to_backup: list[Path],
        browsers: list[str],
        delete_bookmarks: bool = False,
        delete_downloads: bool = False,
    ) -> Optional[Path]:
        """파일 백업 생성

        Args:
            files_to_backup: 백업할 파일 경로 목록
            browsers: 선택된 브라우저 목록
            delete_bookmarks: 북마크 삭제 여부
            delete_downloads: 다운로드 삭제 여부

        Returns:
            백업 디렉토리 경로 (실패 시 None)
        """
        if not files_to_backup:
            logger.warning("백업할 파일이 없습니다")
            return None

        # 백업 디렉토리 생성 (타임스탬프)
        timestamp = datetime.now().isoformat(timespec="seconds")
        backup_dir = self.backup_root / timestamp.replace(":", "-")
        backup_dir.mkdir(parents=True, exist_ok=True)

        # 파일 복사
        copied_files = []
        total_size = 0

        for file_path in files_to_backup:
            if not file_path.exists():
                continue

            try:
                # 상대 경로 유지 (예: C:\Users\... -> Users\...)
                # Windows 절대 경로를 상대 경로로 변환
                if file_path.drive:
                    # C:\ 제거
                    relative_path = Path(*file_path.parts[1:])
                else:
                    relative_path = file_path

                dest_path = backup_dir / relative_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)

                # 파일 복사
                shutil.copy2(file_path, dest_path)
                copied_files.append({
                    "original": str(file_path),
                    "backup": str(relative_path),
                })
                total_size += dest_path.stat().st_size

            except Exception as e:
                logger.error(f"파일 백업 실패: {file_path} - {e}")
                continue

        if not copied_files:
            logger.error("백업된 파일이 없습니다")
            shutil.rmtree(backup_dir, ignore_errors=True)
            return None

        # 메타데이터 저장
        metadata = BackupMetadata(
            timestamp=timestamp,
            browsers=browsers,
            delete_bookmarks=delete_bookmarks,
            delete_downloads=delete_downloads,
            files_count=len(copied_files),
            total_size=total_size,
        )

        metadata_file = backup_dir / "metadata.json"
        metadata_file.write_text(
            json.dumps(
                {
                    **metadata.to_dict(),
                    "files": copied_files,
                },
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        logger.info(f"백업 생성 완료: {backup_dir} ({len(copied_files)}개 파일)")
        return backup_dir

    def list_backups(self) -> list[tuple[Path, BackupMetadata]]:
        """백업 목록 조회

        Returns:
            (백업 경로, 메타데이터) 튜플 리스트 (최신순)
        """
        backups = []

        for backup_dir in self.backup_root.iterdir():
            if not backup_dir.is_dir():
                continue

            metadata_file = backup_dir / "metadata.json"
            if not metadata_file.exists():
                continue

            try:
                data = json.loads(metadata_file.read_text(encoding="utf-8"))
                metadata = BackupMetadata.from_dict(data)
                backups.append((backup_dir, metadata))
            except Exception as e:
                logger.error(f"메타데이터 로드 실패: {metadata_file} - {e}")
                continue

        # 최신순 정렬
        backups.sort(key=lambda x: x[1].timestamp, reverse=True)
        return backups

    def restore_backup(self, backup_dir: Path) -> bool:
        """백업 복원

        Args:
            backup_dir: 백업 디렉토리 경로

        Returns:
            성공 여부
        """
        metadata_file = backup_dir / "metadata.json"
        if not metadata_file.exists():
            logger.error(f"메타데이터 파일이 없습니다: {metadata_file}")
            return False

        try:
            data = json.loads(metadata_file.read_text(encoding="utf-8"))
            files = data.get("files", [])

            restored_count = 0
            for file_info in files:
                backup_path = backup_dir / file_info["backup"]
                original_path = Path(file_info["original"])

                if not backup_path.exists():
                    logger.warning(f"백업 파일이 없습니다: {backup_path}")
                    continue

                try:
                    # 원본 경로에 파일 복원
                    original_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(backup_path, original_path)
                    restored_count += 1
                except Exception as e:
                    logger.error(f"파일 복원 실패: {original_path} - {e}")
                    continue

            logger.info(f"복원 완료: {restored_count}/{len(files)}개 파일")
            return restored_count > 0

        except Exception as e:
            logger.error(f"백업 복원 실패: {e}")
            return False

    def cleanup_old_backups(self) -> int:
        """오래된 백업 정리

        - retention_days보다 오래된 백업 삭제
        - max_backups개 초과 시 오래된 것부터 삭제

        Returns:
            삭제된 백업 개수
        """
        backups = self.list_backups()
        deleted_count = 0

        # 1. 날짜 기준 삭제
        cutoff_date = datetime.now() - timedelta(days=self.retention_days)
        for backup_dir, metadata in backups:
            backup_time = datetime.fromisoformat(metadata.timestamp)
            if backup_time < cutoff_date:
                try:
                    shutil.rmtree(backup_dir)
                    deleted_count += 1
                    logger.info(f"오래된 백업 삭제: {backup_dir.name}")
                except Exception as e:
                    logger.error(f"백업 삭제 실패: {backup_dir} - {e}")

        # 2. 개수 기준 삭제 (최신 max_backups개만 유지)
        remaining_backups = self.list_backups()
        if len(remaining_backups) > self.max_backups:
            for backup_dir, _ in remaining_backups[self.max_backups:]:
                try:
                    shutil.rmtree(backup_dir)
                    deleted_count += 1
                    logger.info(f"초과 백업 삭제: {backup_dir.name}")
                except Exception as e:
                    logger.error(f"백업 삭제 실패: {backup_dir} - {e}")

        return deleted_count

    def delete_backup(self, backup_dir: Path) -> bool:
        """특정 백업 삭제

        Args:
            backup_dir: 백업 디렉토리 경로

        Returns:
            성공 여부
        """
        try:
            shutil.rmtree(backup_dir)
            logger.info(f"백업 삭제: {backup_dir.name}")
            return True
        except Exception as e:
            logger.error(f"백업 삭제 실패: {backup_dir} - {e}")
            return False
