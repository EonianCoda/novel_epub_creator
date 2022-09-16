import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from pyqt.UI import Ui_MainWindow
from PyQt5.QtWidgets import QFileDialog
# sys.path.append('../')
from utils.convert import simple2Trad, translate_and_convert, translate_and_convert_japanese
from utils.download import Downloader, Japanese_downloader
from utils.config import FINDS, JAPANESE_SOURCE_NAME, MAX_CHAPTER_NAME_LEN, TMP_DIRECTORY, TMP_RAR_PATH, TMP_TXT_PATH, SOURCE_NAME
from utils.config import reset_TMP_DIRECTORY, delete_if_exist, is_compressed_file, Setting
from utils.ebook import integrate_japanese_epubs
from utils.tkinter import clear_text_var, open_explorer, create_label_frame
DOWNLOADER = Downloader()

def end_with_epub(novel_name:str):
    if not novel_name.endswith(".epub"):
        novel_name += '.epub'
    return novel_name

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        # in python3, super(Class, self).xxx = super().xxx
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_control()
    def setup_control(self):
        self.ui.open_file_button.clicked.connect(self.open_file) 
        # self.ui..clicked.connect(self.open_folder)
        self.ui.start_trans.clicked.connect(self.start_trans)
        self.ui.start_search__online_button.clicked.connect(self.chinese_novel_download)
    def open_file(self):
        filename, filetype = QFileDialog.getOpenFileName(self,
                  "Open file",
                  "./")                 # start path
        print(filename, filetype)
        self.ui.file_path_text.setText(filename)
    def start_trans(self):
        #todo
        print("test")
    def chinese_novel_download(self):
        search_name = self.ui.search_online_text.text()
        result = DOWNLOADER.search(search_name)

        print(result)



