
from pydub import AudioSegment
from util_file import *
from logd import *
from os_cfg import *


def convert_file_name(url, opts):
    try:
        src = opts['src']
        dst = opts['dst']
    except Exception as e:
        print('Exception: src or dst is not designated')

    bitrate = '128k'    # 256k
    if 'bitrate' in opts:
        bitrate = opts['bitrate']

    print('bitrate = ', bitrate)

    file_list = os.listdir(url)
    files_to_handle = UtilFile.create_file_meta_info(file_list, [src])

    for file_name, file_type in files_to_handle:
        file_url = url + OSConfig.get_dir_delimiter() + file_name
        logd(LOG_LEVEL_NOTIFY, file_url)

        flac_audio = AudioSegment.from_file(file_url, file_type)
        file_url = file_url.split('.')
        file_url[-1] = dst
        print(file_url)
        flac_audio.export('.'.join(file_url), format=dst, bitrate=bitrate)


# from pydub.utils import mediainfo

# source_file = "/path/to/sound.mp3"

# original_bitrate = mediainfo(source_file)['bit_rate']
# sound = AudioSegment.from_mp3(source_file)

# sound.export("/path/to/output.mp3", format="mp3", bitrate=original_bitrate)



def convert_audio_format(opts):
    try:
        dir_path = opts["path"]
    except KeyError:
        print('ERROR: directory is not designated')
        return None

    dirs = UtilFile.find_subdirs(dir_path)
    for url in dirs:
        convert_file_name(url, opts)