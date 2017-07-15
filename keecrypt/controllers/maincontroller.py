from PyQt5.QtWidgets import QFileDialog

from keecrypt.gui.controllers import App, MainWindow


class MainController:
    def __init__(self):
        self.app = App()
        self.main_window = MainWindow(self)
        self.app.set_ui(self.main_window)
        self.app.run()

    def load_file(self):
        dialog = QFileDialog()
        options = dialog.options()
        options |= dialog.DontUseNativeDialog
        filename = dialog.getOpenFileName(self.main_window.centralWidget,
                                          '',
                                          'Open Keepass Database',
                                          'Keepass Database (*.kdbx)',
                                          'Keepass Database (*.kdbx)',
                                          options=options)
        print(filename)
