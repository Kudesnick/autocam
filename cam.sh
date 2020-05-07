#!/bin/bash

if  [ $(date +"%M") == 0 ] && [ $[$(date +"%H") % 2] == 1 ]
then
    printf 'sudo python3 cam.py send\r\n'
else
    printf 'sudo python3 cam.py\r\n'
fi
date +"%H:%M"
