from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable

import pytest


@pytest.fixture
def sandbox(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Provide an isolated sandbox directory and safe environment variables.

    Tests should construct all paths relative to this sandbox. We also sanitize
    HOME and APPDATA-like variables to avoid accidental writes to the real system.
    """
    sandbox_root = tmp_path / "sandbox"
    sandbox_root.mkdir(parents=True, exist_ok=True)

    # Common Windows envs used by the code
    monkeypatch.setenv("LOCALAPPDATA", str(sandbox_root / "LOCALAPPDATA"))
    monkeypatch.setenv("APPDATA", str(sandbox_root / "APPDATA"))
    # Common temp variables referenced by CleanerML
    monkeypatch.setenv("TMP", str(sandbox_root / "LOCALAPPDATA" / "Temp"))
    monkeypatch.setenv("TEMP", str(sandbox_root / "LOCALAPPDATA" / "Temp"))
    monkeypatch.setenv("USERNAME", "testuser")

    # Posix-style HOME for any expansion
    monkeypatch.setenv("HOME", str(sandbox_root / "HOME"))

    return sandbox_root


def _write_file(path: Path, size: int = 3) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = b"x" * size
    path.write_bytes(data)
    return len(data)


@pytest.fixture
def seed_walk_tree():
    def _seed(base: Path, rel_dirs_and_files: dict[str, Iterable[str]]) -> int:
        """Create a directory tree under base.

        rel_dirs_and_files maps a directory (relative to base) to an iterable of
        file names to create in that directory. Returns number of files created.
        """
        count = 0
        for rel_dir, files in rel_dirs_and_files.items():
            d = base / rel_dir
            d.mkdir(parents=True, exist_ok=True)
            for name in files:
                count += 1
                _write_file(d / name)
        return count

    return _seed


@pytest.fixture
def make_glob_files():
    def _make(base: Path, patterns: dict[str, int]) -> list[Path]:
        """Create files that match glob stems.

        patterns: mapping like {"logs/*.log": 3} to create 3 files matching the
        pattern under base. Returns list of created paths.
        """
        created: list[Path] = []
        for pattern, n in patterns.items():
            # Create under base respecting directories
            stem = pattern.split("*")[0]
            dir_part = stem.rsplit("/", 1)[0] if "/" in stem else stem
            target_dir = base / dir_part
            target_dir.mkdir(parents=True, exist_ok=True)
            for i in range(n):
                p = target_dir / f"file{i}.log"
                _write_file(p)
                created.append(p)
        return created

    return _make


