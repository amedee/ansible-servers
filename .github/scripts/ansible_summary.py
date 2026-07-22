#!/usr/bin/env python3
"""Generate a GitHub Actions summary from an Ansible log."""

import re
import sys
from pathlib import Path


def main() -> int:
    """Parse Ansible recap data and print a Markdown summary."""
    if len(sys.argv) != 2:
        print("Usage: ansible_summary.py <ansible.log>")
        return 1

    logfile = Path(sys.argv[1])

    print("## 🚀 Ansible result\n")

    if not logfile.exists():
        print("No Ansible log found.")
        return 0

    content = logfile.read_text(encoding="utf-8")

    matches = re.findall(
        r"(?P<host>\S+)\s+:\s+"
        r"ok=(?P<ok>\d+)\s+"
        r"changed=(?P<changed>\d+)\s+"
        r"unreachable=(?P<unreachable>\d+)\s+"
        r"failed=(?P<failed>\d+)",
        content,
    )

    if not matches:
        print("No Ansible recap found.")
        return 0

    print("| Host | OK | Changed | Failed | Unreachable |")
    print("| --- | ---: | ---: | ---: | ---: |")

    for host, ok, changed, unreachable, failed in matches:
        print(f"| {host} | {ok} | {changed} | {failed} | {unreachable} |")

    return 0


if __name__ == "__main__":
    sys.exit(main())
