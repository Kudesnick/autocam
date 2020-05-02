import RPi.GPIO as GPIO
from time import sleep
from sh import mount
from sh import umount
import os

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
    sleep(5)
    print("Here must be loaded image to the internet.")
    mount('LABEL=CAM_SD', '/media')
    sleep(1)
    for name in os.listdir('/media/DCIM/100MSDCF'):
        print(name)
    umount('/media')
    GPIO.setup([cam_pwr, usb_pwr], GPIO.IN)
    sleep(3)

    print('Ok!')
