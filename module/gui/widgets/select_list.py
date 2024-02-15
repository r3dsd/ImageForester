from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QLabel, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt

from .components.myqlistwidget import MyQListWidget
from ..factory.DialogFactory import DialogFactory
from ...historymanager.r3historymanager import R3HistoryManager
from ..guisignalmanager import GUISignalManager
from ...file_managemant.filemanager import FileManager
from ...data.imagefiledata import ImageFileData
from ...r3util.r3lib import check_save_folder_name
from ...user_setting import Savemode, UserSetting
from ...config import FILEMANAGER_CONFIG
from ..factory.DialogFactory import DialogFactory

from ...logger import get_logger
import traceback

logger = get_logger(__name__)

class SelectList(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

        self.select_count_label = QLabel()
        self.select_count_label.setText("Select Count: 0")
        self.select_count_label.setMinimumHeight(30)
        self.select_count_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(self.select_count_label)

        self.list: QListWidget = MyQListWidget()
        self.list.keyPressEvent = self.keyPressEvent
        self.list.setObjectName("SelectList")
        layout.addWidget(self.list)

        self.save_button = QPushButton("Save")
        self.save_button.setMinimumHeight(30)
        self.save_button.setDisabled(True)
        layout.addWidget(self.save_button)

        self._initSignal()

    def _initSignal(self):
        GUISignalManager().on_list_count_changed.connect(self._update_count_label)
        self.save_button.clicked.connect(self._save_files)
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
                if UserSetting.get('FORCE_DELETE'):
                    self._force_delete()
                else:
                    confirm = DialogFactory(self.parent()).create_confirm_delete_dialog()
                    confirm.exec_()
                    if confirm.result:
                        self._force_delete()
                    else:
                        return
            elif key == Qt.Key_Left:
                self._move_item()
            else:
                QListWidget.keyPressEvent(self.list, event)
                return
        GUISignalManager().emit_on_list_count_changed()

    def _delete(self):
        delete_index = self.list.currentRow()
        taked_item = self.list.takeItem(delete_index)
        R3HistoryManager.add_delete_history(self.list, taked_item, delete_index)

    def _force_delete(self):
        delete_index = self.list.currentRow()
        taked_item: ImageFileData = self.list.takeItem(delete_index).data(Qt.UserRole)
        FileManager.delete_single_file(taked_item)

    def _move_item(self):
        taked_index = self.list.currentRow()
        taked_item = self.list.takeItem(taked_index)
        self.target.list.addItem(taked_item)
        R3HistoryManager.add_move_history(self.list, self.target.list, taked_item, taked_index)

    def _undo(self):
        R3HistoryManager.undo()

    def _update_count_label(self):
        count = self.list.count()
        self.select_count_label.setText(f"Select Count: {count}")
        if count > 0:
            self.save_button.setDisabled(False)
        else:
            self.save_button.setDisabled(True)

    def _on_user_select(self):
        if self.list.currentItem() is not None:
            GUISignalManager().emit_on_item_selection_updated(self.list.currentItem().data(Qt.UserRole))

    def _save_files(self):
        if UserSetting.get('AUTO_GENERATE_FOLDER_NAME') == True:
            FILEMANAGER_CONFIG['SAVE_FILE_NAME'] = ''
        else:
            self._open_set_folder_name_popup()

        target_list: list[ImageFileData] = []
        for index in range(self.list.count()):
            target_list.append(self.list.item(index).data(Qt.UserRole))

        FileManager.image_files_to_save_folder(target_list)
        self.clear()
        GUISignalManager().emit_on_select_list_save(Savemode(UserSetting.get('SAVE_MODE')))
        self._update_count_label()

        if not UserSetting.get('DISABLE_OPEN_FOLDER_POPUP'):
            pass
        else:
            DialogFactory(self.parent()).create_folder_open_dialog(count=len(target_list)).exec_()

    def _open_set_folder_name_popup(self):
        try:
            FILEMANAGER_CONFIG['SAVE_FILE_NAME'] = ''
            while True:
                popup = DialogFactory(self.parent()).create_input_folder_name_dialog()
                popup.exec_()
                folder_name = popup.result
                if folder_name == '':
                    FILEMANAGER_CONFIG['SAVE_FILE_NAME'] = ''
                    logger.info(f"use default folder name: {FILEMANAGER_CONFIG['SAVE_FILE_NAME']}")
                    break

                if check_save_folder_name(folder_name):
                    FILEMANAGER_CONFIG['SAVE_FILE_NAME'] = folder_name.replace(' ', '_')
                    logger.info(f"Save folder name: {FILEMANAGER_CONFIG['SAVE_FILE_NAME']}")
                    break
        except Exception as e:
            logger.error(f'Error: {e}\n{traceback.format_exc()}')