#!/usr/bin/env bash
set -euo pipefail

time="$(curl --silent --output /dev/null --write-out '%{time_total}' "https://${INPUTS_HOST}/")"
awk "BEGIN {exit !(${time} < 10)}"
echo "time=${time}" >>"${GITHUB_OUTPUT}"
