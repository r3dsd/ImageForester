from PyQt5.QtWidgets import QWidget
from ..layout import TaggerLayout

class TaggerTab(QWidget):
    def __init__(self, mainwindow):
        super().__init__(mainwindow)
        self.setLayout(TaggerLayout(mainwindow))