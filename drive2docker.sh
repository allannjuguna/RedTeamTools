#! /usr/bin/python3
# -*- coding: utf-8 -*-
#  @author: zerofrost
#  @date: 2050-01-11
#  @description: This script mounts a physical drive to a docker container 

dockerkali () {
	FOLDER="/media/$USER/KALI" 
	DRIVE="/dev/nvme0n1p5" 
	CONTAINER="8c24eef72f16" 
	echo "[*] Mounting directory"
	ls --color=auto "$FOLDER/root" 2> /dev/null || sudo mount -o rw "$DRIVE" "$FOLDER" 2> /dev/null
	echo sudo ls "$FOLDER/root" | grep --color=auto -q 'root' && echo '[+] Mounted successfully' || (
		echo '[-] Mount failed. Proceeding anyway'
	)
	docker run -it -v "$FOLDER":/mnt -w /root --user root "$CONTAINER" chroot /mnt /bin/bash
}



dockerkali
