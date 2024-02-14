import shutil
from ..user_setting import UserSetting
from ..r3util.r3path import get_defalut_save_path
from ..data.data_container import DataContainer, ImageFileData
import os
import re
from ..logger import get_logger

logger = get_logger(__name__)

def get_save_path(folder_name=None):
    save_folder_path = UserSetting.get('IMAGE_SAVE_DIR')
    if not save_folder_path:
        save_folder_path = get_defalut_save_path()
    if folder_name:
        save_folder_path = os.path.join(save_folder_path, folder_name)
    else:
        search_keyword = DataContainer.get_search_keywords()
        string = '_'.join(search_keyword)
        string = re.sub(r'[\\/:*?"<>|~!]', '', string)
        save_folder_path = os.path.join(save_folder_path, string)
    if not os.path.exists(save_folder_path):
        os.makedirs(save_folder_path)
    logger.debug(f'function get_save_path return: {save_folder_path}')
    return save_folder_path

def copy_files(target_file_list: set[ImageFileData], save_folder_path: str):
    try:
        for target_image_info in target_file_list:
            source_file_path: str = target_image_info.file_path
            filename = os.path.basename(target_image_info.file_path)
            file_name, file_extension = os.path.splitext(filename)
            counter = 1
            new_file_name = f"{file_name}_{counter}"
            destination_file_path = os.path.join(save_folder_path, new_file_name + file_extension)

            while os.path.exists(destination_file_path):
                counter += 1
                new_file_name = f"{file_name}_{counter}"
                destination_file_path = os.path.join(save_folder_path, new_file_name + file_extension)

            shutil.copy(source_file_path, destination_file_path)
            logger.info(f'Copy: {source_file_path} -> {destination_file_path}')
    except Exception as e:
        logger.warning(f'Error: {e}')

def move_files(target_file_list: set[ImageFileData], save_folder_path: str):
    try:
        for target_image_info in target_file_list:
            source_file_path: str = target_image_info.file_path
            filename = os.path.basename(target_image_info.file_path)
            file_name, file_extension = os.path.splitext(filename)

            # 파일 이름에 넘버링 추가
            counter = 1
            new_file_name = f"{file_name}_{counter}"
            destination_file_path = os.path.join(save_folder_path, new_file_name + file_extension)

            # 같은 이름이 있는 경우에만 넘버링 증가
            while os.path.exists(destination_file_path):
                counter += 1
                new_file_name = f"{file_name}_{counter}"
                destination_file_path = os.path.join(save_folder_path, new_file_name + file_extension)

            shutil.move(source_file_path, destination_file_path)
            print(f'파일 이동: {source_file_path} -> {destination_file_path}')
        DataContainer.delete_loaded_data(target_file_list)
    except Exception as e:
        logger.warning(f'Error: {e}')