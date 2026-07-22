#!/usr/bin/env python3
"""Generate a GitHub Actions summary from Ansible JSON output."""

import json
import sys
from pathlib import Path


def main() -> int:
    """Read Ansible JSON output and print a Markdown summary."""
    if len(sys.argv) != 2:
        print("Usage: ansible_summary.py <ansible-result.json>")
        return 1

    json_file = Path(sys.argv[1])

    if not json_file.exists():
        print("## 🚀 Ansible result\n")
        print("No Ansible output found.")
        return 0

    try:
        data = json.loads(json_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print("## 🚀 Ansible result\n")
        print(f"Failed to parse JSON: {exc}")
        return 1

    stats = data.get("stats", {})

    print("## 🚀 Ansible result\n")

    if not stats:
        print("No Ansible statistics found.")
        return 0

    print("| Host | OK | Changed | Failed | Unreachable | Skipped | Rescued | Ignored |")
    print("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")

    total_changed = 0
    total_failed = 0
    total_unreachable = 0

    for host, values in sorted(stats.items()):
        changed = values.get("changed", 0)
        failed = values.get("failures", 0)
        unreachable = values.get("unreachable", 0)

        total_changed += changed
        total_failed += failed
        total_unreachable += unreachable

        print(
            f"| {host} | "
            f"{values.get('ok', 0)} | "
            f"{changed} | "
            f"{failed} | "
            f"{unreachable} | "
            f"{values.get('skipped', 0)} | "
            f"{values.get('rescued', 0)} | "
            f"{values.get('ignored', 0)} |"
        )

    print()
    print(
        f"**Totals:** {total_changed} changed, "
        f"{total_failed} failed, "
        f"{total_unreachable} unreachable."
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
