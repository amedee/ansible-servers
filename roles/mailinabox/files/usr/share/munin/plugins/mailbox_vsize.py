#!/usr/bin/env python3

"""
Munin plugin to report the sizes of top-level mailbox folders (including subfolders)
for a given Dovecot user.
"""

import json
import os
import re
import subprocess  # nosec: Bandit_B404
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

# Configuration
mailbox_user = os.environ.get("mailbox_user", "amedee@vangasse.eu")
cache_dir = Path("/var/cache/munin/mailfolders")
cache_file = cache_dir / f"folders_{mailbox_user.replace('@', '_')}.json"
CACHE_TTL = int(os.environ.get("mailbox_cache_ttl", 86400))  # 24 hours default

preferred_order = ["Inbox", "Archive", "Drafts", "Sent", "Spam", "Trash"]


def run(*args: str) -> List[str]:
    """
    Run a shell command safely, avoiding shell injection by passing arguments directly.
    Accepts multiple string arguments as command and parameters.
    Returns a list of output lines.
    """
    # nosemgrep: dangerous-subprocess-use-audit, dangerous-subprocess-use-tainted-env-args
    result = subprocess.run(
        args, capture_output=True, text=True, check=True
    )  # nosec B603
    return result.stdout.strip().splitlines()


def get_top_level_folders() -> List[str]:
    """
    Return a list of top-level folders for the mailbox user.
    Ensures 'Inbox' is always first and shown capitalized.
    Applies preferred order next (case-insensitive), then all others in alphabetical order.
    Results are cached for performance.
    """
    if cache_file.exists():
        age = time.time() - cache_file.stat().st_mtime
        if age < CACHE_TTL:
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError) as e:
                print(f"Warning: failed to read cache: {e}", file=sys.stderr)

    folders = run("doveadm", "mailbox", "list", "-u", mailbox_user)
    found_raw = [folder.split(".")[0] for folder in folders]

    seen = {}
    for name in found_raw:
        key = name.lower()
        if key not in seen:
            seen[key] = name  # Store the original name, we'll capitalize later

    # Enforce the 'Inbox' capitalized and at the start
    ordered = ["Inbox"] if "inbox" in seen else []

    for folder in preferred_order:
        key = folder.lower()
        if key != "inbox" and key in seen:
            ordered.append(seen[key].capitalize())  # Capitalize directly

    # Remaining folders not already included, capitalized and sorted
    extras = sorted(
        [value.capitalize() for key, value in seen.items() if value not in ordered],
        key=str.casefold,
    )

    top_levels = ordered + extras

    # Cache the result
    cache_dir.mkdir(parents=True, exist_ok=True)
    try:
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(top_levels, f)
    except OSError as e:
        print(f"Warning: could not write cache: {e}", file=sys.stderr)

    return top_levels


def get_vsize_map() -> Dict[str, int]:
    """
    Return a dictionary mapping mailbox names to their virtual size (in bytes),
    as reported by Dovecot's doveadm tool.
    """
    vsize_output = run(
        "doveadm", "-f", "tab", "mailbox", "status", "-u", mailbox_user, "vsize", "*"
    )
    vsize_map: Dict[str, int] = {}
    for line in vsize_output:
        try:
            mailbox, size = line.split("\t")
            vsize_map[mailbox] = int(size)
        except ValueError:
            continue
    return vsize_map


def safe_name(name: str) -> str:
    """
    Convert a folder name to a lowercase, Munin-safe identifier (only a-z, 0-9, _).
    """
    return re.sub(r"[^a-z0-9]", "_", name.lower())


def output_config() -> None:
    """
    Output Munin config block for this plugin, describing each folder and graph details.
    """
    for folder in get_top_level_folders():
        print(f"{safe_name(folder)}.label {folder}")

    print(
        """graph_args --base 1024 --lower-limit 0
graph_scale yes
graph_category email
graph_info Size of each folder including subfolders
graph_title Mail folder sizes (with subfolders)
graph_vlabel Size (bytes)
graph_period second
graph_total total"""
    )


def output_values() -> None:
    """
    Output Munin values block: size of each top-level folder (including subfolders).
    """
    folders = get_top_level_folders()
    folder_map = {f.lower(): f for f in folders}
    vsize_map = get_vsize_map()
    totals: defaultdict[str, int] = defaultdict(int)

    for mailbox, size in vsize_map.items():
        top = mailbox.split(".")[0]
        top_lower = top.lower()
        if top_lower in folder_map:
            totals[folder_map[top_lower]] += size

    for folder in folders:
        print(f"{safe_name(folder)}.value {totals.get(folder, 0)}")


def output_usage() -> None:
    """
    Print usage help text to stderr.
    """
    print(
        f"{sys.argv[0]} - Munin plugin to graph mailbox folder sizes", file=sys.stderr
    )
    print("Usage: [config]", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        output_values()
    elif len(sys.argv) == 2 and sys.argv[1] == "config":
        output_config()
    else:
        output_usage()
        sys.exit(1)
