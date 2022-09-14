from PyQt5 import QtWidgets

from pyqtcontroller import MainWindow
import sys
sys.path.append('../')
from utils.convert import simple2Trad, translate_and_convert

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
