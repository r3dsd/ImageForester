from .imagefiledata import ImageFileData

from ..logger import get_logger

logger = get_logger(__name__)

class DataContainer:
    _loaded_data: set[ImageFileData] = set()
    loaded_data_count: int = 0

    _load_failed_data: set[str] = set() # No Description Files
    load_failed_data_count: int = 0

    _searched_data: set[ImageFileData] = set()
    searched_data_count: int = 0

    _search_keywords: list[str] = []

    @classmethod
    def get_search_keywords(cls) -> list[str]:
        return cls._search_keywords
    
    @classmethod
    def set_search_keywords(cls, keywords: list[str]) -> None:
        cls._search_keywords.clear()
        cls._search_keywords.extend(keywords)

    @classmethod
    def get_loaded_data(cls) -> set[ImageFileData]:
        return cls._loaded_data
    
    @classmethod
    def set_loaded_data(cls, data: set[ImageFileData]) -> None:
        if len(cls._loaded_data) > 0:
            cls._loaded_data.clear()
        cls._loaded_data = data
        cls.loaded_data_count = len(data)
        logger.debug(f"Loaded data count: {cls.loaded_data_count}")

    @classmethod
    def delete_loaded_data(cls, data: set[ImageFileData]) -> None:
        before_count = cls.loaded_data_count
        cls._loaded_data.difference_update(data)
        cls.loaded_data_count = len(cls._loaded_data)
        logger.debug(f"Delete loaded data count: {before_count} -> {cls.loaded_data_count}")

    @classmethod
    def get_searched_data(cls) -> set[ImageFileData]:
        return cls._searched_data
    
    @classmethod
    def set_searched_data(cls, data: set[str]) -> None:
        if len(cls._searched_data) > 0:
            cls._searched_data.clear()
        cls._searched_data = data
        cls.searched_data_count = len(data)

    @classmethod
    def set_load_failed_data(cls, data: set[str]) -> None:
        if len(cls._load_failed_data) > 0:
            cls._load_failed_data.clear()
        cls._load_failed_data = data
        cls.load_failed_data_count = len(data)
        logger.debug(f"No Description File count: {cls.load_failed_data_count}")

    @classmethod
    def get_load_failed_data(cls) -> set[str]:
        logger.debug(f"No Description File count: {cls._load_failed_data}")
        return cls._load_failed_data
    
    @classmethod
    def clear_load_failed_data(cls) -> None:
        cls._load_failed_data.clear()
        cls.load_failed_data_count = 0

    @classmethod
    def clear(cls) -> None:
        cls._loaded_data.clear()
        cls.loaded_data_count = 0

    @classmethod
    def has_load_failed_data(cls) -> bool:
        return cls.load_failed_data_count > 0