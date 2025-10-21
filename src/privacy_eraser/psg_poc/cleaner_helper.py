"""PySimpleGUI용 동기 클리너 헬퍼

기존 CleanerWorker를 동기 방식으로 래핑
"""

import os
import time
from pathlib import Path
from typing import List, Dict, Callable, Optional
from loguru import logger

from privacy_eraser.poc.core.data_config import get_browser_xml_path, get_cleaner_options


def clean_browsers_sync(
    browsers: List[str],
    delete_bookmarks: bool = False,
    delete_downloads: bool = False,
    progress_callback: Optional[Callable[[str, int], None]] = None
) -> Dict:
    """브라우저 데이터 동기 삭제

    Args:
        browsers: 삭제할 브라우저 목록
        delete_bookmarks: 북마크 삭제 여부
        delete_downloads: 다운로드 파일 삭제 여부
        progress_callback: 진행 상황 콜백 (path, size)

    Returns:
        삭제 통계 딕셔너리
    """
    logger.info(f"동기 삭제 시작: {browsers}")

    total_files = 0
    deleted_files = 0
    total_size = 0

    # 백업 관리자
    from privacy_eraser.poc.core.backup_manager import BackupManager
    backup_manager = BackupManager()

    # 1. 파일 수집
    all_files = []
    options = get_cleaner_options(delete_bookmarks, delete_downloads)

    for browser in browsers:
        browser_files = _get_browser_files(browser, options)
        all_files.extend(browser_files)
        logger.info(f"{browser}: {len(browser_files)} 파일 수집됨")

    total_files = len(all_files)
    logger.info(f"총 {total_files}개 파일 수집됨")

    # 2. 백업 생성
    if all_files:
        existing_files = [Path(f) for f in all_files if os.path.exists(f)]

        if existing_files:
            try:
                backup_dir = backup_manager.create_backup(
                    files_to_backup=existing_files,
                    browsers=browsers,
                    delete_bookmarks=delete_bookmarks,
                    delete_downloads=delete_downloads,
                )
                if backup_dir:
                    logger.info(f"백업 생성 완료: {backup_dir}")
            except Exception as e:
                logger.warning(f"백업 생성 실패: {e}")

    # 3. 파일 삭제
    for file_path in all_files:
        try:
            file_size = _get_file_size(file_path) if os.path.exists(file_path) else 0

            # 파일 삭제
            _safe_delete(file_path)

            deleted_files += 1
            total_size += file_size

            # 진행 콜백
            if progress_callback:
                progress_callback(file_path, file_size)

            # 약간의 지연 (UI 업데이트)
            time.sleep(0.001)

        except Exception as e:
            logger.warning(f"파일 삭제 실패 {file_path}: {e}")

    logger.info(f"삭제 완료: {deleted_files}/{total_files} 파일, {total_size / (1024*1024):.2f} MB")

    return {
        'total_files': deleted_files,
        'total_size': total_size,
        'browsers': browsers
    }


def _get_browser_files(browser_name: str, options: List[str]) -> List[str]:
    """브라우저별 삭제 대상 파일 수집"""
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
                    expanded = _expand_path(action.path)
                    files.extend(expanded)

            except Exception as e:
                logger.debug(f"옵션 {option} 처리 실패: {e}")

    except Exception as e:
        logger.warning(f"{browser_name} CleanerML 처리 실패: {e}")

    return files


def _expand_path(path: str) -> List[str]:
    """경로 확장"""
    expanded_files = []

    try:
        expanded = os.path.expandvars(path)

        if "*" in expanded or "?" in expanded:
            from glob import glob
            matched = glob(expanded, recursive=True)
            expanded_files.extend(matched)
        else:
            if os.path.exists(expanded):
                expanded_files.append(expanded)

    except Exception as e:
        logger.debug(f"경로 확장 실패 {path}: {e}")

    return expanded_files


def _safe_delete(path: str) -> None:
    """안전하게 파일 삭제"""
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


def _get_file_size(path: str) -> int:
    """파일 크기 반환 (bytes)"""
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
