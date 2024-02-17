from PyQt5.QtWidgets import QListWidgetItem, QPushButton
from PyQt5.QtCore import Qt

from .connectableList import ConnectableList
from ...data import ImageFileData
from ...file_managemant.filemanager import FileManager

from ...logger import get_logger

logger = get_logger(__name__)

class SearchList(ConnectableList):
    def __init__(self, parent=None, datastorage=None, Key_type=Qt.Key_Right):
        super().__init__(parent, datastorage, Key_type, "Search Count: ", "SearchList")

        self.send2trash_button = QPushButton("Send2Trash")
        self.send2trash_button.setMinimumHeight(30)
        self.send2trash_button.setDisabled(True)
        self.layout().addWidget(self.send2trash_button)

        self.list.itemClicked.connect(self._on_user_select)
        self.list.currentItemChanged.connect(self._on_user_select)

        self._initSignal()

    def _initSignal(self):
        self.send2trash_button.clicked.connect(self._on_clicked_send2trash)

    def _update_count_label(self):
        count = super()._update_count_label()
        if count > 0:
            self.send2trash_button.setDisabled(False)
        else:
            self.send2trash_button.setDisabled(True)

    def on_search_completed(self, search_list: list[ImageFileData]):
        self.clear()
        for item in search_list:
            tmp = QListWidgetItem()
            tmp.setText(item.file_name)
            tmp.setData(Qt.UserRole, item)
            self.list.addItem(tmp)
        self.list.sortItems()
        self._update_count_label()

        if search_list:
            self.setFocus()

    def _on_clicked_send2trash(self):
        target_file_list, count = self._get_all_item_data()
        FileManager.delete_files(self.datastorage, target_file_list, count)
        self.clear()
        self._update_count_label()
        self.on_deleted_data.emit(count)
