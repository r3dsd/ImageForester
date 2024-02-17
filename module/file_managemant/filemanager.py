import os

import send2trash
from ..user_setting import UserSetting, SaveModeEnum
from ..data import ImageFileData, DataStorage
from .fileutil import get_save_path, copy_files, move_files
from ..logger import get_logger
import traceback

logger = get_logger(__name__)

class FileManager:
    @staticmethod
    def image_files_to_save_folder(datastorage : DataStorage, target_file_list: list[ImageFileData]) -> str:
        save_mode = UserSetting.get('SAVE_MODE')
        save_folder_path: str = get_save_path(search_keyword=datastorage.get_search_keywords())
        logger.info(f'Save mode: {save_mode}')
        if save_mode == SaveModeEnum.COPY:
            copy_files(target_file_list, save_folder_path)
        elif save_mode == SaveModeEnum.MOVE:
            move_files(target_file_list, save_folder_path)
            datastorage.delete_loaded_data(target_file_list)
        return save_folder_path
    
    @staticmethod
    def delete_files(datastorage : DataStorage, target_file_list: list[ImageFileData], count: int) -> bool:
        target_file_path_list = [file.file_path for file in target_file_list]
        try:
            send2trash.send2trash(target_file_path_list)
            logger.info(f'Start deleting {count} files.')
            datastorage.delete_loaded_data(target_file_list)
            logger.info(f'Successfully deleted {count} files. you can restore them in the trash.')
            return True
        except Exception as e:
            logger.error(f'Error: {e}\n{traceback.format_exc()}')
            return False

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
            logger.warning(f'File not found: {file_path}')
            return False