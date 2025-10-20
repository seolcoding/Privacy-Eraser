"""POC 삭제 워커 - 별도 스레드에서 파일 삭제 수행"""

import os
import time
from pathlib import Path
from typing import Optional

from PySide6.QtCore import QThread, Signal
from loguru import logger

from privacy_eraser.poc.core.browser_info import CleaningStats
from privacy_eraser.poc.core.data_config import (
    get_browser_xml_path, get_cleaner_options, DEFAULT_CLEANER_OPTIONS, BOOKMARK_OPTIONS
)


class CleanerWorker(QThread):
    """별도 스레드에서 파일 삭제 작업 수행"""

    # 시그널
    started = Signal()  # 작업 시작
    progress_updated = Signal(str, int)  # (file_path, file_size)
    cleaning_finished = Signal(CleaningStats)  # 작업 완료
    error_occurred = Signal(str)  # 에러 발생

    def __init__(self, browsers: list[str], delete_bookmarks: bool = False, parent=None):
        """
        Args:
            browsers: 선택된 브라우저 목록
            delete_bookmarks: 북마크 삭제 여부
            parent: 부모 위젯
        """
        super().__init__(parent)
        self.browsers = browsers
        self.delete_bookmarks = delete_bookmarks
        self.is_cancelled = False

    def run(self) -> None:
        """메인 삭제 로직 (별도 스레드에서 실행)"""
        self.started.emit()

        start_time = time.time()
        stats = CleaningStats(
            total_files=0,
            deleted_files=0,
            failed_files=0,
            total_size=0,
            deleted_size=0,
            duration=0,
            errors=[]
        )

        try:
            # 1. 삭제 대상 파일 수집
            all_files = self._collect_files_to_delete()

            stats.total_files = len(all_files)
            stats.total_size = sum(
                self._get_file_size(f) for f in all_files if os.path.exists(f)
            )

            logger.info(f"삭제 대상: {stats.total_files} 파일, {stats.total_size / (1024*1024):.1f} MB")

            # 2. 파일 삭제
            for file_path in all_files:
                if self.is_cancelled:
                    logger.info("삭제 작업 취소됨")
                    break

                try:
                    file_size = self._get_file_size(file_path) if os.path.exists(file_path) else 0

                    # 파일 삭제
                    self._safe_delete(file_path)

                    stats.deleted_files += 1
                    stats.deleted_size += file_size

                    # UI 업데이트
                    self.progress_updated.emit(file_path, file_size)

                    # 시각적 효과를 위해 약간의 지연
                    time.sleep(0.001)

                except Exception as e:
                    stats.failed_files += 1
                    error_msg = f"{file_path}: {str(e)}"
                    stats.errors.append(error_msg)
                    logger.warning(f"삭제 실패: {error_msg}")

            stats.duration = time.time() - start_time
            logger.info(f"삭제 완료: {stats.deleted_files}/{stats.total_files} 파일, "
                       f"{stats.duration:.1f}초")

            self.cleaning_finished.emit(stats)

        except Exception as e:
            logger.error(f"삭제 작업 실패: {e}")
            self.error_occurred.emit(str(e))

    def _collect_files_to_delete(self) -> list[str]:
        """삭제 대상 파일 수집

        기존 detect_windows, cleanerml_loader 재사용
        """
        files = []

        # 옵션 정의
        options = get_cleaner_options(self.delete_bookmarks)

        for browser in self.browsers:
            try:
                # 브라우저별 파일 경로 수집
                browser_files = self._get_browser_files(browser, options)
                files.extend(browser_files)
                logger.info(f"{browser}: {len(browser_files)} 파일 수집됨")

            except Exception as e:
                logger.warning(f"{browser} 파일 수집 실패: {e}")

        return files

    def _get_browser_files(self, browser_name: str, options: list[str]) -> list[str]:
        """브라우저별 삭제 대상 파일 수집

        기존 cleanerml_loader, file_utils 활용
        """
        files = []

        try:
            # XML 파일 로드
            xml_path = get_browser_xml_path(browser_name)
            if not xml_path:
                logger.warning(f"CleanerML 경로 없음: {browser_name}")
                return files

            # 기존 cleanerml_loader 사용
            from privacy_eraser.cleanerml_loader import load_cleanerml

            cleaner_def = load_cleanerml(xml_path)

            # 옵션별 파일 수집
            for option in options:
                try:
                    actions = cleaner_def.get_actions(option)
                    for action in actions:
                        # 경로 확장
                        expanded = self._expand_path(action.path)
                        files.extend(expanded)

                except Exception as e:
                    logger.debug(f"옵션 {option} 처리 실패: {e}")

        except Exception as e:
            logger.warning(f"{browser_name} CleanerML 처리 실패: {e}")

        return files

    def _expand_path(self, path: str) -> list[str]:
        """경로 확장 (%LOCALAPPDATA%, %APPDATA% 등)"""
        expanded_files = []

        try:
            # 환경변수 확장
            expanded = os.path.expandvars(path)

            # 글로브 패턴 처리
            if "*" in expanded or "?" in expanded:
                # glob 사용
                from glob import glob
                matched = glob(expanded, recursive=True)
                expanded_files.extend(matched)
            else:
                # 파일/디렉토리 존재 확인
                if os.path.exists(expanded):
                    expanded_files.append(expanded)

        except Exception as e:
            logger.debug(f"경로 확장 실패 {path}: {e}")

        return expanded_files

    def _safe_delete(self, path: str) -> None:
        """안전하게 파일 삭제

        기존 file_utils.safe_delete 사용
        """
        try:
            from privacy_eraser.core.file_utils import safe_delete

            safe_delete(path)

        except Exception as e:
            # 재귀적으로 삭제 시도
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
        """파일 크기 반환 (bytes)"""
        try:
            if os.path.isfile(path):
                return os.path.getsize(path)
            elif os.path.isdir(path):
                # 디렉토리 크기
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

    def cancel(self) -> None:
        """작업 취소"""
        logger.info("삭제 작업 취소 요청됨")
        self.is_cancelled = True
