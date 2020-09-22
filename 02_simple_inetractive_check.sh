#!/bin/bash

set -eu -o pipefail
trap 'echo "ERROR: l.$LINENO, exit status = $?" >&2; exit 1' ERR

function check_mount () {
	mkdir -p mnt
	sleep 5
	sudo mount $1 mnt

	ls mnt
	echo "create/remove command is fine."
	sleep 5

	sudo umount mnt
	rmdir mnt
}


for image in $( ls . | grep .tar.xz$ ); do
	tar -Jxf ${image}
done

### main function ###
check_mount fat12.img
check_mount fat16.img
check_mount fat32.img
check_mount exfat.img
