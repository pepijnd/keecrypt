from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

from keecrypt.gui.views.dialogs import OpenDatabaseDialog


class DatabaseController:
    def __init__(self, controller, root):
        super().__init__()

        self.root = root
        self.controller = controller

        self.open_database_dialog = OpenDatabaseDialog(self.controller)

        self.open_database_dialog.root.findChild(
            QtWidgets.QAction, 'actionPasswordEdited').triggered.connect(
            lambda: self.open_database_dialog.root.findChild(
                QtWidgets.QCheckBox, 'passwordCheck').setChecked(True)
        )
        self.open_database_dialog.root.findChild(
            QtWidgets.QAction, 'actionKeyfileEdited').triggered.connect(
            lambda: self.open_database_dialog.root.findChild(
                QtWidgets.QCheckBox, 'keyfileCheck').setChecked(True)
        )

    def load_file(self):
        dialog = QFileDialog()
        options = dialog.options()
        options |= dialog.DontUseNativeDialog
        filename = dialog.getOpenFileName(self.root,
                                          '',
                                          'Open Keepass Database',
                                          'Keepass Database (*.kdbx)',
                                          'Keepass Database (*.kdbx)',
                                          options=options)
        if filename[0]:
            self.open_database_dialog.root.findChild(
                QtWidgets.QComboBox, 'databaseCombo').addItem(filename[0])

            self.open_database_dialog.show()

            # reader = KDBXReader(filename[0])
            # file = reader.decrypt('test_file')
            # entries = file.groups[0].entries
            # self.root.main_controller.entries_model.set_entries(entries)
