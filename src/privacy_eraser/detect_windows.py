from __future__ import annotations

import glob
import os
import re
from dataclasses import dataclass
from typing import Iterable

import psutil

if os.name == "nt":  # guarded import
    import winreg
    USE_MOCK = False
else:  # pragma: no cover - non-Windows fallback
    winreg = None  # type: ignore
    USE_MOCK = True
    from . import mock_windows


_HIVE = {
    "HKCR": getattr(winreg, "HKEY_CLASSES_ROOT", None) if winreg else None,
    "HKCU": getattr(winreg, "HKEY_CURRENT_USER", None) if winreg else None,
    "HKLM": getattr(winreg, "HKEY_LOCAL_MACHINE", None) if winreg else None,
    "HKU": getattr(winreg, "HKEY_USERS", None) if winreg else None,
}


def _split_registry_key(full_key: str):
    hive, subkey = full_key.split("\\", 1)
    hive_obj = _HIVE.get(hive.upper())
    if hive_obj is None:
        raise KeyError(f"Unknown hive: {hive}")
    return hive_obj, subkey


def registry_key_exists(full_key: str) -> bool:
    if USE_MOCK:
        return mock_windows.mock_registry_key_exists(full_key)

    if winreg is None:
        return False
    try:
        hive, subkey = _split_registry_key(full_key)
        winreg.OpenKey(hive, subkey)
        return True
    except FileNotFoundError:
        return False
    except OSError:
        return False


def _winapp_expand_vars(path_pattern: str) -> Iterable[str]:
    # Normal expansion
    primary = os.path.expandvars(path_pattern)
    yield primary
    # Winapp2 convention: ProgramFiles/CommonProgramFiles -> W6432 variants
    subs = (("ProgramFiles", "ProgramW6432"), ("CommonProgramFiles", "CommonProgramW6432"))
    for orig, repl in subs:
        if re.match(rf"%{orig}%.*", path_pattern, flags=re.IGNORECASE):
            yield os.path.expandvars(re.sub(rf"%{orig}%", f"%{repl}%", path_pattern, flags=re.IGNORECASE))


def detect_file_glob(path_pattern: str) -> bool:
    if USE_MOCK:
        return mock_windows.mock_detect_file_glob(path_pattern)

    for expanded in _winapp_expand_vars(path_pattern):
        if any(glob.iglob(expanded)):
            return True
    return False


def is_process_running_windows(exename: str, same_user: bool = True) -> bool:
    if USE_MOCK:
        return mock_windows.mock_is_process_running(exename, same_user)

    target = exename.lower()
    try:
        current_user = psutil.Process().username().lower()
    except Exception:
        current_user = ""
    for proc in psutil.process_iter():
        try:
            if proc.name().lower() != target:
                continue
            if not same_user:
                return True
            try:
                if proc.username().lower() == current_user:
                    return True
            except psutil.AccessDenied:
                continue
        except psutil.NoSuchProcess:
            continue
    return False


@dataclass
class ProgramProbe:
    name: str
    registry_keys: tuple[str, ...] = ()
    file_patterns: tuple[str, ...] = ()
    process_names: tuple[str, ...] = ()


def program_exists(probe: ProgramProbe) -> bool:
    return (
        any(registry_key_exists(k) for k in probe.registry_keys)
        or any(detect_file_glob(p) for p in probe.file_patterns)
    )


def collect_programs(probes: list[ProgramProbe]) -> list[dict[str, str]]:
    """Return table rows with detection details.

    Columns: name, present, running, source
    """
    rows: list[dict[str, str]] = []
    for probe in probes:
        present = program_exists(probe)
        running = any(is_process_running_windows(p, True) for p in probe.process_names)
        source_bits: list[str] = []
        if probe.registry_keys:
            source_bits.append("registry")
        if probe.file_patterns:
            source_bits.append("files")
        if probe.process_names:
            source_bits.append("process")
        rows.append(
            {
                "name": probe.name,
                "present": "yes" if present else "no",
                "running": "yes" if running else "no",
                "source": ",".join(source_bits) or "-",
            }
        )
    return rows


