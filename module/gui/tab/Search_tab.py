from PyQt5.QtWidgets import QWidget
from ..layout import SearchLayout

class SearchTab(QWidget):
    def __init__(self, mainwindow):
        super().__init__(mainwindow)
        self.setLayout(SearchLayout(mainwindow))