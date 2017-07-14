import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog

from keecrypt.gui.ui import Mainwindow


class MainController(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self._window = QMainWindow()
        self._ui = Mainwindow()
        self._ui.setupUi(self._window)
        self._window.show()

        self.init()

    def init(self):
        self._ui.LoadButton.released.connect(self.load_file)

    def load_file(self):
        dialog = QFileDialog()
        options = dialog.options()
        options |= dialog.DontUseNativeDialog
        filename = dialog.getOpenFileName(self._ui.centralWidget,
                                          '',
                                          'Open Keepass Database',
                                          'Keepass Database (*.kdbx)',
                                          'Keepass Database (*.kdbx)',
                                          options=options)
        print(filename)

    def run(self):
        return self.exec_()
