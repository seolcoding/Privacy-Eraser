"""브라우저 카드 위젯 - 감지된 브라우저 시각화"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve, QSize
from PySide6.QtGui import QFont
import qtawesome as qta

from privacy_eraser.poc.core.browser_info import BrowserInfo
from privacy_eraser.poc.ui.styles import Colors, Spacing, Sizes, Typography, Animation


class BrowserCard(QWidget):
    """브라우저 카드 위젯

    아이콘, 브라우저 이름, 체크박스를 포함한 카드
    호버 시 그림자 효과 추가
    """

    # 시그널
    selection_changed = Signal(str, bool)  # (browser_name, is_selected)

    def __init__(self, browser_info: BrowserInfo, parent=None):
        """
        Args:
            browser_info: BrowserInfo 데이터클래스
            parent: 부모 위젯
        """
        super().__init__(parent)
        self.browser_info = browser_info
        self.is_selected = True  # 기본: 모두 선택
        self.is_hovered = False

        self.setup_ui()
        self.apply_styles()

    def setup_ui(self) -> None:
        """UI 구성"""
        # 메인 레이아웃
        layout = QVBoxLayout(self)
        layout.setContentsMargins(Spacing.CARD_PADDING, Spacing.CARD_PADDING,
                                  Spacing.CARD_PADDING, Spacing.CARD_PADDING)
        layout.setSpacing(Spacing.MD)

        # 아이콘 레이블 (qtawesome 사용, 48px)
        icon_label = QLabel()
        icon_label.setAlignment(Qt.AlignCenter)

        # qtawesome 아이콘 생성 (48px)
        try:
            icon = qta.icon(
                self.browser_info.icon,
                color=self.browser_info.color,
                scale_factor=1.5  # 1.5배 크기
            )
            pixmap = icon.pixmap(QSize(48, 48))  # 48x48 픽셀
            icon_label.setPixmap(pixmap)
        except Exception as e:
            # qtawesome 아이콘 로드 실패 시 텍스트로 표시
            icon_label.setText(self.browser_info.name[0])  # 첫 글자
            icon_label.setFont(QFont(Typography.FONT_FAMILY, 32, Typography.WEIGHT_BOLD))
            icon_label.setStyleSheet(f"color: {self.browser_info.color};")

        layout.addWidget(icon_label)

        # 브라우저 이름
        name_label = QLabel(self.browser_info.name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setFont(QFont(Typography.FONT_FAMILY, Typography.SIZE_BODY, Typography.WEIGHT_MEDIUM))
        layout.addWidget(name_label)

        # 체크박스
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(self.is_selected)
        self.checkbox.setText("선택")
        self.checkbox.stateChanged.connect(self.on_checkbox_toggled)
        layout.addWidget(self.checkbox, alignment=Qt.AlignCenter)

        # 스페이서 추가
        layout.addStretch()

        # 고정 크기 설정
        self.setFixedSize(Sizes.CARD_WIDTH, Sizes.CARD_HEIGHT)

    def apply_styles(self) -> None:
        """스타일 적용"""
        stylesheet = f"""
        BrowserCard {{
            background-color: {Colors.SURFACE};
            border: 2px solid {Colors.SURFACE_VARIANT};
            border-radius: {Sizes.CARD_RADIUS}px;
        }}
        """
        self.setStyleSheet(stylesheet)

    def enterEvent(self, event) -> None:
        """마우스 호버 시 테두리 강조"""
        super().enterEvent(event)
        self.is_hovered = True

        # 호버 시 테두리 강조
        self.setStyleSheet(f"""
        BrowserCard {{
            background-color: {Colors.SURFACE};
            border: 3px solid {Colors.PRIMARY_LIGHT};
            border-radius: {Sizes.CARD_RADIUS}px;
        }}
        """)

    def leaveEvent(self, event) -> None:
        """마우스 떠날 때 테두리 복원"""
        super().leaveEvent(event)
        self.is_hovered = False

        # 테두리 원상복구
        selected_border = Colors.PRIMARY if self.is_selected else Colors.SURFACE_VARIANT
        self.setStyleSheet(f"""
        BrowserCard {{
            background-color: {Colors.SURFACE};
            border: 2px solid {selected_border};
            border-radius: {Sizes.CARD_RADIUS}px;
        }}
        """)

    def on_checkbox_toggled(self, state: int) -> None:
        """체크박스 토글 시"""
        self.is_selected = self.checkbox.isChecked()

        # 선택 상태에 따라 스타일 변경
        border_color = Colors.PRIMARY if self.is_selected else Colors.SURFACE_VARIANT
        self.setStyleSheet(f"""
        BrowserCard {{
            background-color: {Colors.SURFACE};
            border: 2px solid {border_color};
            border-radius: {Sizes.CARD_RADIUS}px;
        }}
        """)

        # 시그널 발생
        self.selection_changed.emit(self.browser_info.name, self.is_selected)

    def is_checked(self) -> bool:
        """선택 상태 반환"""
        return self.is_selected

    def set_checked(self, checked: bool) -> None:
        """선택 상태 설정"""
        self.checkbox.setChecked(checked)
