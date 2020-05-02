import RPi.GPIO as GPIO
from time import sleep
from sh import mount
from sh import umount
import os
import subprocess

cam_pwr = 16
cam_pre = 20
cam_push = 21
usb_pwr = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup([cam_pwr, cam_pre, cam_push, usb_pwr], GPIO.IN)

if True:
    GPIO.setup(cam_pwr, GPIO.OUT, initial = GPIO.LOW)
    sleep(5)
    GPIO.setup(cam_pre, GPIO.OUT, initial = GPIO.LOW)
    sleep(1)
    GPIO.setup(cam_push, GPIO.OUT, initial = GPIO.LOW)
    sleep(1)
    GPIO.setup([cam_pre, cam_push], GPIO.IN)
    sleep(5)
    GPIO.setup(usb_pwr, GPIO.OUT, initial = GPIO.LOW)
    sleep(15)

    mount('LABEL=CAM_SD', '/media')
    sleep(1)
    
    mnt_path = '/media/DCIM/100MSDCF'
    cmd = ['python3', 'vk.py']
    for name in os.listdir(mnt_path):
        cmd.append(mnt_path + '/' + name)

    print('Send to server..')
    subprocess.run(cmd)

    for name in os.listdir(mnt_path):
        os.remove(mnt_path + '/' + name)
    
    umount('/media')

    GPIO.setup([cam_pwr, usb_pwr], GPIO.IN)
    sleep(3)

    print('Ok!')
