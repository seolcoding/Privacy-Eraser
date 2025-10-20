# 09_TESTING_PLAN

## Phases
- Phase 1: Unit tests for filesystem cleaning and CleanerML loader
- Phase 2: CLI harness tests (preview/clean) – no GUI
- Phase 3: GUI smoke tests for `customtkinter`

## Coverage goals
- `privacy_eraser.cleaning`: `iter_search`, `DeleteAction`, `CleanerOption`, chromium options
- `privacy_eraser.cleanerml_loader`: minimal CleanerML parsing, var and OS filters
- `privacy_eraser.detect_windows`: Windows-only helpers (guarded)

## Isolation
- All tests run in sandboxed `tmp_path`; environment variables are patched
- No real browser/user directories are accessed

## How to run (uv)
```
uv venv
uv sync -e test
uv run -m pytest -q
uv run -m pytest --cov=privacy_eraser --cov-report=term-missing
```

