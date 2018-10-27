from PyQt5 import QtWidgets, QtGui

from keecrypt.gui import ui


class MainWindow(ui.Mainwindow):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller

    def setupUi(self, mainwindow):
        super().setupUi(mainwindow)

        listview = self.centralWidget.findChild(QtWidgets.QColumnView, 'EntryListView')
        model = QtGui.QStandardItemModel()
        for item in ['apple', 'banana', 'citrus', 'django', 'lkj;slfk']:
            model.appendRow(QtGui.QStandardItem(item))
        listview.setModel(model)

        self.LoadButton.released.connect(self.controller.load_file)
        self.actionOpen.triggered.connect(self.controller.load_file)
