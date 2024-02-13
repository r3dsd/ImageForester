from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton

from ...searchmanager.search_manager import SearchManager
from ..guisignalmanager import GUISignalManager
from ...data.data_container import DataContainer
from .popupFactory import PopupFactory
class SearchBar(QWidget):
    def __init__(self):
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
        if len(keywords) == 0:
            PopupFactory(self).create_popup("Warning", "Please input search keywords.").exec_()
            return
        DataContainer.set_search_keywords(keywords)
        result = SearchManager().search(keywords)
        GUISignalManager().emit_on_search_completed(result)