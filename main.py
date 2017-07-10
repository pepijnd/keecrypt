from tests.utils import get_file
from keecrypt.kdbx.reader import KDBXReader

from PyQt5 import QtWidgets
from keecrypt.gui.ui import Mainwindow


def main():
    with open(get_file('valid_aes_gzip.kdbx'), 'rb') as f:
        KDBXReader(fileobj=f).decrypt('test_file')


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    KeecryptWindow = QtWidgets.QMainWindow()
    ui = Mainwindow()
    ui.setupUi(KeecryptWindow)
    KeecryptWindow.show()
    sys.exit(app.exec_())
