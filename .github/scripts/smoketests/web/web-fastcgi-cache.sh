#!/usr/bin/env bash
set -euo pipefail

get_cache_status() {
	curl --max-time 2 --silent --show-error --head "https://${INPUTS_HOST}/" |
		tr -d '\r' |
		awk 'BEGIN { IGNORECASE=1 } tolower($1) == "x-fastcgi-cache:" { print $2 }' || true
}

first="$(get_cache_status)"
deadline=$((SECONDS + 10))
second=""
while ((SECONDS < deadline)); do
	second="$(get_cache_status)"
	[[ "${second}" == "HIT" ]] && break
	sleep 1
done

{
	echo "first=${first}"
	echo "second=${second}"
} >>"${GITHUB_OUTPUT}"
test "${second}" = "HIT"
