from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Iterable

from loguru import logger


def _which_all(names: Iterable[str]) -> dict[str, str | None]:
    return {name: shutil.which(name) for name in names}


def _possible_paths() -> list[Path]:
    user = os.environ.get("USERNAME", "user")
    local = os.environ.get("LOCALAPPDATA", "")
    appdata = os.environ.get("APPDATA", "")
    candidates = [
        Path(local) / "Google/Chrome/User Data/Default",
        Path(local) / "Microsoft/Edge/User Data/Default",
        Path(local) / "BraveSoftware/Brave-Browser/User Data/Default",
        Path(appdata) / "Mozilla/Firefox/Profiles",
        Path(local) / "Vivaldi/User Data/Default",
        Path(local) / "Opera Software/Opera Stable",
        Path(local) / "Naver/Whale/User Data/Default",
        Path.home() / "AppData/Local/Temp",
    ]
    return [p for p in candidates if p]


def emit_startup_placeholders() -> None:
    logger.info("Starting diagnostics: placeholder scan")

    tools = ["chrome", "msedge", "brave", "firefox", "vivaldi", "opera", "whale"]
    where = _which_all(tools)
    for name, path in where.items():
        if path:
            logger.info(f"found executable: {name} -> {path}")
        else:
            logger.warning(f"executable not found: {name}")

    for p in _possible_paths():
        if p.exists():
            try:
                entries = len(list(p.iterdir()))
                logger.info(f"path exists: {p} ({entries} entries)")
            except Exception as e:
                logger.warning(f"path exists but not listable: {p}: {e}")
        else:
            logger.warning(f"path missing: {p}")

    logger.info("placeholder tasks: browser cache, cookies, history, session, autofill")
    logger.info("placeholder system: temp files, recent docs, dns cache, recycle bin")
    logger.info("diagnostics complete")


