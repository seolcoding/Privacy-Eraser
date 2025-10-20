from __future__ import annotations

import os
from pathlib import Path

import pytest

pytestmark = pytest.mark.skipif(os.name != "nt", reason="Windows-only detection tests")


def test_detect_file_glob(monkeypatch):
    from privacy_eraser.detect_windows import detect_file_glob

    # Simulate environment expansion for %ProgramFiles% and presence of files
    temp_root = Path.cwd() / "_tmp_detect"
    try:
        temp_root.mkdir(exist_ok=True)
        target_dir = temp_root / "Program Files" / "Vendor" / "App"
        target_dir.mkdir(parents=True, exist_ok=True)
        (target_dir / "app.exe").write_text("x")

        monkeypatch.setenv("ProgramFiles", str(temp_root / "Program Files"))
        monkeypatch.setenv("CommonProgramFiles", str(temp_root / "Program Files"))
        pattern = r"%ProgramFiles%\\Vendor\\App\\*.exe"
        assert detect_file_glob(pattern) is True
    finally:
        # Cleanup
        for p in sorted(temp_root.rglob("*"), reverse=True):
            if p.is_file():
                p.unlink()
            else:
                try:
                    p.rmdir()
                except OSError:
                    pass
        try:
            temp_root.rmdir()
        except OSError:
            pass


def test_registry_key_exists(monkeypatch):
    from privacy_eraser import detect_windows as dw

    if dw.winreg is None:
        pytest.skip("winreg not available")

    # Create a fake key by monkeypatching winreg.OpenKey behavior
    class Dummy:
        pass

    def fake_open_key(hive, subkey):  # noqa: ARG001
        if subkey == "SOFTWARE\\Vendor\\App":
            return Dummy()
        raise FileNotFoundError

    monkeypatch.setattr(dw.winreg, "OpenKey", fake_open_key)
    assert dw.registry_key_exists("HKLM\\SOFTWARE\\Vendor\\App") is True
    assert dw.registry_key_exists("HKLM\\SOFTWARE\\Missing") is False


