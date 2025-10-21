"""Privacy Eraser - FreeSimpleGUI POC

심플한 브라우저 개인정보 삭제 도구 (PySimpleGUI 무료 버전)
"""

import FreeSimpleGUI as sg
from typing import List, Dict, Tuple
from loguru import logger


# 테마 설정 (밝은 윈도우 스타일)
sg.theme('SystemDefault')

# 색상 정의
COLORS = {
    'primary': '#0078D4',      # 윈도우 블루
    'danger': '#D83B01',       # 빨간색 (삭제 버튼)
    'secondary': '#5A5A5A',    # 회색 (실행 취소)
    'text': '#000000',         # 검은색 텍스트
    'text_secondary': '#666666',  # 회색 텍스트
    'bg': '#FFFFFF',           # 흰색 배경
}

# 폰트 정의 (컴팩트)
FONTS = {
    'title': ('맑은 고딕', 13, 'bold'),
    'heading': ('맑은 고딕', 10, 'bold'),
    'body': ('맑은 고딕', 9),
    'body_bold': ('맑은 고딕', 9, 'bold'),
    'small': ('맑은 고딕', 8),
    'tiny': ('맑은 고딕', 7),
}


def create_browser_frame(browsers: List[Dict]) -> sg.Frame:
    """브라우저 선택 프레임 생성

    Args:
        browsers: 감지된 브라우저 정보 리스트

    Returns:
        브라우저 선택 프레임
    """
    # 브라우저를 2개씩 행으로 나누기 (컴팩트)
    browser_rows = []

    for i in range(0, len(browsers), 2):
        row_browsers = browsers[i:i+2]
        row = []

        for browser in row_browsers:
            name = browser.get('name', 'Unknown')
            is_installed = browser.get('installed', False)

            # 브라우저 아이콘 이모지 매핑
            icon_map = {
                'chrome': '🔵',
                'edge': '🌊',
                'firefox': '🦊',
                'brave': '🛡️',
                'opera': '⭕',
                'vivaldi': '🎵'
            }
            icon = icon_map.get(name.lower(), '🌐')

            # 체크박스 생성 (설치된 경우 기본 체크)
            checkbox = sg.Checkbox(
                f'{icon} {name}',
                key=f'-BROWSER-{name}-',
                default=is_installed,
                disabled=not is_installed,
                size=(15, 1),
                font=FONTS['body']
            )
            row.append(checkbox)

        # 행이 2개 미만이면 빈 공간 추가
        while len(row) < 2:
            row.append(sg.Text('', size=(15, 1)))

        browser_rows.append(row)

    # 브라우저가 없으면 기본 메시지
    if not browser_rows:
        browser_rows = [[sg.Text('브라우저를 감지하는 중...', font=FONTS['body'])]]

    layout = [
        *browser_rows,
    ]

    return sg.Frame('브라우저 선택', layout, font=FONTS['heading'], relief=sg.RELIEF_RIDGE,
                    title_color=COLORS['text'])


def create_options_frame() -> sg.Frame:
    """삭제 옵션 선택 프레임 생성"""
    layout = [
        [sg.Checkbox('전체 선택', key='-SELECT-ALL-', font=FONTS['body_bold'],
                     enable_events=True, text_color=COLORS['text'])],
        [sg.HorizontalSeparator()],
        [sg.Checkbox('북마크도 삭제', key='-DELETE-BOOKMARKS-', font=FONTS['body'],
                     pad=((20, 0), (8, 8)), text_color=COLORS['text'])],
        [sg.Checkbox('다운로드 파일도 삭제', key='-DELETE-DOWNLOADS-', font=FONTS['body'],
                     pad=((20, 0), (8, 8)), text_color=COLORS['text'])],
        [sg.Text('기본 삭제: 캐시, 쿠키, 히스토리, 세션, 비밀번호',
                 font=FONTS['small'], text_color=COLORS['text_secondary'], pad=((20, 0), (12, 8)))]
    ]

    return sg.Frame('삭제할 항목 선택', layout, font=FONTS['heading'], relief=sg.RELIEF_RIDGE,
                    title_color=COLORS['text'])


def create_action_buttons_frame() -> sg.Frame:
    """작업 버튼 프레임 생성"""
    layout = [
        [sg.Button('🗑️  삭제 실행', key='-CLEAN-', size=(18, 2),
                  font=FONTS['body_bold'],
                  button_color=('white', COLORS['danger']))],
        [sg.Text('')],  # 간격
        [sg.Button('🔄  실행 취소', key='-UNDO-', size=(18, 2),
                  font=FONTS['body'],
                  button_color=('white', COLORS['secondary']))],
    ]

    return sg.Frame('작업', layout, font=FONTS['heading'], relief=sg.RELIEF_RIDGE,
                    title_color=COLORS['text'])


def create_main_window(browsers: List[Dict]) -> sg.Window:
    """메인 윈도우 생성

    Args:
        browsers: 감지된 브라우저 정보 리스트

    Returns:
        PySimpleGUI 윈도우
    """
    # 레이아웃 구성
    layout = [
        # 타이틀
        [sg.Text('🛡️  Privacy Eraser POC', font=FONTS['title'],
                justification='center', expand_x=True, text_color=COLORS['primary'], pad=(0, 10))],
        [sg.Text('감지된 브라우저를 선택하고 개인정보를 삭제하세요',
                 font=FONTS['body'], justification='center', expand_x=True,
                 text_color=COLORS['text_secondary'], pad=(0, 5))],
        [sg.HorizontalSeparator(pad=(0, 5))],

        # 브라우저 선택 프레임 (전체 너비)
        [sg.Column([[create_browser_frame(browsers)]], expand_x=True, pad=(0, 0))],

        # 하단 컨트롤 영역을 하나의 프레임으로 묶기 (전체 너비)
        [sg.Column([[sg.Frame('', [
            [
                sg.Column([
                    [sg.Checkbox('전체 선택', key='-SELECT-ALL-', font=FONTS['body_bold'], enable_events=True)],
                    [sg.HorizontalSeparator()],
                    [sg.Checkbox('북마크도 삭제', key='-DELETE-BOOKMARKS-', font=FONTS['body'], pad=((15, 0), (5, 5)))],
                    [sg.Checkbox('다운로드 파일도 삭제', key='-DELETE-DOWNLOADS-', font=FONTS['body'], pad=((15, 0), (5, 5)))],
                    [sg.Text('기본 삭제: 캐시, 쿠키, 히스토리, 세션, 비밀번호',
                            font=FONTS['small'], text_color=COLORS['text_secondary'], pad=((15, 0), (8, 5)))]
                ], vertical_alignment='top', pad=(5, 5)),

                sg.Column([
                    [sg.Button('🗑️  삭제 실행', key='-CLEAN-', size=(14, 2),
                              font=FONTS['body_bold'],
                              button_color=('white', COLORS['danger']))],
                    [sg.Button('🔄  실행 취소', key='-UNDO-', size=(14, 2),
                              font=FONTS['body'],
                              button_color=('white', COLORS['secondary']))],
                ], vertical_alignment='top', expand_x=True, element_justification='right', pad=(5, 5))
            ]
        ], relief=sg.RELIEF_RIDGE, pad=(0, 5))]], expand_x=True, pad=(0, 0))],

        # 하단 크레딧
        [sg.Push(),
         sg.Text('developed with ❤️ by 설코딩 (seolcoding.com)',
                 font=FONTS['tiny'], text_color=COLORS['text_secondary'], pad=(0, 5)),
         sg.Push()],
    ]

    # 윈도우 생성
    window = sg.Window(
        'Privacy Eraser POC',
        layout,
        size=(475, 400),
        finalize=True,
        icon=None,
        resizable=False,  # 창 크기 고정
        element_justification='center'
    )

    return window


def show_progress_popup(browsers: List[str], delete_bookmarks: bool, delete_downloads: bool) -> Tuple[bool, Dict]:
    """삭제 진행 팝업 표시

    Args:
        browsers: 선택된 브라우저 목록
        delete_bookmarks: 북마크 삭제 여부
        delete_downloads: 다운로드 파일 삭제 여부

    Returns:
        (성공 여부, 통계 정보)
    """
    layout = [
        [sg.Text('브라우저 데이터 삭제 중...', font=FONTS['heading'], text_color=COLORS['text'])],
        [sg.ProgressBar(100, orientation='h', size=(40, 20), key='-PROGRESS-')],
        [sg.Text('', key='-STATUS-', size=(50, 2), font=FONTS['body'], text_color=COLORS['text'])],
        [sg.Button('취소', key='-CANCEL-', font=FONTS['body'])]
    ]

    window = sg.Window('삭제 진행 중', layout, modal=True, finalize=True)

    # 실제 삭제 작업 수행
    from privacy_eraser.psg_poc.cleaner_helper import clean_browsers_sync

    try:
        # 진행 상태 업데이트 콜백
        def progress_callback(path: str, size: int):
            window['-STATUS-'].update(f'삭제 중: {path[:50]}...\n크기: {size / 1024:.1f} KB')
            window['-PROGRESS-'].update(min(window['-PROGRESS-'].get() + 5, 95))
            event, _ = window.read(timeout=10)
            if event == '-CANCEL-':
                raise KeyboardInterrupt('사용자가 취소했습니다')

        # 삭제 시작
        window['-PROGRESS-'].update(0)

        stats = clean_browsers_sync(
            browsers=browsers,
            delete_bookmarks=delete_bookmarks,
            delete_downloads=delete_downloads,
            progress_callback=progress_callback
        )

        # 완료
        window['-PROGRESS-'].update(100)
        window['-STATUS-'].update('삭제 완료!')

        window.close()
        return True, stats

    except KeyboardInterrupt:
        logger.warning('사용자가 삭제를 취소했습니다')
        window.close()
        return False, {}

    except Exception as e:
        logger.error(f'삭제 중 오류: {e}')
        sg.popup_error(f'오류 발생:\n{str(e)}', title='오류')
        window.close()
        return False, {}


def show_completion_popup(stats: Dict):
    """삭제 완료 팝업"""
    total_files = stats.get('total_files', 0)
    total_size = stats.get('total_size', 0) / (1024 * 1024)  # MB

    message = f"""
삭제 완료!

삭제된 파일: {total_files}개
확보된 공간: {total_size:.2f} MB
    """

    sg.popup(message, title='완료', font=FONTS['body'], text_color=COLORS['text'])


def show_undo_dialog():
    """실행 취소 다이얼로그"""
    from privacy_eraser.poc.core.undo_manager import UndoManager

    undo_manager = UndoManager()
    backups = undo_manager.list_backups()

    if not backups:
        sg.popup('복원 가능한 백업이 없습니다.', title='실행 취소')
        return

    # 백업 목록 레이아웃
    backup_list = [
        [f"{i+1}. {backup['timestamp']} ({backup['files_count']}개 파일)"]
        for i, backup in enumerate(backups)
    ]

    layout = [
        [sg.Text('복원할 백업을 선택하세요', font=FONTS['heading'], text_color=COLORS['text'])],
        [sg.Listbox(
            values=[f"{i+1}. {b['timestamp']} ({b['files_count']}개 파일)" for i, b in enumerate(backups)],
            size=(50, 10),
            key='-BACKUP-LIST-',
            font=FONTS['body'],
            text_color=COLORS['text']
        )],
        [sg.Button('복원', key='-RESTORE-', font=FONTS['body']),
         sg.Button('취소', key='-CANCEL-', font=FONTS['body'])]
    ]

    window = sg.Window('실행 취소', layout, modal=True)

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, '-CANCEL-'):
            break

        if event == '-RESTORE-':
            selected = values['-BACKUP-LIST-']
            if selected:
                # 선택된 백업의 인덱스 추출
                backup_index = int(selected[0].split('.')[0]) - 1
                backup_id = backups[backup_index]['id']

                # 복원 확인
                confirm = sg.popup_yes_no(
                    f"{backups[backup_index]['timestamp']}의 백업을 복원하시겠습니까?",
                    title='확인'
                )

                if confirm == 'Yes':
                    try:
                        result = undo_manager.restore_backup(backup_id)
                        if result:
                            sg.popup('복원 완료!', title='성공')
                        else:
                            sg.popup_error('복원 실패', title='오류')
                    except Exception as e:
                        sg.popup_error(f'복원 중 오류:\n{str(e)}', title='오류')
                    break
            else:
                sg.popup('복원할 백업을 선택하세요', title='알림')

    window.close()
