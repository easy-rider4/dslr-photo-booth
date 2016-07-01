#!/bin/bash

echo "[INFO] clean up old entries"
sudo rm -r /media/photobooth

echo "[INFO] remove usb - because of auto mount"
sudo umount /media/photobooth

echo "[INFO] create directory"
sudo mkdir /media/photobooth

echo "[INFO] mount usb with needed file permissions"
sudo mount /dev/sda1 /media/photobooth -o dmask=000,fmask=111,uid=pi,gid=pi

echo "[INFO] stop processes that are working with the camera"
pkill gvfs

echo "[INFO] create directory pictures/ if it does not exist"
mkdir -p pictures

echo "[INFO] start photo-booth"
sudo python photo-booth.py