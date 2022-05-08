import os, shutil
### General file process function ###
def delete_if_exist(file_path:str):
    if os.path.exists(file_path):
        os.remove(file_path)

def is_compressed_file(file_path:str) -> bool:
    file_extension = file_path.split('.')[-1]
    return (file_extension == 'rar' or file_extension == 'zip')

### File path ###
# General path
TMP_TXT_PATH = ".\\.tmp\\novel.txt"
TMP_RAR_PATH = ".\\.tmp\\tmp.rar"
TMP_ZIP_PATH = ".\\.tmp\\tmp.zip"
TMP_DIRECTORY = ".\\.tmp"
OUTPUT_DIRECTORY = '.\\output'
def reset_TMP_DIRECTORY():
    if os.path.exists(TMP_DIRECTORY):
        shutil.rmtree(TMP_DIRECTORY)
    os.mkdir(TMP_DIRECTORY)

def get_OUTPUT_PATH(novel_name:str):
    output_file_name = novel_name + '.epub'
    return os.path.join(OUTPUT_DIRECTORY, output_file_name)
# Line bot path
LINE_BOT_TEMPLATE_FILE_PATH = "'./templates/template.json'"
GOOGLE_DRIVE_PATH = 'https://drive.google.com/file/d/{}/view?usp=sharing'

# databse path
DATABASE_DIRECTORY = "./.database"
SEARCH_RESULTS_JSON = "./.database/search_results.json"
DOWNLOAD_RESULTS_JSON = "./.database/download_results.json"

### Function variable ###
SOURCE_NAME = {'Zxcs':'知軒藏書',
                'Mijjxswco':'久久小說下載網',
                'Ijjxs':'愛久久小說下載網',
                'Qiuyewx':'平板電子書網',
                'Qinkan':'請看小說網',
                'Xsla':'八零電子書',
                }

### For convert ###
MAX_CHAPTER_NAME_LEN = 35
MIN_FIND_NOVELS = 15
MAX_FIND_NOVELS_IF_NOT_MATCH = 30

### Flag ###
USE_DATABASE = True


