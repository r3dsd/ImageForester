import logging
import os
import datetime
import traceback

from .gui.guisignalmanager import GUISignalManager

class CustomFilter(logging.Filter):
    def filter(self, record):
        return record.levelno != logging.CRITICAL

class MyFileHandler(logging.Handler):
    def __init__(self, capacity):
        super().__init__()
        self.capacity = capacity
        self.logs = []

    def emit(self, record):
        self.logs.append(self.format(record))
        if record.levelno == logging.CRITICAL:
            self.flush()

    def flush(self):
        if self.logs:
            log_file_name = datetime.datetime.now().strftime('crash_logs/crash_log_%Y-%m-%d_%H-%M-%S.log')
            os.makedirs('crash_logs', exist_ok=True)
            with open(log_file_name, mode='w') as f:
                f.write("\n".join(self.logs))
            self.logs.clear()

formatter = logging.Formatter('[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s')

memory_handler = MyFileHandler(capacity=10000)
memory_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)
stream_handler.addFilter(CustomFilter())

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(memory_handler)
logger.addHandler(stream_handler)

def get_logger(name):
    return logger.getChild(name)

def unknown_exception(exc_type, exc_value, exc_traceback):
    os.makedirs('crash_logs', exist_ok=True)
    logger.error("!!!!!Unknown Exception!!!!!. Creating crash log. if you want to report this error, please send the log file to the developer.")
    logger.critical("Uncaught Exception", exc_info=(exc_type, exc_value, exc_traceback))
    exc_info_str = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    GUISignalManager().on_crashed_program.emit(exc_info_str)

# 예외 처리 함수 설정
import sys
sys.excepthook = unknown_exception
