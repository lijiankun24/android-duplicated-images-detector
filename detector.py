# -*- coding: utf8 -*-
import os
import zipfile

from utils import copy_file
from utils import get_file_name
from utils import image_md5_hash
from utils import mkdirs
from utils import write_obj_into_txt_in_json


def detect_duplicated_images(write_into_txt=False):
    all_images_path = os.path.join(os.getcwd(), 'all_images')
    duplicated_images_path = os.path.join(os.getcwd(), 'duplicated_images')
    mkdirs(all_images_path)
    mkdirs(duplicated_images_path)

    apk_path = str(raw_input('please input your apk\'s path: '))
    if apk_path.endswith('.apk'):
        # 将源 apk 文件复制到当前目录下
        apk_name = get_file_name(apk_path)
        apk_parent_path = apk_path.replace(apk_name, '')
        copy_file(apk_parent_path, apk_name, os.getcwd(), apk_name)

        # 将当前目录下的 .apk 文件修改为 .zip 文件
        apk_name_split = os.path.splitext(apk_name)
        zip_name = apk_name_split[0] + '.zip'
        zip_path = os.path.join(os.getcwd(), zip_name)
        dest_apk_path = os.path.join(os.getcwd(), apk_name)
        os.rename(dest_apk_path, zip_path)

        # image_total_size 计算所有图片的大小
        image_total_size = 0

        # 通过 zipfile 生成 zip 文件对象
        zip_file = zipfile.ZipFile(zip_path, 'r')
        # 将 apk 中所有的图片写入到当前目录下的 all_images 文件中
        for zip_file_item in zip_file.namelist():
            zip_file_path = str(zip_file_item)
            if zip_file_path.endswith('.png') \
                    or zip_file_path.endswith('.jpg') \
                    or zip_file_path.endswith('.jpeg') \
                    or zip_file_path.endswith('.webp'):
                image_name = get_file_name(zip_file_path)
                new_image_path = os.path.join(all_images_path, image_name)
                f = open(new_image_path, 'w+')
                f.write(zip_file.read(zip_file_path))

                # 下面是累加所有图片的大小
                file_path = unicode(new_image_path, 'utf8')
                image_total_size += (os.path.getsize(file_path) / float(1024))

        print('all images size is %.3fkb.' % image_total_size)

        all_images_file_list = os.listdir(all_images_path)
        all_images_length = len(all_images_file_list)
        all_images_index = 0
        all_images_md5_list = [''] * all_images_length  # 每个 image 对应的 md5 值
        # 对当前目录 all_images 文件中的所有图片生成对应的 md5_hash 放到 image_md5_list 中，一一对应
        for all_image_item_name in all_images_file_list:
            all_image_item_path = os.path.join(all_images_path, all_image_item_name)
            all_images_md5_list[all_images_index] = image_md5_hash(all_image_item_path)
            all_images_index += 1

        # duplicated_images_total_size 计算所有重复图片的大小
        duplicated_images_total_size = 0
        all_images_is_matched_list = [False] * all_images_length  # 是否已经被匹配
        duplicated_images_result = []
        all_images_index = 0
        # 嵌套 for 循环，两两对比所有的 image_md5
        for origin_image_name in all_images_file_list:
            if not all_images_is_matched_list[all_images_index]:
                origin_image_path = os.path.join(all_images_path, origin_image_name)
                origin_image_md5 = all_images_md5_list[all_images_index]
                first_find_similar_image = False
                count = 0
                cur_duplicate_array = []
                for target_image_name in all_images_file_list:
                    if not all_images_is_matched_list[count]:
                        target_image_path = os.path.join(all_images_path, target_image_name)
                        target_image_md5 = all_images_md5_list[count]
                        # 若两个 image 的 path 不同 and md5 相等，则判定为名称不同但是内容相同的图片
                        if not origin_image_path == target_image_path and origin_image_md5 == target_image_md5:
                            duplicated_image_folder = os.path.join(duplicated_images_path, origin_image_name)
                            # 第一次查找到时，需要创建文件夹并将 origin_image copy 到文件夹中
                            if not first_find_similar_image:
                                first_find_similar_image = True
                                mkdirs(duplicated_image_folder)
                                cur_duplicate_array.append(origin_image_name)
                                copy_file(all_images_path, origin_image_name,
                                          duplicated_image_folder, origin_image_name)
                                origin_file_path = unicode(origin_image_path, 'utf8')
                                duplicated_images_total_size += (os.path.getsize(origin_file_path) / float(1024))

                            copy_file(all_images_path, target_image_name, duplicated_image_folder, target_image_name)
                            duplicated_images_total_size += (os.path.getsize(target_image_path) / float(1024))

                            cur_duplicate_array.append(target_image_name)
                            all_images_is_matched_list[count] = True
                    count += 1
                if not len(cur_duplicate_array) == 0:
                    duplicated_images_result.append(cur_duplicate_array)
            all_images_index += 1
        print('all duplicated images size is %.3fkb.' % duplicated_images_total_size)
        print('there ara %d pairs duplicated images.' % len(duplicated_images_result))
        if write_into_txt and not len(duplicated_images_result) == 0:
            write_obj_into_txt_in_json(os.path.join(os.getcwd(), 'duplicated_images.txt'), duplicated_images_result)
        return duplicated_images_result
    else:
        print('Your apk\'s path %s is not correct.' % apk_path)
