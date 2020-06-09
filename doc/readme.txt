; Проверка разметки диска
$ df -h
; Развернуть систему на весь свободный диск:
# /usr/lib/raspi-config/init_resize.sh

; ресайз консольного вывода
$ stty rows 48 cols 120 size
# nano /etc/bash.bashrc
; add
stty rows 48 cols 120
; to end of this file 

; autologin
; see: https://raspberrypi.stackexchange.com/questions/102227/unable-to-set-autologin-on-pi-zero-w-running-raspbian-buster-lite-previous-solu
# systemctl edit serial-getty@ttyS0.service
; add
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin pi --keep-baud 115200,38400,9600 %I $TERM
; reboot system

; доступ к папке всем
# chmod -R 777 <foldername>

? pip3 install gpiozero pigpio
# pip3 install RPi.GPIO

? apt install pigpio
? pigpiod

$ pinout

; Монтируем флешку (по метке диска - CAM_SD) [deprecated]
# mount -L CAM_SD /media
$ ls /media/DCIM/100MSDCF
; _DSC????.JPG
# umount /media

; Автомонтирование флешки
# apt install usbmount
# nano /etc/fstab
; add string:
/dev/sda1 /media auto defaults,noatime,sync,user,nofail,rw,umask=0000 0 0
# nano /etc/usbmount/usbmount.conf
; replase variables to:
MOUNTPOINTS="/media"
FILESYSTEMS="vfat"
FS_MOUNTOPTIONS=""
# nano /lib/systemd/system/systemd-udevd.service
; replace
PrivateMounts=yes
; to
PrivateMounts=no
; warning! this option must be autoreset after upgrade system

тестовая группа: club194929390

; Cron с выводом ошибок в консоль:
# crontab -e
0 * * * * cd /home/pi/autocam ; /usr/bin/phython3 cam.py > /dev/ttyS0 2>&1

; установка opensv
# pip3 install opencv-python
# pip3 install opencv-contrib-python==3.4.3.18
# apt install libwebp-dev
# apt install libtiff-dev
# apt install libjasper-dev
# apt install libhdf5-dev
# apt install libharfbuzz-dev
# apt install liblapack-dev
# apt install libatlas-base-dev
# apt install libilmbase23
# apt install libopenexr-dev
# apt install libavcodec-dev
# apt install libavformat-dev
# apt install libswscale-dev
# apt install libqtgui4
# apt install libgstreamer1.0-0

; установка rclone
$ curl https://rclone.org/install.sh | sudo bash

; работа с i2c
# sudo raspi-config
Interfacing Options -> I2C -> YES
# apt install i2c-tools
# i2cdetect -y 1
# i2cdump -y -f -r 0-15 1 0x68
# nano /etc/modules
; add 'rtc-ds3231' string to this file and reboot system
# hwclock --set --date "2005/01/12 23:24:25"
# hwclock --show --verbose
