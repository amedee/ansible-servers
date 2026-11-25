#!/usr/bin/env bash
set -euo pipefail

error=""
domain="${INPUTS_HOST#*.}"
mx_record="$(dig +short MX "${domain}" 2>&1)" || error="DNS query failed"
echo "${mx_record}" | grep -q "${INPUTS_HOST}" || error="MX record not found"

mx_priority="$(echo "${mx_record}" | grep "${INPUTS_HOST}" | awk '{print $1}' | head -n 1 | tr -d '\r')"
mx_server="$(echo "${mx_record}" | grep "${INPUTS_HOST}" | awk '{print $2}' | head -n 1 | tr -d '\r' | sed 's/\.$//')"

{
	echo "priority=${mx_priority}"
	echo "server=${mx_server}"
	echo "error=${error}"
} >>"${GITHUB_OUTPUT}"
