import json
import os
import struct
import concurrent.futures
from PIL import Image
from .data_container import DataContainer
from .stealth_pnginfo import read_info_from_image_stealth
from ..constants import IMAGE_FORMATS
from ..user_setting import UserSetting
from .imagefiledata import ImageFileData
from .database import DB
from ..logger import get_logger
from ..r3util.r3path import process_path

logger = get_logger(__name__)

class DataLoader:
    _loadable_file_set: set[str] = set()

    @classmethod
    def load_from_DB(cls) -> None:
        logger.info("Load Data from Database")
        data = DB().get_data()
        DataContainer.set_loaded_data(data)

    @classmethod
    def load_using_multi(cls) -> None:
        """
        Load image from _loadable_file_list
        """
        def process_file(file_path: str) -> ImageFileData:
            image_file_data, is_acessable = get_png_description(file_path)
            if is_acessable:
                image_file_data.process_file_tags()
                return image_file_data
            return None
        
        files_to_process = list(cls._loadable_file_set)

        max_workers = 4
        results: set[ImageFileData] = set()
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            for result in executor.map(process_file, files_to_process):
                    if result is not None:
                        results.add(result)
        
        result_path_list: list[str] = [result.file_path for result in results]
        load_failed_data = set(files_to_process) - set(result_path_list)
        DataContainer.set_load_failed_data(load_failed_data)
        cls._loadable_file_set.clear()
        # Update Database
        final_results = results.union(DB().get_data())
        DB().add_datas(results)
        DataContainer.add_loaded_data(final_results)

    @classmethod
    def get_loadable_count(cls, directory_path: str) -> int:
        for root, _, files in os.walk(directory_path):
            for file_name in files:
                if file_name.split('.')[-1].lower() in IMAGE_FORMATS:
                    path = process_path(os.path.join(root, file_name))
                    cls._loadable_file_set.add(path)
        # Remove already exist in database
        logger.debug(f"All File : {len(cls._loadable_file_set)}")
        db_paths = DB().get_db_paths()
        cls._loadable_file_set.difference_update(db_paths)
        count = len(cls._loadable_file_set)
        logger.debug(f"Need to Load : {count}")
        return count
    
def get_png_description(file_path) -> tuple[ImageFileData, bool]:
    with open(file_path, 'rb') as f:
        if f.read(8) != b'\x89PNG\r\n\x1a\n':
            raise ValueError("Not a valid PNG file")

        while True:
            chunk_length, chunk_type = struct.unpack(">I4s", f.read(8))
            if chunk_type == b'IEND':
                break

            # tEXt chunk
            if chunk_type == b'tEXt':
                data = f.read(chunk_length)
                parts = data.split(b'\x00', 1)
                if len(parts) == 2:
                    key, value = parts
                    key = key.decode('latin1')
                    if key == "Description":
                        value = value.decode('latin1')
                        logger.info(f"sucessfully extracted from Description : {file_path}")
                        return (ImageFileData(file_path, value), True)
                    elif key == "Comment":
                        value = value.decode('latin1')
                        prompt_data = json.loads(value)['prompt']
                        logger.info(f"sucessfully extracted from Comment : {file_path}")
                        return (ImageFileData(file_path, prompt_data), True)
            else:
                f.seek(chunk_length, 1)
            f.read(4)
    if UserSetting.check('STEALTH_MODE'):
        with Image.open(file_path) as img:
            tmp = read_info_from_image_stealth(img)
            if tmp:
                logger.info(f"Description sucessfully extracted from Stealth data : {file_path}")
                desc = json.loads(tmp)['Description']
                return (ImageFileData(file_path, desc), True)
    logger.warning(f"Description Not Found : {file_path}")
    return (None, False)