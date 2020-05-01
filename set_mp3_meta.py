from util_file import *

import mutagen
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

from os_cfg import *


def set_mp3_meta_in_a_dir(url):    
    print(url)
    file_list = os.listdir(url)
    files_to_handle = UtilFile.filter_files(file_list, ['mp3', 'mp2'])

    url_chunk = url.split(OSConfig.get_dir_delimiter())
    album = url_chunk[-1]
    title_chunk = album.split()
    artist = title_chunk[0].split('_')

    for file_name, file_ext in files_to_handle:
        file_url = url + OSConfig.get_dir_delimiter() + file_name
        file_chunk = file_url.split(OSConfig.get_dir_delimiter())
        title = file_chunk[-1].split('.')
        title.pop()
        title = ''.join(title)

        try:
            audio = EasyID3(file_url)
            continue
        except mutagen.id3.ID3NoHeaderError:
            audio = mutagen.File(file_url, easy=True)
            audio.add_tags()

        audio['title'] = title
        audio['artist'] = artist
        audio['album'] = album
        audio.save()


def set_mp3_meta(opts):    
    freq = collections.defaultdict(list)

    try:
        dir_path = opts["path"]
    except KeyError:
        print('ERROR: directory is not designated')
        return None

    dirs = UtilFile.find_subdirs(dir_path)
    dirs = set(dirs)
    for url in dirs:
        set_mp3_meta_in_a_dir(url)

