import os

import send2trash
from ..user_setting import UserSetting 
from ..data.data_container import ImageFileData, DataContainer
from .fileutil import get_save_path, copy_files, move_files
from ..logger import get_logger
import traceback

logger = get_logger(__name__)

class FileManager:
    @staticmethod
    def image_files_to_save_folder(target_file_list: list[ImageFileData]) -> str:
        save_mode = UserSetting.get('SAVE_MODE')
        save_folder_path = get_save_path()
        logger.info(f'Save mode: {save_mode}')
        if save_mode == 'Copy':
            copy_files(target_file_list, save_folder_path)
        else:
            move_files(target_file_list, save_folder_path)
            DataContainer.delete_loaded_data(target_file_list)
        return save_folder_path
    
    @staticmethod
    def delete_files(target_file_list: list[ImageFileData], count: int) -> bool:
        target_file_path_list = [file.file_path for file in target_file_list]
        try:
            send2trash.send2trash(target_file_path_list)
            logger.info(f'Start deleting {count} files.')
            DataContainer.delete_loaded_data(target_file_list)
            logger.info(f'Successfully deleted {count} files. you can restore them in the trash.')
            return True
        except Exception as e:
            logger.error(f'Error: {e}\n{traceback.format_exc()}')
            return False

    @staticmethod
    def delete_single_file(target_file: ImageFileData) -> bool:
        file_path = target_file.file_path
        if os.path.exists(file_path):
            send2trash.send2trash(file_path)
            logger.info(f'Delete file: {file_path}')
            DataContainer.delete_loaded_data([target_file])
            logger.info(f'Successfully deleted file. you can restore it in the trash.')
            return True
        else:
            logger.warning(f'File not found: {file_path}')
            return False