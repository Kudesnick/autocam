#!/bin/bash

cd /home/pi/autocam

date

M=$(date +'%-M')
H=$(date +'%-H')

if   [ $(($M +  0)) == 0 ] && [ $(($H %  2)) == 0 ]; then
    printf 'Repo update..\r\n'
    git pull
    printf 'Repo update complete.\r\n'
fi

if   [ $(($M +  0)) == 0 ] && [ $(($H %  4)) == 0 ]; then
    printf 'Autocam send and sync starting..\r\n'
    python3 cam.py --send --sync
    printf 'Autocam finished.\r\n'
elif [ $(($M +  0)) == 0 ] && [ $(($H %  2)) == 0 ]; then
    printf 'Autocam send starting..\r\n'
    python3 cam.py --send
    printf 'Autocam finished.\r\n'
elif [ $(($M % 10)) == 0 ] && [ $(($H %  1)) == 0 ]; then
    printf 'Autocam starting..\r\n'
    python3 cam.py
    printf 'Autocam finished.\r\n'
elif [ $(($M %  5)) == 0 ] && [ $(($H %  1)) == 0 ]; then
    printf 'Autocam for cloud only starting..\r\n'
    python3 cam.py --cloud
    printf 'Autocam finished.\r\n'
fi
