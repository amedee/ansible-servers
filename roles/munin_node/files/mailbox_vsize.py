#!/usr/bin/env python3
"""
Munin plugin for graphing the size in bytes per mail folder.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from mailbox_base import run_plugin  # pylint: disable=C0413  # noqa: E402

run_plugin(metric="vsize", metric_label="Size (bytes)")
