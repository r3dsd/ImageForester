from PyQt5.QtWidgets import QBoxLayout, QLabel, QPushButton, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt
from ...data.data_container import DataContainer
from ..guisignalmanager import GUISignalManager
from ..factory.PopupFactory import PopupFactory
from ..factory.DialogFactory import DialogFactory
from ...data.imagefiledata import ImageFileData
from ..widgets.path_selector import PathSelector
from ...r3util.r3lib import HighlightingText
from ...user_setting import Savemode
from ...config import FILEMANAGER_CONFIG

class BottomLayout(QBoxLayout):
    def __init__(self, mainwindow):
        super().__init__(QBoxLayout.TopToBottom)
        self._mainwindow = mainwindow

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

        self.path_selector = PathSelector(self._mainwindow)
        bar_layout.addWidget(self.path_selector, 8)

        self.option_button = QPushButton("Short Cut Options")
        self.option_button.setToolTip("Open User Setting (Simple Mode)")
        self.option_button.setMinimumHeight(25)
        self.option_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        bar_layout.addWidget(self.option_button)

        self.addLayout(bar_layout)

    def _initsignal(self):
        self.option_button.clicked.connect(self._on_option_button_clicked)
        GUISignalManager().on_item_selection_updated.connect(self._on_item_selection_updated)
        GUISignalManager().on_load_complete.connect(self._on_load_complete)
        GUISignalManager().on_load_image_empty.connect(self._on_load_image_empty)
        GUISignalManager().on_search_list_send2trash.connect(self._on_search_list_send2trash)
        GUISignalManager().on_select_list_save.connect(self._on_select_list_save)

    def _on_option_button_clicked(self):
        DialogFactory(self._mainwindow).create_setting_dialog()

    def _on_item_selection_updated(self, image_data: ImageFileData):
        highlight_text = HighlightingText(image_data.file_tags_text, DataContainer.get_search_keywords())
        self.info_console.setText(f"<b>Tags</b>: {highlight_text}")

    def _on_load_complete(self):
        self.load_count_label.setText(f"Loaded {DataContainer.loaded_data_count}")
        self.info_console.setText(f"Successfully loaded {DataContainer.loaded_data_count} images.")

    def _on_load_image_empty(self):
        PopupFactory.show_info_message(self._mainwindow, "No loadable images in the selected folder.")
        self.load_count_label.setText("Loaded Image : 0")

    def _on_search_list_send2trash(self):
        self.info_console.setText(f"Successfully moved {DataContainer.loaded_data_count} images to the trash. <br> You can restore it in the trash.")
        self.load_count_label.setText(f"Loaded {DataContainer.loaded_data_count}")

    def _on_select_list_save(self, mode: Savemode):
        if mode == Savemode.Copy:
            self.info_console.setText(f"Successfully copied {DataContainer.loaded_data_count} images to the {FILEMANAGER_CONFIG['FINAL_SAVE_FOLDER_PATH']}")
        elif mode == Savemode.Move:
            self.info_console.setText(f"Successfully moved {DataContainer.loaded_data_count} images to the {FILEMANAGER_CONFIG['FINAL_SAVE_FOLDER_PATH']}")
            self.load_count_label.setText(f"Loaded {DataContainer.loaded_data_count}")