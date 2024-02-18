from .imagefiledata import ImageFileData, ImageFileDataFactory
from .database import DB

from ..logger import get_logger
import traceback

logger = get_logger(__name__)

class DataStorage:
    def __init__(self, name: str = "DataStorage"):
        self.name = name # name is DB Accesser
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

    def load_from_DB(self) -> bool:
        logger.info(f"Load Data from Database")
        data = DB(self.name).get_data()
        if len(data) == 0:
            logger.debug(f"Database is empty. No data loaded.")
            return False
        self.set_loaded_data(data)
        logger.debug(f"Load from DB: {self}")
        return True
    
    # loaded data methods
    
    def set_loaded_data(self, data: set[ImageFileData]) -> None:
        if len(self._loaded_data) > 0:
            self._loaded_data.clear()
        self._loaded_data = data
        self._loaded_data_count = len(data)
        logger.debug(f"Set Loaded Data: {self}")

    def get_loaded_data(self) -> set[ImageFileData]:
        return self._loaded_data
    
    def get_loaded_data_count(self) -> int:
        return self._loaded_data_count
    
    def delete_loaded_data(self, data: set[ImageFileData]) -> None:
        if type(data) != set:
            data = set(data)
        before_count = self._loaded_data_count
        self._loaded_data.difference_update(data)
        self._loaded_data_count = len(self._loaded_data)
        DB(self.name).delete_datas(data)
        logger.debug(f"[{self.name}] Delete loaded data: {before_count} -> {self._loaded_data_count}")

    def add_loaded_data(self, data) -> None:
        before_count = self._loaded_data_count
        if isinstance(data, ImageFileData):
            self._loaded_data.add(data)
        else:
            set_data = data if isinstance(data, set) else set(data)
            self._loaded_data.update(set_data)
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
    
    # searched data methods TODO: for future use (searched data is not used yet) need refactoring (search_list.py)
        
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
    
    def on_copy(self, target_list : list[tuple[ImageFileData, str]]) -> None:
        pass

    def on_move(self, target_list : list[tuple[ImageFileData, str]]) -> None:
        pass
    
class TaggerDataStorage(DataStorage):
    def __init__(self):
        super().__init__("Tagger Data Storage")

class SearchDataStorage(DataStorage):
    def __init__(self):
        super().__init__("Search Data Storage")

    def load_from_DB(self) -> bool:
        logger.info(f"Load Data from Database")
        data = DB(self.name).get_data()
        if len(data) == 0:
            logger.debug(f"Database is empty. No data loaded.")
            return False
        super().set_loaded_data(data)
        logger.debug(f"Load from DB: {self}")
        return True

    def set_load_failed_data(self, data: set[str]) -> None:
        super().set_load_failed_data(data)
        DB(self.name).add_no_tags_datas(data)

    def set_loaded_data(self, data: set[ImageFileData]) -> None:
        if type(data) != set:
            data = set(data)
        db = DB(self.name)
        db_data = db.get_data()
        final_results = data.union(db_data)
        super().set_loaded_data(final_results)
        logger.debug(f"Set Loaded Data: {self.name} - {len(final_results)}")
        db.add_datas(data)

    def on_copy(self, target_list : list[tuple[ImageFileData, str]]) -> None:
        db = DB(self.name)
        copy_data = [ImageFileDataFactory.create(destination, source.file_tags_text) for source, destination in target_list]
        db.add_datas(copy_data)
        self.add_loaded_data(copy_data)

    def on_move(self, target_list : list[tuple[ImageFileData, str]]) -> None:
        db = DB(self.name)
        move_data = [ImageFileDataFactory.create(destination, source.file_tags_text) for source, destination in target_list]
        db.add_datas(move_data)
        self.add_loaded_data(move_data)

class SortDataStorage(DataStorage):
    def __init__(self):
        super().__init__("Sort Data Storage")

    def set_loaded_data(self, data: set[ImageFileData]) -> None:
        super().set_loaded_data(data)
        DB(self.name).add_datas(data)
        logger.debug(f"Set Loaded Data: {self.name} - {len(data)}")

    def on_copy(self, target_list : list[tuple[ImageFileData, str]]) -> None:
        pass
    
    def on_move(self, target_list : list[tuple[ImageFileData, str]]) -> None:
        db = DB(self.name)
        db.delete_datas(target_list)