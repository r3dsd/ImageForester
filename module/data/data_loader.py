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
from ..logger import get_logger

logger = get_logger(__name__)

class DataLoader:
    _loadable_file_list: list[str] = [] # str : file_path

    @classmethod
    def load_using_multi(cls) -> None:
        """
        Load image from _loadable_file_list
        """
        DataContainer.clear()

        def process_file(file_path) -> ImageFileData:
            image_file_data, is_acessable = get_png_description(file_path)
            if is_acessable:
                image_file_data.process_file_tags()
                return image_file_data
            return None
        
        files_to_process = cls._loadable_file_list

        max_workers = os.cpu_count()
        results = set()
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            for result in executor.map(process_file, files_to_process):
                    if result is not None:
                        results.add(result)
        cls._loadable_file_list.clear()
        DataContainer.set_loaded_data(results)

    @classmethod
    def get_loadable_count(cls, directory_path: str) -> int:
        count = 0
        for root, _, files in os.walk(directory_path):
            for file_name in files:
                if file_name.split(".")[-1] in IMAGE_FORMATS:
                    cls._loadable_file_list.append(os.path.join(root, file_name))
                    count += 1
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
    if UserSetting.get('STEALTH_MODE') == 'True':
        with Image.open(file_path) as img:
            tmp = read_info_from_image_stealth(img)
            if tmp:
                logger.info(f"sucessfully extracted from Stealth data : {file_path}")
                desc = json.loads(tmp)['Description']
                return (ImageFileData(file_path, desc), True)
    logger.warning(f"Description Not Found : {file_path}")
    return (None, False)

def check_is_image(file_name: str) -> bool:
    return file_name.split(".")[-1] in IMAGE_FORMATS

