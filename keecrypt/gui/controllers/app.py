import sys

from PyQt5.QtWidgets import QApplication, QMainWindow


class App(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.main_controller = None
        self.root = QMainWindow()

    def setup(self, controller):
        self.main_controller = controller
        self.main_controller.setup()

    def run(self):
        self.root.show()
        return self.exec_()
