from PyQt5.QtWidgets import QBoxLayout, QListWidget, QLabel

class MiddleLayout(QBoxLayout):
    def __init__(self, mainwindow):
        super().__init__(QBoxLayout.LeftToRight)
        self.mainwindow = mainwindow
        self._initUI()

    def _initUI(self):
        self.searched_list = QListWidget()
        self.addWidget(self.searched_list)

        self.selected_list = QListWidget()
        self.addWidget(self.selected_list)

        self.image_viewer = QLabel()
        self.image_viewer.setMinimumSize(512, 512)
        self.addWidget(self.image_viewer)