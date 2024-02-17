from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt, pyqtSignal

from enum import Enum

from ..factory import DialogFactory
from .connectableList import ConnectableList
from ...file_managemant.filemanager import FileManager
from ...data import ImageFileData
from ...r3util.r3lib import check_save_folder_name
from ...user_setting import UserSetting
from ...config import FILEMANAGER_CONFIG

from ...logger import get_logger
import traceback

logger = get_logger(__name__)

class SelectList(ConnectableList):
    on_select_list_saved = pyqtSignal(Enum) # SaveModeEnum

    def __init__(self, parent=None, datastorage=None, Key_type=Qt.Key_Left):
        super().__init__(parent, datastorage, Key_type, "Select Count: ", "SelectList")

        self.save_button = QPushButton("Save")
        self.save_button.setMinimumHeight(30)
        self.save_button.setDisabled(True)
        self.layout().addWidget(self.save_button)

        self._initSignal()

    def _initSignal(self):
        self.save_button.clicked.connect(self._save_files)

    def _update_count_label(self):
        count = super()._update_count_label()
        if count > 0:
            self.save_button.setDisabled(False)
        else:
            self.save_button.setDisabled(True)

    def _save_files(self):
        if UserSetting.check('AUTO_GENERATE_FOLDER_NAME'):
            FILEMANAGER_CONFIG['SAVE_FILE_NAME'] = ''
        else:
            self._open_set_folder_name_popup()

        target_list: list[ImageFileData] = []
        for index in range(self.list.count()):
            target_list.append(self.list.item(index).data(Qt.UserRole))

        FileManager.image_files_to_save_folder(self.datastorage, target_list)
        self.clear()
        self.save_button.setDisabled(True)
        self.select_count_label.setText(f"Select Count: 0")
        self.on_select_list_saved.emit(UserSetting.get('SAVE_MODE'))
        if not UserSetting.check('DISABLE_OPEN_FOLDER_POPUP'):
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