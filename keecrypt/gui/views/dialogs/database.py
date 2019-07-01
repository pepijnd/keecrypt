from PyQt5.QtWidgets import QDialog

from keecrypt.gui import ui


class OpenDatabaseDialog(ui.dialogs.OpenDatabaseDialog):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        self.root = self.controller.root

        self.dialog = QDialog(self.root)
        super().setupUi(self.dialog)

    def show(self):
        self.dialog.show()
