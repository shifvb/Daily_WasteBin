# /usr/bin/env python3
# -*- coding: utf-8 -*-
from hashlib import md5
import os
import sys
import logging

version = (0, 2)
target_ext = ('.jpg', '.png', '.gif')
logger = None
log_file_name = "hash_photos.log"


def main():
    if _check_python_version() is False:  # check python version
        raise SystemExit("python 3.2+ required!")

    path = _get_folder_path_from_user()  # get folder path from user input
    if not os.path.isdir(path):
        raise SystemExit('不是文件夹的说...')

    global logger
    logger = _get_logger(path)  # get logger from path
    file_list = _get_abs_filename_from_path_str(path)  # get photos from path
    logger.info('共找到{}个文件...'.format(len(file_list)))

    success_counter = 0  # rename result counter
    for file_name in file_list:
        new_file_name = os.path.join(path, _get_hex_digest_from_file(md5, file_name) + os.path.splitext(file_name)[-1])
        if _rename_file(file_name, new_file_name):  # rename file
            success_counter += 1

    logger.info('成功：{}, 忽略：{}'.format(success_counter, len(file_list) - success_counter))
    print("操作已记录到{}".format("hash_photos.log"))


def _check_python_version():
    return sys.version_info[0] == 3 and sys.version_info[1] >= 2


def _get_folder_path_from_user():
    print('会把你某文件夹里的' + '/'.join([x[1:].upper() for x in target_ext]) + '文件按md5值重命名')
    path = input('请输入文件夹路径(当前文件夹请按[Enter](回车键):\n')
    return os.path.abspath('.' if path == '' else path)


def _get_abs_filename_from_path_str(path: str):
    return [os.path.join(path, x) for x in os.listdir(path) if x.lower()[-4:] in target_ext]


def _get_hex_digest_from_file(hash_algorithm, file: str):
    m = hash_algorithm()
    with open(file, 'rb') as f:
        for data in f:
            m.update(data)
    return m.hexdigest()


def _rename_file(old: str, new: str) -> bool:
    try:
        if old == new:
            raise Exception("新文件名与原文件名相同！")
        os.rename(old, new)
        logger.info('重命名文件 ' + old + ' -> ' + new)
        return True
    except Exception as e:
        logger.warning('重命名文件 ' + old + ' -> ' + new + ' 失败! 原因:{}'.format(str(e)))
        return False


def _get_logger(log_path: str):
    global logger
    logger = logging.getLogger('my_loggger')
    logger.setLevel(logging.INFO)
    log_format = logging.Formatter(fmt="%(asctime)s %(levelname)s %(message)s", datefmt='%y-%m-%d %H:%M:%S')
    file_handler = logging.FileHandler(filename=os.path.join(log_path, log_file_name), mode='a', encoding='utf-8')
    file_handler.setFormatter(log_format)
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setFormatter(log_format)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


if __name__ == '__main__':
    try:
        main()
    except SystemExit as e:
        print(e)
    finally:
        input("press [Enter] to exit...")
