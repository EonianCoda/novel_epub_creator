import os 
import shutil
import configparser

SETTING_FILE = "setting.ini"
DEFAULT_OUTPUT_DIRECTORY = '.\\output'
DEFAULT_INPUT_DIRECTORY = '.\\'


class Setting(object):
    def __init__(self):
        self.cf = configparser.ConfigParser() 
        if os.path.exists(SETTING_FILE):
            self.cf.read(SETTING_FILE)
            if 'Current_setting' not in self.cf.sections():
                self.cf['Cur_setting'] = {'used_setting':"Default",}
        else:
            self.cf['Cur_setting'] = {'used_setting':"Default",}
            self.cf['Default'] = {'output_dir':DEFAULT_OUTPUT_DIRECTORY,
                                'input_dir':DEFAULT_INPUT_DIRECTORY}
        self.setting = self.cf[self.cf['Cur_setting']['used_setting']]
        self.update_cfg()

    def __getitem__(self, key):
        return self.setting[key]

    def get_output_path(self, novel_name:str):
        if not novel_name.endswith('.epub'):
            novel_name += '.epub'
        return os.path.join(self['output_dir'], novel_name)

    def update_cfg(self):
        with open(SETTING_FILE, 'w') as f:
            self.cf.write(f)

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
def reset_TMP_DIRECTORY():
    if os.path.exists(TMP_DIRECTORY):
        shutil.rmtree(TMP_DIRECTORY)
    os.mkdir(TMP_DIRECTORY)

# def get_OUTPUT_PATH(novel_name:str):
#     output_file_name = novel_name + '.epub'
#     return os.path.join(DEFAULT_OUTPUT_DIRECTORY, output_file_name)
# Line bot path
LINE_BOT_TEMPLATE_FILE_PATH = "'./templates/template.json'"
# Google drive path
GOOGLE_DRIVE_PATH = 'https://drive.google.com/file/d/{}/view?usp=sharing'

# databse path
DATABASE_DIRECTORY = "./.database"
DATABASE_VERSION = "./.database/version"
SEARCH_RESULTS_JSON = "./.database/search_results.json"
DOWNLOAD_RESULTS_JSON = "./.database/download_results.json"

### Function variable ###
SOURCE_NAME = {'Zxcs':'知軒藏書',
                'Mijjxswco':'久久小說網',
                'Ijjxs':'愛久久小說網',
                'Qiuyewx':'平板電子書',
                'Qinkan':'請看小說網',
                'Xsla':'八零電子書',
                }

### For convert ###
MAX_CHAPTER_NAME_LEN = 35
MIN_FIND_NOVELS = 15
MAX_FIND_NOVELS_IF_NOT_MATCH = 30
FINDS = [u'第(\d)+[章卷話]',
        '第[一二三四五六七八九十千百零兩]+[章卷話]',
        '序章']

### Flag ###
USE_DATABASE = True


