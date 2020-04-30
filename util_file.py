
import os
import collections
import sys
from enum import Enum


class FileType(Enum):
    CPP_HEADER = 1
    CPP_IMPL = 2
    JAVASCRIPT = 3
    PYTHON = 4


class UtilFile:
    def __init__(self):
        pass

    def __del__(self):
        pass

    file_types = collections.defaultdict(None)

    @staticmethod
    def find_subdirs(url):
        q = [(url, 0)]
        dirs = [url]

        while q:
            url, depth = q.pop(0)
            try:
                dir_names = os.listdir(url)
            except FileNotFoundError:
                print('ERROR: no such a url = {}'.format(url))
                continue

            for dir_name in dir_names:
                full_url = os.path.join(url, dir_name)
                if os.path.isdir(full_url):
                    q += (full_url, depth + 1),
                    dirs += full_url,

        return dirs

    @staticmethod
    def init_file_type():
        UtilFile.file_types['h'] = FileType.CPP_HEADER
        UtilFile.file_types['hpp'] = FileType.CPP_HEADER
        UtilFile.file_types['hxx'] = FileType.CPP_HEADER
        UtilFile.file_types['cpp'] = FileType.CPP_IMPL
        UtilFile.file_types['cxx'] = FileType.CPP_IMPL
        UtilFile.file_types['c'] = FileType.CPP_IMPL

    @staticmethod
    def get_file_type(extension):
        return UtilFile.file_types[extension]

    @staticmethod
    def get_all_files(url, extension_filter):
        """
        find all the files to check
        """
        res = []
        try:
            file_list = os.listdir(url)
        except FileNotFoundError:
            print('ERROR: no such a url = {}'.format(url))
            return

        for file in file_list:
            extension = file.split('.')[-1]
            if extension not in extension_filter:
                continue

            full_filename = os.path.join(url, file)
            res += (full_filename, UtilFile.get_file_type(extension)),

        return res

    @staticmethod
    def get_files(url, is_resursive, extension_filter = ['h', 'hpp', 'cpp', 'c']):
        """
        OUT
            {"dir1" : [("file1", type1), ("file2", type2)], "dir2" : ...}
        """
        # get all the sub dires
        dirs = UtilFile.find_subdirs(url) if is_resursive else [url]
        files = collections.defaultdict(list)

        for directory in dirs:
            ret = UtilFile.get_all_files(directory, extension_filter)
            if not ret:
                continue
            files[directory] += ret

        return files

    @staticmethod
    def filter_files(file_list, ext_to_handle = ['h', 'hpp']):
        files_to_handle = []
        for file in file_list:
            ext = file.split('.')[-1].lower()
            if ext not in ext_to_handle:
                continue

            files_to_handle += (file, ext),

        return files_to_handle

