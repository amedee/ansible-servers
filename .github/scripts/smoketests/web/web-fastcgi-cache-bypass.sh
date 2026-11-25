#!/usr/bin/env bash
set -euo pipefail

status="$(curl --silent --show-error --head "https://${INPUTS_HOST}/?smoketest=$(date +%s)" |
	tr -d '\r' |
	awk 'BEGIN { IGNORECASE=1 } tolower($1) == "x-fastcgi-cache:" { print $2 }')"

echo "status=${status}" >>"${GITHUB_OUTPUT}"
test "${status}" = "BYPASS"
