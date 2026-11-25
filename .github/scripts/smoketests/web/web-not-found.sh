#!/usr/bin/env bash
set -euo pipefail

status="$(curl --silent --output /dev/null --write-out '%{http_code}' "https://${INPUTS_HOST}/nonexistent-page-12345/")"
echo "status=${status}" >>"${GITHUB_OUTPUT}"
test "${status}" = "404"
