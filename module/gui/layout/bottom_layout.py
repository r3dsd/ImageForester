from PyQt5.QtWidgets import QBoxLayout, QLabel, QPushButton, QHBoxLayout, QSizePolicy, QDialog, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread
from ..widgets.settingdialog import SettingDialog
from ...user_setting import UserSetting
from ...data.data_loader import DataLoader
from ...data.data_container import DataContainer
from ..guisignalmanager import GUISignalManager
from ...data.imagefiledata import ImageFileData
from ..worker import Worker

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

        self.path_label = QLabel()
        self.path_label.setText("Selected Path: ")
        self.path_label.setMinimumHeight(30)
        self.path_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        bar_layout.addWidget(self.path_label, 7)

        self.path_select_button = QPushButton("Select Path")
        self.path_select_button.setMinimumHeight(30)
        bar_layout.addWidget(self.path_select_button, 1)

        self.option_button = QPushButton("Options")
        self.option_button.setMinimumHeight(30)
        bar_layout.addWidget(self.option_button, 1)

        self.save_button = QPushButton("Save")
        self.save_button.setMinimumHeight(30)
        bar_layout.addWidget(self.save_button, 1)

        self.addLayout(bar_layout)

    def _initsignal(self):
        self.option_button.clicked.connect(self._on_option_button_clicked)
        self.path_select_button.clicked.connect(self._on_path_select_button_clicked)
        GUISignalManager().on_item_selection_updated.connect(self._on_item_selection_updated)

    def _on_option_button_clicked(self):
        SettingDialog(self.mainwindow)

    def _on_item_selection_updated(self, image_data: ImageFileData):
        highlight_text = HighlightingText(image_data.file_tags_text, DataContainer.get_search_keywords())
        self.info_console.setText(f"<b>Tags</b>: {highlight_text}")

    def _on_path_select_button_clicked(self):
        sourcepath = QFileDialog.getExistingDirectory(self.mainwindow, 'Select Source Path')
        if sourcepath:
            self.path_label.setText(f"Selected Path: {sourcepath}")
            UserSetting.set('IMAGE_SOURCE_DIR', sourcepath)
            
            self.background_thread = QThread()
            self.worker = Worker(DataLoader.get_loadable_count, sourcepath)
            self.worker.moveToThread(self.background_thread)

            self.worker.result.connect(self._on_loadable_counting_finished)
            self.worker.finished.connect(self.worker.deleteLater)
            self.worker.finished.connect(self.background_thread.quit)

            self.background_thread.finished.connect(self.background_thread.deleteLater)

            self.background_thread.started.connect(self.worker.run)
            self.background_thread.start()

    def _on_loadable_counting_finished(self, count):
        LoadPopup(self.mainwindow, count).exec_()
        if LoadPopup.result:
            self.load_count_label.setText(f"Loaded Image : {DataContainer.loaded_data_count}")
            self.info_console.setText(f"Successfully loaded {DataContainer.loaded_data_count} images.")


class LoadPopup(QDialog):
    def __init__(self, parent, count):
        super().__init__(parent)
        self.setWindowTitle("Loading")
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.info_label = QLabel(f"Find {count} loadable images. Do you want to load?")
        self.info_label.setMinimumHeight(50)
        self.info_label.setContentsMargins(5, 5, 5, 5)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        button_layout = QBoxLayout(QBoxLayout.LeftToRight)
        self.load_button = QPushButton("Yes")
        self.load_button.setMinimumHeight(30)
        self.load_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.load_button.clicked.connect(self.accept)

        self.reject_button = QPushButton("No")
        self.reject_button.setMinimumHeight(30)
        self.reject_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.reject_button.clicked.connect(self.reject)

        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.layout.addWidget(self.info_label)
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.reject_button)
        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)
    
    def accept(self):
        self.result = True
        DataLoader.load_using_multi()
        super().accept()

    def reject(self):
        self.result = False
        super().reject()


def HighlightingText(text: str, keywords: list[str]):
    words = [text.strip() for text in text.split(',')]

    for i in range(len(words)):
        for keyword in keywords:
            if keyword.startswith('~'):
                if words[i] == keyword[1:]:
                    words[i] = "<span style='background-color: #0F0'>" + words[i] + "</span>"
            else:
                if keyword in words[i]:
                    words[i] = words[i].replace(keyword, "<span style='background-color: #F00'>" + keyword + "</span>")
    return ', '.join(words)