from PyQt5.QtWidgets import QWidget
from ..layout import SearchLayout

from ...data import SearchDataStorage

class SearchTab(QWidget):
    def __init__(self, mainwindow):
        super().__init__(mainwindow)

        self.datastorage = SearchDataStorage()
        
        self._layout = SearchLayout(mainwindow, self.datastorage)

        self.setLayout(self._layout)