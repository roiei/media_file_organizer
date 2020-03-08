import os
import datetime
import sys
import exifread


LOG_LEVEL_ERROR = 3
LOG_LEVEL_WARN = 2
LOG_LEVEL_NOTIFY = 1
LOG_LEVEL_IGNORE = 0

LOG_LEVEL_ENABLED = LOG_LEVEL_WARN


if 1 >= len(sys.argv):
    print('Not enough parameter: give path to process')
    sys.exit()


dir_path = sys.argv[1]

ext_to_handle = ['jpg', 'png', 'mov', 'avi', 'mkv', 'mp4']


def find_subdir(url):
    q = [(url, 0)]
    dirs = [url]

    while q:
        url, depth = q.pop(0)
        dir_names = os.listdir(url)
        for dir_name in dir_names:
            full_url = os.path.join(url, dir_name)
            if os.path.isdir(full_url):
                q += (full_url, depth + 1),
                dirs += full_url,

    return dirs


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


def logd(opt, log):
    if opt >= LOG_LEVEL_ENABLED:
        print(log)


def create_file_meta_info(file_list):
    files_to_handle = []
    for file in file_list:
        ext = file.split('.')[-1].lower()
        if ext not in ext_to_handle:
            continue

        files_to_handle += (file, ext),

    return files_to_handle


def convert_file_name(dir_path):
    file_list = os.listdir(dir_path)
    files_to_handle = create_file_meta_info(file_list)

    for file_name, file_type in files_to_handle:
        file_url = dir_path + '\\' + file_name
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



dirs = find_subdir(dir_path)
for url in dirs:
    convert_file_name(url)

