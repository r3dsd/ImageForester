from .top_layout import TopLayout
from .bottom_layout import BottomLayout
from .middle_layout import MiddleLayout

from PyQt5.QtWidgets import QVBoxLayout

from ....data import DataStorage

class TaggerLayout(QVBoxLayout):
    def __init__(self, mainwindow):
        super().__init__()
        self.setContentsMargins(5, 5, 5, 5)

        self.datastorage = DataStorage("Tagger Data Storage")

        top_layout = TopLayout(mainwindow, self.datastorage)
        middle_layout = MiddleLayout(mainwindow, self.datastorage)
        bottom_layout = BottomLayout(mainwindow, self.datastorage)

        self.addLayout(top_layout)
        self.addLayout(middle_layout)
        self.addLayout(bottom_layout)