from enum import Enum
from PyQt5.QtCore import QObject, pyqtSignal

# Special thanks to https://stackoverflow.com/questions/59459770/receiving-pyqtsignal-from-singleton
class Singleton(type(QObject), type):
    def __init__(cls, name, bases, dict):
        super().__init__(name, bases, dict)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance
    
class GUISearchSignalManager(QObject, metaclass=Singleton):
    # only for search_layout
    # top_layout
    on_search_request = pyqtSignal(object) # not needed now
    on_search_completed = pyqtSignal(object, int) # ImageFileData list
    # middle_layout
    on_item_selection_updated = pyqtSignal(object) # ImageFileData
    on_deleted_data = pyqtSignal(int) # deleted count
    on_select_list_saved = pyqtSignal(Enum) # SaveModeEnum

    on_auto_database_load_started = pyqtSignal()
    on_auto_database_load_finished = pyqtSignal()

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def emit_on_item_selection_updated(self, data):
        self.on_item_selection_updated.emit(data)
    
    def emit_on_search_completed(self, data, count):
        self.on_search_completed.emit(data, count)

    def emit_on_deleted_data(self, int):
        self.on_deleted_data.emit(int)

    def emit_on_select_list_saved(self, mode: Enum):
        self.on_select_list_saved.emit(mode)

    def emit_on_auto_database_load_started(self):
        self.on_auto_database_load_started.emit()

    def emit_on_auto_database_load_finished(self):
        self.on_auto_database_load_finished.emit()

class GUISortSignalManager(QObject, metaclass=Singleton):
    on_search_request = pyqtSignal(object) # not needed now
    on_search_completed = pyqtSignal(object, int) # ImageFileData list

    on_item_selection_updated = pyqtSignal(object) # ImageFileData
    on_deleted_data = pyqtSignal(int) # deleted count
    on_select_list_saved = pyqtSignal(Enum) # SaveModeEnum

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def emit_on_item_selection_updated(self, data):
        self.on_item_selection_updated.emit(data)

    def emit_on_search_completed(self, data, count):
        self.on_search_completed.emit(data, count)
    
    def emit_on_deleted_data(self, int):
        self.on_deleted_data.emit(int)

    def emit_on_select_list_saved(self, mode: Enum):
        self.on_select_list_saved.emit(mode)

class GUITaggerSignalManager(QObject, metaclass=Singleton):

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

class GUISignalManager(QObject, metaclass=Singleton):
    # using for all layout
    on_crashed_program = pyqtSignal(str)
    # from search_layout, sort_layout
    on_load_complete = pyqtSignal(object) # load failed data (object is set[str(path)])
    # from tagger_layout
    on_tag_added = pyqtSignal(object, int) # ImageFileData or ImageFileData list

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def emit_on_crashed_program(self, error_log: str):
        self.on_crashed_program.emit(error_log)

    def emit_on_load_complete(self, data):
        self.on_load_complete.emit(data)

    def emit_on_tag_added(self, data, count):
        self.on_tag_added.emit(data, count)