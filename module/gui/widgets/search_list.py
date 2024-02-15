from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QLabel, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt

from ...historymanager.r3historymanager import R3HistoryManager
from ..guisignalmanager import GUISignalManager
from ...data.imagefiledata import ImageFileData
from ...file_managemant.filemanager import FileManager

class SearchList(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

        self.search_count_label = QLabel()
        self.search_count_label.setText("Search Count: 0")
        self.search_count_label.setMinimumHeight(30)
        self.search_count_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(self.search_count_label)

        self.list: QListWidget = QListWidget()
        self.list.keyPressEvent = self.keyPressEvent
        self.list.setObjectName("SearchList")
        layout.addWidget(self.list)

        self.send2trash_button = QPushButton("Send2Trash")
        self.send2trash_button.setMinimumHeight(30)
        self.send2trash_button.setDisabled(True)
        layout.addWidget(self.send2trash_button)

        self.list.itemClicked.connect(self._on_user_select)
        self.list.currentItemChanged.connect(self._on_user_select)

        self._initSignal()

    def _initSignal(self):
        GUISignalManager().list_count_changed.connect(self._update_count_label)
        GUISignalManager().on_search_complete.connect(self._on_search_complete)
        self.send2trash_button.clicked.connect(self._sand2trash)

    def set(self, target_list):
        self.target = target_list

    def clear(self):
        self.list.clear()
        self.search_count_label.setText(f"Search Count: 0")

    def setFocus(self):
        self.list.setFocus()
        if self.list.currentItem() is None:
            self.list.setCurrentRow(0)

    def keyPressEvent(self, event) -> None:
        key = event.key()
        if key == Qt.Key_Z and event.modifiers() == Qt.ControlModifier:
            R3HistoryManager.undo()
        elif event.modifiers() == Qt.ControlModifier:
            if key == Qt.Key_Right:
                self.target.setFocus()
                return
        elif self.list.hasFocus() and self.list.currentItem() is not None:
            if key == Qt.Key_Delete:
                self._delete()
            elif key == Qt.Key_Right:
                self._move_item()
            else:
                QListWidget.keyPressEvent(self.list, event)
                return

        GUISignalManager().emit_list_count_changed()

    def _on_search_complete(self, search_list: list[ImageFileData]):
        self.clear()
        for item in search_list:
            tmp = QListWidgetItem()
            tmp.setText(item.file_name)
            tmp.setData(Qt.UserRole, item)
            self.list.addItem(tmp)
        self._update_count_label()

        if search_list:
            self.setFocus()

    def _delete(self):
        delete_index = self.list.currentRow()
        taked_item = self.list.takeItem(delete_index)
        R3HistoryManager.add_delete_history(self.list, taked_item, delete_index)

    def _move_item(self):
        taked_index = self.list.currentRow()
        taked_item = self.list.takeItem(taked_index)
        self.target.list.addItem(taked_item)
        R3HistoryManager.add_move_history(self.list, self.target.list, taked_item, taked_index)

    def _update_count_label(self):
        count = self.list.count()
        self.search_count_label.setText(f"Search Count: {count}")
        if count > 0:
            self.send2trash_button.setDisabled(False)
        else:
            self.send2trash_button.setDisabled(True)

    def _on_user_select(self):
        if self.list.currentItem() is not None:
            GUISignalManager().emit_on_item_selection_updated(self.list.currentItem().data(Qt.UserRole))

    def _sand2trash(self):
        target_list: list[ImageFileData] = []
        for index in range(self.list.count()):
            target_list.append(self.list.item(index).data(Qt.UserRole))
        FileManager.delete_files(target_list)
        self.clear()
        GUISignalManager().emit_on_search_list_send2trash()
        self._update_count_label()