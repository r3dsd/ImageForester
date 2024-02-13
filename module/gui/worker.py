from PyQt5.QtCore import QObject, pyqtSignal, QThread

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

        # 시그널 연결
        self.finished.connect(self.thread.quit)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.started.connect(self.run)

    def start(self):
        """스레드 시작 메서드"""
        self.thread.start()

    def run(self):
        """스레드에서 실행할 작업"""
        result = self.func(*self.args, **self.kwargs)
        self.result.emit(result)
        self.finished.emit()