#!/bin/bash

cd ~/autocam

if  [ $[$(date +"%M") +  0] == 0 ] && [ $[$(date +"%H") %  2] == 0 ]
then
    printf 'Repo update..'
    git pull
    printf 'Repo update complete.'
fi

if  [ $[$(date +"%M") +  0] == 0 ] && [ $[$(date +"%H") %  2] == 0 ]
then
    printf 'Autocam send starting..'
    sudo python3 cam.py send
    printf 'Autocam finished.'
elif [ $[$(date +"%M") % 10] == 0 ] && [ $[$(date +"%H") %  1] == 0 ]
    printf 'Autocam starting..'
    sudo python3 cam.py
    printf 'Autocam finished.'
fi
