# Privacy Eraser - TODO

다음 작업 목록 및 우선순위입니다.

---

## 📝 작업 우선순위

| 순위 | 작업 | 예상 시간 | 난이도 |
|------|------|-----------|--------|
| 1 | DEV 모드 경고 메시지 | 10분 | ⭐ |
| 2 | 커스텀 앱 아이콘 | 30분 | ⭐ |
| 3 | 시스템 트레이 기능 | 1시간 | ⭐⭐ |
| 4 | 트레이 간편 예약 메뉴 | 1시간 | ⭐⭐ |
| 5 | 예약 실행 30초 전 알림 | 1.5시간 | ⭐⭐⭐ |
| 6 | 브라우저 설정 보존 | 2시간 | ⭐⭐⭐ |

**권장 작업 순서**: 1 → 2 → 3 → 4 → 5 → 6

---

## 1. DEV 모드 경고 메시지 추가 ⏳

**목적**: 개발자가 DEV 모드에서 작업 중임을 명확히 인지하도록 함

**구현 위치**: `src/privacy_eraser/ui/main.py`

**상세 내용**:
- UI 상단 또는 삭제 버튼 근처에 경고 배너 표시
- 메시지: "⚠️ 개발자 모드: 실제 파일이 삭제되지 않습니다"
- 배경색: `AppColors.WARNING` (amber)
- 조건: `AppConfig.is_dev_mode()` 확인

**구현 예시**:
```python
if AppConfig.is_dev_mode():
    ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.INFO_ROUNDED, color=AppColors.WARNING),
            ft.Text("개발자 모드: 실제 파일이 삭제되지 않습니다")
        ]),
        bgcolor=f"{AppColors.WARNING}20",
        padding=8,
        border_radius=6
    )
```

---

## 2. 브라우저 설정 보존 (초기화 방지) 🔧

**문제**: 현재 sync 옵션으로 브라우저 동기화 데이터를 삭제하면 브라우저가 완전히 초기화됨

**목표**: 개인정보만 삭제하고 브라우저 설정(테마, 확장프로그램 설정 등)은 유지

**분석 필요**:
1. CleanerML에서 어떤 파일들이 설정 관련인지 확인
2. `sync` 옵션이 삭제하는 파일 목록 검토
3. Preferences, Local State 파일 중 어떤 키를 보존해야 하는지 확인

**제외해야 할 항목** (예상):
- `Preferences` 파일의 특정 섹션 (테마, UI 설정)
- `Local State` 파일의 프로필 리스트 제외 항목
- 확장프로그램 설정 (`Extension Settings/`)

**구현 방법**:
1. `sync` 옵션을 더 세밀하게 분리
2. JSON 파일 부분 삭제 기능 구현 (특정 키만 삭제)
3. 또는 `sync` 옵션을 제거하고 개별 파일만 삭제

**참고**:
- `src/privacy_eraser/cleaners/google_chrome.xml` - sync 옵션
- `src/privacy_eraser/cleaners/whale.xml` - sync 옵션

---

## 3. 시스템 트레이 기능 구현 🖥️

**목적**: 앱을 최소화해도 백그라운드에서 실행 유지

**구현 사항**:
- 창 닫기 버튼 클릭 시 → 트레이로 최소화
- 트레이 아이콘 더블클릭 → 창 복원
- 트레이 우클릭 메뉴:
  - "열기"
  - "종료"

**Flet 구현**:
```python
def window_event_handler(e):
    if e.data == "close":
        page.window_minimized = True
        # Show tray notification
        page.show_snack_bar(
            ft.SnackBar(content=ft.Text("트레이로 최소화되었습니다"))
        )

page.window_prevent_close = True
page.on_window_event = window_event_handler
```

**참고 문서**: `ai-docs/flet.md` - Window Events 섹션

**추가 기능**:
- 트레이 알림: "Privacy Eraser가 백그라운드에서 실행 중입니다"
- 시작 프로그램 등록 옵션 (선택사항)

---

## 4. 커스텀 앱 아이콘 제작 및 적용 🎨

**현재 문제**: Flet 기본 아이콘 사용 중

**작업 내용**:
1. **아이콘 디자인**
   - 테마: 빗자루 + 자물쇠/방패 조합
   - 색상: 메인 컬러 (#6366F1 Indigo) 기반
   - 크기: 256x256, 128x128, 64x64, 32x32, 16x16

2. **파일 형식**
   - Windows: `.ico` 파일
   - macOS: `.icns` 파일
   - Linux: `.png` 파일

3. **저장 위치**
   - `static/icons/app_icon.ico`
   - `static/icons/app_icon.png`

4. **적용 방법**
   ```python
   # main.py
   page.window_icon = "static/icons/app_icon.png"

   # Flet build 시
   flet build windows --icon static/icons/app_icon.ico
   ```

**디자인 도구**:
- 무료: GIMP, Inkscape
- 온라인: favicon.io, flaticon.com

**참고**:
- Flet 아이콘 설정: `ai-docs/flet.md` 참고

---

## 5. 트레이 간편 예약 메뉴 🕐

**목적**: 트레이 메뉴에서 빠르게 예약 설정

**트레이 우클릭 메뉴 구조**:
```
Privacy Eraser
├── 열기
├── 간편 예약 ▶
│   ├── 10분 후
│   ├── 30분 후
│   ├── 1시간 후
│   ├── 3시간 후
│   └── 예약 취소
├── 예약 목록 보기
└── 종료
```

**구현 방법**:
1. 간편 예약용 임시 스케줄 생성
2. `ScheduleManager`에 one-time 스케줄 추가
3. 기존 간편 예약이 있으면 덮어쓰기

**코드 예시**:
```python
def create_quick_schedule(minutes: int):
    schedule_time = datetime.now() + timedelta(minutes=minutes)

    scenario = ScheduleScenario(
        id="quick_schedule",
        name=f"{minutes}분 후 자동 삭제",
        enabled=True,
        schedule_type="once",
        time=schedule_time.strftime("%H:%M"),
        browsers=get_selected_browsers(),
        delete_bookmarks=False,
        delete_downloads=False,
        created_at=datetime.now().isoformat(),
        description=f"트레이 간편 예약: {minutes}분 후 실행"
    )

    schedule_manager.add_schedule(scenario)
```

**참고 파일**:
- `src/privacy_eraser/core/schedule_manager.py`
- `src/privacy_eraser/schedule_executor.py`

---

## 6. 예약 실행 30초 전 알림 및 취소 옵션 ⏰

**목적**: 사용자가 실수로 예약을 설정했을 경우 마지막 기회 제공

**구현 내용**:

1. **30초 전 알림 표시**
   - 시스템 트레이 알림
   - 앱이 열려있으면 Dialog 표시
   - 메시지: "30초 후 브라우저 데이터가 삭제됩니다"

2. **카운트다운 UI**
   ```python
   ft.AlertDialog(
       title=ft.Text("예약 실행 알림"),
       content=ft.Column([
           ft.Text("30초 후 다음 작업이 실행됩니다:"),
           ft.Text(f"• 브라우저: {', '.join(browsers)}"),
           ft.Text(f"• 삭제 항목: 쿠키, 히스토리, 세션"),
           ft.Text(f"남은 시간: {countdown}초",
                   size=24, weight=ft.FontWeight.BOLD)
       ]),
       actions=[
           ft.TextButton("취소", on_click=cancel_schedule),
           ft.ElevatedButton("지금 실행", on_click=execute_now),
       ]
   )
   ```

3. **취소 기능**
   - "취소" 버튼 클릭 → 예약 비활성화 (삭제하지 않음)
   - "지금 실행" 버튼 → 즉시 실행
   - 30초 경과 → 자동 실행

4. **구현 위치**
   - `src/privacy_eraser/schedule_executor.py`의 `execute_scenario()` 함수 시작 부분
   - 또는 APScheduler의 `before_job` 이벤트 활용

**스케줄러 수정**:
```python
def execute_scenario_with_countdown(scenario: ScheduleScenario):
    # 30초 카운트다운 및 알림
    if not show_countdown_notification(scenario, timeout=30):
        logger.info("User cancelled scheduled execution")
        return

    # 기존 실행 로직
    execute_scenario(scenario)
```

**알림 방법**:
1. Flet Dialog (앱이 실행 중일 때)
2. Windows 알림 (`plyer` 라이브러리 사용)
   ```python
   from plyer import notification
   notification.notify(
       title="Privacy Eraser",
       message="30초 후 브라우저 데이터가 삭제됩니다",
       timeout=30
   )
   ```
