#!/bin/bash

MAILDIR='/home/user-data/mail/mailboxes/vangasse.eu/amedee/.Spam/cur/'
SAVED_ATTACHMENTS='/root/attachments/'

function cleanup()
{
    cd "$HOME" || exit
    rm --force --recursive "$ATTACHMENTS_DIR"
}
trap cleanup EXIT

ATTACHMENTS_DIR=$(mktemp --directory -t attachments-XXXX) || exit 1
mkdir --parents "$SAVED_ATTACHMENTS" || exit 1
cd "$ATTACHMENTS_DIR" || exit

(
    grep --files-with-matches --recursive --null --extended-regexp --regexp='Content-Type: (image|video)' "$MAILDIR" \
        | xargs --null --max-args=1 munpack
) &>/dev/null
rm --force ./*.desc*
fdupes --hardlinks --noempty --order=name --delete --noprompt --quiet .
rsync --archive --ignore-missing-args ./*.jpeg* ./*.jpg* ./*.png* ./*.mp4* "$SAVED_ATTACHMENTS"
