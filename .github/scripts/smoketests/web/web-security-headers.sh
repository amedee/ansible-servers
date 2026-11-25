#!/usr/bin/env bash
set -euo pipefail

headers="$(mktemp)"
curl --fail --silent --show-error --dump-header "${headers}" --output /dev/null "https://${INPUTS_HOST}/"

hsts="$(awk '
  BEGIN { IGNORECASE=1 }
  tolower($1) == "strict-transport-security:" {
    sub(/\r$/, "")
    $1 = ""
    sub(/^[[:space:]]+/, "")
    print
  }
' "${headers}")"

echo "HSTS: ${hsts}"
test -n "${hsts}"

max_age="$(printf '%s\n' "${hsts}" | grep -oiE 'max-age=[0-9]+' | head -n 1 | cut -d= -f2)"
test -n "${max_age}"
test "${max_age}" -gt 0
echo "max_age=${max_age}" >>"${GITHUB_OUTPUT}"
