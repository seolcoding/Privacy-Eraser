# Privacy Eraser POC

🛡️ 브라우저 개인정보 자동 삭제 프로그램 (Proof of Concept)

## Features

- 🔍 자동 브라우저 감지 (Chrome, Edge, Firefox, Brave 등)
- 🗑️ 원클릭 개인정보 삭제 (캐시, 쿠키, 히스토리, 세션, 비밀번호)
- 📚 북마크 삭제 옵션
- 📥 다운로드 파일 삭제 옵션
- ↩️ 실행 취소 기능 (백업/복원)
- 🎨 Material Design 3 UI (Flet/Flutter)

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

# Run Flet UI
python -m privacy_eraser.ui.main

# Or use entry point
privacy_eraser
privacy_eraser_poc

# Run tests
uv run pytest
```

### Build EXE

```bash
# Build single-file executable (Flet Pack)
scripts/build_pack.bat

# Or auto-release with GitHub
scripts/release.bat 2.0.1

# Output: dist/PrivacyEraser.exe (single file)
```

## Project Structure

```
Privacy-Eraser/
├── src/privacy_eraser/
│   ├── core/                 # Core cleaning engine
│   │   ├── cleaner_engine.py
│   │   ├── file_utils.py
│   │   └── windows_utils.py
│   ├── ui/                   # Flet UI (official GUI)
│   │   ├── core/             # UI business logic
│   │   │   ├── backup_manager.py
│   │   │   ├── browser_info.py
│   │   │   └── data_config.py
│   │   └── main.py           # Flet UI entry point
│   ├── cleaning.py           # Core cleaner engine
│   ├── detect_windows.py     # Windows browser detection
│   └── settings_db.py        # Settings persistence
├── tests/                    # Test suite (22 tests)
├── scripts/                  # Build scripts (Flet Pack)
├── main.py                   # Build wrapper entry point
└── static/images/            # Browser logos
```

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Inspired by [BleachBit](https://www.bleachbit.org/)
- UI Framework: [Flet](https://flet.dev/) (Flutter for Python)

---

<div align="center">

**Developed with ❤️ by [설코딩](https://seolcoding.com)**

</div>
