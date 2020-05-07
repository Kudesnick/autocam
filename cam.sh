#!/bin/bash

printf 'Autocam starting..'
if  [ $(date +"%M") == 0 ] && [ $[$(date +"%H") % 2] == 1 ]
then
    sudo python3 cam.py send
else
    sudo python3 cam.py
fi
printf 'Autocam finished.'
