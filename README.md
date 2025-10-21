# Privacy Eraser POC

🛡️ 브라우저 개인정보 자동 삭제 프로그램 (Proof of Concept)

## Features

- 🔍 자동 브라우저 감지 (Chrome, Edge, Firefox, Brave 등)
- 🗑️ 원클릭 개인정보 삭제 (캐시, 쿠키, 히스토리, 세션, 비밀번호)
- 📚 북마크 삭제 옵션
- 📥 다운로드 파일 삭제 옵션
- ↩️ 실행 취소 기능 (백업/복원)
- 🎨 Material Design UI (PySide6)

## Download

[![Download Latest](https://img.shields.io/github/v/release/seolcoding/Privacy-Eraser?label=Download&style=for-the-badge)](https://github.com/seolcoding/Privacy-Eraser/releases/latest)

**Windows 10/11 (64-bit)**
- [PrivacyEraser.exe](https://github.com/seolcoding/Privacy-Eraser/releases/latest/download/PrivacyEraser.exe) - 최신 안정 버전

> **참고**: Windows SmartScreen 경고가 표시될 수 있습니다. "추가 정보" → "실행"을 클릭하여 우회하세요. (코드 사이닝 인증서 미적용)

## Development

### Requirements

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager

### Setup

```bash
# Install dependencies
uv sync

# Run POC
uv run python run_poc.py

# Run with hot reload (development mode)
uv run python dev_server.py

# Run tests
uv run pytest
```

### Build EXE

```bash
# Build executable
scripts/build_exe.bat

# Output: dist/PrivacyEraser.exe
```

## Project Structure

```
Privacy-Eraser/
├── src/privacy_eraser/poc/   # POC implementation
│   ├── core/                 # Business logic
│   │   ├── backup_manager.py # Backup/restore engine
│   │   ├── poc_cleaner.py    # Cleaning engine
│   │   └── data_config.py    # Browser configurations
│   ├── ui/                   # PySide6 UI
│   │   ├── main_window.py    # Main window
│   │   ├── browser_card.py   # Browser card widget
│   │   ├── progress_dialog.py # Progress dialog
│   │   └── undo_dialog.py    # Undo dialog
│   └── main.py               # Entry point
├── tests/                    # Test suite
├── run_poc.py                # Simple launcher
└── dev_server.py             # Hot reload server
```

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Inspired by [BleachBit](https://www.bleachbit.org/)
- Icons by [QtAwesome](https://github.com/spyder-ide/qtawesome)
