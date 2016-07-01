#!/bin/bash

echo "[INFO] stop processes that are working with the camera"
pkill gvfs

echo "[INFO] create directory pictures/ if it does not exist"
mkdir -p pictures

echo "[INFO] start photo-booth"
sudo python photo-booth.py