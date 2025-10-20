from __future__ import annotations

import sqlite3
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional


DB_PATH = Path.home() / ".privacy_eraser" / "privacy_eraser.db"


def _resolve_db_path(db_path: Path | str | None = None) -> Path:
    """Return the active database path."""
    if db_path is not None:
        return Path(db_path)
    return Path(DB_PATH)


def _ensure_db_directory(db_path: Path) -> None:
    """Ensure the database directory exists."""
    db_path.parent.mkdir(parents=True, exist_ok=True)


class DatabaseManager:
    """Privacy Eraser database manager."""

    def __init__(self, db_path: Path | str | None = None):
        self.db_path = _resolve_db_path(db_path)
        self._ensure_database()

    def _ensure_database(self):
        """Create the database file and schema if missing."""
        _ensure_db_directory(self.db_path)

        conn = sqlite3.connect(self.db_path)
        try:
            # 설정 테이블
            conn.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
            """)

            # 정리 작업 로그 테이블
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cleaning_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    operation_type TEXT NOT NULL,  -- 'manual', 'scheduled', 'preset'
                    browsers TEXT,                 -- JSON array of browser names
                    categories TEXT,               -- JSON array of cleaned categories
                    items_deleted INTEGER DEFAULT 0,
                    bytes_deleted INTEGER DEFAULT 0,
                    duration_seconds INTEGER DEFAULT 0,
                    success BOOLEAN DEFAULT 1,
                    error_message TEXT,
                    preset_name TEXT               -- 사용된 프리셋 이름 (있는 경우)
                )
            """)

            # 스케줄 테이블
            conn.execute("""
                CREATE TABLE IF NOT EXISTS schedules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    schedule_type TEXT NOT NULL,   -- 'daily', 'weekly', 'monthly', 'idle'
                    time_config TEXT NOT NULL,     -- JSON configuration
                    enabled BOOLEAN DEFAULT 1,
                    last_run TIMESTAMP,
                    next_run TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 프리셋 테이블
            conn.execute("""
                CREATE TABLE IF NOT EXISTS presets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    description TEXT,
                    config TEXT NOT NULL,          -- JSON configuration
                    is_builtin BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 브라우저 상태 캐시 테이블 (실시간 모니터링용)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS browser_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    browser_name TEXT NOT NULL,
                    cache_size_bytes INTEGER DEFAULT 0,
                    cookie_count INTEGER DEFAULT 0,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(browser_name)
                )
            """)

            # 통계 집계 테이블 (성능을 위해 미리 계산된 값들)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS statistics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE NOT NULL,
                    total_cleanings INTEGER DEFAULT 0,
                    total_bytes_deleted INTEGER DEFAULT 0,
                    total_items_deleted INTEGER DEFAULT 0,
                    browser_stats TEXT,            -- JSON per browser stats
                    category_stats TEXT,           -- JSON per category stats
                    UNIQUE(date)
                )
            """)
        finally:
            conn.close()

    # 설정 관리 메서드들
    def save_setting(self, key: str, value: str) -> None:
        """설정 저장"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO settings (key, value, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)",
                (key, value),
            )

    def load_setting(self, key: str, default: str = "") -> str:
        """설정 로드"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT value FROM settings WHERE key = ?", (key,))
            row = cursor.fetchone()
            return row[0] if row else default

    def get_all_settings(self) -> Dict[str, str]:
        """모든 설정 반환"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT key, value FROM settings")
            return dict(cursor.fetchall())

    # 로그 관리 메서드들
    def add_cleaning_log(self, operation_type: str, browsers: List[str],
                        categories: List[str], items_deleted: int = 0,
                        bytes_deleted: int = 0, duration_seconds: int = 0,
                        success: bool = True, error_message: str = None,
                        preset_name: str = None) -> int:
        """정리 작업 로그 추가"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT INTO cleaning_logs
                (operation_type, browsers, categories, items_deleted, bytes_deleted,
                 duration_seconds, success, error_message, preset_name)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                operation_type,
                json.dumps(browsers),
                json.dumps(categories),
                items_deleted,
                bytes_deleted,
                duration_seconds,
                success,
                error_message,
                preset_name
            ))
            
            return cursor.lastrowid

    def get_cleaning_logs(self, limit: int = 100, offset: int = 0,
                         operation_type: str = None, success: bool = None) -> List[Dict]:
        """정리 로그 조회"""
        with sqlite3.connect(self.db_path) as conn:
            query = "SELECT * FROM cleaning_logs ORDER BY timestamp DESC LIMIT ? OFFSET ?"
            params = [limit, offset]

            if operation_type or success is not None:
                conditions = []
                if operation_type:
                    conditions.append("operation_type = ?")
                    params.insert(0, operation_type)
                if success is not None:
                    conditions.append("success = ?")
                    params.insert(0, success)

                if conditions:
                    query = f"SELECT * FROM cleaning_logs WHERE {' AND '.join(conditions)} ORDER BY timestamp DESC LIMIT ? OFFSET ?"
                    params.extend([limit, offset])

            cursor = conn.execute(query, params)
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_log_statistics(self, days: int = 30) -> Dict[str, Any]:
        """로그 기반 통계 계산"""
        since_date = datetime.now() - timedelta(days=days)

        with sqlite3.connect(self.db_path) as conn:
            # 기본 통계
            cursor = conn.execute("""
                SELECT
                    COUNT(*) as total_cleanings,
                    SUM(items_deleted) as total_items,
                    SUM(bytes_deleted) as total_bytes,
                    AVG(duration_seconds) as avg_duration
                FROM cleaning_logs
                WHERE timestamp >= ? AND success = 1
            """, (since_date,))

            basic_stats = cursor.fetchone()

            # 브라우저별 통계
            cursor = conn.execute("""
                SELECT
                    json_extract(browsers, '$[0]') as browser,
                    COUNT(*) as count,
                    SUM(bytes_deleted) as total_bytes
                FROM cleaning_logs
                WHERE timestamp >= ? AND success = 1
                GROUP BY browser
                ORDER BY total_bytes DESC
            """, (since_date,))

            browser_stats = cursor.fetchall()

            # 카테고리별 통계
            cursor = conn.execute("""
                SELECT
                    json_extract(value, '$') as category,
                    COUNT(*) as count,
                    SUM(bytes_deleted) as total_bytes
                FROM cleaning_logs,
                     json_each(categories)
                WHERE timestamp >= ? AND success = 1
                GROUP BY category
                ORDER BY total_bytes DESC
            """, (since_date,))

            category_stats = cursor.fetchall()

            return {
                'total_cleanings': basic_stats[0] or 0,
                'total_items_deleted': basic_stats[1] or 0,
                'total_bytes_deleted': basic_stats[2] or 0,
                'avg_duration_seconds': basic_stats[3] or 0,
                'browser_stats': [
                    {'browser': row[0], 'count': row[1], 'bytes': row[2]}
                    for row in browser_stats
                ],
                'category_stats': [
                    {'category': row[0], 'count': row[1], 'bytes': row[2]}
                    for row in category_stats
                ]
            }

    # 브라우저 캐시 관리 메서드들
    def update_browser_cache(self, browser_name: str, cache_size_bytes: int,
                           cookie_count: int) -> None:
        """브라우저 캐시 정보 업데이트"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO browser_cache
                (browser_name, cache_size_bytes, cookie_count, last_updated)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            """, (browser_name, cache_size_bytes, cookie_count))
            

    def get_browser_cache_info(self) -> Dict[str, Dict[str, Any]]:
        """브라우저 캐시 정보 조회"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT browser_name, cache_size_bytes, cookie_count, last_updated
                FROM browser_cache
            """)
            return {
                row[0]: {
                    'cache_size_bytes': row[1],
                    'cookie_count': row[2],
                    'last_updated': row[3]
                }
                for row in cursor.fetchall()
            }

    # 통계 관리 메서드들
    def update_daily_statistics(self, date: str = None) -> None:
        """일일 통계 업데이트"""
        if date is None:
            date = datetime.now().date().isoformat()

        stats = self.get_log_statistics(days=1)

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO statistics
                (date, total_cleanings, total_bytes_deleted, total_items_deleted,
                 browser_stats, category_stats)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                date,
                stats['total_cleanings'],
                stats['total_bytes_deleted'],
                stats['total_items_deleted'],
                json.dumps(stats['browser_stats']),
                json.dumps(stats['category_stats'])
            ))
            

    def get_statistics(self, days: int = 30) -> Dict[str, Any]:
        """기간별 통계 조회"""
        start_date = (datetime.now() - timedelta(days=days)).date()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT * FROM statistics
                WHERE date >= ?
                ORDER BY date DESC
            """, (start_date,))

            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()

            # 데이터 변환
            statistics_data = []
            for row in rows:
                row_dict = dict(zip(columns, row))
                row_dict['browser_stats'] = json.loads(row_dict['browser_stats'] or '[]')
                row_dict['category_stats'] = json.loads(row_dict['category_stats'] or '[]')
                statistics_data.append(row_dict)

            return {
                'period_days': days,
                'start_date': start_date.isoformat(),
                'daily_stats': statistics_data,
                'summary': self._calculate_summary_stats(statistics_data)
            }

    def _calculate_summary_stats(self, daily_stats: List[Dict]) -> Dict[str, Any]:
        """일일 통계로부터 종합 통계 계산"""
        if not daily_stats:
            return {
                'total_cleanings': 0,
                'total_bytes_deleted': 0,
                'total_items_deleted': 0,
                'avg_cleanings_per_day': 0,
                'avg_bytes_per_day': 0
            }

        total_cleanings = sum(stat['total_cleanings'] for stat in daily_stats)
        total_bytes = sum(stat['total_bytes_deleted'] for stat in daily_stats)
        total_items = sum(stat['total_items_deleted'] for stat in daily_stats)

        return {
            'total_cleanings': total_cleanings,
            'total_bytes_deleted': total_bytes,
            'total_items_deleted': total_items,
            'avg_cleanings_per_day': total_cleanings / len(daily_stats),
            'avg_bytes_per_day': total_bytes / len(daily_stats)
        }

    # 유틸리티 메서드들
    def cleanup_old_logs(self, days_to_keep: int = 90) -> int:
        """오래된 로그 정리"""
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "DELETE FROM cleaning_logs WHERE timestamp < ?",
                (cutoff_date,)
            )
            deleted_count = cursor.rowcount
            
            return deleted_count

    def get_database_info(self) -> Dict[str, Any]:
        """데이터베이스 정보 반환"""
        with sqlite3.connect(self.db_path) as conn:
            # 테이블별 레코드 수
            tables = ['settings', 'cleaning_logs', 'schedules', 'presets', 'browser_cache', 'statistics']
            counts = {}

            for table in tables:
                cursor = conn.execute(f"SELECT COUNT(*) FROM {table}")
                counts[table] = cursor.fetchone()[0]

            # 데이터베이스 파일 크기
            db_size = self.db_path.stat().st_size if self.db_path.exists() else 0

            return {
                'database_path': str(self.db_path),
                'database_size_bytes': db_size,
                'table_counts': counts,
                'created_at': datetime.fromtimestamp(self.db_path.stat().st_ctime) if self.db_path.exists() else None
            }


# 전역 데이터베이스 관리자 인스턴스
_db_manager: DatabaseManager | None = None


def init_settings_db() -> None:
    """Initialise the database (idempotent)."""
    get_database_manager()


def save_setting(key: str, value: str) -> None:
    """Persist a user setting."""
    db_path = _resolve_db_path()
    _ensure_db_directory(db_path)
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            "INSERT OR REPLACE INTO settings (key, value, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)",
            (key, value),
        )
        conn.commit()
    finally:
        conn.close()


def load_setting(key: str, default: str = "") -> str:
    """Load a setting, falling back to the provided default."""
    db_path = _resolve_db_path()
    _ensure_db_directory(db_path)
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = cursor.fetchone()
        return row[0] if row else default
    finally:
        conn.close()


def get_database_manager() -> DatabaseManager:
    """Return a singleton database manager for the active path."""
    global _db_manager
    current_path = _resolve_db_path()
    if (_db_manager is None) or (_db_manager.db_path != current_path):
        _db_manager = DatabaseManager(current_path)
    return _db_manager


__all__ = [
    "DatabaseManager",
    "get_database_manager",
    "init_settings_db",
    "save_setting",
    "load_setting",
]


