from .imagefiledata import ImageFileData
from .database import DB

from ..logger import get_logger
import traceback

logger = get_logger(__name__)

class DataStorage:
    def __init__(self, name: str = "DataStorage"):
        self.name = name
        logger.debug(f"Create DataStorage: {name}")
        self._loaded_data = set()
        self._loaded_data_count = 0
        self._load_failed_data = set()
        self._load_failed_data_count = 0
        self._searched_data = set()
        self._searched_data_count = 0
        self._search_keywords = []

    def __str__(self):
        return f"[{self.name}] - Loaded: {self._loaded_data_count}, No Description: {self._load_failed_data_count}, Searched: {self._searched_data_count}"
    
    def clear(self) -> None:
        self._loaded_data.clear()
        self._loaded_data_count = 0
        self._load_failed_data.clear()
        self._load_failed_data_count = 0
        self._searched_data.clear()
        self._searched_data_count = 0
        self._search_keywords.clear()
        logger.debug(f"{self.name} - Data cleared")
    
    # loaded data methods
    
    def set_loaded_data(self, data: set[ImageFileData]) -> None:
        if len(self._loaded_data) > 0:
            self._loaded_data.clear()
        self._loaded_data = data
        self._loaded_data_count = len(data)
        logger.debug(f"{self}")

    def get_loaded_data(self) -> set[ImageFileData]:
        return self._loaded_data
    
    def get_loaded_data_count(self) -> int:
        return self._loaded_data_count
    
    def delete_loaded_data(self, data: set[ImageFileData]) -> None:
        try:
            if type(data) != set:
                data = set(data)
            DB().delete_datas(data)
            before_count = self._loaded_data_count
            self._loaded_data.difference_update(data)
            self._loaded_data_count = len(self._loaded_data)
            logger.debug(f"[{self.name}] Delete loaded data: {before_count} -> {self._loaded_data_count}")
        except Exception as e:
            logger.error(f"Error: {e}\n{traceback.format_exc()}")

    def add_loaded_data(self, data) -> None:
        before_count = self._loaded_data_count
        db = DB()
        if isinstance(data, ImageFileData):
            self._loaded_data.add(data)
            db.add_data(data)
        else:
            set_data = data if isinstance(data, set) else set(data)
            self._loaded_data.update(set_data)
            db.add_datas(set_data)
        self._loaded_data_count = len(self._loaded_data)
        logger.debug(f"[{self.name}] Add loaded data: {before_count} -> {self._loaded_data_count}")

    # load failed data methods
    
    def set_load_failed_data(self, data: set[str]) -> None:
        if len(self._load_failed_data) > 0:
            self._load_failed_data.clear()
        self._load_failed_data = data
        self._load_failed_data_count = len(data)
        logger.debug(f"{self}")

    def get_load_failed_data(self) -> set[str]:
        logger.debug(f"{self.name} - No Description count: {self._load_failed_data_count}")
        return self._load_failed_data
    
    def get_load_failed_data_count(self) -> int:
        return self._load_failed_data_count
    
    def delete_load_failed_data(self, data: set[str]) -> None:
        if type(data) != set:
            data = set(data)
        before_count = self._load_failed_data_count
        self._load_failed_data.difference_update(data)
        self._load_failed_data_count = len(self._load_failed_data)
        logger.debug(f"[{self.name}] Remove load failed data: {before_count} -> {self._load_failed_data_count}")

    def clear_load_failed_data(self) -> None:
        self._load_failed_data.clear()
        self._load_failed_data_count = 0
    
    def has_load_failed_data(self) -> bool:
        return self._load_failed_data_count > 0
    
    # searched data methods
        
    def set_searched_data(self, data: set[str]) -> None:
        if len(self._searched_data) > 0:
            self._searched_data.clear()
        self._searched_data = data
        self._searched_data_count = len(data)

    def get_searched_data(self) -> set[ImageFileData]:
        return self._searched_data
    
    def delete_searched_data(self, data: set[ImageFileData]) -> None:
        try:
            before_searched_count = len(self._searched_data)
            self._searched_data.difference_update(data)
            after_searched_count = len(self._searched_data)
            logger.debug(f"[{self.name}] Delete searched data: {before_searched_count} -> {after_searched_count}")

            before_loaded_count = len(self._loaded_data)
            self._loaded_data.difference_update(data)
            after_loaded_count = len(self._loaded_data)
            logger.debug(f"[{self.name}] Update loaded data after deleting searched data: {before_loaded_count} -> {after_loaded_count}")
        except Exception as e:
            logger.error(f"Error deleting searched data: {e}\n{traceback.format_exc()}")


    def get_searched_data_count(self) -> int:
        return self._searched_data_count
    
    # search keywords methods

    def set_search_keywords(self, keywords: list[str]) -> None:
        self._search_keywords.clear()
        self._search_keywords.extend(keywords)

    def get_search_keywords(self) -> list[str]:
        return self._search_keywords
    
class TaggerDataStorage(DataStorage):
    pass

class SearchDataStorage(DataStorage):
    pass

class SortDataStorage(DataStorage):
    pass