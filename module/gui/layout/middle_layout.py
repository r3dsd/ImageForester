from PyQt5.QtWidgets import QBoxLayout, QListWidget, QLabel

from ..widgets.search_list import SearchList
from ..widgets.select_list import SelectList

class MiddleLayout(QBoxLayout):
    def __init__(self, mainwindow):
        super().__init__(QBoxLayout.LeftToRight)
        self.mainwindow = mainwindow
        self._initUI()

    def _initUI(self):
        self.searched_list = SearchList()
        self.addWidget(self.searched_list)

        self.selected_list = SelectList()
        self.addWidget(self.selected_list)

        self.searched_list.set(self.selected_list)
        self.selected_list.set(self.searched_list)

        self.image_viewer = QLabel()
        self.image_viewer.setMinimumSize(512, 512)
        self.addWidget(self.image_viewer)

        # 테스트용 더미데이터 삽입
        self.searched_list.update_search_list(["test1", "test2", "test3", "test4", "test5"])
        self.selected_list.update_select_list(["test11", "test22", "test33", "test44", "test55"])