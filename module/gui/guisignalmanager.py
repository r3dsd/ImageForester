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

class GUISignalManager(QObject, metaclass=Singleton):
    list_count_changed = pyqtSignal()

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def emit_list_count_changed(self):
        self.list_count_changed.emit()