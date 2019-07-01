from PyQt5 import QtWidgets

from keecrypt.gui.views import MainWindow
from keecrypt.gui.models import KeePassEntriesModel

from .database import DatabaseController


class MainController():
    def __init__(self, controller, root):
        super().__init__()

        self.root = root
        self.controller = controller
        self.main_window = MainWindow(self)
        self.entries_model = None

        self.database_controller = DatabaseController(self.controller, self.root)

    def setup(self):
        table_view = self.root.findChild(QtWidgets.QTableView, 'entryTableView')
        self.entries_model = KeePassEntriesModel()
        table_view.setModel(self.entries_model)

        self.root.findChild(QtWidgets.QAction, 'actionOpen').triggered.connect(
            self.database_controller.load_file)
        self.root.findChild(QtWidgets.QAction, 'actionSave').triggered.connect(
            lambda: print('save action triggered'))
