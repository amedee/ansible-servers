#!/usr/bin/env bash
set -euo pipefail

cert_info="$(echo | openssl s_client -servername "${INPUTS_HOST}" -connect "${INPUTS_HOST}:443" -verify_return_error 2>&1 | openssl x509 -noout -dates -subject)"
echo "${cert_info}"

expires="$(echo "${cert_info}" | grep 'notAfter=' | cut -d= -f2)"
issuer="$(echo "${cert_info}" | grep 'subject=' | grep -oE 'CN = [^/]+|CN=[^/]+|CN =[^/]+' | sed 's/CN[ =]//' | head -n 1)"

{
	echo "expires=${expires}"
	echo "issuer=${issuer}"
} >>"${GITHUB_OUTPUT}"
