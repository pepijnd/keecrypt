from PyQt5 import QtWidgets

from keecrypt.gui.views import MainWindow
from keecrypt.gui.models import TestModel


class MainController():
    def __init__(self, controller, root):
        super().__init__()

        self.root = root
        self.controller = controller
        self.main_window = MainWindow(self)

    def setup(self):
        self.main_window.setupUi()
        table_view = self.root.findChild(QtWidgets.QTableView, 'entryTableView')
        table_view.setModel(TestModel())

        self.root.findChild(QtWidgets.QAction, 'actionOpen').triggered.connect(self.controller.load_file)
        self.root.findChild(QtWidgets.QAction, 'actionSave').triggered.connect(lambda: print('save action triggered'))
