#!/bin/bash
set -euo pipefail

LOGFILE="/var/log/resize_disk.log"
exec > >(tee -a "$LOGFILE") 2>&1

log() {
	echo "[$(date)] $*"
}

require_tools() {
	local tools=("$@")
	for tool in "${tools[@]}"; do
		if ! command -v "$tool" &>/dev/null; then
			log "ERROR: Required tool '$tool' is missing. Exiting."
			exit 1
		fi
	done
}

get_partition_info() {
	local output
	output=$(parted --script /dev/sda unit s print || true)

	local part total
	read -r part total < <(awk '
		/ 3 / {part = $4}
		/^Disk \/dev\/sda:/ {total = $3}
		END {print part, total}
	' <<<"$output")

	part="${part%s}"
	total="${total%s}"
	echo "$part $total"
}

resize_partition_if_needed() {
	local part_size=$1
	local total_size=$2

	if ((part_size < total_size)); then
		log "Resizing partition /dev/sda3..."
		parted --fix --script /dev/sda resizepart 3 100%
	else
		log "Partition /dev/sda3 is already at full size. Skipping."
	fi
}

resize_pv_if_needed() {
	if ! pvresize --test /dev/sda3 2>&1 | grep -q "successfully resized"; then
		log "Resizing physical volume..."
		pvresize /dev/sda3
	else
		log "Physical volume is already resized. Skipping."
	fi
}

resize_lv_if_needed() {
	local lv_path="/dev/ubuntu-vg/ubuntu-lv"
	local vg_path="/dev/ubuntu-vg"

	local lv_size
	lv_size=$(lvdisplay --units M "$lv_path" | awk '/LV Size/ {gsub("MiB","",$3); print $3}')

	local pe_size
	pe_size=$(vgdisplay --units M "$vg_path" | awk '/PE Size/ {gsub("MiB","",$3); print $3}')

	local current_le
	current_le=$(lvdisplay "$lv_path" | awk '/Current LE/ {print $3}')

	local used_space
	used_space=$(echo "$current_le * $pe_size" | bc)

	local free_space
	free_space=$(echo "$lv_size - $used_space" | bc)

	if (($(echo "$free_space > 0" | bc -l))); then
		log "Resizing logical volume..."
		lvresize -rl +100%FREE "$lv_path"
	else
		log "Logical volume is already fully extended. Skipping."
	fi
}

main() {
	log "Starting disk resize process..."
	require_tools parted pvresize lvresize lvdisplay vgdisplay grep awk bc tee

	local part_size total_size
	read -r part_size total_size < <(get_partition_info)

	resize_partition_if_needed "$part_size" "$total_size"
	resize_pv_if_needed
	resize_lv_if_needed
}

main "$@"
