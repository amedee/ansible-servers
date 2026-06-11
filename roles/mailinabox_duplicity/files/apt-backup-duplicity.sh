#!/bin/bash
set -x

mkdir -p /var/backups/debs/duplicity

cp -vn /var/cache/apt/archives/duplicity_*.deb /var/backups/debs/duplicity/ 2>/dev/null || true
cp -vn /root/duplicity_*.deb /var/backups/debs/duplicity/ 2>/dev/null || true
