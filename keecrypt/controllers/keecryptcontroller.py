from keecrypt.gui.controllers import App, MainController


class KeecryptController:
    def __init__(self):
        self.app = App()
        self.root = self.app.root
        self.main_controller = MainController(self, self.root)
        self.app.setup(self.main_controller)
        self.app.run()

