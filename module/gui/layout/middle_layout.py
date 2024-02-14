import os
from PyQt5.QtWidgets import QBoxLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt

from ..widgets.search_list import SearchList
from ..widgets.select_list import SelectList
from ...data.imagefiledata import ImageFileData

from ..guisignalmanager import GUISignalManager
from PyQt5.QtGui import QPixmap

class MiddleLayout(QBoxLayout):
    def __init__(self, mainwindow):
        super().__init__(QBoxLayout.LeftToRight)
        self.mainwindow = mainwindow
        self._initUI()

    def _initUI(self):
        self.searched_list = SearchList()
        self.searched_list.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.addWidget(self.searched_list)

        self.selected_list = SelectList()
        self.selected_list.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.addWidget(self.selected_list)

        # Reference to each other for moving items, and focus
        self.searched_list.set(self.selected_list)
        self.selected_list.set(self.searched_list)

        self.image_viewer = QLabel()
        self.image_viewer.setMinimumSize(512, 512)
        self.image_viewer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_viewer.setAlignment(Qt.AlignCenter)
        self.addWidget(self.image_viewer)

        GUISignalManager().on_item_selection_updated.connect(self._on_item_selection_updated)
        GUISignalManager().on_search_list_send2trash.connect(self.clear_image_viewer)
        GUISignalManager().on_select_list_save.connect(self._on_select_list_save)

    def _on_item_selection_updated(self, image_data: ImageFileData):
        self.set_image_viewer(image_data.file_path)

    def _on_select_list_save(self, mode):
        self.clear_image_viewer()

    def set_image_viewer(self, image_path: str):
        normpath = os.path.normpath(image_path)
        pixmap = QPixmap(normpath)
        scaled_pixmap = pixmap.scaled(self.image_viewer.width(), self.image_viewer.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_viewer.setPixmap(scaled_pixmap)

    def clear_image_viewer(self):
        self.image_viewer.clear()