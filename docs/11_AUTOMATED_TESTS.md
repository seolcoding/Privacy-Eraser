# Automated Tests: How-To

## Install and run (uv)
```
uv venv
uv sync -e test
uv run -m pytest -q
```

## Coverage
```
uv run -m pytest --cov=privacy_eraser --cov-report=term-missing
```

## Notes
- Tests operate only within a temporary sandbox.
- Windows-only tests are skipped on non-Windows systems.

