from dataclasses import dataclass, field
from typing import List, Optional
import os

from ..logger import get_logger

logger = get_logger(__name__)

@dataclass
class ImageFileData:
    file_path: str
    file_tags_text: str
    file_tags_list: Optional[List[str]] = field(default=None, init=False)
    file_name: Optional[str] = field(default=None, init=False)

    def process_file_tags(self):
        self.file_tags_list = [tag.strip().lower() for tag in self.file_tags_text.split(",")]
        self.file_name = os.path.basename(self.file_path)

    def __str__(self) -> str:
        return f"ImageFileData: {self.file_path}"
    
    def __hash__(self) -> int:
        return hash(self.file_path)
    
    def __eq__(self, other) -> bool:
        if other is None:
            return False
        if isinstance(other, self.__class__):
            return self.file_path == other.file_path
        return False
    
class ImageFileDataFactory:
    @staticmethod
    def create(file_path: str, file_tags_text: str) -> ImageFileData:
        norm_path = os.path.normpath(file_path)
        data = ImageFileData(norm_path, file_tags_text)
        data.process_file_tags()
        logger.debug(f"Create Data: {data}")
        return data
    
    @staticmethod
    def create_no_process(file_path: str, file_tags_text: str) -> ImageFileData:
        norm_path = os.path.normpath(file_path)
        data = ImageFileData(norm_path, file_tags_text)
        logger.debug(f"Create Data: {data}")
        return data