from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt, pyqtSignal

from .components.myqlistwidget import MyQListWidget
from ...historymanager.r3historymanager import R3HistoryManager
from ...file_managemant.filemanager import FileManager
from ...data import ImageFileData
from ...user_setting import UserSetting
from ..factory.DialogFactory import DialogFactory
from ...logger import get_logger

logger = get_logger(__name__)

class ConnectableList(QWidget):
    on_item_selection_updated = pyqtSignal(ImageFileData)
    on_deleted_data = pyqtSignal(int)

    def __init__(self, parent=None, datastorage=None, Key_type=None, count_label_text="Count : ", object_name="ConnectableList"):
        super().__init__(parent)
        self.move_key = Key_type
        self.target : ConnectableList = None
        self.datastorage = datastorage
        self.count_label_text = count_label_text

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

        self.count_label = QLabel()
        layout.addWidget(self.count_label)
        self.count_label.setText(f"{count_label_text} 0")
        self.count_label.setMinimumHeight(30)
        self.count_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.list: QListWidget = MyQListWidget()
        layout.addWidget(self.list)
        self.list.keyPressEvent = self.keyPressEvent
        self.list.setObjectName(object_name)

    def connect(self, target):
        self.target: ConnectableList = target

    def add_item(self, item: QListWidgetItem):
        self.list.addItem(item)
        self._update_count_label()

    def clear(self):
        self.list.clear()
        self.count_label.setText(f"{self.count_label_text} 0")

    def setFocus(self):
        self.list.setFocus()
        if self.list.currentItem() is None:
            self.list.setCurrentRow(0)

    def keyPressEvent(self, event) -> None:
        key = event.key()
        if key == Qt.Key_Z and event.modifiers() == Qt.ControlModifier:
            R3HistoryManager.undo()
        elif event.modifiers() == Qt.ControlModifier:
            if key == self.move_key:
                self.target.setFocus()
                return
        elif self.list.hasFocus() and self.list.currentItem() is not None:
            if key == Qt.Key_Delete:
                if UserSetting.check('FORCE_DELETE'):
                    self._delete()
                else:
                    path = self.list.currentItem().data(Qt.UserRole).file_path
                    confirm = DialogFactory(self.parent()).create_confirm_delete_dialog(path)
                    confirm.exec_()
                    if confirm.result:
                        self._delete()
                    else:
                        return
            elif key == self.move_key:
                self._move_item()
            else:
                QListWidget.keyPressEvent(self.list, event)
                return
        self._update_count_label()

    def _update_count_label(self):
        count = self.list.count()
        self.count_label.setText(f"{self.count_label_text} {count}")
        return count

    def _delete(self):
        delete_index = self.list.currentRow()
        taked_item :ImageFileData = self.list.takeItem(delete_index).data(Qt.UserRole)
        FileManager.delete_single_file(self.datastorage, taked_item)
        self.on_deleted_data.emit(1)

    def _move_item(self):
        taked_index = self.list.currentRow()
        taked_item = self.list.takeItem(taked_index)
        self.target.add_item(taked_item)
        R3HistoryManager.add_move_history(self.list, self.target.list, taked_item, taked_index)

    def _on_user_select(self):
        if self.list.currentItem() is not None:
            self.on_item_selection_updated.emit(self.list.currentItem().data(Qt.UserRole))

    def _get_all_item_data(self):
        items = []
        for i in range(self.list.count()):
            items.append(self.list.item(i).data(Qt.UserRole))
        return items, len(items)