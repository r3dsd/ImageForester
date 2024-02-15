from PyQt5.QtWidgets import QBoxLayout

from ..widgets.search_bar import SearchBar

class TopLayout(QBoxLayout):
    def __init__(self, mainwindow):
        super().__init__(QBoxLayout.LeftToRight)
        self.mainwindow = mainwindow
        self._initUI()

    def _initUI(self):
        self.search_bar = SearchBar()
        self.addWidget(self.search_bar)