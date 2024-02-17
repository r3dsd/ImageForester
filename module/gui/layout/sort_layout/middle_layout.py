from PyQt5.QtWidgets import QHBoxLayout, QSizePolicy

from ...widgets.search_list import SearchList
from ...widgets.select_list import SelectList
from ....data import ImageFileData
from ...widgets.image_viewer import ImageViewer

from ...guisignalmanager import GUISortSignalManager

class MiddleLayout(QHBoxLayout):
    def __init__(self, mainwindow, datastorage):
        super().__init__()
        self.mainwindow = mainwindow
        self.datastorage = datastorage
        self._initUI()
        self._initSignal()

    def _initUI(self):
        self.searched_list = SearchList(self.mainwindow, self.datastorage)
        self.searched_list.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.addWidget(self.searched_list)

        self.selected_list = SelectList(self.mainwindow, self.datastorage)
        self.selected_list.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.addWidget(self.selected_list)

        self.searched_list.connect(self.selected_list)
        self.selected_list.connect(self.searched_list)

        self.image_viewer = ImageViewer(self.mainwindow)
        self.addWidget(self.image_viewer)


    def _initSignal(self):
        self.searched_list.on_item_selection_updated.connect(self._on_item_selection_updated)
        self.searched_list.on_deleted_data.connect(self._on_deleted_data)
        self.selected_list.on_item_selection_updated.connect(self._on_item_selection_updated)
        self.selected_list.on_deleted_data.connect(self._on_deleted_data)
        self.selected_list.on_select_list_saved.connect(self._on_select_list_saved)
        GUISortSignalManager().on_search_completed.connect(self.searched_list.on_search_completed)

    def _on_item_selection_updated(self, image_data: ImageFileData):
        GUISortSignalManager().emit_on_item_selection_updated(image_data)
        self.image_viewer.update_image(image_data.file_path)

    def _on_select_list_saved(self, mode):
        GUISortSignalManager().emit_on_select_list_saved(mode)

    def _on_deleted_data(self, int):
        self.image_viewer.clear()
        GUISortSignalManager().emit_on_deleted_data(int)