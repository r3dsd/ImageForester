import os
import sys

from ..logger import get_logger

logger = get_logger(__name__)

def get_program_start_path() -> str:
    """
    return the path where the program started
    """
    if getattr(sys, 'frozen', False):
        # using PyInstaller
        main_path = os.path.dirname(sys.executable)
    else:
        # using python3 interpreter
        util_path = os.path.dirname(os.path.abspath(__file__))
        main_path = os.path.abspath(os.path.join(util_path, '..', '..'))
    logger.debug(f"main_path: {main_path}")
    return main_path

def get_defalut_save_path() -> str:
    """
    return the default save path
    """
    return os.path.join(get_program_start_path(), "ImageForestResult")

def check_path_exists(path: str) -> bool:
    """
    return the path exists
    """
    return os.path.exists(path)

def get_resource_path(relative_path: str):
    """
    Get absolute path to resource, works for dev and for PyInstaller
    """
    if getattr(sys, 'frozen', False):
        # using PyInstaller
        base_path = sys._MEIPASS
    else:
        # using python3 interpreter
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)