import os

import send2trash
from ..user_setting import UserSetting 
from ..data.data_container import ImageFileData, DataContainer
from .fileutil import get_save_path, copy_files, move_files
from ..logger import get_logger

logger = get_logger(__name__)

class FileManager:
    @staticmethod
    def image_files_to_save_folder(target_file_list: list[ImageFileData]):
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
    def delete_files(file_list: list[str]):
        for file_path in file_list:
            normpath = os.path.normpath(file_path)
            if os.path.exists(normpath):
                send2trash.send2trash(normpath)
                logger.info(f'Delete file: {file_path}')
        logger.info(f'Successfully deleted {len(file_list)} files. you can restore them in the trash.')

    @staticmethod
    def delete_single_file(file_path: str):
        normpath = os.path.normpath(file_path)
        if os.path.exists(normpath):
            send2trash.send2trash(normpath)
            logger.info(f'Delete file: {file_path}')
        logger.info(f'Successfully deleted file. you can restore it in the trash.')