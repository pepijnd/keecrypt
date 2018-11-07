from PyQt5.QtWidgets import QFileDialog

from keecrypt.gui.controllers import App, MainController
from keecrypt.kdbx import KDBXReader


class KeecryptController:
    def __init__(self):
        self.app = App()
        self.root = self.app.root
        self.main_controller = MainController(self, self.root)
        self.app.setup(self.main_controller)
        self.app.run()

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
            reader = KDBXReader(filename=filename[0])
            file = reader.decrypt('test_file')
            entries = file.groups[0].entries
            self.main_controller.entries_model.set_entries(entries)
