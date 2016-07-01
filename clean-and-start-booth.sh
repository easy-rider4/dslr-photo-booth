#!/bin/bash

echo "[INFO] stop processes that are working with the camera"
pkill gvfs

echo "[INFO] delete old images from directory pictures"
sudo rm -rf pictures

echo "[INFO] create directory pictures/ if it does not exist"
sudo mkdir -p pictures

echo "[INFO] start photo-booth"
sudo python photo-booth.py