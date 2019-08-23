from keecrypt.gui import ui


class MainWindow(ui.Mainwindow):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        self.root = self.controller.root

        super().setupUi(self.root)
