#!/usr/bin/env bash
set -euo pipefail

output="$(curl --fail --silent --show-error --write-out '%{http_code} %{size_download}' "https://${INPUTS_HOST}/wp-login.php" 2>/dev/null | tail -1)"
status="$(echo "${output}" | awk '{print $1}')"
size="$(echo "${output}" | awk '{print $2}')"

{
	echo "status=${status}"
	echo "size=${size}"
} >>"${GITHUB_OUTPUT}"
