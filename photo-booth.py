# -*- coding: utf8 -*-

# ------------- IMPORTS 
import os, glob
import subprocess
import datetime
import sys
import time
import RPi.GPIO as GPIO
import config
from PIL import Image


# -------------- set GPIO-Input
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP) # shut down pi


# -------------- functions
def get_latest_image(dirpath, valid_extensions=('jpg','jpeg','png')):
    valid_files = get_valid_files(dirpath, valid_extensions=('jpg','jpeg','png'))
    if not valid_files:
        return ''
    return max(valid_files, key=os.path.getmtime)


def get_valid_files(dirpath, valid_extensions=('jpg','jpeg','png')):
    # get filepaths of all files and dirs in the given dir
    valid_files = [os.path.join(dirpath, filename) for filename in os.listdir(dirpath)]

    # filter out directories, no-extension, and wrong extension files
    valid_files = [f for f in valid_files if '.' in f and \
        f.rsplit('.',1)[-1] in valid_extensions and os.path.isfile(f)]

    #sortedFiles = valid_files.sort(key=lambda x: os.path.getmtime)
    return valid_files


# returns a string with all files in a set camera folder
def list_all_pictures():
    return subprocess.check_output(['gphoto2', '--list-files', '--folder=' + config.CAMERA_FOLDER])


def save_particular_pictures(currentPath, picFrom, picTo):
    os.chdir(picturePath)   
    getFiles = subprocess.check_output(['gphoto2', '--get-file=' + str(picFrom) + '-' + str(picTo) , '--folder='  + config.CAMERA_FOLDER, '--force-overwrite'])
    os.chdir(currentPath)
    print('[INFO] --------')
    print(getFiles.rstrip('\n'))
    print('---------------')
    

def save_all_pictures(currentPath):
    os.chdir(picturePath)
    getFiles = subprocess.check_output(['gphoto2', '--get-all-files', '--folder=' + config.CAMERA_FOLDER, '--force-overwrite'])
    os.chdir(currentPath)
    print('[INFO] --------')
    print(getFiles.rstrip('\n'))
    print('---------------')
    

def get_camera_picture_count():
    fileCount = subprocess.check_output(['gphoto2', '--num-files', '--folder=' + config.CAMERA_FOLDER])
    countList = fileCount.split(': ')
    if (len(countList) > 1):
        return int(float(countList[1]))
    return 0


# -------------- script
# open background image
print('[INFO] photo-booth with dslr started')
backgroundLoading = subprocess.Popen(['feh', '--fullscreen', config.BACKGROUND_IMAGE_LOADING])

currentPath = os.getcwd()
picturePath = currentPath + '/pictures'
if (config.WEB_GALLERY != ''):
    picturePath = config.WEB_GALLERY

#save all prictures from the camera at program start
save_all_pictures(currentPath)
#wait till camera is free again
loadCount = 0
while (loadCount < 7):
    time.sleep(1)
    loadCount = loadCount + 1

#open background image
background = subprocess.Popen(['feh', '--fullscreen', config.BACKGROUND_IMAGE])
time.sleep(1)
backgroundLoading.terminate()
backgroundLoading.kill()


# wait for input 
while True:

    # ----- shutdown pi
    if (GPIO.input(17) == False):
        print('Bye bye!')
        background.terminate()
	background.kill()
        os.system("sudo shutdown -h now")  

        
    # ----- check for input
    camPicCount = get_camera_picture_count()

    # wait a moment to free camera
    time.sleep(0.8) 
    
    dirPicCount = len(glob.glob1(picturePath, '*.JPG'))

    if(camPicCount != 0):
        #are pictures on the camera
        
        if(dirPicCount < camPicCount):
            #are new pictures on the camaera that are not in on the pi

            #save new pics
            print ('[INFO] save pics from ' + str(dirPicCount+1) + '-' + str(camPicCount))
            save_particular_pictures(currentPath, dirPicCount+1, camPicCount)

            # wait a moment to save the pics
            time.sleep(1)

    #get new directory image count    
    validFiles = glob.glob1(picturePath, '*.JPG')
    countValidFiles = len(validFiles)

    #sort files on creation datetime
    validFiles.sort()
    countDisplayPics = camPicCount - dirPicCount

    #display new pics
    if (countDisplayPics > 0):
        print('[INFO] display ' + str(countDisplayPics) + ' pictures')
    pictureList = []
    counter = countDisplayPics
    while (counter > 0):
        path = picturePath + '/' + validFiles[countValidFiles-counter]
        pictureList.append(subprocess.Popen(['feh', '--fullscreen', path]))
        time.sleep(config.DISPLAY_TIME)
        counter = counter -1

    #close feh instances
    counter2 = 0
    while (counter2 < len(pictureList)):
        pictureList[counter2].terminate()
        pictureList[counter2].kill()
        counter2 = counter2 + 1    
                          
    time.sleep(0.1);
