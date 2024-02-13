from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class ImageFileData:
    file_path: str
    file_tags_text: str
    file_tags_list: Optional[List[str]] = field(default=None, init=False)

    def process_file_tags(self):
        self.file_tags_list = [tag.strip().lower() for tag in self.file_tags_text.split(",")]

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