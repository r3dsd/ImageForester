from PyQt5.QtWidgets import QVBoxLayout

class BottomLayout(QVBoxLayout):
    def __init__(self, mainwindow):
        super().__init__()
        self._mainwindow = mainwindow

        self._initUI()
        self._initsignal()

    def _initUI(self):
        pass

    def _initsignal(self):
        pass