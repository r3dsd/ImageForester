import json
import os
import struct
import concurrent.futures
from PIL import Image
from .data_storage import DataStorage
from .stealth_pnginfo import read_info_from_image_stealth
from ..constants import IMAGE_FORMATS
from ..user_setting import UserSetting
from .imagefiledata import ImageFileData
from ..logger import get_logger
from ..r3util.r3path import process_path
from ..data.database import DB

logger = get_logger(__name__)

class DataLoader:
    _loadable_files: set[str] = set()

    @classmethod
    def load_using_multi(cls, datastorage : DataStorage = None) -> None:
        """
        Load image from _loadable_file_list
        """
        def process_file(file_path: str) -> ImageFileData:
            image_file_data, is_acessable = get_png_description(file_path)
            if is_acessable:
                image_file_data.process_file_tags()
                return image_file_data
            return None
        
        files_to_process = list(cls._loadable_files)

        max_workers = 4
        logger.info(f"Found {len(cls._loadable_files)} Images. [thread={max_workers}] [DataStorage={datastorage}]")
        results: set[ImageFileData] = set()
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            for result in executor.map(process_file, files_to_process):
                    if result is not None:
                        results.add(result)
        result_path_list: list[str] = [result.file_path for result in results]
        load_failed_data = set(files_to_process) - set(result_path_list)
        logger.info(f"Load Complete. {len(results)} Images Loaded. {len(load_failed_data)} Images Failed to Load")

        datastorage.set_load_failed_data(load_failed_data)
        datastorage.set_loaded_data(results)
        cls._loadable_files.clear()


    @classmethod
    def get_loadable_count(cls, directory_path: str, use_DB=False) -> int:
        logger.debug(f"Counting Loadable Images in {directory_path}... (Use_DB={use_DB})")
        cls._loadable_files = {
            process_path(os.path.join(root, file_name))
            for root, _, files in os.walk(directory_path)
            for file_name in files
            if file_name.split('.')[-1].lower() in IMAGE_FORMATS
        }
        logger.debug(f"Total {len(cls._loadable_files)} images found")
        # If using database, remove files already present in database
        if use_DB:
            logger.debug("Using DB... Removing already exist in DB")
            existing_in_db = DB("DataLoader").get_db_paths()
            cls._loadable_files.difference_update(existing_in_db)

        count = len(cls._loadable_files)
        logger.debug(f"need to load {count} images")
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