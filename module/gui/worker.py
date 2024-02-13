from PyQt5.QtCore import QObject, pyqtSignal, QThread

from ..logger import get_logger

logger = get_logger(__name__)

class Worker(QObject):
    finished = pyqtSignal()
    result = pyqtSignal(object)

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        result = self.func(*self.args, **self.kwargs)
        self.result.emit(result)
        self.finished.emit()

class ExtendedWorker(QObject):
    finished = pyqtSignal()
    result = pyqtSignal(object)

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.thread = QThread()
        self.moveToThread(self.thread)
        self.finished.connect(self.thread.quit)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.started.connect(self.run)

    def start(self):
        logger.info("worker started.")
        self.thread.start()

    def run(self):
        logger.info("worker running.")
        result = self.func(*self.args, **self.kwargs)
        self.finished.emit()
        self.result.emit(result)