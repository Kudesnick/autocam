#!/bin/bash

# lock execute other instance of this script
lock_file=/var/lock/$(basename $0).lock

echo $lock_file

lock_waiting=50
lock_repeat=5

while [ $lock_waiting > 0 ]; do
    lock_waiting=$[ $lock_waiting - $lock_repeat ]
    
    if fuser $lock_file > /dev/null 2>&1; then
        sleep $lock_repeat
    else
        break
    fi

    if [ $lock_waiting -le 0 ]; then
        echo 'WARNING: Other instance of $(basename $0) running.'
        exit 1
    fi
done

exec 3> $lock_file

# main functional
cd /home/pi/autocam

date

M=$(date +'%-M')
H=$(date +'%-H')

# run cam.py in the desired mode
if   [ $(($M +  0)) == 0 ] && [ $(($H %  4)) == 0 ]; then
    echo 'Autocam send and sync starting..'
    python3 cam.py --send --sync
    echo 'Autocam finished.'
elif [ $(($M +  0)) == 0 ] && [ $(($H %  2)) == 0 ]; then
    echo 'Autocam send starting..'
    python3 cam.py --send
    echo 'Autocam finished.'
elif [ $(($M % 10)) == 0 ] && [ $(($H %  1)) == 0 ]; then
    echo 'Autocam starting..'
    python3 cam.py
    echo 'Autocam finished.'
elif [ $(($M %  5)) == 0 ] && [ $(($H %  1)) == 0 ]; then
    echo 'Autocam for cloud only starting..'
    python3 cam.py --cloud
    echo 'Autocam finished.'
fi

# repo update
if   [ $(($M % 30)) == 0 ] && [ $(($H %  1)) == 0 ]; then
    echo 'Repo update..'
    git pull
    echo 'Repo update complete.'
fi
