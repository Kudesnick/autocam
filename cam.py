from time import sleep
import subprocess
from pathlib import Path

import vk

is_debug = Path('debug').exists()

if is_debug:
    print('Run in debug mode.')
else:
    print('Run in release mode.')

if not is_debug:
    import RPi.GPIO as GPIO
    from sh import mount
    from sh import umount

cam_pwr = 16
cam_pre = 20
cam_push = 21
usb_pwr = 12

def cam_pwr_on():
    if is_debug:
        print('Debug: cam_pwr_on')
        return

    GPIO.setmode(GPIO.BCM)
    GPIO.setup([cam_pwr, cam_pre, cam_push, usb_pwr], GPIO.IN)
    GPIO.setup(cam_pwr, GPIO.OUT, initial = GPIO.LOW)
    sleep(2)

def cam_pwr_off():
    if is_debug:
        print('Debug: cam_pwr_off')
        return

    GPIO.setup([cam_pwr, cam_pre, cam_push, usb_pwr], GPIO.IN)
    GPIO.cleanup()

def cam_push_btn():
    if is_debug:
        print('Debug: cam_push')
        return

    GPIO.setup(cam_pre, GPIO.OUT, initial = GPIO.LOW)
    sleep(0.2)
    GPIO.setup(cam_push, GPIO.OUT, initial = GPIO.LOW)
    sleep(0.2)
    GPIO.setup([cam_pre, cam_push], GPIO.IN)
    sleep(20)

def cam_disc_mount():
    if is_debug:
        print('Debug: cam_disc_mount')
        return

    GPIO.setup(usb_pwr, GPIO.OUT, initial = GPIO.LOW)
    sleep(5)
    mount('LABEL=CAM_SD', '/media')

def cam_disc_unmount():
    if is_debug:
        print('Debug: cam_disc_unmount')
        return

    umount('/media')
    GPIO.setup(usb_pwr, GPIO.IN)

def add_path_to_vk(_path: str, _del_after: bool = False):
    files = list()
    for name in Path(_path).glob('*.JP*'):
        files.append(str(name))

    print('Send to server..')
    vk.main(files)

    if _del_after:
        for name in Path(_path).glob('*'):
            name.unlink()

try:
    cam_pwr_on()
    cam_push_btn()
    
    cam_disc_mount()
    if is_debug:
        add_path_to_vk('dbg_files', False)
    else:
        add_path_to_vk('/media/DCIM/100MSDCF', True)

finally:
    cam_disc_unmount()
    cam_pwr_off()

    print('Ok!')
