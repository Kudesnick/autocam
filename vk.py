# -*- coding: utf-8 -*-

import sys
import os
import argparse
import datetime
from getpass import getpass
import vk_api
from vk_api import VkUpload

user = input('input user name (mail):')
password = getpass('input password:')

owner_id = '-194929390' # club194929390

def auth_handler():
    key = input("Enter authentication code: ")
    remember_device = True

    return key, remember_device

vk_session = vk_api.VkApi(user, password, auth_handler = auth_handler)
#vk_session = vk_api.VkApi(user, password)
vk_session.auth()

vk = vk_session.get_api()

upload = VkUpload(vk_session)

photos = ['m.jpg', 'm1.jpg']
photo_list = upload.photo_wall(photos)
attachment = ','.join('photo{owner_id}_{id}'.format(**item) for item in photo_list)

result = vk.wall.post(
    owner_id = owner_id,
    from_group = 1,
    message = 'Text to post',
     attachments = attachment
    )

print(result)
print('Ok')
