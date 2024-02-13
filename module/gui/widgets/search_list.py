from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QLabel, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt

from ...historymanager.r3historymanager import R3HistoryManager
from ..guisignalmanager import GUISignalManager
from ...data.imagefiledata import ImageFileData

class SearchList(QWidget):
    def __init__(self):
        super().__init__()

        GUISignalManager().list_count_changed.connect(self._update_count_label)
        GUISignalManager().on_search_complete.connect(self._on_search_complete)

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

        self.list.itemClicked.connect(self._on_user_select)
        self.list.currentItemChanged.connect(self._on_user_select)

    def set(self, target_list):
        self.target = target_list

    def clear(self):
        self.list.clear()
        self.search_count_label.setText(f"Search Count: 0")

    def setFocus(self):
        self.list.setFocus()
        if self.list.currentItem() is None:
            self.list.setCurrentRow(0)

    def _on_search_complete(self, search_list: list[ImageFileData]):
        self.clear()
        for item in search_list:
            tmp = QListWidgetItem()
            tmp.setText(item.file_path)
            tmp.setData(Qt.UserRole, item)
            self.list.addItem(tmp)
        self._update_count_label()

        self.setFocus()

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
        self.search_count_label.setText(f"Search Count: {self.list.count()}")

    def _on_user_select(self):
        if self.list.currentItem() is not None:
            GUISignalManager().emit_on_item_selection_updated(self.list.currentItem().data(Qt.UserRole))