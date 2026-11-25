#!/usr/bin/env bash
set -euo pipefail

error=""
banner="$(echo "QUIT" | nc -w 5 "${INPUTS_HOST}" 25 2>&1 | head -n 1)" || error="Connection failed"
echo "${banner}" | grep -q '220' || error="No 220 banner"

banner_text="$(echo "${banner}" | sed 's/^220 //' | tr -d '\r')"
{
	echo "banner=${banner_text}"
	echo "error=${error}"
} >>"${GITHUB_OUTPUT}"
