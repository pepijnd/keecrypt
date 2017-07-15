from keecrypt.gui import ui


class MainWindow(ui.Mainwindow):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller

    def setupUi(self, mainwindow):
        super().setupUi(mainwindow)

        self.LoadButton.released.connect(self.controller.load_file)
        self.actionOpen.triggered.connect(self.controller.load_file)
