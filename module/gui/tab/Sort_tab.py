from PyQt5.QtWidgets import QWidget
from ..layout import SortLayout
from ...data import SortDataStorage

class SortTab(QWidget):
    def __init__(self, mainwindow):
        super().__init__(mainwindow)

        self.datastorage = SortDataStorage()

        self._layout = SortLayout(mainwindow, self.datastorage)

        self.setLayout(self._layout)