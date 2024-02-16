from module.gui.maingui import MainGui

import logging

def setup_logging():
    logging.basicConfig(filename='app_crash.log',
                        level=logging.ERROR,
                        format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    setup_logging()
    try:
        MainGui()
    except Exception as e:
        logging.error("Unhandled exception occurred", exc_info=True)
        raise
if __name__ == "__main__":
    main()