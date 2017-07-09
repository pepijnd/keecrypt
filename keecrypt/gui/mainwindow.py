import sys
import os

from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtWidgets import QMainWindow, QApplication


def get_file(filename):
    working_path = sys.modules[__name__].__file__
    working_dir = os.path.dirname(working_path)
    return f'{working_dir}/{filename}'


Ui_MainWindow, QtBaseClass = uic.loadUiType(get_file('mainwindow.ui'))

class KeecryptApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

def run():
    app = QApplication(sys.argv)
    window = KeecryptApp()
    window.show()
    sys.exit(app.exec_())
