import os
from time import sleep
import cv2
import numpy as np
from PIL import Image
import re
import subprocess
from random import randint


def set_wallpaper(pic_path):
    os.system(f'wal -i {pic_path}')


def fading(pic_path_1, pic_path_2):
    for i in range(1,11):
        lion = cv2.imread(pic_path_1,3)
        taj = cv2.imread(pic_path_2,3)
        alpha = cv2.imread(f'../masks/mask{i}.png',0).astype(np.float32)
        
        a_B, a_G, a_R = cv2.split(lion)
        b_B, b_G, b_R = cv2.split(taj)

        b = (a_B * (alpha/255.0)) + (b_B * (1.0 - (alpha/255.0)))
        g = (a_G * (alpha/255.0)) + (b_G * (1.0 - (alpha/255.0)))
        r = (a_R * (alpha/255.0)) + (b_R * (1.0 - (alpha/255.0)))
        output = cv2.merge((b,g,r)) 

        cv2.imwrite("wall_paper_pic.png", output)
        set_wallpaper('./wall_paper_pic.png')


def manage_wall_pic(old_path):
    new_path = '/tmp/new_image/'
    if not os.path.exists(new_path):
        os.mkdir(new_path)

    for root, dirs, files in os.walk(old_path):
        for file in files:
            image_path = root+'/'+file
            
            image = Image.open(image_path)
            width, height = image.size

            print('(',width, height,')', '==>', image_path)
            
            # TODO: dynamicly find dimension of every monitor with 
            # xdpyinfo | grep 'dimensions:'

            subprocess_cmd = subprocess.Popen("xdpyinfo | grep 'dimensions:'", shell=True, stdout=subprocess.PIPE)
            subprocess_return = subprocess_cmd.stdout.read().decode('UTF-8').strip()

            resulution = re.findall('\s(\d*)x(\d*)\spixels',subprocess_return)[0]
            print('screen resulotion: ',resulution)
            width  = int(resulution[0])
            hight = int(resulution[1])


            new_image = image.resize((1920, 1080))
            new_image.save(new_path+file)

    wall_pics_paths = []
    for root, dirs, files in os.walk(new_path):
        for file in files:
            wall_pics_paths += [root+file]

    return wall_pics_paths

# pic_path_1='../pics/1.jpg'
# pic_path_2='../pics/2.jpg'
# fading(pic_path_1, pic_path_2)


old_path = input('Enter your pictures directory full path: ')
time_sleep = int(input("Enter the time to wait between each wallpaper to change: "))

wall_pics_paths = manage_wall_pic(old_path)

current_wallpaper = wall_pics_paths.pop(randint(0,len(wall_pics_paths)-1))
set_wallpaper(current_wallpaper)

while len(wall_pics_paths) > 0:
    new_wallpaper = wall_pics_paths.pop(randint(0,len(wall_pics_paths)-1))
    sleep(time_sleep)
    fading(current_wallpaper, new_wallpaper)
    current_wallpaper = new_wallpaper
