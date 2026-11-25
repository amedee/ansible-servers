#!/usr/bin/env bash
set -euo pipefail

feed="$(curl --fail --silent --show-error "https://${INPUTS_HOST}/feed/")"
grep -q '<rss' <<<"${feed}"

item_count="$(echo "${feed}" | grep -c '<item>')"
latest_title="$(echo "${feed}" | tr '\n' ' ' | grep -oP '<item>\s*<title>\K[^<]+' | sed -n '1p')"

{
	echo "item_count=${item_count}"
	echo "latest_title=${latest_title}"
} >>"${GITHUB_OUTPUT}"
