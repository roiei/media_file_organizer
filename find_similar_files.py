import collections
from util_file import *
from mutagen.mp3 import MP3
from os_cfg import *


class MediaFileInfo:
    def __init__(self, name = None, url = None, size = 0, ext = None, bit_rate = 0):
        self.name = name
        self.url = url
        self.size = size
        self.bit_rate = bit_rate
        self.ext = ext

    def __del__(self):
        pass


def find_similar_files_in_a_directory(url, freq):
    file_list = os.listdir(url)
    files_to_handle = UtilFile.filter_files(file_list, ['mp3', 'aac', 'flac', 'wma'])

    for file_name, file_ext in files_to_handle:
        file_url = url + OSConfig.get_dir_delimiter() + file_name

        file_stats = os.stat(file_url)
        size = file_stats.st_size//1024
        bitrate = 0

        freq[file_name] += MediaFileInfo(file_name, file_url, size, file_ext, bitrate),


def print_result(infos):
    for file_name, file_info in infos.items():
        if len(file_info) < 2:
            continue

        print(file_name)
        for info in file_info:
            print(f'url  = {info.url}')
            print(f'size = {info.size} kB')
        print()


def find_similar_files(opts):
    freq = collections.defaultdict(list)

    try:
        dir_path = opts["path"]
    except KeyError:
        print('ERROR: directory is not designated')
        return None

    dirs = UtilFile.find_subdirs(dir_path)
    dirs = set(dirs)
    for url in dirs:
        find_similar_files_in_a_directory(url, freq)

    print_result(freq)
