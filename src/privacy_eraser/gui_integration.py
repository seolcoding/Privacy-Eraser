from __future__ import annotations

import os
from loguru import logger

from .app_state import app_state

# Check if we should use mock data (macOS/Linux)
USE_MOCK = os.name != "nt"

if USE_MOCK:
    from . import mock_windows

# Detection utilities
try:
    from .detect_windows import (
        ProgramProbe,
        collect_programs,
        registry_key_exists,
        detect_file_glob,
        is_process_running_windows,
    )
except Exception:  # pragma: no cover
    ProgramProbe = None
    collect_programs = None
    registry_key_exists = None
    detect_file_glob = None
    is_process_running_windows = None

# Cleaning engine
try:
    from .cleaning import CleanerOption, chromium_cleaner_options
except Exception:  # pragma: no cover
    CleanerOption = None
    chromium_cleaner_options = None

try:
    from .cleanerml_loader import load_cleaner_options_from_file
except Exception:  # pragma: no cover
    load_cleaner_options_from_file = None


def get_default_probes() -> list:
    if ProgramProbe is None:
        return []
    return [
        ProgramProbe(
            name="Google Chrome",
            registry_keys=(r"HKCU\\Software\\Google\\Chrome", r"HKLM\\SOFTWARE\\Google\\Chrome"),
            file_patterns=(r"%LOCALAPPDATA%\\Google\\Chrome\\User Data\\Default\\Preferences",),
            process_names=("chrome.exe",),
        ),
        ProgramProbe(
            name="Mozilla Firefox",
            registry_keys=(r"HKCU\\Software\\Mozilla\\Firefox", r"HKLM\\SOFTWARE\\Mozilla\\Firefox"),
            file_patterns=(r"%APPDATA%\\Mozilla\\Firefox\\profiles.ini",),
            process_names=("firefox.exe",),
        ),
        ProgramProbe(
            name="Microsoft Edge",
            registry_keys=(r"HKCU\\Software\\Microsoft\\Edge", r"HKLM\\SOFTWARE\\Microsoft\\Edge"),
            file_patterns=(r"%LOCALAPPDATA%\\Microsoft\\Edge\\User Data\\Default\\Preferences",),
            process_names=("msedge.exe",),
        ),
        ProgramProbe(
            name="Naver Whale",
            registry_keys=(r"HKCU\\Software\\Naver\\Whale", r"HKLM\\SOFTWARE\\Naver\\Whale"),
            file_patterns=(r"%LOCALAPPDATA%\\Naver\\Naver Whale\\User Data",),
            process_names=("whale.exe",),
        ),
        ProgramProbe(
            name="Arc Browser",
            registry_keys=(r"HKCU\\Software\\The Browser Company", r"HKLM\\SOFTWARE\\The Browser Company"),
            file_patterns=(r"%LOCALAPPDATA%\\Arc\\User Data\\Default\\Preferences",),
            process_names=("Arc.exe", "arc.exe"),
        ),
        ProgramProbe(
            name="Vivaldi",
            registry_keys=(),
            file_patterns=(r"%LOCALAPPDATA%\\Vivaldi\\User Data",),
            process_names=("vivaldi.exe",),
        ),
        ProgramProbe(
            name="Brave",
            registry_keys=(r"HKCU\\Software\\BraveSoftware\\Brave-Browser",),
            file_patterns=(r"%LOCALAPPDATA%\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Preferences",),
            process_names=("brave.exe",),
        ),
        ProgramProbe(
            name="Opera",
            registry_keys=(r"HKCU\\Software\\Opera Software",),
            file_patterns=(r"%APPDATA%\\Opera Software\\Opera Stable",),
            process_names=("opera.exe",),
        ),
    ]


def run_scan() -> list[dict]:
    """Scan for installed browsers and update AppState."""
    # Use mock data on macOS/Linux
    if USE_MOCK:
        logger.info("scan> using mock browser data (macOS/Linux)")
        mock_browsers = mock_windows.get_mock_browsers()
        app_state.scanned_programs = mock_browsers
        logger.info(f"scan> loaded {len(mock_browsers)} mock browsers")
        return mock_browsers

    if ProgramProbe is None or collect_programs is None:
        logger.warning("Detection module unavailable")
        return []

    logger.info("scan> starting program detection")
    probes = get_default_probes()
    logger.info(f"scan> loaded {len(probes)} probes")

    rows = collect_programs(probes)
    logger.info(f"scan> collected {len(rows)} programs")
    
    # Enrich with UI metadata
    enriched = []
    for row in rows:
        name = row.get("name", "")
        present_flag = str(row.get("present", "")).lower() in {"yes", "true", "1"}
        running_flag = str(row.get("running", "")).lower() in {"yes", "true", "1"}

        # Map browser names to icons and colors
        icon_map = {
            "Google Chrome": ("C", "#1E88E5", "fa5b.chrome"),
            "Microsoft Edge": ("E", "#0F9D58", "fa5b.edge"),
            "Mozilla Firefox": ("F", "#FF6F00", "fa5b.firefox"),
            "Brave": ("B", "#FB8C00", "fa5b.firefox-browser"),
            "Opera": ("O", "#FF1744", "fa5b.opera"),
            "Vivaldi": ("V", "#EF4444", None),
            "Naver Whale": ("W", "#4FC3F7", None),
            "Arc Browser": ("A", "#9C27B0", None),
        }
        icon, color, fa_icon = icon_map.get(name, ("?", "#6c757d", None))
        enriched.append({
            **row,
            "present": present_flag,
            "running": running_flag,
            "status": "설치됨" if present_flag else "미설치",
            "icon": icon,
            "fa_icon": fa_icon,
            "color": color,
            "cache_size": "N/A",
            "cookies": "N/A",
        })
    
    # Update app_state
    app_state.scanned_programs = enriched
    logger.info(f"scan> updated app_state with {len(enriched)} programs")
    
    return enriched


def guess_user_data_path(program_name: str) -> str:
    """Get user data path for a browser."""
    mapping = {
        "Google Chrome": r"%LOCALAPPDATA%\\Google\\Chrome\\User Data",
        "Microsoft Edge": r"%LOCALAPPDATA%\\Microsoft\\Edge\\User Data",
        "Brave": r"%LOCALAPPDATA%\\BraveSoftware\\Brave-Browser\\User Data",
        "Naver Whale": r"%LOCALAPPDATA%\\Naver\\Naver Whale\\User Data",
        "Opera": r"%APPDATA%\\Opera Software\\Opera Stable",
        "Vivaldi": r"%LOCALAPPDATA%\\Vivaldi\\User Data",
        "Arc Browser": r"%LOCALAPPDATA%\\Arc\\User Data",
    }
    base = mapping.get(program_name, "")
    return os.path.normpath(os.path.expandvars(base)) if base else ""


def load_cleaner_options(program_name: str, user_data_path: str) -> list:
    """Load CleanerML options for a browser, fallback to chromium_cleaner_options."""
    # Use mock data on macOS/Linux
    if USE_MOCK:
        logger.info(f"cleanerml> using mock options for {program_name}")
        return mock_windows.get_mock_cleaner_options(program_name)

    opts: list = []

    # Try CleanerML mapping first
    xml_map = {
        "Google Chrome": "google_chrome.xml",
        "Microsoft Edge": "microsoft_edge.xml",
        "Brave": "brave.xml",
        "Opera": "opera.xml",
        "Vivaldi": "vivaldi.xml",
    }
    xml_name = xml_map.get(program_name)

    if xml_name:
        try_paths = [os.path.join(os.getcwd(), "bleachbit", "cleaners", xml_name)]
        for p in try_paths:
            if load_cleaner_options_from_file and os.path.isfile(p):
                try:
                    opts = load_cleaner_options_from_file(p)
                    logger.info(f"cleanerml> loaded {len(opts)} options from {p}")
                    return opts
                except Exception as e:
                    logger.warning(f"cleanerml> failed to load {p}: {e}")

    # Fallback for Chromium-like
    if chromium_cleaner_options is not None and user_data_path:
        opts = chromium_cleaner_options(user_data_path)
        logger.info(f"cleanerml> using chromium fallback for {program_name}, {len(opts)} options")

    return opts


def preview_selected_options(selected_options: list) -> tuple[int, list[str]]:
    """Preview selected cleaner options.
    
    Args:
        selected_options: List of CleanerOption instances
    
    Returns:
        Tuple of (total_count, preview_items_list)
    """
    total = 0
    preview_items = []
    
    for opt in selected_options:
        items = opt.preview()
        logger.info(f"preview> {opt.label}: {len(items)} items")
        for p in items[:50]:
            logger.info(f"preview>  {p}")
            preview_items.append(f"  {p}")
        if len(items) > 50:
            logger.info(f"preview>  ... and {len(items)-50} more")
            preview_items.append(f"  ... and {len(items)-50} more")
        total += len(items)
    
    logger.info(f"preview> total items: {total}")
    return total, preview_items


def execute_clean(selected_options: list) -> tuple[int, int]:
    """Execute clean for selected options.
    
    Args:
        selected_options: List of CleanerOption instances
    
    Returns:
        Tuple of (total_count, total_bytes)
    """
    total_c = 0
    total_b = 0
    
    for opt in selected_options:
        c, b = opt.execute()
        logger.info(f"clean> {opt.label}: deleted {c} items, {b} bytes")
        total_c += c
        total_b += b
    
    logger.info(f"clean> total deleted {total_c} items, {total_b} bytes")
    return total_c, total_b


__all__ = [
    "get_default_probes",
    "run_scan",
    "guess_user_data_path",
    "load_cleaner_options",
    "preview_selected_options",
    "execute_clean",
]

