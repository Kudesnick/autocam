# -*- coding: utf-8 -*-

import sys
import os
import argparse
import datetime
from getpass import getpass
import vk_api
from vk_api import VkUpload

user = ''
password = ''
owner_id = ''

# user     = input('input user name (mail):')
# password = getpass('input password:')
# owner_id = '-194929390' # club194929390

with open('vk_config_auth', 'r') as f:
    user = f.readline().strip('\r\n \t')
    password = f.readline().strip('\r\n \t')
    owner_id = f.readline().strip('\r\n \t')

def auth_handler():
    key = input("Enter authentication code: ")
    remember_device = True

    return key, remember_device

def main(_files: list):
    vk_session = vk_api.VkApi(user, password, auth_handler = auth_handler)
    vk_session.auth()

    vk = vk_session.get_api()

    upload = VkUpload(vk_session)

    for i in range(0, len(_files), 9): # 10 - VK limit on post attachments

        photo_list = []
        for j in range(i, i + len(_files[i : i + 9])):
            photo_list.extend(upload.photo_wall(_files[j]))
        attachment = ','.join('photo{owner_id}_{id}'.format(**item) for item in photo_list)

        result = vk.wall.post(
            owner_id = owner_id,
            from_group = 1,
            message = '#timetolookatthesky',
            attachments = attachment
            )

        print(result)

if __name__ == "__main__":
    main(sys.argv[1:])
