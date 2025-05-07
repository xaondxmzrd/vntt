from PySide6.QtWidgets import QApplication
import window


class App(QApplication):
    def __init__(self, argv):
        super().__init__(argv)

        self.window = window.Window()
        self.window.resize(800, 600)
        self.window.show()
