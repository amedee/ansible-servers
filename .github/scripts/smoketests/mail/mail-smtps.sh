#!/usr/bin/env bash
set -euo pipefail

error=""
nc -zv "${INPUTS_HOST}" 465 2>&1 || error="Connection refused"
echo "error=${error}" >>"${GITHUB_OUTPUT}"
