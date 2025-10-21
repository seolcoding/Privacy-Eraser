"""Privacy Eraser - PySimpleGUI POC Main

심플한 브라우저 개인정보 삭제 도구 메인 앱
"""

import FreeSimpleGUI as sg
from loguru import logger
from typing import List, Dict

from privacy_eraser.psg_poc.gui import (
    create_main_window,
    show_progress_popup,
    show_completion_popup,
    show_undo_dialog
)


def detect_browsers() -> List[Dict]:
    """브라우저 감지

    Returns:
        감지된 브라우저 정보 리스트
    """
    try:
        from privacy_eraser.detect_windows import detect_browsers as detect

        detected = detect()
        browsers = []

        for browser in detected:
            browsers.append({
                'name': browser.get('name', 'Unknown'),
                'installed': browser.get('present') == 'yes'
            })

        logger.info(f"{len(browsers)}개 브라우저 감지됨")
        return browsers

    except Exception as e:
        logger.error(f"브라우저 감지 실패: {e}")
        return []


def get_selected_browsers(values: Dict, browsers: List[Dict]) -> List[str]:
    """선택된 브라우저 목록 반환

    Args:
        values: 윈도우 values
        browsers: 전체 브라우저 목록

    Returns:
        선택된 브라우저 이름 리스트
    """
    selected = []

    for browser in browsers:
        name = browser['name']
        key = f'-BROWSER-{name}-'

        if values.get(key, False):
            selected.append(name)

    return selected


def handle_select_all(window: sg.Window, values: Dict, browsers: List[Dict]):
    """전체 선택/해제 처리

    Args:
        window: 메인 윈도우
        values: 현재 values
        browsers: 브라우저 목록
    """
    is_checked = values['-SELECT-ALL-']

    # 개별 체크박스 업데이트
    window['-DELETE-BOOKMARKS-'].update(value=is_checked)
    window['-DELETE-DOWNLOADS-'].update(value=is_checked)

    logger.info(f"전체 선택: {is_checked}")


def main():
    """메인 앱 실행"""
    logger.info("Privacy Eraser POC (PySimpleGUI) 시작")

    # 브라우저 감지
    browsers = detect_browsers()

    if not browsers:
        sg.popup('감지된 브라우저가 없습니다.', title='알림')
        return

    # 메인 윈도우 생성
    window = create_main_window(browsers)

    # 이벤트 루프
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        # 전체 선택 이벤트
        if event == '-SELECT-ALL-':
            handle_select_all(window, values, browsers)

        # 삭제 실행 버튼
        if event == '-CLEAN-':
            selected_browsers = get_selected_browsers(values, browsers)

            if not selected_browsers:
                sg.popup('선택된 브라우저가 없습니다.', title='알림')
                continue

            delete_bookmarks = values['-DELETE-BOOKMARKS-']
            delete_downloads = values['-DELETE-DOWNLOADS-']

            # 확인 팝업
            confirm = sg.popup_yes_no(
                f"선택된 브라우저: {', '.join(selected_browsers)}\n"
                f"북마크 삭제: {'예' if delete_bookmarks else '아니오'}\n"
                f"다운로드 파일 삭제: {'예' if delete_downloads else '아니오'}\n\n"
                f"정말 삭제하시겠습니까?",
                title='확인'
            )

            if confirm == 'Yes':
                logger.info(f"삭제 시작: {selected_browsers}")

                # 진행 팝업 표시 및 삭제 실행
                success, stats = show_progress_popup(
                    selected_browsers,
                    delete_bookmarks,
                    delete_downloads
                )

                if success:
                    show_completion_popup(stats)

        # 실행 취소 버튼
        if event == '-UNDO-':
            show_undo_dialog()

    window.close()
    logger.info("Privacy Eraser POC 종료")


if __name__ == '__main__':
    main()
