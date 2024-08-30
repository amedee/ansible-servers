#!/bin/sh
# Expunge Trash and Spam
DOVEADM=$(which doveadm)

$DOVEADM expunge -A mailbox Trash before 30d
$DOVEADM expunge -A mailbox Spam  before 60d
