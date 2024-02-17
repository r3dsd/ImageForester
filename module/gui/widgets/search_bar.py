from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton
from PyQt5.QtCore import pyqtSignal

from ...searchmanager.search_manager import SearchManager
from ...data import DataStorage
from ..factory import PopupFactory

from ...logger import get_logger

logger = get_logger(__name__)

class SearchBar(QWidget):
    on_search_completed = pyqtSignal(object, int)
    def __init__(self, datastorage: DataStorage):

        self._datastorage: DataStorage = datastorage

        super().__init__()

        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Search with tags...")
        self.input_field.setFixedHeight(25)
        layout.addWidget(self.input_field)

        self.search_button = QPushButton("Search")
        self.search_button.setFixedHeight(25)
        layout.addWidget(self.search_button)

        self.search_button.clicked.connect(self.search_request)
        self.input_field.returnPressed.connect(self.search_request)

    def search_request(self):
        keywords = [x.strip() for x in self.input_field.text().split(",") if x.strip() != ""]
        if self._datastorage.get_loaded_data_count() == 0:
            PopupFactory.show_info_message(self, "You must load images first. Please select a folder to load images.")
            return
        if len(keywords) == 0:
            PopupFactory.show_info_message(self, "Please input search keywords.")
            return
        self._datastorage.set_search_keywords(keywords)
        logger.info(f"Start searching with keywords: {keywords}... in {self._datastorage.name}")
        result = SearchManager.search(self._datastorage.get_loaded_data(), keywords)
        # self._datastorage.set_searched_data(result) not implemented yet (TODO : Update connectableList.py, filemanager.py delete_loaded_data method to delete searched data.)
        count = len(result)
        self.on_search_completed.emit(result, count)
