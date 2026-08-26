#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

MAILDIR="${MAILDIR:-/home/user-data/mail/mailboxes/vangasse.eu/amedee/.Spam/cur/}"
SAVED_ATTACHMENTS="${SAVED_ATTACHMENTS:-/root/attachments}"

cleanup() {
	cd / || true

	if [[ -n "${ATTACHMENTS_DIR:-}" && -d "$ATTACHMENTS_DIR" ]]; then
		rm --force --recursive "$ATTACHMENTS_DIR"
	fi
}

trap cleanup EXIT

ATTACHMENTS_DIR="$(mktemp --directory --tmpdir attachments-XXXXXX)"

mkdir --parents "$SAVED_ATTACHMENTS"

cd "$ATTACHMENTS_DIR"

grep \
	--recursive \
	--files-with-matches \
	--null \
	--ignore-case \
	--extended-regexp \
	--regexp='Content-Type:[[:space:]]*(image|video)/' \
	"$MAILDIR" |
	while IFS= read -r -d '' mailfile; do
		# Continue even if one message is malformed.
		munpack "$mailfile" >/dev/null 2>&1 || true
	done

# Remove munpack description files if any were generated.
find . \
	-maxdepth 1 \
	-type f \
	-name '*.desc*' \
	-delete

# Deduplicate extracted files.
fdupes \
	--hardlinks \
	--noempty \
	--order=name \
	--delete \
	--noprompt \
	--quiet \
	.

# Copy all extracted image/video files. The destination filename
# is the SHA256 checksum plus a file extension derived from the MIME type.
find . -maxdepth 1 -type f -print0 |
	while IFS= read -r -d '' attachment; do
		mime_type="$(file --brief --mime-type "$attachment")"

		case "$mime_type" in
		image/* | video/*)
			subtype="${mime_type##*/}"

			case "$subtype" in
			jpeg)
				extension="jpg"
				;;
			svg+xml)
				extension="svg"
				;;
			quicktime)
				extension="mov"
				;;
			x-msvideo)
				extension="avi"
				;;
			x-matroska)
				extension="mkv"
				;;
			x-ms-wmv)
				extension="wmv"
				;;
			*)
				# Remove structured syntax suffixes.
				# Example: foo+xml -> foo
				extension="${subtype%%+*}"

				# Remove common vendor prefix.
				# Examples:
				#   x-icon -> icon
				#   x-ms-bmp -> ms-bmp
				extension="${extension#x-}"
				;;
			esac
			;;
		*)
			continue
			;;
		esac

		checksum="$(sha256sum "$attachment" | awk '{print $1}')"

		original_filename="$(basename "$attachment")"
		original_filename="${original_filename%.*}"

		destination="${SAVED_ATTACHMENTS}/${checksum}-${original_filename}.${extension}"

		if ! compgen -G "${SAVED_ATTACHMENTS}/${checksum}-*" >/dev/null; then
			rsync \
				--archive \
				"$attachment" \
				"$destination"
		fi
	done

fdupes \
	--hardlinks \
	--noempty \
	--order=name \
	--delete \
	--noprompt \
	--quiet \
	"$SAVED_ATTACHMENTS"
