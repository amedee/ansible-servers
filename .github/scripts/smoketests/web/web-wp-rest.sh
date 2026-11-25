#!/usr/bin/env bash
set -euo pipefail

json="$(curl --fail --silent --show-error "https://${INPUTS_HOST}/wp-json/")"
echo "${json}" | grep -q '"name"'

site_name="$(echo "${json}" | grep -oE '"name":"[^"]*"' | head -n 1 | cut -d'"' -f4)"
posts_count="$(curl --silent --head "https://${INPUTS_HOST}/wp-json/wp/v2/posts?per_page=1" |
	grep -i '^X-WP-Total:' |
	awk '{print $2}' |
	tr -d '\r')"

{
	echo "site_name=${site_name}"
	echo "posts_count=${posts_count}"
} >>"${GITHUB_OUTPUT}"
