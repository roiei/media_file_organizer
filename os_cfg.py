import os
from enum import Enum


class OSType(Enum):
    WINDOWS = 1
    LINUX = 2


class OSConfig:
    cfgs = {}

    def __init__(self):
        pass

    def __del__(self):
        pass

    @staticmethod
    def init():
        if os.name == 'nt':
            OSConfig.init_as_windows()
        else:
            OSConfig.init_as_linux()

    @staticmethod
    def init_as_windows():
        OSConfig.cfgs['os'] = OSType.WINDOWS
        OSConfig.cfgs['dir_delimiter'] = '\\'

    @staticmethod
    def init_as_linux():
        OSConfig.cfgs['os'] = OSType.LINUX
        OSConfig.cfgs['dir_delimiter'] = '/'

    @staticmethod
    def get_dir_delimiter():
        return OSConfig.cfgs['dir_delimiter']
