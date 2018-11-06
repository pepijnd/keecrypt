from PyQt5.QtGui import QStandardItemModel, QStandardItem


class KeepassFileModel(QStandardItemModel):
    def __init__(self, keepassfile, *__args):
        super().__init__(*__args)
        self.keepassfile = keepassfile
