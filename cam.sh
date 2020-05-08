#!/bin/bash

cd /home/pi/autocam

date

if  [ $[$(date +"%M") +  0] == 0 ] && [ $[$(date +"%H") %  2] == 0 ]; then
    printf 'Repo update..\r\n'
    git pull
    printf 'Repo update complete.\r\n'
fi

if  [ $[$(date +"%M") +  0] == 0 ] && [ $[$(date +"%H") %  2] == 0 ]; then
    printf 'Autocam send starting..\r\n'
    sudo python3 cam.py send
    printf 'Autocam finished.\r\n'
elif [ $[$(date +"%M") % 10] == 0 ] && [ $[$(date +"%H") %  1] == 0 ]; then
    printf 'Autocam starting..\r\n'
    sudo python3 cam.py
    printf 'Autocam finished.\r\n'
fi
