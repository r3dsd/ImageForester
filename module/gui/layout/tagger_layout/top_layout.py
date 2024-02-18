from PyQt5.QtWidgets import QHBoxLayout
class TopLayout(QHBoxLayout):
    def __init__(self, mainwindow):
        super().__init__()
        self.mainwindow = mainwindow
        self._initUI()

    def _initUI(self):
        pass