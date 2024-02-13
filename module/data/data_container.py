from .imagefiledata import ImageFileData

class DataContainer:
    _loaded_data: set[ImageFileData] = set()
    loaded_data_count: int = 0

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
    def clear(cls) -> None:
        cls._loaded_data.clear()
        cls.loaded_data_count = 0