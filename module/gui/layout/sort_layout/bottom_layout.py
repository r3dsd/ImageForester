from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt

from ....data import DataStorage, ImageFileData
from ...factory import DialogFactory, PopupFactory
from ....r3util.r3lib import HighlightingText
from ....user_setting import SaveModeEnum
from ....config import FILEMANAGER_CONFIG
from ...guisignalmanager import GUISortSignalManager, GUISignalManager
from ...widgets.path_selector import PathSelector

from ....logger import get_logger

logger = get_logger(__name__)

class BottomLayout(QVBoxLayout):
    def __init__(self, mainwindow, datastorage: DataStorage):
        super().__init__()
        self._mainwindow = mainwindow
        self._datastorage: DataStorage = datastorage

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
        self.load_count_label.setText("Loaded : 0")
        self.load_count_label.setMinimumHeight(25)
        self.load_count_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.load_count_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        bar_layout.addWidget(self.load_count_label)

        self.path_selector = PathSelector(self._mainwindow, use_DB=False, datastorage=self._datastorage)
        bar_layout.addWidget(self.path_selector, 8)

        self.option_button = QPushButton("Short Cut Options")
        self.option_button.setToolTip("Open User Setting (Simple Mode)")
        self.option_button.setMinimumHeight(25)
        self.option_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        bar_layout.addWidget(self.option_button)

        self.addLayout(bar_layout)

    def _initsignal(self):
        self.option_button.clicked.connect(self.__on_option_button_clicked)
        self.path_selector.on_load_complete.connect(self._on_load_complete)

        sort_signal_manager = GUISortSignalManager()
        sort_signal_manager.on_item_selection_updated.connect(self._on_item_selection_updated)
        sort_signal_manager.on_deleted_data.connect(self._on_deleted_data)
        sort_signal_manager.on_select_list_saved.connect(self._on_select_list_saved)
        sort_signal_manager.on_search_completed.connect(self._on_search_completed)

    def __on_option_button_clicked(self):
        DialogFactory(self._mainwindow).create_setting_dialog()

    def _on_item_selection_updated(self, image_data: ImageFileData):
        highlight_text = HighlightingText(image_data.file_tags_text, self._datastorage.get_search_keywords())
        self.info_console.setText(f"<b>Tags</b>: {highlight_text}")

    def _on_select_list_saved(self, mode: SaveModeEnum):
        if mode == SaveModeEnum.COPY:
            self.info_console.setText(f"Successfully copied {self._datastorage.get_loaded_data_count()} images to the {FILEMANAGER_CONFIG['FINAL_SAVE_FOLDER_PATH']}")
        elif mode == SaveModeEnum.MOVE:
            self.info_console.setText(f"Successfully moved {self._datastorage.get_loaded_data_count()} images to the {FILEMANAGER_CONFIG['FINAL_SAVE_FOLDER_PATH']}")
            self._update_count_label()

    def _on_load_complete(self):
        count = self._datastorage.get_loaded_data_count()
        if count == 0:
            PopupFactory.show_info_message(self._mainwindow, "No loadable images.")
            return
        self.info_console.setText(f"Successfully loaded {count} images.")
        self.load_count_label.setText(f"Loaded {count}")
        GUISignalManager().emit_on_load_complete()

    def _update_count_label(self, count):
        self.load_count_label.setText(f"Loaded {count}")

    def _on_deleted_data(self, count):
        self.load_count_label.setText(f"Loaded {self._datastorage.get_loaded_data_count()}")

    def _on_search_completed(self, _, count):
        self.info_console.setText(f"Search Completed. {count} images found.")