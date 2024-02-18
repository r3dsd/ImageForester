from concurrent.futures import ThreadPoolExecutor
import os
import re
import shutil

import send2trash
from ..user_setting import UserSetting, SaveModeEnum
from ..data import ImageFileData, DataStorage, DB, SearchDataStorage
from ..logger import get_logger
from ..user_setting import UserSetting
from ..r3util.r3path import get_defalut_save_path, process_path
from ..config import FILEMANAGER_CONFIG
import traceback

logger = get_logger(__name__)
# TODO
# 1. FileUtil에서 작성한 함수 copy_files, move_files를 리팩토링해야함. 그때그때 옮길걸 계산하지 말고, 미리 옮겨야할 Path를 계산, 그리고 그 함수에서 두개의 set을 반환하고,
#   FileManager에서는 그 set을 받아서 DataStorage에 있는 on_copy, on_move를 호출하도록 수정해야함.
#   그렇게 하면 데이터베이스에 있는 정보를 업데이트하기 쉬워짐.

class FileManager:
    @staticmethod
    def image_files_to_save_folder(datastorage : DataStorage, source_file_list: list[ImageFileData]) -> str:
        save_mode = UserSetting.get('SAVE_MODE')
        save_folder_path: str = get_save_path(search_keyword=datastorage.get_search_keywords())
        target_file_list = generate_unique_file_paths(source_file_list, save_folder_path)
        logger.info(f'Save mode: {save_mode}')
        if save_mode == SaveModeEnum.COPY:
            copy_files(target_file_list)
            datastorage.on_copy(target_file_list)
        elif save_mode == SaveModeEnum.MOVE:
            move_files(target_file_list)
            datastorage.on_move(target_file_list)
        return save_folder_path
    
    @staticmethod
    def delete_files(datastorage : DataStorage, target_file_list: list[ImageFileData], count: int) -> bool:
        target_file_path_list = [file.file_path for file in target_file_list]
        send2trash.send2trash(target_file_path_list)
        logger.info(f'Start deleting {count} files.')
        datastorage.delete_loaded_data(target_file_list)
        logger.info(f'Successfully deleted {count} files. you can restore them in the trash.')
        return True

    @staticmethod
    def delete_single_file(datastorage : DataStorage, target_file: ImageFileData) -> bool:
        file_path = target_file.file_path
        if os.path.exists(file_path):
            send2trash.send2trash(file_path)
            logger.info(f'Delete file: {file_path}')
            datastorage.delete_loaded_data([target_file])
            logger.info(f'Successfully deleted file. you can restore it in the trash.')
            return True
        else:
            logger.warning(f'File not exists: {file_path}')
            return False

def generate_unique_file_paths(source_list: list[ImageFileData], destination_folder: str) -> list[tuple[ImageFileData, str]]:
    results = []
    name_counter = {}

    for image_data in source_list:
        file_name = os.path.basename(image_data.file_path)
        base_name, extension = os.path.splitext(file_name)

        counter = name_counter.get(base_name, 0)
        unique_name = file_name
        while os.path.join(destination_folder, unique_name) in [path[1] for path in results]:
            counter += 1
            unique_name = f"{base_name}_{counter}{extension}"
            name_counter[base_name] = counter
        new_destination_path = os.path.join(destination_folder, unique_name)
        results.append((image_data, new_destination_path))
    return results

def copy_files(target_list: list[tuple[ImageFileData, str]]) -> None:
    logger.debug(f'copy files : ThreadPoolExecutor max_workers: 4')

    with ThreadPoolExecutor(max_workers=4) as executor:
        for target_path, destination_path in target_list:
            executor.submit(copy_file, target_path.file_path, destination_path)

def copy_file(target_path: str, destination_path: str) -> None:
    shutil.copy(target_path, destination_path)
    logger.debug(f'copy file: {target_path} -> {destination_path}')

def move_files(target_list: list[tuple[ImageFileData, str]]) -> None:
    logger.debug(f'move files : ThreadPoolExecutor max_workers: 4')

    with ThreadPoolExecutor(max_workers=4) as executor:
        for target_path, destination_path in target_list:
            executor.submit(move_file, target_path.file_path, destination_path)

def move_file(target_path: str, destination_path: str) -> None:
    shutil.move(target_path, destination_path)
    logger.debug(f'move file: {target_path} -> {destination_path}')

def get_save_path(search_keyword: list[str] = []):
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
        string = _create_folder_name_using_search_keyword(search_keyword)
        base_save_folder_path = os.path.join(base_save_folder_path, string)

    logger.info(f'Set Save folder path: {base_save_folder_path}')

    if not os.path.exists(base_save_folder_path):
        os.makedirs(base_save_folder_path)
    else:
        logger.info(f'folder already exists: {base_save_folder_path}')
    base_save_folder_path = process_path(base_save_folder_path)
    FILEMANAGER_CONFIG['FINAL_SAVE_FOLDER_PATH'] = base_save_folder_path
    return base_save_folder_path

def _create_folder_name_using_search_keyword(search_keyword: list[str] = []):
    logger.info(f'Try Create folder name using search keyword: {search_keyword}')
    string = '_'.join(search_keyword)
    string = re.sub(r'[\\/:*?"<>|~!]', '', string)
    length = len(string)
    if length > 50:
        string = string[:50]
    elif length == 0:
        string = 'Image_Search_Result'
    logger.info(f'Created folder name using search keyword: {string}')
    return string


# test
# storage = SearchDataStorage()
# storage.set_search_keywords(["test"])
# data1 = ImageFileData("test1", "tag1")
# data2 = ImageFileData("test2", "tag2")
# data3 = ImageFileData("test3", "tag3")
# data4 = ImageFileData("test4", "tag4")

# data1.process_file_tags()
# data2.process_file_tags()
# data3.process_file_tags()
# data4.process_file_tags()

# file_list = [data1, data2, data3, data4]
# storage.set_loaded_data(file_list)

# FileManager.image_files_to_save_folder(storage, file_list)