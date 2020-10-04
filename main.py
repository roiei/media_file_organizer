#!/usr/bin/python3.6

import os
import sys
from help_msg import *
from option import *
from file_rename import *
from find_similar_files import *
from set_mp3_meta import *
from audio_converter import *


cmd_handler = {}
cmd_handler['help']   = print_help
cmd_handler['convert'] = convert_file_names
cmd_handler['find_similar_files'] = find_similar_files
cmd_handler['set_mp3_meta'] = set_mp3_meta
cmd_handler['convert_codec'] = convert_audio_format

sys_ver_info = tuple(list(sys.version_info)[:3])
if sys_ver_info < (3, 5, 0):
    sys.exit('Python version {}-{}-{}, is not supported. Use more than 3.5'.
        format(*sys_ver_info))

opts = get_opts(sys.argv)
opts['os'] = os.name

OSConfig.init()

try:
    cmd = opts["cmd"]
except KeyError:
    print('ERROR: wrong parameter')
    print_help(sys.argv)
    sys.exit()

if cmd not in cmd_handler:
    print('Not supported command {}'.format(cmd))
    print_help(sys.argv)
    sys.exit()

ret = cmd_handler[cmd](opts)
exit_code = 0
if False == ret:
    #print_help(sys.argv)
    exit_code = 1

sys.exit(exit_code)
