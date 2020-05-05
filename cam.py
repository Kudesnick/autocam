# -*- coding: utf-8 -*-

import sys
from time import sleep
import subprocess
from pathlib import Path
import vk
import diff

is_debug = Path('debug').exists()

if not is_debug:
    import RPi.GPIO as GPIO
    from sh import mount
    from sh import umount

cam_pwr = 16
cam_pre = 20
cam_push = 21
usb_pwr = 12

def cam_pwr_on():
    global is_debug
    if is_debug:
        print('Debug: cam_pwr_on')
        return
    GPIO.setmode(GPIO.BCM)
    GPIO.setup([cam_pwr, cam_pre, cam_push, usb_pwr], GPIO.IN)
    GPIO.setup(cam_pwr, GPIO.OUT, initial = GPIO.LOW)
    sleep(2)

def cam_pwr_off():
    global is_debug
    if is_debug:
        print('Debug: cam_pwr_off')
        return
    GPIO.setup([cam_pwr, cam_pre, cam_push, usb_pwr], GPIO.IN)
    GPIO.cleanup()

def cam_push_btn():
    global is_debug
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
    global is_debug
    if is_debug:
        print('Debug: cam_disc_mount')
        return
    GPIO.setup(usb_pwr, GPIO.OUT, initial = GPIO.LOW)
    sleep(5)
    mount('LABEL=CAM_SD', '/media')

def cam_disc_unmount():
    global is_debug
    if is_debug:
        print('Debug: cam_disc_unmount')
        return
    umount('/media')
    GPIO.setup(usb_pwr, GPIO.IN)

def add_path_to_vk(_path: str, _send: bool = False):
    global is_debug
    files = list()
    for name in Path(_path).glob('*.JP*'):
        files.append(str(name))

    if len(files) < 1:
        return

    # delete files if too similar ->
    hash_file = Path(_path).joinpath('hash')
    last_hash = ''
    if hash_file.is_file():
        last_hash = hash_file.read_text()
    new_hash, new_light = diff.CalcImageHash(files[-1], 32, 32)
    if new_light > 35 and (last_hash == '' or diff.CompareHash(last_hash, new_hash) > 150):
        hash_file.write_text(new_hash)
    # dirty hack for detect if not added new files
    elif last_hash == '' or diff.CompareHash(last_hash, new_hash) != 0:
        # files is too similar or darkness
        f_path = Path(files[-1])
        if is_debug:
            f_path.rename(f_path.with_suffix('.back'))
        else:
            f_path.unlink()
    # delete files if too similar <-

    if _send:
        print('Send to server..')
        vk.main(files)
        if not is_debug:
            for name in Path(_path).glob('*.JP*'):
                name.unlink()

def main(_send_msg: bool = False):
    global is_debug
    if is_debug:
        print('Run in debug mode.')
    else:
        print('Run in release mode.')
    try:
        cam_pwr_on()
        cam_push_btn()
        cam_disc_mount()
        img_path = '/media/DCIM/100MSDCF' if not is_debug else 'dbg_files'
        add_path_to_vk(img_path, _send_msg)
    finally:
        cam_disc_unmount()
        cam_pwr_off()

        print('Complete.')

if __name__ == "__main__":
    if is_debug:
        send = input('Send files to server? (y/n): ') == 'y'
        main(send)
    else:
        main(len(sys.argv) > 1 and sys.argv[1] == 'send')
