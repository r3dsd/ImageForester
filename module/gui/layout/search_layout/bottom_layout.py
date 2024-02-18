from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt

from ....data import DataStorage, ImageFileData
from ...factory.PopupFactory import PopupFactory
from ...factory.DialogFactory import DialogFactory
from ....r3util.r3lib import HighlightingText
from ....user_setting import SaveModeEnum
from ....config import FILEMANAGER_CONFIG
from ...guisignalmanager import GUISearchSignalManager, GUISignalManager
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
        self.load_count_label = QLabel("Loaded : 0")
        self.load_count_label.setMinimumHeight(25)
        self.load_count_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.load_count_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        bar_layout.addWidget(self.load_count_label)

        self.path_selector = PathSelector(self._mainwindow, use_DB=True, datastorage=self._datastorage)
        bar_layout.addWidget(self.path_selector, 8)

        self.database_connect_button = QPushButton("Database Connect")
        self.database_connect_button.setToolTip("Connect to the database")
        self.database_connect_button.setMinimumHeight(25)
        self.database_connect_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        bar_layout.addWidget(self.database_connect_button)

        self.option_button = QPushButton("Short Cut Options")
        self.option_button.setToolTip("Open User Setting (Simple Mode)")
        self.option_button.setMinimumHeight(25)
        self.option_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        bar_layout.addWidget(self.option_button)

        self.addLayout(bar_layout)

    def _initsignal(self):
        self.option_button.clicked.connect(self.__on_option_button_clicked)
        self.database_connect_button.clicked.connect(self.__on_database_connect_button_clicked)
        self.path_selector.on_load_complete.connect(self._on_load_complete)

        search_signal_manager = GUISearchSignalManager()
        search_signal_manager.on_item_selection_updated.connect(self._on_item_selection_updated)
        search_signal_manager.on_deleted_data.connect(self._on_deleted_data)
        search_signal_manager.on_select_list_saved.connect(self._on_select_list_saved)
        search_signal_manager.on_search_completed.connect(self._on_search_completed)
        search_signal_manager.on_auto_database_load_started.connect(self._on_database_load_started)
        search_signal_manager.on_auto_database_load_finished.connect(self._on_database_load_finished)
        
        GUISignalManager().on_tag_added.connect(self._on_tag_added)

    def __on_option_button_clicked(self):
        DialogFactory(self._mainwindow).create_setting_dialog()

    def __on_database_connect_button_clicked(self):
        self._on_database_load_started()
        result = self._datastorage.load_from_DB()
        if not result:
            self.path_selector.set_path_label("Succesfully connected to the database.")
            PopupFactory.show_warning_message(self._mainwindow, "Database is empty.")
            self.info_console.setText("Database is empty. you can load another way. (e.g. Load from folder)")
            return
        self._on_database_load_finished()

    def _on_item_selection_updated(self, image_data: ImageFileData):
        highlight_text = HighlightingText(image_data.file_tags_text, self._datastorage.get_search_keywords())
        self.info_console.setText(f"<b>Tags</b>: {highlight_text}")

    def _on_select_list_saved(self, mode: SaveModeEnum):
        if mode == SaveModeEnum.COPY:
            count = self._datastorage.get_loaded_data_count()
            self.info_console.setText(f"Successfully copied {count} images to the {FILEMANAGER_CONFIG['FINAL_SAVE_FOLDER_PATH']}")
            self._update_count_label(count)
        elif mode == SaveModeEnum.MOVE:
            self.info_console.setText(f"Successfully moved {count} images to the {FILEMANAGER_CONFIG['FINAL_SAVE_FOLDER_PATH']}")
            self._update_count_label(count)

    def _on_load_complete(self):
        count = self._datastorage.get_loaded_data_count()
        if count == 0:
            PopupFactory.show_info_message(self._mainwindow, "No loadable images.")
            return
        self.info_console.setText(f"Successfully loaded {count} images.")
        self.load_count_label.setText(f"Loaded {count}")

    def _update_count_label(self, count):
        self.load_count_label.setText(f"Loaded {count}")

    def _on_deleted_data(self, count : int): # count is deleted count
        self.load_count_label.setText(f"Loaded {self._datastorage.get_loaded_data_count()}")

    def _on_database_load_started(self):
        self.path_selector.set_path_label("Connecting to the database...")
        self.info_console.setText("Loading images from the database...")

    def _on_database_load_finished(self):
        logger.debug(f"Database load finished. {self._datastorage}")
        count = self._datastorage.get_loaded_data_count()
        self.path_selector.set_path_label(f"Succesfully connected to the database. Loaded {count} images.")
        self.info_console.setText(f"Successfully loaded {count} images")
        self.load_count_label.setText(f"Loaded {count}")
        GUISignalManager().emit_on_load_complete(self._datastorage.get_no_tag_data())

    def _on_search_completed(self, _, count):
        self.info_console.setText(f"Search Completed. {count} images found.")

    def _on_tag_added(self, data, count):
        self._datastorage.add_loaded_data(data)
        self._datastorage.clear_no_tag_data()
        self.info_console.setText(f"Successfully added tags to {count} images.")
        self._update_count_label(self._datastorage.get_loaded_data_count())