import os
import re

import send2trash
from ..user_setting import UserSetting 
from ..data.data_container import ImageFileData
from .fileutil import get_save_path, copy_files, move_files
from ..logger import get_logger

logger = get_logger(__name__)

class FileManager:
    @staticmethod
    def image_files_to_save_folder(target_file_list: list[str]):
        save_mode = UserSetting.get('SAVE_MODE')
        save_folder_path = get_save_path()
        if save_mode == 'copy':
            copy_files(target_file_list, save_folder_path)
        else:
            move_files(target_file_list, save_folder_path)

        return save_folder_path
    
    @staticmethod
    def delete_files(file_list: set[ImageFileData]):
        for file in file_list:
            normpath = os.path.normpath(file.file_path)
            if os.path.exists(normpath):
                send2trash.send2trash(normpath)
                logger.info(f'Delete file: {file.file_path}')
        logger.info(f'Successfully deleted {len(file_list)} files. you can restore them in the trash.')