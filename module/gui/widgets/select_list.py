from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QLabel, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt

from ...historymanager.r3historymanager import R3HistoryManager
from ..guisignalmanager import GUISignalManager

class SelectList(QWidget):
    def __init__(self):
        super().__init__()

        GUISignalManager().list_count_changed.connect(self._update_count_label)

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

        self.select_count_label = QLabel()
        self.select_count_label.setText("Select Count: 0")
        self.select_count_label.setMinimumHeight(30)
        self.select_count_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(self.select_count_label)

        self.list: QListWidget = QListWidget()
        self.list.keyPressEvent = self.keyPressEvent
        self.list.setObjectName("SelectList")
        layout.addWidget(self.list)

        self.list.itemClicked.connect(self._on_user_select)
        self.list.currentItemChanged.connect(self._on_user_select)

    def set(self, target_list):
        self.target = target_list

    def clear(self):
        self.list.clear()
        self.select_count_label.setText(f"Select Count: 0")

    def setFocus(self):
        self.list.setFocus()
        if self.list.currentItem() is None:
            self.list.setCurrentRow(0)

    def update_select_list(self, select_list: list[str]):
        self.list.clear()
        for item in select_list:
            self.list.addItem(QListWidgetItem(item))

        self._update_count_label()

    def keyPressEvent(self, event) -> None:
        key = event.key()
        if key == Qt.Key_Z and event.modifiers() == Qt.ControlModifier:
            R3HistoryManager.undo()
        elif event.modifiers() == Qt.ControlModifier:
            if key == Qt.Key_Left:
                self.target.setFocus()
                return
        elif self.list.hasFocus() and self.list.currentItem() is not None:
            if key == Qt.Key_Delete:
                self._delete()
            elif key == Qt.Key_Left:
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

    def _undo(self):
        R3HistoryManager.undo()

    def _update_count_label(self):
        self.select_count_label.setText(f"Select Count: {len(self.list)}")

    def _on_user_select(self):
        if self.list.currentItem() is not None:
            GUISignalManager().emit_on_item_selection_updated(self.list.currentItem().data(Qt.UserRole))