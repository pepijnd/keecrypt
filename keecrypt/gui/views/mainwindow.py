from keecrypt.gui import ui


class MainWindow(ui.Mainwindow):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        self.root = self.controller.root

    def setupUi(self, *args,  **kwargs):
        super().setupUi(self.root)
