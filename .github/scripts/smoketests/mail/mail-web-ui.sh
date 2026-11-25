#!/usr/bin/env bash
set -euo pipefail

error=""
output="$(curl --fail --silent --show-error --write-out '%{http_code} %{size_download}' "https://${INPUTS_HOST}/" 2>&1 | tail -1)" || error="Request failed"
status="$(echo "${output}" | awk '{print $1}')"
size="$(echo "${output}" | awk '{print $2}')"

{
	echo "status=${status}"
	echo "size=${size}"
	echo "error=${error}"
} >>"${GITHUB_OUTPUT}"
