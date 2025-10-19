#!/usr/bin/env python3
"""
Munin plugin base module for visualizing mailbox statistics (size, message count, etc.)
via `doveadm` for a Mail-in-a-Box server.
"""

from __future__ import annotations  # pylint: disable=E0611

import json
import os
import re
import subprocess  # nosec: Bandit_B404
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import DefaultDict, Dict, List, Optional


def run(*args: str) -> List[str]:
    """
    Run a shell command safely, avoiding shell injection by passing arguments directly.
    Accepts multiple string arguments as command and parameters.
    Returns a list of output lines.
    """
    # nosemgrep: dangerous-subprocess-use-audit, dangerous-subprocess-use-tainted-env-args
    result = subprocess.run(args, capture_output=True, text=True, check=True)  # nosec B603
    return result.stdout.strip().splitlines()


def safe_name(name: str) -> str:
    """
    Convert a folder name to a lowercase, Munin-safe identifier (only a-z, 0-9, _).
    """
    return re.sub(r"[^a-z0-9]", "_", name.lower())


def _load_cached_folders(cache_file: Path, ttl: int) -> Optional[List[str]]:
    if cache_file.exists():
        age = time.time() - cache_file.stat().st_mtime
        if age < ttl:
            try:
                with open(cache_file, "r", encoding="utf-8") as file_handle:
                    return json.load(file_handle)
            except (json.JSONDecodeError, OSError):
                pass
    return None


def _parse_folder_list(folders: List[str]) -> Dict[str, str]:
    seen = {}
    for folder in folders:
        top = folder.split(".")[0]
        key = top.lower()
        if key not in seen:
            seen[key] = top.capitalize()
    return seen


def _order_folders(seen: Dict[str, str], preferred_order: List[str]) -> List[str]:
    seen_lower = {k.lower(): v for k, v in seen.items()}
    ordered = []

    if "inbox" in seen_lower:
        ordered.append("Inbox")

    for folder in preferred_order:
        key = folder.lower()
        if key != "inbox" and key in seen_lower:
            val = seen_lower[key].capitalize()
            if val not in ordered:
                ordered.append(val)

    extras = sorted(
        [value.capitalize() for value in seen.values() if value.capitalize() not in ordered],
        key=str.casefold,
    )

    return ordered + extras


def _cache_folders(cache_file: Path, folders: List[str]) -> None:
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(cache_file, "w", encoding="utf-8") as file_handle:
            json.dump(folders, file_handle)
    except OSError:
        pass


def get_top_level_folders(
    mailbox_user: str,
    cache_file: Path,
    preferred_order: List[str],
    ttl: int,
) -> List[str]:
    """
    Return a list of top-level folders for the mailbox user.
    Ensures 'Inbox' is always first and shown capitalized.
    Applies preferred order next (case-insensitive), then all others in alphabetical order.
    Results are cached for performance.
    """
    cached = _load_cached_folders(cache_file, ttl)
    if cached:
        return cached

    folders_raw = run("doveadm", "mailbox", "list", "-u", mailbox_user)
    seen = _parse_folder_list(folders_raw)
    top_levels = _order_folders(seen, preferred_order)

    _cache_folders(cache_file, top_levels)
    return top_levels


def get_mailbox_stat_map(mailbox_user: str, metric: str) -> Dict[str, int]:
    """
    Return a dictionary mapping mailbox names to the requested metric,
    as reported by Dovecot's doveadm tool.
    """
    output = run("doveadm", "-f", "tab", "mailbox", "status", "-u", mailbox_user, metric, "*")
    result: Dict[str, int] = {}
    for line in output:
        try:
            mailbox, value = line.split("\t")
            result[mailbox] = int(value)
        except ValueError:
            continue
    return result


def output_config(folders: List[str], metric_label: str) -> None:
    """
    Output Munin config block for this plugin, describing each folder and graph details.
    """
    for folder in folders:
        print(f"{safe_name(folder)}.label {folder.capitalize()}")
    print(
        f"""graph_args --base 1024 --lower-limit 0
graph_scale yes
graph_category email
graph_info {metric_label} per folder including subfolders
graph_title Mail folder {metric_label}
graph_vlabel {metric_label}
graph_period second
graph_total total"""
    )


def output_values(folders: List[str], mailbox_user: str, metric: str) -> None:
    """
    Output Munin values block: metric of each top-level folder (including subfolders).
    """
    folder_map = {f.lower(): f for f in folders}
    stat_map = get_mailbox_stat_map(mailbox_user, metric)
    totals: DefaultDict[str, int] = defaultdict(int)
    for mailbox, value in stat_map.items():
        top = mailbox.split(".")[0]
        top_lower = top.lower()
        if top_lower in folder_map:
            totals[folder_map[top_lower]] += value
    for folder in folders:
        print(f"{safe_name(folder)}.value {totals.get(folder, 0)}")


def run_plugin(metric: str, metric_label: str) -> None:
    """Entry point to run the Munin plugin with the given metric and label."""
    mailbox_user = os.environ.get("mailbox_user", "amedee@vangasse.eu")
    cache_dir = Path("/var/cache/munin/mailfolders")
    cache_file = cache_dir / f"folders_{mailbox_user.replace('@', '_')}.json"
    cache_ttl = int(os.environ.get("mailbox_cache_ttl", 86400))
    preferred_order = ["Inbox", "Archive", "Drafts", "Sent", "Spam", "Trash"]

    folders = get_top_level_folders(mailbox_user, cache_file, preferred_order, cache_ttl)

    if len(sys.argv) == 1:
        output_values(folders, mailbox_user, metric)
    elif len(sys.argv) == 2 and sys.argv[1] == "config":
        output_config(folders, metric_label)
    else:
        print(
            f"{sys.argv[0]} - Munin plugin to graph mailbox folder {metric_label}",
            file=sys.stderr,
        )
        print("Usage: [config]", file=sys.stderr)
        sys.exit(1)
