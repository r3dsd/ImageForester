from PyQt5.QtWidgets import QBoxLayout, QLabel, QPushButton, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt
from ..widgets.settingdialog import SettingDialog
from ...data.data_container import DataContainer
from ..guisignalmanager import GUISignalManager
from ...data.imagefiledata import ImageFileData
from ..widgets.path_selector import PathSelector
from ...r3util.r3lib import HighlightingText

class BottomLayout(QBoxLayout):
    def __init__(self, mainwindow):
        super().__init__(QBoxLayout.TopToBottom)
        self.mainwindow = mainwindow

        self._initUI()
        self._initsignal()

    def _initUI(self):
        self.info_console = QLabel()
        self.info_console.setAlignment(Qt.AlignLeft)
        self.info_console.setMinimumHeight(100)
        self.info_console.setTextFormat(Qt.RichText)
        self.info_console.setWordWrap(True)
        self.info_console.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.addWidget(self.info_console)

        bar_layout = QHBoxLayout()
        self.load_count_label = QLabel()
        self.load_count_label.setText("Loaded Image : 0")
        self.load_count_label.setMinimumHeight(30)
        self.load_count_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        bar_layout.addWidget(self.load_count_label, 1)

        self.path_selector = PathSelector(self.mainwindow)
        bar_layout.addWidget(self.path_selector, 8)

        self.option_button = QPushButton("Options")
        self.option_button.setMinimumHeight(30)
        bar_layout.addWidget(self.option_button, 1)

        self.addLayout(bar_layout)

    def _initsignal(self):
        self.option_button.clicked.connect(self._on_option_button_clicked)
        GUISignalManager().on_item_selection_updated.connect(self._on_item_selection_updated)
        GUISignalManager().on_load_complete.connect(self.on_load_complete)
        GUISignalManager().on_load_image_empty.connect(self.on_load_image_empty)

    def _on_option_button_clicked(self):
        SettingDialog(self.mainwindow)

    def _on_item_selection_updated(self, image_data: ImageFileData):
        highlight_text = HighlightingText(image_data.file_tags_text, DataContainer.get_search_keywords())
        self.info_console.setText(f"<b>Tags</b>: {highlight_text}")

    def on_load_complete(self):
        self.load_count_label.setText(f"Loaded Image : {DataContainer.loaded_data_count}")
        self.info_console.setText(f"Successfully loaded {DataContainer.loaded_data_count} images.")

    def on_load_image_empty(self):
        self.info_console.setText("No loadable images in the selected path.")
        self.load_count_label.setText("Loaded Image : 0")