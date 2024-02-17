from PyQt5.QtWidgets import QHBoxLayout
class TopLayout(QHBoxLayout):
    def __init__(self, mainwindow, datastorage):
        super().__init__()
        self.mainwindow = mainwindow
        self.datastorage = datastorage
        self._initUI()

    def _initUI(self):
        pass