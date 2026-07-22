#!/usr/bin/env python3
"""Generate a GitHub Actions summary from an Ansible log file."""

import json
import re
import sys
from pathlib import Path


def extract_stats(content: str) -> dict:
    """Extract Ansible play recap statistics from the log content."""
    match = re.search(
        r'"stats":\s*({.*?})\s*}\s*$',
        content,
        re.DOTALL,
    )

    if not match:
        return {}

    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError:
        return {}


def main() -> int:
    """Parse an Ansible log file and print a GitHub Actions summary."""
    if len(sys.argv) < 2:
        print("Usage: ansible_summary.py <logfile>")
        return 1

    logfile = Path(sys.argv[1])

    if not logfile.exists():
        print("## 🚀 Ansible result\n\nNo Ansible log found.")
        return 0

    content = logfile.read_text(encoding="utf-8")

    stats = extract_stats(content)

    print("## 🚀 Ansible result\n")

    if not stats:
        print("No Ansible stats found.")
        return 0

    print("| Host | OK | Changed | Failed | Unreachable | Skipped |")
    print("| --- | ---: | ---: | ---: | ---: | ---: |")

    for host, values in stats.items():
        print(
            f"| {host} | "
            f"{values.get('ok', 0)} | "
            f"{values.get('changed', 0)} | "
            f"{values.get('failures', 0)} | "
            f"{values.get('unreachable', 0)} | "
            f"{values.get('skipped', 0)} |"
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
