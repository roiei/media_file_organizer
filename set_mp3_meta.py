from util_file import *
import mutagen
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2
from mutagen.easyid3 import EasyID3
from os_cfg import *


def set_mp3_add_meta_info(file_url, title, artist, album):
    try:
        audio = EasyID3(file_url)
    except mutagen.id3.ID3NoHeaderError:
        audio = mutagen.File(file_url, easy=True)
        audio.add_tags()
    except mutagen.id3._util.ID3NoHeaderError:
        pass
    except mutagen.mp3.HeaderNotFoundError:
        pass
    else:
        audio['title'] = title
        audio['artist'] = artist
        audio['album'] = album

        try:
            audio.save()
        except mutagen.MutagenError:
            print(f'ERROR @ {file_url}')


def set_mp3_is_albumart_exist(url):
    audio = File(url)
    for k in audio.keys():
        if u'covr' in k or u'APIC' in k:
            return True

    return False


def set_mp3_add_albumart(file_url, img_info=None):
    if not img_info:
        return

    img_file, img_ext = img_info

    mime = 'image/jpg' if img_ext == 'jpg' else 'image/png'
    print(mime)
    audio = MP3(file_url , ID3=ID3)
    audio.tags.add(
        mutagen.id3.APIC(
            encoding=3,         # 3 is for utf-8
            mime=mime,          # image/jpeg or image/png
            type=3,             # 3 is for the cover image
            desc='Cover', 
            data=open(img_file, 'rb').read()
            )
        )
    audio.save()


def get_img_url(file_list, url):
    img_files = UtilFile.filter_files(file_list, ['jpg', 'png'])
    for file_name, ext in img_files:
        file_url = url + OSConfig.get_dir_delimiter() + file_name
        file_stats = os.stat(file_url)
        if file_stats.st_size:
            break
    else:
        return None

    return (url + OSConfig.get_dir_delimiter() + file_name, ext)


def set_mp3_meta_in_a_dir(url, update_albumart=False):    
    print(url)
    file_list = os.listdir(url)
    files_to_handle = UtilFile.filter_files(file_list, ['mp3', 'mp2'])
    if not files_to_handle:
        return

    if update_albumart:
        img_info = get_img_url(file_list, url)

    url_chunk = url.split(OSConfig.get_dir_delimiter())
    album = url_chunk[-1]
    title_chunk = album.split()
    artist = title_chunk[0].split('_')

    for file_name, file_ext in files_to_handle:
        file_url = url + OSConfig.get_dir_delimiter() + file_name
        file_stats = os.stat(file_url)
        if not file_stats.st_size:
            continue

        file_chunk = file_url.split(OSConfig.get_dir_delimiter())
        title = file_chunk[-1].split('.')
        title.pop()
        title = ''.join(title)

        set_mp3_add_meta_info(file_url, title, artist, album)

        if update_albumart:
            set_mp3_add_albumart(file_url, img_info)


def set_mp3_meta(opts):
    freq = collections.defaultdict(list)

    try:
        dir_path = opts["path"]
    except KeyError:
        print('ERROR: directory is not designated')
        return None

    update_albumart = False
    if 'albumart' in opts:
        update_albumart = opts['albumart']

    dirs = UtilFile.find_subdirs(dir_path)
    dirs = set(dirs)
    for url in dirs:
        set_mp3_meta_in_a_dir(url, update_albumart)

