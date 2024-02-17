from PyQt5.QtWidgets import QWidget
from ..layout import SortLayout

class SortTab(QWidget):
    def __init__(self, mainwindow):
        super().__init__(mainwindow)
        self.setLayout(SortLayout(mainwindow))