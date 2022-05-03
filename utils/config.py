import os, shutil
# File path
TMP_TXT_PATH = ".\\.tmp\\novel.txt"
TMP_RAR_PATH = "tmp.rar"
TMP_DIRECTORY = ".\\.tmp"
OUTPUT_DIRECTORY = '.\\output'

def reset_TMP_DIRECTORY():
    if os.path.exists(TMP_DIRECTORY):
        shutil.rmtree(TMP_DIRECTORY)
    os.mkdir(TMP_DIRECTORY)
# For convert
MAX_CHAPTER_NAME_LEN = 30
# Databse variable
SEARCH_RESULTS_PICKLE = "./database/search_results.pickle"
DOWNLOAD_RESULTS_PICKLE = "./database/download_results.pickle"
SEARCH_RESULTS_CSV = "./database/search_results.csv"
DOWNLOAD_RESULTS_CSV = "./database/download_results.csv"
