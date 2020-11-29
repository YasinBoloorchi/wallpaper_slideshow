#!/bin/bash

# pkill wall_run.sh
ps -ef | grep "wallpaper_slideshow.py" | awk '{print $2}' | xargs kill 2> /dev/null

python /home/hakim/.config/i3/scripts/wallpaper_slideshow/wall_changer/wallpaper_slideshow.py /home/hakim/Pictures/backgrounds/i3_background 60


