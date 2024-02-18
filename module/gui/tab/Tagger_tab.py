from PyQt5.QtWidgets import QWidget
from ..layout import TaggerLayout
from ...data import TaggerDataStorage

class TaggerTab(QWidget):
    def __init__(self, mainwindow):
        super().__init__(mainwindow)
        
        self._layout = TaggerLayout(mainwindow)

        self.setLayout(self._layout)