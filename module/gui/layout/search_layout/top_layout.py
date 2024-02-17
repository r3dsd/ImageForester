from PyQt5.QtWidgets import QHBoxLayout

from ...widgets.search_bar import SearchBar
from ...guisignalmanager import GUISearchSignalManager

class TopLayout(QHBoxLayout):
    def __init__(self, mainwindow, datastorage):
        super().__init__()
        self.mainwindow = mainwindow
        self.datastorage = datastorage
        self._initUI()

    def _initUI(self):
        self.search_bar = SearchBar(self.datastorage)
        self.search_bar.on_search_completed.connect(self.on_search_completed)
        self.addWidget(self.search_bar)

    def on_search_completed(self, result, count):
        GUISearchSignalManager().on_search_completed.emit(result, count)