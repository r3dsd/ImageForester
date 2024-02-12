from PyQt5.QtWidgets import QBoxLayout, QLineEdit, QPushButton

class TopLayout(QBoxLayout):
    def __init__(self, mainwindow):
        super().__init__(QBoxLayout.LeftToRight)
        self.mainwindow = mainwindow
        self._initUI()

    def _initUI(self):
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Search with tags...")
        self.input_field.setFixedHeight(30)
        self.addWidget(self.input_field)

        self.search_button = QPushButton("Search")
        self.search_button.setFixedHeight(30)
        self.addWidget(self.search_button)

    def search_request(self):
        print(f"Search request: {self.input_field.text()}")