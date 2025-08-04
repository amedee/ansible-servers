#!/usr/bin/env bash
set -euo pipefail

IFS=',' read -ra SECRET_NAMES <<<"$1"
missing=0

echo "🔍 Checking required secrets..."

for secret_name in "${SECRET_NAMES[@]}"; do
	trimmed=$(echo "$secret_name" | xargs)
	value="${!trimmed}"

	if [ -z "$value" ]; then
		echo "❌ Missing or empty required secret: $trimmed"
		missing=1
	else
		echo "✅ Found secret: $trimmed"
	fi
done

if [ "$missing" -eq 1 ]; then
	echo "🛑 One or more required secrets are missing or empty. Exiting."
	exit 1
fi

echo "🎉 All required secrets are present and non-empty."
