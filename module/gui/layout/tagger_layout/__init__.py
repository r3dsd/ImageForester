from .top_layout import TopLayout
from .bottom_layout import BottomLayout
from .middle_layout import MiddleLayout

from PyQt5.QtWidgets import QVBoxLayout

class TaggerLayout(QVBoxLayout):
    def __init__(self, mainwindow):
        super().__init__()
        self.setContentsMargins(5, 5, 5, 5)

        top_layout = TopLayout(mainwindow)
        middle_layout = MiddleLayout(mainwindow)
        bottom_layout = BottomLayout(mainwindow)

        self.addLayout(top_layout)
        self.addLayout(middle_layout)
        self.addLayout(bottom_layout)