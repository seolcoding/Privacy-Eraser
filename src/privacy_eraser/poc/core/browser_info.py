"""브라우저 정보 데이터 클래스"""

from dataclasses import dataclass


@dataclass
class BrowserInfo:
    """감지된 브라우저 정보"""

    name: str  # Chrome, Firefox, Edge, etc.
    icon: str  # 이모지 (🌐, 🦊, 등)
    color: str  # Hex 색상 (#4285F4 등)
    installed: bool = True  # 설치 여부

    def __str__(self) -> str:
        """문자열 표현"""
        status = "✓" if self.installed else "✗"
        return f"{self.icon} {self.name} [{status}]"


@dataclass
class CleaningStats:
    """삭제 작업 통계"""

    total_files: int  # 총 파일 개수
    deleted_files: int  # 삭제된 파일 개수
    failed_files: int  # 실패한 파일 개수
    total_size: int  # 총 크기 (bytes)
    deleted_size: int  # 삭제된 크기 (bytes)
    duration: float  # 작업 소요 시간 (초)
    errors: list[str] = None  # 에러 메시지 목록

    def __post_init__(self):
        """초기화 후 처리"""
        if self.errors is None:
            self.errors = []

    @property
    def success_rate(self) -> float:
        """성공률 (0-100)"""
        if self.total_files == 0:
            return 100.0
        return (self.deleted_files / self.total_files) * 100

    @property
    def total_size_mb(self) -> float:
        """총 크기 (MB)"""
        return self.total_size / (1024 * 1024)

    @property
    def deleted_size_mb(self) -> float:
        """삭제된 크기 (MB)"""
        return self.deleted_size / (1024 * 1024)

    def __str__(self) -> str:
        """문자열 표현"""
        return (
            f"삭제 완료: {self.deleted_files}/{self.total_files} 파일 "
            f"({self.deleted_size_mb:.1f}MB / {self.total_size_mb:.1f}MB), "
            f"소요 시간: {self.duration:.1f}초"
        )
