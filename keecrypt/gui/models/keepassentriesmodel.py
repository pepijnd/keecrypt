from PyQt5 import QtCore
from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class KeePassEntriesModel(QSortFilterProxyModel):
    def __init__(self):
        super().__init__()
        self.columns = ['Title', 'UserName', 'Password', 'URL']
        self.model = QStandardItemModel()
        self.entries = []
        self.setSourceModel(self.model)

    def set_entries(self, entries):
        self.entries = entries
        self.model.clear()
        for entry in self.entries:
            row = []
            for col in self.columns:
                try:
                    row.append(QStandardItem(entry[col]))
                except KeyError:
                    row.append(QStandardItem(''))
            self.model.appendRow(row)

