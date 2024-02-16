from concurrent.futures import ThreadPoolExecutor
import shutil
import os
import re
import threading
from ..data.data_container import ImageFileData
from ..user_setting import UserSetting
from ..data.data_container import DataContainer
from ..r3util.r3path import get_defalut_save_path, process_path
from ..config import FILEMANAGER_CONFIG

from ..logger import get_logger
import traceback

logger = get_logger(__name__)

lock = threading.Lock()

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
    destination_file_path = process_path(destination_file_path)
    shutil.copy(file_path, destination_file_path)
    logger.info(f'Copy: {file_path} -> {destination_file_path}')

def move_file(file_path, save_folder_path):
    destination_file_path = generate_unique_file_path(file_path, save_folder_path, '_Move')
    destination_file_path = process_path(destination_file_path)
    shutil.move(file_path, destination_file_path)
    logger.info(f'Move: {file_path} -> {destination_file_path}')

def generate_unique_file_path(original_path, save_folder_path, savemode: str):
    with lock:
        filename = os.path.basename(original_path)
        file_name, file_extension = os.path.splitext(filename)
        base_length = len(file_extension) + len(savemode)
        max_name_length = 50 - base_length - 1
        
        if len(file_name) > max_name_length:
            file_name = f"{file_name[:max_name_length]}..."
        
        new_filename = f"{file_name}{savemode}{file_extension}"
        full_path = os.path.join(save_folder_path, new_filename)
        counter = 1

        while os.path.exists(full_path):
            new_filename = f"{file_name[:max_name_length]}{savemode}_{counter}{file_extension}"
            full_path = os.path.join(save_folder_path, new_filename)
            counter += 1

    return full_path


def get_save_path():
    """
    return the save folder path
    """
    save_folder_name = FILEMANAGER_CONFIG['SAVE_FILE_NAME']
    base_save_folder_path = UserSetting.get('SAVE_PATH')
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
    base_save_folder_path = process_path(base_save_folder_path)
    FILEMANAGER_CONFIG['FINAL_SAVE_FOLDER_PATH'] = base_save_folder_path
    return base_save_folder_path

def create_folder_name_using_search_keyword():
    search_keyword = DataContainer.get_search_keywords()
    logger.info(f'Create folder name using search keyword: {search_keyword}')
    string = '_'.join(search_keyword)
    string = re.sub(r'[\\/:*?"<>|~!]', '', string)
    length = len(string)
    if length > 50:
        string = string[:50]
    elif length == 0:
        string = 'Image_Search_Result'
    logger.info(f'Create folder name using search keyword: {string}')
    return string
