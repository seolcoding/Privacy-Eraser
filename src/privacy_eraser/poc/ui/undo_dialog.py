"""실행 취소 다이얼로그

백업 목록을 표시하고 복원할 수 있는 다이얼로그
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QMessageBox, QWidget
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from loguru import logger

from privacy_eraser.poc.ui.styles import Colors, Spacing, Sizes, Typography
from privacy_eraser.poc.core.backup_manager import BackupManager


class BackupListItem(QWidget):
    """백업 아이템 위젯"""

    restore_clicked = Signal(str)  # backup_dir path
    delete_clicked = Signal(str)   # backup_dir path

    def __init__(self, backup_dir_path: str, display_name: str, browsers: str, files_count: int, size_mb: float):
        super().__init__()
        self.backup_dir_path = backup_dir_path

        layout = QHBoxLayout(self)
        layout.setContentsMargins(Spacing.SM, Spacing.SM, Spacing.SM, Spacing.SM)
        layout.setSpacing(Spacing.MD)

        # 왼쪽: 정보
        info_layout = QVBoxLayout()
        info_layout.setSpacing(Spacing.XS)

        # 시간
        time_label = QLabel(f"📅 {display_name}")
        time_label.setFont(QFont(Typography.FONT_FAMILY, Typography.SIZE_BODY, Typography.WEIGHT_MEDIUM))
        info_layout.addWidget(time_label)

        # 브라우저
        browser_label = QLabel(f"🌐 {browsers}")
        browser_label.setFont(QFont(Typography.FONT_FAMILY, Typography.SIZE_CAPTION))
        browser_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        info_layout.addWidget(browser_label)

        # 파일 개수 & 크기
        stats_label = QLabel(f"📄 {files_count}개 파일 • {size_mb:.1f} MB")
        stats_label.setFont(QFont(Typography.FONT_FAMILY, Typography.SIZE_CAPTION))
        stats_label.setStyleSheet(f"color: {Colors.TEXT_HINT};")
        info_layout.addWidget(stats_label)

        layout.addLayout(info_layout, stretch=1)

        # 오른쪽: 버튼
        button_layout = QHBoxLayout()
        button_layout.setSpacing(Spacing.SM)

        # 복원 버튼
        restore_btn = QPushButton("↩️ 복원")
        restore_btn.setMinimumHeight(36)
        restore_btn.setFont(QFont(Typography.FONT_FAMILY, Typography.SIZE_BODY_SMALL, Typography.WEIGHT_MEDIUM))
        restore_btn.clicked.connect(lambda: self.restore_clicked.emit(self.backup_dir_path))
        button_layout.addWidget(restore_btn)

        # 삭제 버튼
        delete_btn = QPushButton("🗑️")
        delete_btn.setMinimumHeight(36)
        delete_btn.setMaximumWidth(40)
        delete_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.ERROR};
                color: white;
            }}
            QPushButton:hover {{
                background-color: #D32F2F;
            }}
        """)
        delete_btn.clicked.connect(lambda: self.delete_clicked.emit(self.backup_dir_path))
        button_layout.addWidget(delete_btn)

        layout.addLayout(button_layout)


class UndoDialog(QDialog):
    """실행 취소 다이얼로그

    - 백업 목록 표시 (최신 5개)
    - 복원 버튼
    - 삭제 버튼
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("실행 취소")
        self.setFixedSize(600, 500)
        self.setModal(True)

        # 백업 관리자
        self.backup_manager = BackupManager()

        # UI 구성
        self.setup_ui()

        # 백업 목록 로드
        self.load_backups()

    def setup_ui(self) -> None:
        """UI 구성"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(Spacing.LG, Spacing.LG, Spacing.LG, Spacing.LG)
        layout.setSpacing(Spacing.LG)

        # 제목
        title_label = QLabel("🔄 백업 목록")
        title_label.setFont(QFont(Typography.FONT_FAMILY, Typography.SIZE_H3, Typography.WEIGHT_BOLD))
        layout.addWidget(title_label)

        # 설명
        desc_label = QLabel("최근 삭제한 파일을 복원할 수 있습니다 (최대 5개, 7일간 보관)")
        desc_label.setFont(QFont(Typography.FONT_FAMILY, Typography.SIZE_BODY_SMALL))
        desc_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        layout.addWidget(desc_label)

        # 백업 목록
        self.backup_list = QListWidget()
        self.backup_list.setSpacing(Spacing.SM)
        layout.addWidget(self.backup_list)

        # 하단 버튼
        button_layout = QHBoxLayout()
        button_layout.setSpacing(Spacing.MD)
        button_layout.addStretch()

        # 새로고침 버튼
        refresh_btn = QPushButton("🔄 새로고침")
        refresh_btn.setMinimumHeight(Sizes.BUTTON_HEIGHT)
        refresh_btn.setFont(QFont(Typography.FONT_FAMILY, Typography.SIZE_BODY, Typography.WEIGHT_MEDIUM))
        refresh_btn.clicked.connect(self.load_backups)
        button_layout.addWidget(refresh_btn)

        # 닫기 버튼
        close_btn = QPushButton("닫기")
        close_btn.setMinimumHeight(Sizes.BUTTON_HEIGHT)
        close_btn.setFont(QFont(Typography.FONT_FAMILY, Typography.SIZE_BODY, Typography.WEIGHT_MEDIUM))
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)

        layout.addLayout(button_layout)

    def load_backups(self) -> None:
        """백업 목록 로드"""
        self.backup_list.clear()

        backups = self.backup_manager.list_backups()

        if not backups:
            # 백업이 없을 때
            item = QListWidgetItem(self.backup_list)
            item.setSizeHint(QWidget().sizeHint())

            empty_widget = QLabel("📭 백업이 없습니다")
            empty_widget.setAlignment(Qt.AlignCenter)
            empty_widget.setFont(QFont(Typography.FONT_FAMILY, Typography.SIZE_BODY))
            empty_widget.setStyleSheet(f"color: {Colors.TEXT_HINT}; padding: 40px;")

            self.backup_list.addItem(item)
            self.backup_list.setItemWidget(item, empty_widget)
            return

        # 백업 아이템 추가
        for backup_dir, metadata in backups:
            item = QListWidgetItem(self.backup_list)

            # 브라우저 문자열
            browsers_str = ", ".join(metadata.browsers)

            # 크기 (MB)
            size_mb = metadata.total_size / (1024 * 1024)

            # 백업 아이템 위젯
            backup_widget = BackupListItem(
                backup_dir_path=str(backup_dir),
                display_name=metadata.display_name,
                browsers=browsers_str,
                files_count=metadata.files_count,
                size_mb=size_mb,
            )
            backup_widget.restore_clicked.connect(self.on_restore_clicked)
            backup_widget.delete_clicked.connect(self.on_delete_clicked)

            item.setSizeHint(backup_widget.sizeHint())
            self.backup_list.addItem(item)
            self.backup_list.setItemWidget(item, backup_widget)

        logger.info(f"{len(backups)}개 백업 로드됨")

    def on_restore_clicked(self, backup_dir_path: str) -> None:
        """복원 버튼 클릭"""
        from pathlib import Path

        # 확인 다이얼로그
        reply = QMessageBox.question(
            self,
            "복원 확인",
            "선택한 백업을 복원하시겠습니까?\n\n"
            "⚠️ 주의: 현재 파일이 백업 파일로 덮어씌워집니다.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        # 복원 실행
        backup_dir = Path(backup_dir_path)
        success = self.backup_manager.restore_backup(backup_dir)

        if success:
            QMessageBox.information(
                self,
                "복원 완료",
                "✅ 백업이 성공적으로 복원되었습니다!"
            )
            self.accept()  # 다이얼로그 닫기
        else:
            QMessageBox.critical(
                self,
                "복원 실패",
                "❌ 백업 복원 중 오류가 발생했습니다."
            )

    def on_delete_clicked(self, backup_dir_path: str) -> None:
        """삭제 버튼 클릭"""
        from pathlib import Path

        # 확인 다이얼로그
        reply = QMessageBox.question(
            self,
            "백업 삭제 확인",
            "선택한 백업을 삭제하시겠습니까?\n\n"
            "⚠️ 주의: 삭제된 백업은 복구할 수 없습니다.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        # 삭제 실행
        backup_dir = Path(backup_dir_path)
        success = self.backup_manager.delete_backup(backup_dir)

        if success:
            QMessageBox.information(
                self,
                "삭제 완료",
                "✅ 백업이 삭제되었습니다."
            )
            self.load_backups()  # 목록 새로고침
        else:
            QMessageBox.critical(
                self,
                "삭제 실패",
                "❌ 백업 삭제 중 오류가 발생했습니다."
            )
