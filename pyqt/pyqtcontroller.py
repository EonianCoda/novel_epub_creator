from PyQt5 import QtWidgets, QtGui, QtCore
from UI import Ui_MainWindow
from PyQt5.QtWidgets import QFileDialog

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        # in python3, super(Class, self).xxx = super().xxx
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_control()
    def setup_control(self):
        self.ui.pushButton.clicked.connect(self.open_file) 
        # self.ui.folder_button.clicked.connect(self.open_folder)

    def open_file(self):
        filename, filetype = QFileDialog.getOpenFileName(self,
                  "Open file",
                  "./")                 # start path
        print(filename, filetype)
        self.ui.textBrowser.setText(filename)




