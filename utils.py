# -*- coding: utf8 -*-
import hashlib
import json
import os

from PIL import Image
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True


def mkdirs(file_path):
    if not os.path.exists(file_path):
        os.makedirs(file_path)


def get_file_name(file_path):
    path_split = file_path.split('/')
    length = len(path_split)
    if length == 0:
        return ''
    else:
        return path_split[length - 1]


def copy_file(src_path, src_name, dest_path, dest_name):
    src_image_path = os.path.join(src_path, src_name)
    dest_image_path = os.path.join(dest_path, dest_name)
    src_image_file = open(src_image_path, 'r+')
    dest_image_file = open(dest_image_path, 'w+')
    dest_image_file.write(src_image_file.read())


def image_md5_hash(im_file_path):
    im_file = Image.open(im_file_path)
    return hashlib.md5(im_file.tobytes()).hexdigest()


def write_obj_into_txt_in_json(result_file_path, obj):
    open(result_file_path, 'w').close()
    result_file = open(result_file_path, 'w')
    json_result = json.dumps(obj, skipkeys=True, indent=4, sort_keys=True)
    result_file.write(json_result)
    result_file.close()
    print("write obj into txt in json successful!")
