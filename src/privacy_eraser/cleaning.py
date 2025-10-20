"""Legacy cleaning module - maintained for compatibility.

This module provides backward-compatible wrappers around the new core module.
New code should use privacy_eraser.core.cleaner_engine directly.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Iterator, Literal

from .core.cleaner_engine import (
    ActionType,
    CleaningAction,
    SearchType as CoreSearchType,
)
from .core.cleaner_engine import CleanerOption as CoreCleanerOption

# Legacy type alias
SearchType = Literal["file", "glob", "walk.files", "walk.all", "walk.top"]

# Map legacy search types to core search types
_SEARCH_TYPE_MAP = {
    "file": CoreSearchType.FILE,
    "glob": CoreSearchType.GLOB,
    "walk.files": CoreSearchType.WALK_FILES,
    "walk.all": CoreSearchType.WALK_ALL,
    "walk.top": CoreSearchType.WALK_TOP,
}


@dataclass
class DeleteAction:
    """Legacy delete action wrapper."""
    search: SearchType
    path: str

    def preview(self) -> list[str]:
        action = CleaningAction(
            action_type=ActionType.DELETE,
            search_type=_SEARCH_TYPE_MAP[self.search],
            path=self.path,
        )
        return action.preview()

    def execute(self) -> tuple[int, int]:
        action = CleaningAction(
            action_type=ActionType.DELETE,
            search_type=_SEARCH_TYPE_MAP[self.search],
            path=self.path,
        )
        return action.execute()


@dataclass
class CleanerOption:
    """Legacy cleaner option wrapper."""
    id: str
    label: str
    description: str
    warning: str | None = None
    actions: list[DeleteAction] = field(default_factory=list)

    def preview(self) -> list[str]:
        items: list[str] = []
        for a in self.actions:
            items.extend(a.preview())
        return sorted(set(os.path.normpath(p) for p in items))

    def execute(self) -> tuple[int, int]:
        total_count = 0
        total_bytes = 0
        for a in self.actions:
            c, b = a.execute()
            total_count += c
            total_bytes += b
        return total_count, total_bytes


def chromium_default_profile(base_user_data: str) -> str:
    return os.path.join(base_user_data, "Default")


def iter_search(search: SearchType, path: str) -> Iterator[str]:
    """Compatibility helper used by legacy tests.

    Leverages the new core engine's preview capability so existing tests and
    integrations that relied on the old generator continue to work.
    """
    action = CleaningAction(
        action_type=ActionType.DELETE,
        search_type=_SEARCH_TYPE_MAP[search],
        path=path,
    )
    for item in action.preview():
        yield os.path.normpath(item)


def chromium_cleaner_options(base_user_data: str) -> list[CleanerOption]:
    profile = chromium_default_profile(base_user_data)
    opts: list[CleanerOption] = []
    # Cache
    opts.append(
        CleanerOption(
            id="cache",
            label="Cache",
            description="Delete browser cache",
            actions=[
                DeleteAction("walk.files", os.path.join(profile, "Cache")),
                DeleteAction("walk.files", os.path.join(profile, "Code Cache")),
                DeleteAction("walk.files", os.path.join(profile, "GPUCache")),
                DeleteAction("walk.files", os.path.join(profile, "Media Cache")),
                DeleteAction("walk.all", os.path.join(base_user_data, "ShaderCache")),
                DeleteAction("walk.all", os.path.join(profile, "Service Worker")),
                DeleteAction("walk.all", os.path.join(profile, "File System")),
            ],
        )
    )
    # Cookies
    opts.append(
        CleanerOption(
            id="cookies",
            label="Cookies",
            description="Delete cookies databases",
            actions=[
                DeleteAction("file", os.path.join(profile, "Cookies")),
                DeleteAction("file", os.path.join(profile, "Cookies-journal")),
                DeleteAction("file", os.path.join(profile, "Network", "Cookies")),
                DeleteAction("file", os.path.join(profile, "Network", "Cookies-journal")),
            ],
        )
    )
    # History
    opts.append(
        CleanerOption(
            id="history",
            label="History",
            description="Delete site history and related caches",
            actions=[
                DeleteAction("file", os.path.join(profile, "History")),
                DeleteAction("file", os.path.join(profile, "History-journal")),
                DeleteAction("file", os.path.join(profile, "Favicons")),
                DeleteAction("file", os.path.join(profile, "Top Sites")),
                DeleteAction("walk.files", os.path.join(profile, "Session Storage")),
            ],
        )
    )
    # Session
    opts.append(
        CleanerOption(
            id="session",
            label="Session",
            description="Delete current and last sessions",
            actions=[
                DeleteAction("file", os.path.join(profile, "Current Session")),
                DeleteAction("file", os.path.join(profile, "Current Tabs")),
                DeleteAction("file", os.path.join(profile, "Last Session")),
                DeleteAction("file", os.path.join(profile, "Last Tabs")),
                DeleteAction("walk.all", os.path.join(profile, "Extension State")),
                DeleteAction("walk.all", os.path.join(profile, "Sessions")),
            ],
        )
    )
    # Passwords (dangerous)
    opts.append(
        CleanerOption(
            id="passwords",
            label="Passwords",
            description="Delete saved passwords",
            warning="This will delete all saved passwords.",
            actions=[
                DeleteAction("file", os.path.join(profile, "Login Data")),
                DeleteAction("file", os.path.join(profile, "Login Data-journal")),
            ],
        )
    )
    return opts


