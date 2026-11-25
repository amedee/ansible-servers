#!/usr/bin/env bash
set -euo pipefail

headers="$(mktemp)"
curl --silent --output /dev/null --dump-header "${headers}" "http://${INPUTS_HOST}/"

status="$(awk 'NR == 1 {print $2}' "${headers}")"
location="$(awk 'BEGIN{IGNORECASE=1} /^Location:/ {print $2}' "${headers}" | tr -d '\r')"

{
	echo "status=${status}"
	echo "location=${location}"
} >>"${GITHUB_OUTPUT}"

test "${status}" = "301" || test "${status}" = "302" || test "${status}" = "307" || test "${status}" = "308"
test "${location}" = "https://${INPUTS_HOST}/"
