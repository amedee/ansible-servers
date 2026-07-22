#!/usr/bin/env python3

import re
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: ansible-summary.py <logfile>")
        return 1

    logfile = Path(sys.argv[1])

    if not logfile.exists():
        print("## Ansible summary\n\nNo Ansible log found.")
        return 0

    content = logfile.read_text()

    hosts = {}

    for line in content.splitlines():
        match = re.search(
            r"(?P<host>\S+)\s+:\s+"
            r"ok=(?P<ok>\d+)\s+"
            r"changed=(?P<changed>\d+)\s+"
            r"unreachable=(?P<unreachable>\d+)\s+"
            r"failed=(?P<failed>\d+)",
            line,
        )

        if match:
            hosts[match.group("host")] = match.groupdict()

    print("## 🚀 Ansible result\n")

    if not hosts:
        print("No Ansible recap found.")
        return 0

    print("| Host | OK | Changed | Failed | Unreachable |")
    print("| --- | ---: | ---: | ---: | ---: |")

    for host, stats in hosts.items():
        print(
            f"| {host} | {stats['ok']} | {stats['changed']} | "
            f"{stats['failed']} | {stats['unreachable']} |"
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
