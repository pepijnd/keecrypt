from PyQt5 import QtCore
from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from .keepassfilemodel import KeepassFileModel


class TestModel(QSortFilterProxyModel):
    def __init__(self):
        super().__init__()
        self.model = KeepassFileModel(None)
        for i in range(100):
            row = [QStandardItem(f'row: {i}')]
            for j in range(5):
                row.append(QStandardItem(f'{j}'))
            self.model.appendRow(row)
        self.setSourceModel(self.model)


