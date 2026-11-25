#!/usr/bin/env bash
set -euo pipefail

error=""
domain="${INPUTS_HOST#*.}"
spf_record="$(dig +short TXT "${domain}" 2>&1 | grep 'v=spf1')" || error="DNS query failed"
echo "${spf_record}" | grep -q 'v=spf1' || error="SPF record not found"

spf_policy="$(echo "${spf_record}" | head -n 1 | tr -d '"' | tr -d '\r')"
{
	echo "policy=${spf_policy}"
	echo "error=${error}"
} >>"${GITHUB_OUTPUT}"
