

## media file organizer


### Purpose

> with this tool, you can organize all of media files in your computer

&nbsp;

### Features

as of now, following features are supported with the tool

* file rename
  * rename JPG file based on its own Exif tag information
* find same (or similar) media file
  * it finds similar files in the given root directory
    * Now mp3 is supported but, simply can support other media types
* create/modify ID3 tag
  * create ID3 tag for mp3 file based on its own directory name and file name

&nbsp;

### Prerequisite

* mutagen
  * for ID3 tag
* exifread
  * for JPG Exif tag
  

&nbsp;

### Usage

> python main.py --cmd=convert --path=./

> python main.py --cmd=find_similar_files --path=./

> python main.py --cmd=set_mp3_meta --path=./


* argument types
  * cmd
    * operation to start
  * path
    * location to check

&nbsp;
