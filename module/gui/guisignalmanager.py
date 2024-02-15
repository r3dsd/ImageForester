from PyQt5.QtCore import QObject, pyqtSignal
from ..data.imagefiledata import ImageFileData

from ..user_setting import SaveModeEnum

# Special thanks to https://stackoverflow.com/questions/59459770/receiving-pyqtsignal-from-singleton
class Singleton(type(QObject), type):
    def __init__(cls, name, bases, dict):
        super().__init__(name, bases, dict)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance

class GUISignalManager(QObject, metaclass=Singleton):
    on_list_count_changed = pyqtSignal()
    on_search_complete = pyqtSignal(object)
    on_load_complete = pyqtSignal()
    on_item_selection_updated = pyqtSignal(ImageFileData)
    on_load_image_empty = pyqtSignal()
    on_gui_style_changed = pyqtSignal(str)
    on_select_list_save = pyqtSignal(SaveModeEnum)
    on_search_list_send2trash = pyqtSignal()
    on_tag_added = pyqtSignal(str)
    on_auto_tagging_finished = pyqtSignal(int)
    on_deleted_loaded_data = pyqtSignal()

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def emit_on_list_count_changed(self):
        self.on_list_count_changed.emit()

    def emit_on_search_completed(self, data):
        self.on_search_complete.emit(data)

    def emit_on_load_completed(self):
        self.on_load_complete.emit()

    def emit_on_item_selection_updated(self, data):
        self.on_item_selection_updated.emit(data)

    def emit_on_load_image_empty(self):
        self.on_load_image_empty.emit()

    def emit_on_gui_style_changed(self, style):
        self.on_gui_style_changed.emit(style)

    def emit_on_select_list_save(self, mode: SaveModeEnum):
        self.on_select_list_save.emit(mode)

    def emit_on_search_list_send2trash(self, count: int):
        self.on_search_list_send2trash.emit(count)

    def emit_on_tag_added(self, path: str):
        self.on_tag_added.emit(path)

    def emit_on_auto_tagging_finished(self, count: int):
        self.on_auto_tagging_finished.emit(count)

    def emit_on_deleted_loaded_data(self):
        self.on_deleted_loaded_data.emit()