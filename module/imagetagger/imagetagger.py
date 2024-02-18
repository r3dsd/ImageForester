import os
import re
import struct
import zlib
import cv2
import numpy as np
import pandas as pd
from PIL import Image
from onnxruntime import InferenceSession
from typing import Mapping, Tuple, Dict
from tqdm import tqdm
import send2trash

from ..config import TAGGER_CONFIG
from ..user_setting import UserSetting
from ..HuggingFaceDownloader.HuggingFaceDownloader import HFDownloader
from ..logger import get_logger
from ..r3util.r3path import process_path
from ..data import DB

logger = get_logger(__name__)

class ImageTagger:
    def __init__(self) -> None:
        self.__initialized = False
        self._model, self._tags = None, None

    def _init(self) -> None:
        if self.__initialized:
            return
        self.__model_path = HFDownloader().download_model(TAGGER_CONFIG["MODEL_NAME"])
        self.__tags_path = HFDownloader().download_model(TAGGER_CONFIG["TAGS_FILE_NAME"])

        logger.info(f"Succesfully model and tags loaded!")

        self._model = InferenceSession(self.__model_path)
        self._tags = pd.read_csv(self.__tags_path)
        self.__initialized = True

    # noinspection PyUnresolvedReferences
    def make_square(self, img, target_size):
        old_size = img.shape[:2]
        desired_size = max(old_size)
        desired_size = max(desired_size, target_size)

        delta_w = desired_size - old_size[1]
        delta_h = desired_size - old_size[0]
        top, bottom = delta_h // 2, delta_h - (delta_h // 2)
        left, right = delta_w // 2, delta_w - (delta_w // 2)

        color = [255, 255, 255]
        return cv2.copyMakeBorder(
            img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color
        )

    # noinspection PyUnresolvedReferences
    def smart_resize(self, img, size):
        # Assumes the image has already gone through make_square
        if img.shape[0] > size:
            img = cv2.resize(img, (size, size), interpolation=cv2.INTER_AREA)
        elif img.shape[0] < size:
            img = cv2.resize(img, (size, size), interpolation=cv2.INTER_CUBIC)
        else:  # just do nothing
            pass

        return img

    def _calculation(self, image: Image.Image) -> pd.DataFrame:
        self._init()

        _, height, _, _ = self._model.get_inputs()[0].shape
        image = image.convert("RGBA")
        new_image = Image.new("RGBA", image.size, "WHITE")
        new_image.paste(image, mask=image)
        image = new_image.convert("RGB")
        image = np.asarray(image)
        image = image[:, :, ::-1]
        image = self.make_square(image, height)
        image = self.smart_resize(image, height)
        image = image.astype(np.float32)
        image = np.expand_dims(image, 0)

        input_name = self._model.get_inputs()[0].name
        label_name = self._model.get_outputs()[0].name
        confidence = self._model.run([label_name], {input_name: image})[0]

        full_tags = self._tags[["name", "category"]].copy()
        full_tags["confidence"] = confidence[0]

        return full_tags

    def interrogate(self, image: Image) -> Tuple[Dict[str, float], Dict[str, float]]:
        full_tags = self._calculation(image)
        ratings = dict(
            full_tags[full_tags["category"] == 9][["name", "confidence"]].values
        )
        tags = dict(
            full_tags[full_tags["category"] != 9][["name", "confidence"]].values
        )
        return ratings, tags

    def tag_image(
        self,
        image: Image.Image,
        threshold: float,
        use_spaces: bool,
        use_escape: bool,
        include_ranks: bool,
        score_descend: bool,
    ) -> Tuple[Mapping[str, float], str, Mapping[str, float]]:
        ratings, tags = self.interrogate(image)

        filtered_tags = {
            tag: score for tag, score in tags.items() if score >= threshold
        }

        text_items = []
        tags_pairs = filtered_tags.items()

        if score_descend:
            tags_pairs = sorted(tags_pairs, key=lambda x: (-x[1], x[0]))
        for tag, score in tags_pairs:
            tag_outformat = tag
            if use_spaces:
                tag_outformat = tag_outformat.replace("_", " ")
            if use_escape:
                RE_SPECIAL = re.compile(r"([\\()])")
                tag_outformat = re.sub(RE_SPECIAL, r"\\\1", tag_outformat)
            text_items.append(tag_outformat)
        output_text = ", ".join(text_items)
        
        return ratings, output_text, filtered_tags
    
    def _has_description(self, image) -> bool:
        try:
            image.info["Description"]
            return True
        except KeyError:
            return False

    def _add_text_chunk(self, png_file_path, text_key, text_value):
        png_file_path = process_path(png_file_path)
        
        with open(png_file_path, 'rb') as f:
            original_data = f.read()
        
        if original_data[:8] != b'\x89PNG\r\n\x1a\n':
            raise ValueError("Not a valid PNG file")
        
        ihdr_end = 8 + 4 + 4 + 13 + 4
        
        text_data = text_key.encode('latin1') + b'\x00' + text_value.encode('latin1')
        text_chunk_length = struct.pack(">I", len(text_data))
        text_chunk_type = b'tEXt'
        text_chunk_crc = struct.pack(">I", zlib.crc32(text_chunk_type + text_data) & 0xffffffff)
        text_chunk = text_chunk_length + text_chunk_type + text_data + text_chunk_crc
        
        new_png_data = original_data[:ihdr_end] + text_chunk + original_data[ihdr_end:]

        save_directory = os.path.join(os.path.dirname(png_file_path), "taged_images")
        os.makedirs(save_directory, exist_ok=True)

        new_file_path = os.path.join(save_directory, os.path.basename(png_file_path).rsplit('.', 1)[0] + "_with_tags.png")
        counter = 1
        while os.path.exists(new_file_path):
            new_file_path = os.path.join(save_directory, os.path.basename(png_file_path).rsplit('.', 1)[0] + f"_with_tags_{counter}.png")
            counter += 1

        with open(new_file_path, 'wb') as f:
            f.write(new_png_data)

        return process_path(new_file_path)

    def auto_tagging(self, source_file_path_list: list[str], 
                    confidence=TAGGER_CONFIG["IMAGE_TAGGER_CONFIDENCE_THRESHOLD"], 
                    use_spaces=True, use_escape=True, 
                    include_ranks=False, 
                    score_descend=True) -> list[tuple]:
        logger.info(f"Auto Tagging Started")
        results: list[tuple] = []
        for file_path in source_file_path_list:
            image = Image.open(file_path)
            if self._has_description(image):
                logger.error(f"Description already exists: {file_path}")
                continue
            else:
                ratings, tags_text, filtered_tags = self.tag_image(
                    image,
                    confidence,
                    use_spaces,
                    use_escape,
                    include_ranks,
                    score_descend,
                )
                new_file_path = self._add_text_chunk(file_path, "Description", tags_text)
                results.append((new_file_path, tags_text))
                logger.info(f"Tags added to {file_path}")
        logger.info(f"Auto Tagging Finished")
        return results

def add_tag(png_file_path, text_value):
    png_file_path = process_path(png_file_path)

    logger.info(f"Adding tag to {png_file_path}")
    key = "Description"
    with open(png_file_path, 'rb') as f:
        original_data = f.read()
    
    if original_data[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError("Not a valid PNG file")
    
    ihdr_end = 8 + 4 + 4 + 13 + 4
    
    text_data = key.encode('latin1') + b'\x00' + text_value.encode('latin1')
    text_chunk_length = struct.pack(">I", len(text_data))
    text_chunk_type = b'tEXt'
    text_chunk_crc = struct.pack(">I", zlib.crc32(text_chunk_type + text_data) & 0xffffffff)
    text_chunk = text_chunk_length + text_chunk_type + text_data + text_chunk_crc
    
    new_png_data = original_data[:ihdr_end] + text_chunk + original_data[ihdr_end:]
    save_directory = os.path.join(os.path.dirname(png_file_path), "taged_images")
    os.makedirs(save_directory, exist_ok=True)
    new_file_path = os.path.join(save_directory, os.path.basename(png_file_path).rsplit('.', 1)[0] + "_with_tags.png")
    counter = 1
    while os.path.exists(new_file_path):
        new_file_path = os.path.join(save_directory, os.path.basename(png_file_path).rsplit('.', 1)[0] + f"_with_tags_{counter}.png")
        counter += 1
    with open(new_file_path, 'wb') as f:
        f.write(new_png_data)
    logger.info(f"Succesfully added tag to {png_file_path}")
    return new_file_path