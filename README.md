# Privacy Eraser

🛡️ 브라우저 개인정보 자동 삭제 프로그램

## Features

- 🔍 자동 브라우저 감지 (Chrome, Edge, Firefox, Brave, Opera, Whale, Safari)
- 🗑️ 원클릭 개인정보 삭제 (캐시, 쿠키, 히스토리, 세션, 비밀번호)
- 📚 북마크/다운로드 삭제 옵션
- ⏰ 스케줄 관리 (시간별/일별/주별/월별 자동 실행)
- 🔔 Windows 알림 (작업 완료 시 토스트 알림)
- ↩️ 백업/복원 기능
- 🎨 Material Design 3 UI (Flet/Flutter)

## Download

[![Download Latest](https://img.shields.io/github/v/release/seolcoding/Privacy-Eraser?label=Download&style=for-the-badge)](https://github.com/seolcoding/Privacy-Eraser/releases/latest)

**설치 방법:**
1. 최신 릴리즈에서 ZIP 파일 다운로드
2. 압축 해제 후 `privacy_eraser.exe` 실행

## Development

### Requirements

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager

### Setup

```bash
# Install dependencies
uv sync

# Run application
python -m privacy_eraser.ui.main

# Or use entry point
privacy_eraser

# Run tests
uv run pytest
```

### Build & Release

```bash
# Build and release to GitHub (Flutter build)
scripts/release_flutter.bat 2.0.5

# Output: PrivacyEraser-v2.0.5-win-x64.zip
```

**Requirements for Build:**
- Flutter SDK (auto-installed by Flet)
- GitHub CLI (`gh`) for releases

## Project Structure

```
Privacy-Eraser/
├── src/privacy_eraser/
│   ├── core/                     # Core cleaning engine
│   ├── ui/                       # Flet UI
│   │   ├── core/
│   │   │   ├── backup_manager.py
│   │   │   ├── browser_info.py
│   │   │   ├── data_config.py
│   │   │   └── schedule_manager.py  # NEW: Schedule management
│   │   └── main.py
│   ├── scheduler.py              # NEW: APScheduler integration
│   ├── schedule_executor.py      # NEW: Scheduled task executor
│   ├── notification_manager.py   # NEW: Windows notifications
│   ├── config.py                 # NEW: Dev/Prod mode config
│   └── cleaning.py
├── static/images/                # Browser logos
└── scripts/                      # Build & release scripts
```

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Inspired by [BleachBit](https://www.bleachbit.org/)
- UI Framework: [Flet](https://flet.dev/) (Flutter for Python)
- Scheduler: [APScheduler](https://apscheduler.readthedocs.io/)

---

<div align="center">

**Developed with ❤️ by [설코딩](https://seolcoding.com)**

</div>
