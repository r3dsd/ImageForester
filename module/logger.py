import logging
import os
from datetime import datetime

class CriticalExceptionHandler(logging.Handler):
    def __init__(self, directory='crash_logs'):
        super().__init__()
        self.directory = directory
        os.makedirs(self.directory, exist_ok=True)

    def emit(self, record):
        if record.levelno >= logging.CRITICAL:
            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{self.directory}/crash_{current_time}.log"
            with open(filename, 'a') as file:
                file.write(self.format(record) + '\n')

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
                                    datefmt='%Y-%m-%d %H:%M:%S')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    critical_handler = CriticalExceptionHandler()
    critical_handler.setLevel(logging.CRITICAL)
    critical_handler.setFormatter(formatter)
    logger.addHandler(critical_handler)

    return logger