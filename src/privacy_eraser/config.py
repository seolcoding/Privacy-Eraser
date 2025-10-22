"""Privacy Eraser Configuration

Environment-based configuration for development and production modes.
"""

import os
from pathlib import Path

# ═══════════════════════════════════════════════════════════
# Development Mode Configuration
# ═══════════════════════════════════════════════════════════


class AppConfig:
    """Application configuration (runtime modifiable)"""

    _dev_mode: bool = os.getenv("PRIVACY_ERASER_DEV_MODE", "false").lower() == "true"

    @classmethod
    def is_dev_mode(cls) -> bool:
        """Check if application is running in development mode"""
        return cls._dev_mode

    @classmethod
    def set_dev_mode(cls, enabled: bool):
        """Set development mode (runtime)"""
        cls._dev_mode = enabled

    @classmethod
    def toggle_dev_mode(cls) -> bool:
        """Toggle development mode and return new state"""
        cls._dev_mode = not cls._dev_mode
        return cls._dev_mode

# ═══════════════════════════════════════════════════════════
# Path Configuration
# ═══════════════════════════════════════════════════════════

# 프로젝트 루트 디렉토리
PROJECT_ROOT = Path(__file__).parent.parent.parent

# 테스트 데이터 디렉토리 (개발 모드용)
TEST_DATA_DIR = PROJECT_ROOT / "test_data"

# ═══════════════════════════════════════════════════════════
# Development Mode Settings
# ═══════════════════════════════════════════════════════════

# 브라우저별 더미 파일 개수 범위 (개발 모드용)
DEV_FILE_COUNTS = {
    "Chrome": (100, 150),
    "Firefox": (80, 120),
    "Edge": (70, 100),
    "Brave": (60, 90),
    "Opera": (50, 80),
    "Whale": (50, 80),
    "Safari": (40, 70),
}

# 더미 파일 크기 범위 (bytes)
DEV_FILE_SIZE_MIN = 1024  # 1 KB
DEV_FILE_SIZE_MAX = 5 * 1024 * 1024  # 5 MB

# ═══════════════════════════════════════════════════════════
# Utility Functions (Backward Compatibility)
# ═══════════════════════════════════════════════════════════


def is_dev_mode() -> bool:
    """Check if application is running in development mode"""
    return AppConfig.is_dev_mode()


def get_test_data_dir() -> Path:
    """Get test data directory path"""
    return TEST_DATA_DIR


def ensure_test_data_dir():
    """Create test data directory if it doesn't exist"""
    if not TEST_DATA_DIR.exists():
        TEST_DATA_DIR.mkdir(parents=True, exist_ok=True)
