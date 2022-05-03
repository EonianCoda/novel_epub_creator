import os, shutil
### File path ###
TMP_TXT_PATH = ".\\.tmp\\novel.txt"
TMP_RAR_PATH = "tmp.rar"
TMP_DIRECTORY = ".\\.tmp"
OUTPUT_DIRECTORY = '.\\output'

def reset_TMP_DIRECTORY():
    if os.path.exists(TMP_DIRECTORY):
        shutil.rmtree(TMP_DIRECTORY)
    os.mkdir(TMP_DIRECTORY)

def get_OUTPUT_PATH(novel_name:str):
    output_file_name = novel_name + '.epub'
    return os.path.join(OUTPUT_DIRECTORY, output_file_name)
# For App
LINE_BOT_TEMPLATE_FILE_PATH = "'./templates/template.json'"

### For convert ###
MAX_CHAPTER_NAME_LEN = 35


### Databse variable ###
SEARCH_RESULTS_PICKLE = "./database/search_results.pickle"
DOWNLOAD_RESULTS_PICKLE = "./database/download_results.pickle"
SEARCH_RESULTS_CSV = "./database/search_results.csv"
DOWNLOAD_RESULTS_CSV = "./database/download_results.csv"
