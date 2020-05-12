# -*- coding: utf-8 -*-

import sys
from time import sleep
from datetime import datetime
import subprocess

class img_file:
    __name: str
    __date: datetime

    def __init__(self, _name: str):
        self.__name = _name
        self.__date = datetime.fromtimestamp(int(_name[0:_name.find('_')], 0))

    def __repr__(self):
        return '"{}" [{}]'.format(self.__name, self.__date)
    def __str__(self):
        return '"{}" [{}]'.format(self.__name, self.__date)
    
    def name(self):
        return self.__name

    def date(self):
        return str(self.__date)

    def timestamp(self):
        return self.__date.timestamp()

def main():
    print('Verifying cloud files..')
    p = subprocess.Popen(['rclone', 'cat', 'cloud-mailru:/autocam_imgs/ignore.txt'], stdout = subprocess.PIPE)
    ignore_rules = p.stdout.read().decode('utf-8').splitlines()

    p = subprocess.Popen(['rclone', 'lsf', 'cloud-mailru:/autocam_imgs', '--include', '*.jpg'], stdout = subprocess.PIPE)
    f_list = list(map(lambda i: img_file(i), p.stdout.read().decode('utf-8').splitlines()))

    print('Veryfying interval between {} and {}..'.format(f_list[0].date(), f_list[-1].date()))
    warnings = 0
    for k, _ in enumerate(f_list):
        if k == 0: continue
        if ignore_rules.count(f_list[k-1].name() + ' >') != 0: continue
        if ignore_rules.count(f_list[k].name() + ' <') != 0: continue

        interval = int(f_list[k].timestamp() - f_list[k-1].timestamp())
        if abs(interval - (5 * 60)) < 10: continue
        
        print('Warning! Bad interval: {} seconds between {} and {}.'.format(
            interval, f_list[k-1], f_list[k]))
        warnings += 1

    print('Complete. {} warnings found.'.format(warnings))

if __name__ == "__main__":
    main()
