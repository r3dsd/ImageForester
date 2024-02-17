from .top_layout import TopLayout
from .middle_layout import MiddleLayout
from .bottom_layout import BottomLayout

from PyQt5.QtWidgets import QVBoxLayout

from ....data import DataStorage

class SearchLayout(QVBoxLayout):
    def __init__(self, mainwindow):
        super().__init__()
        self.setContentsMargins(5, 5, 5, 5)

        self.datastorage = DataStorage("Search_Tab_DataStorage")

        top_layout = TopLayout(mainwindow, self.datastorage)
        middle_layout = MiddleLayout(mainwindow, self.datastorage)
        bottom_layout = BottomLayout(mainwindow, self.datastorage)

        self.addLayout(top_layout)
        self.addLayout(middle_layout)
        self.addLayout(bottom_layout)
