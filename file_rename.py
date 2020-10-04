import os
import datetime
import sys
import exifread
from util_file import *
from logd import *
from os_cfg import *


def get_shot_date(url):
    time_keys = ['Image DateTime', 'EXIF DateTimeOriginal']
    f = open(url, 'rb')
    tags = exifread.process_file(f)
    f.close()
    
    time = None
    for key in time_keys:
        if key not in tags:
            continue

        time = tags[key]
        break
    else:
        print('No exif info', url)

    return time

def convert_file_name(dir_path):
    file_list = os.listdir(dir_path)
    files_to_handle = UtilFile.create_file_meta_info(file_list)

    for file_name, file_type in files_to_handle:
        file_url = dir_path + OSConfig.get_dir_delimiter() + file_name
        time = None
        logd(LOG_LEVEL_NOTIFY, file_url)

        if file_type == 'jpg':
            time = get_shot_date(file_url)

        if not time:
            mtime = os.path.getmtime(file_url)
            time = datetime.datetime.fromtimestamp(mtime)

        if not time:
            continue

        time = str(time).replace(' ', '_')
        time = str(time).replace(':', '_')
        ori_name = dir_path + '\\' + file_name
        to_name = dir_path + '\\' + time + '.' + file_type

        try:
            cnt = 0
            while os.path.isfile(to_name):
                to_name = dir_path + '\\' + time + '_' + '{:032h}'.format(cnt) + '.' + file_type
                cnt += 1
            
            os.rename(ori_name, to_name)
        except:
            print('error = ', ori_name)
        logd(LOG_LEVEL_NOTIFY, '')


def convert_file_names(opts):
    try:
        dir_path = opts["path"]
    except KeyError:
        print('ERROR: directory is not designated')
        return None

    dirs = UtilFile.find_subdirs(dir_path)
    for url in dirs:
        convert_file_name(url)

