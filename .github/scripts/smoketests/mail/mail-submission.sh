#!/usr/bin/env bash
set -euo pipefail

error=""
ehlo_response="$(echo "EHLO smoke-test" | nc -w 5 "${INPUTS_HOST}" 587 2>&1)" || error="Connection failed"
echo "${ehlo_response}" | grep -q 'STARTTLS' || error="No STARTTLS advertised"

ehlo_name="$(echo "${ehlo_response}" | head -n 1 | awk '{print $2}' | tr -d '\r')"
{
	echo "ehlo_name=${ehlo_name}"
	echo "error=${error}"
} >>"${GITHUB_OUTPUT}"
