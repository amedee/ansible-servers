#!/usr/bin/env bash
set -euo pipefail

: "${ANSIBLE_HOST:?ANSIBLE_HOST is required}"
: "${SSH_PRIVATE_KEY:?SSH_PRIVATE_KEY is required}"
: "${VAULT_PASSWORD:?VAULT_PASSWORD is required}"

# Retry policy
readonly MAX_ATTEMPTS=5
readonly BASE_SLEEP=5
readonly JITTER_MAX=5
WAIT=$BASE_SLEEP
ansible_args=()

umask 077
VAULT_FILE="$(mktemp)"
if [[ -n "${CHECK_MODE:-}" ]]; then
	ansible_args+=("$CHECK_MODE")
fi

mkdir --parents ~/.ssh/controlmasters

cleanup() {
	shred -u "$VAULT_FILE" 2>/dev/null || rm -f "$VAULT_FILE"
	ssh-agent -k >/dev/null 2>&1 || true
}
trap cleanup EXIT

# -----------------------------
# 🔐 Vault password handling
# -----------------------------
echo "${VAULT_PASSWORD}" >"$VAULT_FILE"
chmod 600 "$VAULT_FILE"

# -----------------------------
# 🔐 SSH agent setup
# -----------------------------
eval "$(ssh-agent -s)" >/dev/null
printf '%s\n' "${SSH_PRIVATE_KEY}" | tr -d '\r' | ssh-add - >/dev/null

export ANSIBLE_CONFIG=ansible.cfg
export ANSIBLE_STDOUT_CALLBACK=json

RETRY_PATTERNS=(
	"SSH:UNREACHABLE!|FAILED.*ssh"
	"SSH:Connection (timed out|refused|reset)"
	"NET:Could not resolve hostname|No route to host"
	"SSH:SSH connection"
	"DNS:Temporary failure in name resolution"
)

is_retryable_ssh_error() {
	local log_file="$1"

	for rule in "${RETRY_PATTERNS[@]}"; do
		category="${rule%%:*}"
		pattern="${rule#*:}"

		if grep -Eqi "$pattern" "$log_file"; then
			echo "🔁 Retry triggered by: $category"
			return 0
		fi
	done

	return 1
}

print_ssh_context() {
	echo "----- SSH/network failure context -----"
	grep -Ei \
		'UNREACHABLE|ssh|timeout|refused|reset|No route|Temporary failure' \
		"$1" || true
	echo "----------------------------------------"
}

for attempt in $(seq 1 "$MAX_ATTEMPTS"); do
	echo "🚀 Ansible attempt $attempt/$MAX_ATTEMPTS"

	LOG=$(mktemp)

	if ansible-playbook playbooks/site.yml \
		--inventory inventory/production \
		--limit "$ANSIBLE_HOST" \
		"${ansible_args[@]}" \
		--vault-password-file "$VAULT_FILE" \
		-vv 2>&1 | tee "$LOG"; then

		echo "✅ Success on attempt $attempt"
		exit 0
	fi

	echo "❌ Attempt $attempt failed"

	# -------------------------------------------------
	# 🚨 Decide retry vs fail immediately
	# -------------------------------------------------
	if ! is_retryable_ssh_error "$LOG"; then
		echo "💥 Non-retryable failure detected — not retrying"
		print_ssh_context "$LOG"
		exit 1
	fi

	# -------------------------------------------------
	# 🔍 SSH/network failure (retryable)
	# -------------------------------------------------
	print_ssh_context "$LOG"

	if [ "$attempt" -lt "$MAX_ATTEMPTS" ]; then
		JITTER=$((RANDOM % JITTER_MAX))
		WAIT=$((WAIT + JITTER))

		echo "🔁 Retryable SSH issue detected"
		echo "⏳ Sleeping ${WAIT}s (base=${BASE_SLEEP}, jitter=${JITTER})"

		sleep "$WAIT"
		WAIT=$((WAIT * 2))
		continue
	fi

	echo "💥 Max retries reached"
	exit 1
done
