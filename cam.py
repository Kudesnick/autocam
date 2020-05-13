# -*- coding: utf-8 -*-

import sys
from time import sleep
from datetime import datetime
import subprocess
from pathlib import Path
import vk
import diff

is_debug = Path('debug').exists()

if not is_debug:
    import RPi.GPIO as GPIO

cam_pwr = 16
cam_pre = 20
cam_push = 21
usb_pwr = 12
relay = 18

def cam_pwr_on():
    global is_debug
    if is_debug:
        print('Debug: cam_pwr_on')
        return True
    GPIO.setmode(GPIO.BCM)
    GPIO.setup([cam_pwr, cam_pre, cam_push, usb_pwr], GPIO.IN)
    if not GPIO.input(cam_pwr):
        return False
    GPIO.setup([cam_pwr], GPIO.OUT, initial = GPIO.LOW)
    GPIO.setup([relay], GPIO.OUT, initial = GPIO.HIGH)
    sleep(2)
    return True

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
    GPIO.setup(relay, GPIO.OUT, initial = GPIO.HIGH)
    GPIO.setup(cam_pre, GPIO.OUT, initial = GPIO.LOW)
    sleep(0.2)
    GPIO.setup(cam_push, GPIO.OUT, initial = GPIO.LOW)
    sleep(0.2)
    GPIO.setup([cam_pre, cam_push], GPIO.IN)
    sleep(10)
    GPIO.setup(relay, GPIO.OUT, initial = GPIO.LOW)
    sleep(10)

def cam_disc_mount():
    global is_debug
    if is_debug:
        print('Debug: cam_disc_mount')
        return
    GPIO.setup(usb_pwr, GPIO.OUT, initial = GPIO.LOW)
    sleep(10)

def cam_disc_umount():
    global is_debug
    if is_debug:
        print('Debug: cam_disc_unmount')
        return
    GPIO.setup(usb_pwr, GPIO.IN)

def delete_file(_path: Path):
    _path.rename(_path.with_suffix('.jpg'))

def files_first_rename(_path: str, _cloud_only: bool):
    new_files = [name for name in Path(_path).glob('*.JPG')]
    suffix = '.jpg' if _cloud_only else '.jpeg'
    for name in new_files:
        name.rename(Path(name.parent, hex(int(datetime.utcnow().timestamp())) + name.stem + suffix))

def add_path_to_vk(_path: str, _send: bool):
    global is_debug
    files = [str(name) for name in Path(_path).glob('*.jpeg')]
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
        delete_file(Path(files.pop()))
    # delete files if too similar <-

    if _send:

        max_img_nums = 7 # maximum images to sending
        if (len(files) > max_img_nums):
            print('Thinning images..')
            divers_sum = []
            for f in files:
                tmp, _ = diff.CalcImageHash(f, 32, 32)
                divers_sum.append((diff.DiversityHash(tmp), f))

            to_remove = sorted(divers_sum)[:-max_img_nums]
            for f in to_remove:
                delete_file(Path(f[1]))
                files.remove(f[1])

        print('Send to server..')
        vk.main(files)
        for name in Path(_path).glob('*.jpeg'):
            delete_file(name)

def add_to_cloud(_path: str):
    subprocess.run(['rclone', 'move', _path, 'cloud-mailru:/autocam_imgs', '--include', '*.jpg'])

def main(_send_msg: bool = False, _cloud_only: bool = False, _cloud_sync: bool = False):
    global is_debug
    if is_debug:
        print('Run in debug mode.')
    else:
        print('Run in release mode.')
    try:
        if not cam_pwr_on():
            print('Error. Camera is power-on in manual mode.')
            exit(1)
        cam_push_btn()
        cam_disc_mount()
        img_path = '/media/DCIM/100MSDCF' if not is_debug else 'dbg_files'
        for _ in range(3):
            if Path(img_path).is_dir():
                print('SD CARD mounted.')
                break
            else:
                sleep(5)
        else:
            print('Error! SD CARD not mounted!')
        files_first_rename(img_path, _cloud_only)
        if not _cloud_only:
            add_path_to_vk(img_path, _send_msg)
        if _cloud_sync:
            add_to_cloud(img_path)
    finally:
        cam_disc_umount()
        cam_pwr_off()

        print('Complete.')

if __name__ == "__main__":
    if is_debug:
        send = input('Send files to server? (y/n): ') == 'y'
        main(send)
    else:
        params = sys.argv[1:]
        main(params.count('--send') > 0, params.count('--cloud') > 0, params.count('--sync') > 0)
