import sys

from PyQt5.QtWidgets import QApplication, QMainWindow


class App(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self._window = QMainWindow()
        self._ui = None

    def set_ui(self, mainwindow):
        self._ui = mainwindow
        self._ui.setupUi(self._window)
        self._window.show()

    def run(self):
        return self.exec_()
