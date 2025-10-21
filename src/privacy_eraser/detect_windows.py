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


def detect_browsers() -> list[dict[str, str]]:
    """주요 브라우저 감지 (Windows)

    Returns:
        감지된 브라우저 정보 리스트
        각 항목: {"name": str, "present": "yes"|"no", "running": "yes"|"no", "source": str}
    """
    # 브라우저 probe 정의
    browser_probes = [
        ProgramProbe(
            name="Chrome",
            registry_keys=(
                r"HKLM\SOFTWARE\Google\Chrome",
                r"HKCU\SOFTWARE\Google\Chrome",
            ),
            file_patterns=(
                r"%ProgramFiles%\Google\Chrome\Application\chrome.exe",
                r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe",
                r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe",
            ),
            process_names=("chrome.exe",),
        ),
        ProgramProbe(
            name="Edge",
            registry_keys=(
                r"HKLM\SOFTWARE\Microsoft\Edge",
                r"HKCU\SOFTWARE\Microsoft\Edge",
            ),
            file_patterns=(
                r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe",
                r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe",
            ),
            process_names=("msedge.exe",),
        ),
        ProgramProbe(
            name="Firefox",
            registry_keys=(
                r"HKLM\SOFTWARE\Mozilla\Mozilla Firefox",
                r"HKCU\SOFTWARE\Mozilla\Mozilla Firefox",
            ),
            file_patterns=(
                r"%ProgramFiles%\Mozilla Firefox\firefox.exe",
                r"%ProgramFiles(x86)%\Mozilla Firefox\firefox.exe",
            ),
            process_names=("firefox.exe",),
        ),
        ProgramProbe(
            name="Brave",
            file_patterns=(
                r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\Application\brave.exe",
                r"%ProgramFiles%\BraveSoftware\Brave-Browser\Application\brave.exe",
            ),
            process_names=("brave.exe",),
        ),
        ProgramProbe(
            name="Opera",
            registry_keys=(
                r"HKLM\SOFTWARE\Opera Software",
                r"HKCU\SOFTWARE\Opera Software",
            ),
            file_patterns=(
                r"%ProgramFiles%\Opera\launcher.exe",
                r"%ProgramFiles(x86)%\Opera\launcher.exe",
                r"%LOCALAPPDATA%\Programs\Opera\launcher.exe",
            ),
            process_names=("opera.exe",),
        ),
        ProgramProbe(
            name="Vivaldi",
            file_patterns=(
                r"%LOCALAPPDATA%\Vivaldi\Application\vivaldi.exe",
                r"%ProgramFiles%\Vivaldi\Application\vivaldi.exe",
            ),
            process_names=("vivaldi.exe",),
        ),
    ]

    return collect_programs(browser_probes)


