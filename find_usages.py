# -*- coding: utf8 -*-
import os

from detector import detect_duplicated_images
from utils import write_obj_into_txt_in_json


class DuplicatedImageUsage(object):
    def __init__(self, duplicated_image_array):
        self._duplicated_image_array = duplicated_image_array
        self._duplicated_image_file = []

    @property
    def duplicated_image_array(self):
        return self._duplicated_image_array

    @property
    def duplicated_image_file(self):
        return self._duplicated_image_file

    def set_duplicate_image_file(self, image_file_list):
        self._duplicated_image_file.append(image_file_list)

    def get_desc(self):
        return {'duplicated_image': self._duplicated_image_array,
                'duplicated_image_usages': self._duplicated_image_file}


def find_usage():
    duplicated_images = detect_duplicated_images(True)

    print('please input src\'s path【single ‘:q‘ would exit】:')
    src_path_list = []
    for line in iter(raw_input, ':q'):
        src_path_list.append(line)

    if len(src_path_list) == 0:
        print('src\'s path is nothing and exit.')
        return

    duplicated_images_usages_list = []
    for single_duplicated_image in duplicated_images:
        duplicated_image_usages = DuplicatedImageUsage(single_duplicated_image)
        for image in single_duplicated_image:
            image = str(image).replace('.9.png', '')
            image = str(image).replace('.png', '')
            image = str(image).replace('.jpg', '')
            image = str(image).replace('.jpeg', '')
            image = str(image).replace('.webp', '')
            duplicated_image_file = []
            for src_path_index in range(0, len(src_path_list), 1):
                src_path = src_path_list[src_path_index]
                for root, dirs, files in os.walk(src_path):
                    for file_name in files:
                        if ('.java' in file_name or '.xml' in file_name) \
                                and not file_name.endswith('R.java') \
                                and not file_name.endswith('R2.java'):
                            cur_file = open(os.path.join(root, file_name), 'r')
                            line_number = 1
                            for line in cur_file:
                                if '/' + image in line or '.' + image in line:
                                    duplicated_image_file.append('file name is ===== ' + cur_file.name +
                                                                 ' and the line_number is ===== ' + str(line_number))
                                line_number += 1
            duplicated_image_usages.set_duplicate_image_file(duplicated_image_file)
        duplicated_images_usages_list.append(duplicated_image_usages)

    all_duplicated_image_usage = []
    for usages in duplicated_images_usages_list:
        all_duplicated_image_usage.append(usages.get_desc())

    result_file_path = os.path.join(os.getcwd(), 'duplicated_images_usages.txt')
    write_obj_into_txt_in_json(result_file_path, all_duplicated_image_usage)


if __name__ == '__main__':
    find_usage()
