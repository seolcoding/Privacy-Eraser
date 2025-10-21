"""POC 메인 윈도우"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QCheckBox, QScrollArea, QFrame
)
from PySide6.QtCore import Qt, Signal, QThread, QTimer
from PySide6.QtGui import QFont

from loguru import logger

from privacy_eraser.poc.ui.styles import Colors, Spacing, Sizes, Typography, get_stylesheet
from privacy_eraser.poc.ui.browser_card import BrowserCard
from privacy_eraser.poc.ui.progress_dialog import ProgressDialog
from privacy_eraser.poc.core.browser_info import BrowserInfo, CleaningStats
from privacy_eraser.poc.core.data_config import (
    get_browser_display_name, get_browser_icon, get_browser_color
)


class BrowserDetectionThread(QThread):
    """브라우저 감지 스레드"""

    browsers_detected = Signal(list)  # List[BrowserInfo]

    def run(self):
        """브라우저 감지 실행"""
        try:
            from privacy_eraser.detect_windows import detect_browsers
            from privacy_eraser.poc.core.data_config import (
                get_browser_icon, get_browser_color
            )

            detected = detect_browsers()
            browsers = []

            for browser in detected:
                browser_name = browser.get("name", "Unknown").lower()
                icon = get_browser_icon(browser_name)
                color = get_browser_color(browser_name)

                browser_info = BrowserInfo(
                    name=browser.get("name", "Unknown"),
                    icon=icon,
                    color=color,
                    installed=browser.get("present") == "yes"
                )
                browsers.append(browser_info)

            self.browsers_detected.emit(browsers)

        except Exception as e:
            logger.error(f"브라우저 감지 실패: {e}")
            self.browsers_detected.emit([])


class MainWindow(QMainWindow):
    """POC 메인 윈도우

    - 감지된 브라우저를 카드 그리드로 표시
    - 북마크 삭제 토글
    - 메인 삭제 버튼
    """

    def __init__(self, auto_detect: bool = True):
        """메인 윈도우 초기화

        Args:
            auto_detect: 자동 브라우저 감지 여부 (테스트에서는 False)
        """
        super().__init__()
        self.setWindowTitle("Privacy Eraser POC")
        self.setFixedSize(Sizes.MAIN_WINDOW_WIDTH, Sizes.MAIN_WINDOW_HEIGHT)

        # 상태 변수
        self.detected_browsers: list[BrowserInfo] = []
        self.browser_cards: dict[str, BrowserCard] = {}
        self.delete_bookmarks = False
        self.delete_downloads = False  # 다운로드 파일 삭제 옵션
        self.cleaner_worker = None
        self.progress_dialog = None

        # 선택된 브라우저 추적
        self.selected_browsers: dict[str, bool] = {}

        # UI 구성
        self.setup_ui()
        self.apply_styles()

        # 브라우저 감지 시작 (별도 스레드)
        if auto_detect:
            self.detect_browsers_async()

    def setup_ui(self) -> None:
        """UI 구성"""
        # 메인 위젯
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 메인 레이아웃
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(Spacing.LG, Spacing.LG, Spacing.LG, Spacing.LG)
        main_layout.setSpacing(Spacing.LG)

        # 제목
        title_label = QLabel("🛡️  Privacy Eraser POC")
        title_font = QFont(Typography.FONT_FAMILY, Typography.SIZE_H2, Typography.WEIGHT_BOLD)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)

        # 설명
        description_label = QLabel("감지된 브라우저를 선택하고 개인정보를 삭제하세요")
        description_font = QFont(Typography.FONT_FAMILY, Typography.SIZE_BODY)
        description_label.setFont(description_font)
        description_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        main_layout.addWidget(description_label)

        # 브라우저 카드 컨테이너 (스크롤 없이 고정, 4x3 그리드)
        cards_container = QWidget()
        self.cards_layout = QGridLayout(cards_container)
        self.cards_layout.setSpacing(Spacing.MD)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)

        # 고정 높이 설정 (3행 * 180px + 간격)
        cards_container.setMinimumHeight(3 * (Sizes.CARD_HEIGHT + Spacing.MD))

        main_layout.addWidget(cards_container)

        # 스페이서 추가 (나머지 공간 차지)
        main_layout.addStretch()

        # 하단 영역: 추가 옵션 + 안내 텍스트 + 삭제 버튼 (같은 수평선)
        footer_layout = QHBoxLayout()
        footer_layout.setSpacing(Spacing.LG)

        # 좌측: 옵션 영역
        left_section = QVBoxLayout()
        left_section.setSpacing(Spacing.SM)

        options_label = QLabel("추가 옵션:")
        options_label.setFont(QFont(Typography.FONT_FAMILY, Typography.SIZE_BODY, Typography.WEIGHT_MEDIUM))
        left_section.addWidget(options_label)

        # 북마크 체크박스
        self.bookmark_checkbox = QCheckBox("북마크도 삭제")
        self.bookmark_checkbox.setFont(QFont(Typography.FONT_FAMILY, Typography.SIZE_BODY))
        self.bookmark_checkbox.stateChanged.connect(self.on_bookmark_toggle)
        left_section.addWidget(self.bookmark_checkbox)

        # 다운로드 파일 체크박스
        self.downloads_checkbox = QCheckBox("다운로드 파일도 삭제")
        self.downloads_checkbox.setFont(QFont(Typography.FONT_FAMILY, Typography.SIZE_BODY))
        self.downloads_checkbox.stateChanged.connect(self.on_downloads_toggle)
        left_section.addWidget(self.downloads_checkbox)

        # 안내 텍스트
        info_label = QLabel("기본 삭제: 캐시, 쿠키, 히스토리, 세션, 비밀번호")
        info_label.setFont(QFont(Typography.FONT_FAMILY, Typography.SIZE_CAPTION))
        info_label.setStyleSheet(f"color: {Colors.TEXT_HINT};")
        left_section.addWidget(info_label)

        footer_layout.addLayout(left_section)

        # 중간 스페이서
        footer_layout.addStretch()

        # 우측: 버튼 영역
        right_buttons = QHBoxLayout()
        right_buttons.setSpacing(Spacing.MD)

        # 실행 취소 버튼
        self.undo_button = QPushButton("↩️  실행 취소")
        self.undo_button.setMinimumWidth(140)
        self.undo_button.setMinimumHeight(Sizes.BUTTON_HEIGHT)
        self.undo_button.setFont(QFont(Typography.FONT_FAMILY, Typography.SIZE_BODY, Typography.WEIGHT_MEDIUM))
        self.undo_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.SECONDARY};
                color: white;
            }}
            QPushButton:hover {{
                background-color: {Colors.SECONDARY_DARK};
            }}
        """)
        self.undo_button.clicked.connect(self.on_undo_clicked)
        right_buttons.addWidget(self.undo_button)

        # 삭제 버튼
        self.clean_button = QPushButton("🗑️  개인정보 지우기")
        self.clean_button.setMinimumWidth(200)
        self.clean_button.setMinimumHeight(Sizes.BUTTON_HEIGHT)
        self.clean_button.setFont(QFont(Typography.FONT_FAMILY, Typography.SIZE_BODY, Typography.WEIGHT_MEDIUM))
        self.clean_button.clicked.connect(self.on_clean_clicked)
        right_buttons.addWidget(self.clean_button)

        footer_layout.addLayout(right_buttons, alignment=Qt.AlignRight | Qt.AlignVCenter)

        main_layout.addLayout(footer_layout)

    def apply_styles(self) -> None:
        """스타일 적용"""
        self.setStyleSheet(get_stylesheet())

    def detect_browsers_async(self) -> None:
        """비동기로 브라우저 감지"""
        # 감지 스레드 생성 및 시작
        self.detection_thread = BrowserDetectionThread()
        self.detection_thread.browsers_detected.connect(self.on_browsers_detected)
        self.detection_thread.start()

    def on_browsers_detected(self, browsers: list[BrowserInfo]) -> None:
        """브라우저 감지 완료 시"""
        # 설치된 브라우저만 필터링
        installed_browsers = [b for b in browsers if b.installed]

        logger.info(f"{len(browsers)}개 브라우저 스캔, {len(installed_browsers)}개 설치됨")
        self.detected_browsers = installed_browsers

        # 카드 생성 및 그리드에 추가 (설치된 브라우저만)
        for i, browser_info in enumerate(installed_browsers):
            row = i // 3
            col = i % 3

            card = BrowserCard(browser_info)
            card.selection_changed.connect(self.on_browser_selection_changed)

            self.browser_cards[browser_info.name] = card
            self.selected_browsers[browser_info.name] = True
            self.cards_layout.addWidget(card, row, col)

    def on_browser_selection_changed(self, browser_name: str, is_selected: bool) -> None:
        """브라우저 선택 상태 변경"""
        self.selected_browsers[browser_name] = is_selected
        logger.info(f"{browser_name}: {'선택' if is_selected else '미선택'}")

    def on_bookmark_toggle(self, state: int) -> None:
        """북마크 토글"""
        self.delete_bookmarks = self.bookmark_checkbox.isChecked()
        logger.info(f"북마크 삭제: {self.delete_bookmarks}")

    def on_downloads_toggle(self, state: int) -> None:
        """다운로드 파일 토글"""
        self.delete_downloads = self.downloads_checkbox.isChecked()
        logger.info(f"다운로드 파일 삭제: {self.delete_downloads}")

    def on_undo_clicked(self) -> None:
        """실행 취소 버튼 클릭"""
        from privacy_eraser.poc.ui.undo_dialog import UndoDialog

        dialog = UndoDialog(self)
        dialog.exec()

    def on_clean_clicked(self) -> None:
        """삭제 버튼 클릭"""
        # 선택된 브라우저 확인
        selected = [name for name, selected in self.selected_browsers.items() if selected]

        if not selected:
            logger.warning("선택된 브라우저가 없습니다")
            return

        logger.info(f"삭제 시작: {', '.join(selected)} 브라우저")

        # 진행 팝업 표시
        self.start_cleaning(selected)

    def start_cleaning(self, selected_browsers: list[str]) -> None:
        """삭제 작업 시작

        Args:
            selected_browsers: 선택된 브라우저 이름 목록
        """
        # 진행 팝업 생성
        self.progress_dialog = ProgressDialog(self)
        self.progress_dialog.show()

        # 워커 스레드에서 삭제 작업 수행 (임시: 시뮬레이션)
        self.simulate_cleaning(selected_browsers)

    def simulate_cleaning(self, selected_browsers: list[str]) -> None:
        """삭제 시뮬레이션 (테스트용)"""
        # 실제 CleanerWorker 사용 (또는 시뮬레이션 워커)
        from privacy_eraser.poc.core.poc_cleaner import CleanerWorker

        # 워커 스레드 생성
        self.cleaner_worker = CleanerWorker(
            browsers=selected_browsers,
            delete_bookmarks=self.delete_bookmarks,
            delete_downloads=self.delete_downloads
        )

        # 시그널 연결
        self.cleaner_worker.started.connect(
            lambda: self.progress_dialog.start_cleaning()
        )
        self.cleaner_worker.progress_updated.connect(
            lambda path, size: self.progress_dialog.update_progress(path, size)
        )
        self.cleaner_worker.cleaning_finished.connect(
            lambda stats: self.progress_dialog.show_completion(stats)
        )
        self.cleaner_worker.error_occurred.connect(
            lambda error: self.progress_dialog.show_error(error)
        )

        # 워커 시작
        self.cleaner_worker.start()
