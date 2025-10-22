from __future__ import annotations

import os
import sys
import xml.dom.minidom as minidom
from typing import Iterable

from .cleaning import CleanerOption, DeleteAction


def _text(node_list) -> str:
    parts: list[str] = []
    for node in node_list:
        if node.nodeType == node.TEXT_NODE:
            parts.append(node.data)
    return "".join(parts).strip()


def _os_match(os_str: str, platform: str | None = None) -> bool:
    if not os_str:
        return True
    plat = platform or sys.platform
    if plat == "darwin":
        current = ("darwin", "bsd", "unix")
    elif plat == "linux":
        current = ("linux", "unix")
    elif plat.startswith("openbsd"):
        current = ("bsd", "openbsd", "unix")
    elif plat.startswith("netbsd"):
        current = ("bsd", "netbsd", "unix")
    elif plat.startswith("freebsd"):
        current = ("bsd", "freebsd", "unix")
    elif plat == "win32":
        current = ("windows",)
    else:
        current = (plat,)
    return os_str in current


def _expand_multi_vars(s: str, vars_map: dict[str, list[str]]) -> list[str]:
    if "$$" not in s:
        return [s]
    # find all $$name$$ tokens
    out: list[str] = [s]
    for name, values in vars_map.items():
        token = f"$${name}$$"
        if token not in s:
            continue
        new_out: list[str] = []
        for base in out:
            for val in values:
                new_out.append(base.replace(token, val))
        out = new_out
    return out or [s]


def load_cleaner_options_from_file(pathname: str) -> list[CleanerOption]:
    dom = minidom.parse(pathname)
    cleaner_nodes = dom.getElementsByTagName("cleaner")
    if not cleaner_nodes:
        return []
    cleaner = cleaner_nodes[0]
    if not _os_match(cleaner.getAttribute("os")):
        return []

    # vars
    vars_map: dict[str, list[str]] = {}
    for var in cleaner.getElementsByTagName("var"):
        name = var.getAttribute("name")
        values: list[str] = []
        for v in var.getElementsByTagName("value"):
            if not _os_match(v.getAttribute("os")):
                continue
            s = _text(v.childNodes)
            if not s:
                continue
            # expand glob later via DeleteAction search; store raw
            values.append(s)
        if values:
            vars_map[name] = values

    options: list[CleanerOption] = []
    for option in cleaner.getElementsByTagName("option"):
        opt_id = option.getAttribute("id")
        label_node = option.getElementsByTagName("label")
        desc_node = option.getElementsByTagName("description")
        warn_node = option.getElementsByTagName("warning")
        opt_label = _text(label_node[0].childNodes) if label_node else opt_id
        opt_desc = _text(desc_node[0].childNodes) if desc_node else ""
        opt_warn = _text(warn_node[0].childNodes) if warn_node else None
        actions: list[DeleteAction] = []
        for act in option.getElementsByTagName("action"):
            if not _os_match(act.getAttribute("os")):
                continue
            command = act.getAttribute("command")
            # Support delete, chrome.history, chrome.favicons commands
            # (treat them all as file deletion)
            if command not in ("delete", "chrome.history", "chrome.favicons", "json"):
                # unsupported in minimal loader; skip
                continue
            search = act.getAttribute("search") or "file"
            raw_path = act.getAttribute("path")
            if not raw_path:
                continue
            for expanded in _expand_multi_vars(raw_path, vars_map):
                actions.append(DeleteAction(search=search, path=expanded))
        if actions:
            options.append(CleanerOption(id=opt_id, label=opt_label, description=opt_desc, warning=opt_warn, actions=actions))

    return options


