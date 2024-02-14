from concurrent.futures import ThreadPoolExecutor
import shutil
import os
import re
from datetime import datetime

from ..data.data_container import ImageFileData
from ..user_setting import UserSetting
from ..data.data_container import DataContainer
from ..r3util.r3path import get_defalut_save_path
from ..config import FILEMANAGER_CONFIG

from ..logger import get_logger
import traceback


logger = get_logger(__name__)

def move_files(target_file_list: set[ImageFileData], save_folder_path: str):
    try:
        logger.debug(f'move files : ThreadPoolExecutor max_workers: 4')
        with ThreadPoolExecutor(max_workers=4) as executor:
            for target_image_info in target_file_list:
                executor.submit(move_file, target_image_info.file_path, save_folder_path)
    except Exception as e:
        logger.warning(f'Error: {e}\n{traceback.format_exc()}')

def copy_files(target_file_list: set[ImageFileData], save_folder_path: str):
    try:
        logger.debug(f'copy files : ThreadPoolExecutor max_workers: 4')
        with ThreadPoolExecutor(max_workers=4) as executor:
            for target_image_info in target_file_list:
                executor.submit(copy_file, target_image_info.file_path, save_folder_path)
    except Exception as e:
        logger.warning(f'Error: {e}\n{traceback.format_exc()}')

def copy_file(file_path, save_folder_path):
    destination_file_path = generate_unique_file_path(file_path, save_folder_path, '_Copy')
    shutil.copy(file_path, destination_file_path)
    logger.info(f'Copy: {file_path} -> {destination_file_path}')

def move_file(file_path, save_folder_path):
    destination_file_path = generate_unique_file_path(file_path, save_folder_path, '_Move')
    shutil.move(file_path, destination_file_path)
    logger.info(f'Move: {file_path} -> {destination_file_path}')

def fit_filename(original_filename, timestamp, extension, max_length=50) -> str:
    """
    return the filename that fits the maximum length if the filename is too long to fit the maximum length (50 characters)
    """
    base_length = len(timestamp) + len(extension) + 3
    available_length = max_length - base_length

    if len(original_filename) > available_length:
        return f"{original_filename[:available_length - 3]}..."
    else:
        return original_filename

def generate_unique_file_path(original_path, save_folder_path, savemode: str):
    """
    return the unique file path in the save folder
    """
    filename = os.path.basename(original_path)
    file_name, file_extension = os.path.splitext(filename)
    timestamp = datetime.now().strftime("_%y%m%d_%H%M%S")  # ex) _210101_123456

    final_filename = fit_filename(file_name, timestamp, file_extension)
    new_filename = f"{final_filename}{timestamp}{savemode}{file_extension}"
    return os.path.join(save_folder_path, new_filename)

def get_save_path():
    save_folder_name = FILEMANAGER_CONFIG['SAVE_FILE_NAME']
    base_save_folder_path = UserSetting.get('IMAGE_SAVE_DIR')
    if not base_save_folder_path:
        base_save_folder_path = get_defalut_save_path()

    if save_folder_name != '':
        base_save_folder_path = os.path.join(base_save_folder_path, save_folder_name)
    else:
        string = create_folder_name_using_search_keyword()
        base_save_folder_path = os.path.join(base_save_folder_path, string)

    logger.info(f'Set Save folder path: {base_save_folder_path}')

    if not os.path.exists(base_save_folder_path):
        os.makedirs(base_save_folder_path)
    else:
        logger.info(f'folder already exists: {base_save_folder_path}')
    logger.debug(f'function get_save_path return: {base_save_folder_path}')
    return base_save_folder_path

def create_folder_name_using_search_keyword():
    search_keyword = DataContainer.get_search_keywords()
    string = '_'.join(search_keyword)
    string = re.sub(r'[\\/:*?"<>|~!]', '', string)
    return string
