import os
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QMenu
from PyQt5.QtCore import Qt

from ....data import ImageFileData

from ....logger import get_logger
import traceback

logger = get_logger(__name__)

class MyQListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        action1 = contextMenu.addAction("Open Folder")
        action2 = contextMenu.addAction("Open File")
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        
        if action == action1:
            self.folder_open()
        elif action == action2:
            self.file_view()

    def file_view(self):
        item = self.currentItem()
        try:
            if item:
                image_info: ImageFileData = item.data(Qt.UserRole)
                if image_info and hasattr(image_info, 'file_path') and image_info.file_path:
                    os.startfile(image_info.file_path)
                else:
                    item_text = item.text()
                    os.startfile(item_text)
        except Exception as e:
            logger.error(f"Error: {e}\n{traceback.format_exc()}")


    def folder_open(self):
        item = self.currentItem()
        try:
            if item:
                image_info: ImageFileData = item.data(Qt.UserRole)
                if image_info and hasattr(image_info, 'file_path') and image_info.file_path:
                    os.startfile(os.path.dirname(image_info.file_path))
                else:
                    item_text = item.text()
                    os.startfile(os.path.dirname(item_text))
        except Exception as e:
            logger.error(f"Error: {e}\n{traceback.format_exc()}")
