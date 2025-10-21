"""삭제 진행 팝업 다이얼로그"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar,
    QListWidget, QListWidgetItem, QPushButton, QFrame
)
from PySide6.QtCore import Qt, Signal, QTimer, QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtGui import QFont, QColor

from privacy_eraser.poc.core.browser_info import CleaningStats
from privacy_eraser.poc.ui.styles import Colors, Spacing, Sizes, Typography


class ProgressDialog(QDialog):
    """삭제 진행 팝업 다이얼로그

    실시간 파일 삭제 리스트, 프로그레스 바, 카운터를 표시
    """

    # 시그널
    cancelled = Signal()

    def __init__(self, parent=None):
        """
        Args:
            parent: 부모 위젯
        """
        super().__init__(parent)
        self.total_files = 0
        self.total_size = 0
        self.deleted_files = 0
        self.deleted_size = 0
        self.is_started = False  # 시작 여부
        self.is_completed = False  # 완료 여부

        # 카운터 애니메이션
        self.counter_animation_timer = QTimer()
        self.counter_animation_timer.timeout.connect(self.animate_counter)
        self.animated_files = 0
        self.animated_size = 0

        # 스피너 애니메이션 (진행 중 표시)
        self.spinner_timer = QTimer()
        self.spinner_timer.timeout.connect(self.update_spinner)
        self.spinner_frame = 0
        self.spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

        self.setup_ui()
        self.apply_styles()

    def setup_ui(self) -> None:
        """UI 구성"""
        self.setWindowTitle("개인정보 삭제 중...")
        self.setModal(True)
        self.setFixedSize(Sizes.PROGRESS_DIALOG_WIDTH, Sizes.PROGRESS_DIALOG_HEIGHT)

        # 메인 레이아웃
        layout = QVBoxLayout(self)
        layout.setContentsMargins(Spacing.CARD_PADDING, Spacing.CARD_PADDING,
                                  Spacing.CARD_PADDING, Spacing.CARD_PADDING)
        layout.setSpacing(Spacing.LG)

        # 상태 메시지
        self.status_label = QLabel("💚 개인정보가 안전하게 삭제되고 있습니다")
        status_font = QFont(Typography.FONT_FAMILY, Typography.SIZE_BODY, Typography.WEIGHT_MEDIUM)
        self.status_label.setFont(status_font)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet(f"color: {Colors.SUCCESS};")
        layout.addWidget(self.status_label)

        # 카운터 레이블
        counter_layout = QHBoxLayout()
        self.counter_label = QLabel()
        self.counter_label.setFont(QFont(Typography.FONT_FAMILY, Typography.SIZE_BODY))
        self.counter_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        counter_layout.addWidget(self.counter_label)
        counter_layout.addStretch()
        layout.addLayout(counter_layout)

        # 용량 레이블
        self.size_label = QLabel()
        self.size_label.setFont(QFont(Typography.FONT_FAMILY, Typography.SIZE_CAPTION))
        self.size_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        layout.addWidget(self.size_label)

        # 프로그레스 바
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet(f"""
        QProgressBar {{
            border: none;
            border-radius: 4px;
            background-color: {Colors.SURFACE_VARIANT};
            height: 8px;
        }}
        QProgressBar::chunk {{
            background-color: {Colors.PRIMARY};
            border-radius: 4px;
        }}
        """)
        layout.addWidget(self.progress_bar)

        # 파일 리스트 레이블
        files_label = QLabel("삭제 중인 파일들:")
        files_label.setFont(QFont(Typography.FONT_FAMILY, Typography.SIZE_BODY, Typography.WEIGHT_MEDIUM))
        layout.addWidget(files_label)

        # 파일 리스트
        self.file_list = QListWidget()
        self.file_list.setStyleSheet(f"""
        QListWidget {{
            border: 1px solid {Colors.SURFACE_VARIANT};
            border-radius: 8px;
            background-color: {Colors.SURFACE};
            color: {Colors.TEXT_PRIMARY};
            font-family: "{Typography.FONT_FAMILY}";
            font-size: {Typography.SIZE_CAPTION}px;
        }}
        QListWidget::item {{
            padding: 4px;
            margin: 1px 0;
        }}
        QListWidget::item:hover {{
            background-color: {Colors.SURFACE_VARIANT};
        }}
        """)
        layout.addWidget(self.file_list)

        # 현재 파일 레이블
        self.current_file_label = QLabel()
        self.current_file_label.setFont(QFont(Typography.FONT_FAMILY, Typography.SIZE_CAPTION))
        self.current_file_label.setStyleSheet(f"color: {Colors.TEXT_HINT};")
        self.current_file_label.setWordWrap(True)
        layout.addWidget(self.current_file_label)

    def apply_styles(self) -> None:
        """다이얼로그 스타일 적용"""
        self.setStyleSheet(f"""
        QDialog {{
            background-color: {Colors.BACKGROUND};
        }}
        """)

    def set_total_files(self, total: int) -> None:
        """전체 파일 개수 설정"""
        self.total_files = total
        # 프로그레스 바는 항상 0-100 백분율로 동작
        self.progress_bar.setMaximum(100)
        self.update_counter()

    def set_total_size(self, total: int) -> None:
        """전체 크기 설정 (bytes)"""
        self.total_size = total
        self.update_counter()

    def update_progress(self, file_path: str, file_size: int) -> None:
        """파일 삭제 시 진행 상황 업데이트

        Args:
            file_path: 삭제된 파일 경로
            file_size: 파일 크기 (bytes)
        """
        self.deleted_files += 1
        self.deleted_size += file_size

        # 리스트에 추가
        self.add_file_to_list(file_path)

        # 현재 파일 표시
        self.current_file_label.setText(f"현재: {file_path}")

        # 프로그레스 바 업데이트
        if self.total_files > 0:
            progress = int((self.deleted_files / self.total_files) * 100)
            self.progress_bar.setValue(progress)

        # 카운터 애니메이션 시작
        self.animate_to(self.deleted_files, self.deleted_size)

    def add_file_to_list(self, file_path: str) -> None:
        """리스트에 파일 경로 추가 (실시간)"""
        # 경로 단축 (너무 길면 앞부분 자르기)
        display_path = file_path
        if len(display_path) > 70:
            display_path = "..." + display_path[-67:]

        item = QListWidgetItem(display_path)
        item.setForeground(QColor(Colors.TEXT_SECONDARY))
        self.file_list.addItem(item)

        # 자동 스크롤 (맨 아래로)
        self.file_list.scrollToBottom()

    def update_counter(self) -> None:
        """카운터 레이블 업데이트"""
        if self.total_files > 0:
            self.counter_label.setText(
                f"삭제된 파일: {self.deleted_files} / {self.total_files}"
            )

        if self.total_size > 0:
            deleted_mb = self.deleted_size / (1024 * 1024)
            total_mb = self.total_size / (1024 * 1024)
            self.size_label.setText(
                f"삭제된 용량: {deleted_mb:.1f} MB / {total_mb:.1f} MB"
            )

    def animate_to(self, target_files: int, target_size: int) -> None:
        """카운터를 목표값으로 부드럽게 애니메이션"""
        self.counter_animation_timer.stop()
        self.counter_animation_timer.start(10)  # 10ms마다 업데이트

        # 목표값 저장 (애니메이션 중 사용)
        self.target_files = target_files
        self.target_size = target_size

    def animate_counter(self) -> None:
        """카운터 애니메이션 프레임"""
        # 파일 개수 증가
        if self.animated_files < self.target_files:
            increment = max(1, (self.target_files - self.animated_files) // 10)
            self.animated_files = min(self.animated_files + increment, self.target_files)

        # 용량 증가
        if self.animated_size < self.target_size:
            increment = max(1, (self.target_size - self.animated_size) // 10)
            self.animated_size = min(self.animated_size + increment, self.target_size)

        # 레이블 업데이트
        if self.total_files > 0:
            self.counter_label.setText(
                f"삭제된 파일: {self.animated_files} / {self.total_files}"
            )

        if self.total_size > 0:
            deleted_mb = self.animated_size / (1024 * 1024)
            total_mb = self.total_size / (1024 * 1024)
            self.size_label.setText(
                f"삭제된 용량: {deleted_mb:.1f} MB / {total_mb:.1f} MB"
            )

        # 애니메이션 종료 조건
        if self.animated_files >= self.target_files and self.animated_size >= self.target_size:
            self.counter_animation_timer.stop()

    def start_cleaning(self) -> None:
        """삭제 시작 - 준비 중 상태 표시"""
        self.is_started = True
        self.status_label.setText("🔍 삭제 대상 파일을 검색하는 중...")
        self.status_label.setStyleSheet(f"color: {Colors.PRIMARY};")

        # 스피너 애니메이션 시작
        self.spinner_timer.start(100)  # 100ms마다 업데이트

    def update_spinner(self) -> None:
        """스피너 애니메이션 업데이트"""
        if self.is_completed:
            self.spinner_timer.stop()
            return

        # 스피너 문자 회전
        spinner = self.spinner_chars[self.spinner_frame % len(self.spinner_chars)]
        self.spinner_frame += 1

        # 상태 메시지 업데이트 (스피너 포함)
        if not self.total_files:
            self.status_label.setText(f"{spinner} 삭제 대상 파일을 검색하는 중...")
        else:
            self.status_label.setText(f"{spinner} 개인정보를 안전하게 삭제하는 중...")

    def show_completion(self, stats: CleaningStats) -> None:
        """완료 결과 표시"""
        self.is_completed = True
        self.spinner_timer.stop()

        # 큰 체크마크와 성공 메시지
        self.status_label.setText(f"✅ 삭제 완료! ({stats.duration:.1f}초 소요)")
        self.status_label.setStyleSheet(f"color: {Colors.SUCCESS}; font-size: 18px; font-weight: bold;")

        # 최종 통계
        self.counter_label.setText(
            f"✓ 삭제된 파일: {stats.deleted_files} / {stats.total_files}"
        )
        self.counter_label.setStyleSheet(f"color: {Colors.SUCCESS};")

        self.size_label.setText(
            f"✓ 삭제된 용량: {stats.deleted_size_mb:.1f} MB / {stats.total_size_mb:.1f} MB"
        )
        self.size_label.setStyleSheet(f"color: {Colors.SUCCESS};")

        # 프로그레스 바 완성
        self.progress_bar.setValue(100)
        self.progress_bar.setStyleSheet(f"""
        QProgressBar {{
            border: none;
            border-radius: 4px;
            background-color: {Colors.SURFACE_VARIANT};
            height: 8px;
        }}
        QProgressBar::chunk {{
            background-color: {Colors.SUCCESS};
            border-radius: 4px;
        }}
        """)

    def show_error(self, error_msg: str) -> None:
        """에러 표시"""
        self.status_label.setText(f"⚠️ 삭제 중단: {error_msg}")
        self.status_label.setStyleSheet(f"color: {Colors.ERROR};")

    def closeEvent(self, event) -> None:
        """다이얼로그 닫기 시"""
        self.counter_animation_timer.stop()
        super().closeEvent(event)
