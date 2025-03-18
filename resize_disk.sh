#!/bin/bash

# Enable strict error handling
set -euo pipefail

# Define log file
LOGFILE="/var/log/resize_disk.log"

# Log output to both console and file
exec > >(tee -a "$LOGFILE") 2>&1

echo "[$(date)] Starting disk resize process..."

# Check if required tools are available
REQUIRED_TOOLS=("parted" "pvresize" "lvresize" "lvdisplay" "grep" "awk")

for tool in "${REQUIRED_TOOLS[@]}"; do
	if ! command -v "$tool" &>/dev/null; then
		echo "[$(date)] ERROR: Required tool '$tool' is missing. Exiting."
		exit 1
	fi
done

# Get partition and total disk size
parted_output=$(parted --script /dev/sda unit s print || true)
read -r PARTITION_SIZE TOTAL_SIZE < <(echo "$parted_output" | awk '
    / 3 / {part = $4}          # Extracts the size of partition 3
    /^Disk \/dev\/sda:/ {total = $3}  # Extracts the total disk size
    END {print part, total}
')

# Remove the 's' suffix and compare the numerical values
PARTITION_SIZE_NUM="${PARTITION_SIZE%s}"
TOTAL_SIZE_NUM="${TOTAL_SIZE%s}"

# Resize partition if needed
if [[ "$PARTITION_SIZE_NUM" -lt "$TOTAL_SIZE_NUM" ]]; then
	echo "[$(date)] Resizing partition /dev/sda3..."
	parted --fix --script /dev/sda resizepart 3 100%
else
	echo "[$(date)] Partition /dev/sda3 is already at full size. Skipping."
fi

# Resize the physical volume if needed
if [[ "$(pvresize --test /dev/sda3 2>&1)" != *"successfully resized"* ]]; then
	echo "[$(date)] Resizing physical volume..."
	pvresize /dev/sda3
else
	echo "[$(date)] Physical volume is already resized. Skipping."
fi

# Get the LV size in MiB
LV_SIZE=$(lvdisplay --units M /dev/ubuntu-vg/ubuntu-lv | grep "LV Size" | awk '{print $3}' | tr -d 'MiB')

# Get the PE size in MiB
PE_SIZE=$(vgdisplay --units M /dev/ubuntu-vg | grep "PE Size" | awk '{print $3}' | tr -d 'MiB')

# Get the Current LE
CURRENT_LE=$(lvdisplay /dev/ubuntu-vg/ubuntu-lv | grep "Current LE" | awk '{print $3}')

# Calculate the used space (Current LE * PE Size)
USED_SPACE=$(echo "$CURRENT_LE * $PE_SIZE" | bc)

# Calculate free space using bc for floating-point arithmetic
FREE_SPACE=$(echo "$LV_SIZE - $USED_SPACE" | bc)

# Check if there is free space (non-zero)
if (($(echo "$FREE_SPACE > 0" | bc -l))); then
	echo "[$(date)] Resizing logical volume..."
	lvresize -rl +100%FREE /dev/ubuntu-vg/ubuntu-lv
else
	echo "[$(date)] Logical volume is already fully extended. Skipping."
fi
