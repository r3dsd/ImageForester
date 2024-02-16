from module.gui.maingui import MainGui
from module.logger import get_logger
import sys

logger = get_logger(__name__)

def error_catch(exc_type, exc_value, exc_traceback):
    logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    sys.exit(1)

sys.excepthook = error_catch

def main():
    MainGui()

if __name__ == "__main__":
    main()
