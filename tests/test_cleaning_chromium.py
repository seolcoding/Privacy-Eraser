from __future__ import annotations
from pathlib import Path

from privacy_eraser.cleaning import chromium_cleaner_options, chromium_default_profile


def _create_file(p: Path, size: int = 5) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(b"x" * size)


def test_chromium_options_preview_and_execute(sandbox: Path):
    base = sandbox / "User Data"
    profile = Path(chromium_default_profile(str(base)))

    # Seed minimal structures for each option
    # Cache
    for d in ["Cache", "Code Cache", "GPUCache", "Media Cache"]:
        _create_file(profile / d / "a.bin")
    _create_file(base / "ShaderCache" / "bin.cache")
    _create_file(profile / "Service Worker" / "script.js")
    _create_file(profile / "File System" / "meta.json")

    # Cookies
    for f in ["Cookies", "Cookies-journal"]:
        _create_file(profile / f)
    for f in ["Network/Cookies", "Network/Cookies-journal"]:
        _create_file(profile / f)

    # History
    for f in ["History", "History-journal", "Favicons", "Top Sites"]:
        _create_file(profile / f)
    _create_file(profile / "Session Storage" / "store.bin")

    # Session
    for f in ["Current Session", "Current Tabs", "Last Session", "Last Tabs"]:
        _create_file(profile / f)
    for d in ["Extension State", "Sessions"]:
        _create_file(profile / d / "state.bin")

    # Passwords
    for f in ["Login Data", "Login Data-journal"]:
        _create_file(profile / f)

    opts = chromium_cleaner_options(str(base))
    assert {o.id for o in opts} == {"cache", "cookies", "history", "session", "passwords"}

    # Each option should preview at least 1 item
    for opt in opts:
        prev = opt.preview()
        assert len(prev) >= 1
        # Execute deletes and returns counts/bytes
        c, b = opt.execute()
        assert c >= 1 and b >= 0

    # After all executes, all files should be removed; allow empty directories
    remaining_files = [p for p in profile.rglob("*") if p.is_file()]
    assert not remaining_files, f"Expected no files, found: {remaining_files[:5]}"


