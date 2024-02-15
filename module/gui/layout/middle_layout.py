import os
from PyQt5.QtWidgets import QBoxLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt

from ..widgets.search_list import SearchList
from ..widgets.select_list import SelectList
from ...data.imagefiledata import ImageFileData
from ..widgets.image_viewer import ImageViewer

from ..guisignalmanager import GUISignalManager
from PyQt5.QtGui import QPixmap

class MiddleLayout(QBoxLayout):
    def __init__(self, mainwindow):
        super().__init__(QBoxLayout.LeftToRight)
        self.mainwindow = mainwindow
        self._initUI()

    def _initUI(self):
        self.searched_list = SearchList(self.mainwindow)
        self.searched_list.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.addWidget(self.searched_list)

        self.selected_list = SelectList(self.mainwindow)
        self.selected_list.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.addWidget(self.selected_list)

        # Reference to each other for moving items, and focus
        self.searched_list.set(self.selected_list)
        self.selected_list.set(self.searched_list)

        self.image_viewer = ImageViewer(self.mainwindow)
        self.addWidget(self.image_viewer)

        GUISignalManager().on_item_selection_updated.connect(self._on_item_selection_updated)
        GUISignalManager().on_search_list_send2trash.connect(self.image_viewer.clear)
        GUISignalManager().on_select_list_save.connect(self._on_select_list_save)

    def _on_item_selection_updated(self, image_data: ImageFileData):
        self.image_viewer.update_image(image_data.file_path)

    def _on_select_list_save(self, mode):
        self.image_viewer.clear()