import os
import re
import shutil
import subprocess
import sys
from random import randint
from time import sleep

import cv2
import numpy as np
from PIL import Image


def set_wallpaper(pic_path):
    os.system(f'feh --bg-fill {pic_path} 2> /dev/null')


def fading(pic_path_1, pic_path_2):
    for i in range(1,11):
        lion = cv2.imread(pic_path_1,3)
        taj = cv2.imread(pic_path_2,3)
        alpha = cv2.imread(f'/home/hakim/.config/i3/scripts/wallpaper_slideshow/masks/mask{i}.png',0).astype(np.float32)
        
        a_B, a_G, a_R = cv2.split(lion)
        b_B, b_G, b_R = cv2.split(taj)

        b = (a_B * (alpha/255.0)) + (b_B * (1.0 - (alpha/255.0)))
        g = (a_G * (alpha/255.0)) + (b_G * (1.0 - (alpha/255.0)))
        r = (a_R * (alpha/255.0)) + (b_R * (1.0 - (alpha/255.0)))
        output = cv2.merge((b,g,r)) 

        cv2.imwrite("/tmp/new_image/wall_paper_pic.png", output)
        cv2.imwrite(f"/tmp/new_image/wall_paper_pic_{i}.png", output)
    
    for i in range(1, 11):
        set_wallpaper(f'/tmp/new_image/wall_paper_pic_{i}.png')


def manage_wall_pic(old_path):
    new_path = '/tmp/new_image/'
    pictures_count = 0
    
    if os.path.exists(new_path):
        shutil.rmtree(new_path)
    
    os.mkdir(new_path)
    
    subprocess_cmd = subprocess.Popen("xdpyinfo | grep 'dimensions:'", shell=True, stdout=subprocess.PIPE)
    subprocess_return = subprocess_cmd.stdout.read().decode('UTF-8').strip()
    resulution = re.findall('\s(\d*)x(\d*)\spixels',subprocess_return)[0]

    for root, dirs, files in os.walk(old_path):
        for file in files:
            pictures_count += 1

            image_path = root+'/'+file
            
            image = Image.open(image_path)
            width, height = image.size
        

            screen_width  = int(resulution[0])
            screen_hight = int(resulution[1])

            new_image = image.resize((1920, 1080))
            new_image.save(new_path+file)
            
            print(f'Pic #{pictures_count}:' , '(',width, height,')', '==>', image_path, end='\r')

    wall_pics_paths = []
    for root, dirs, files in os.walk(new_path):
        for file in files:
            wall_pics_paths += [root+file]

    return wall_pics_paths

# pic_path_1='../pics/1.jpg'
# pic_path_2='../pics/2.jpg'
# fading(pic_path_1, pic_path_2)

# get the arguments that we want (pic path and time interval)
try:
    old_path = sys.argv[1]
except:
    raise Exception('No pictures directory path has been specified!')

try:
    time_sleep = int(sys.argv[2])
except:
    raise Exception("No time interval has been specified!")

# keep a source file so that we can run this program infinitly
source_wall_pics_paths = manage_wall_pic(old_path)
wall_pics_paths = source_wall_pics_paths.copy()

# set the initial wallpaper picture
current_wallpaper = wall_pics_paths.pop(randint(0,len(wall_pics_paths)-1))
set_wallpaper(current_wallpaper)

# program infinity loop
while True:
    while len(wall_pics_paths) > 0:
        new_wallpaper = wall_pics_paths.pop(randint(0,len(wall_pics_paths)-1))
        sleep(time_sleep)
        fading(current_wallpaper, new_wallpaper)
        current_wallpaper = new_wallpaper

    wall_pics_paths = source_wall_pics_paths.copy()