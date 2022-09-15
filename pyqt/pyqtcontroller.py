import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from pyqt.UI import Ui_MainWindow
from PyQt5.QtWidgets import QFileDialog
# sys.path.append('../')
from utils.convert import simple2Trad, translate_and_convert

sys.path.append("..")
print(os.path.abspath('.')) # 用os.path模組來查看這個相對路經的起始目錄是否是我們所預期的

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
    def open_file(self):
        filename, filetype = QFileDialog.getOpenFileName(self,
                  "Open file",
                  "./")                 # start path
        print(filename, filetype)
        self.ui.file_path_text.setText(filename)
    def start_trans(self):
        #todo
        print("test")
        pass



