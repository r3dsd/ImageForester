from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QSizePolicy, QFileDialog, QDialog
from PyQt5.QtCore import Qt, QTimer
from ..worker import ExtendedWorker
from ...data.data_loader import DataLoader
from ..widgets.popupFactory import PopupFactory
from ...user_setting import UserSetting
from ..guisignalmanager import GUISignalManager

from ...logger import get_logger

logger = get_logger(__name__)

class PathSelector(QWidget):
    def __init__(self, mainwindow):
        super().__init__(mainwindow)
        self.mainwindow = mainwindow
        self._init_ui()

    def _init_ui(self):
        bar_layout = QHBoxLayout()
        self.setLayout(bar_layout)
        bar_layout.setContentsMargins(0, 0, 0, 0)

        self.path_label = QLabel()
        self.path_label.setText("Selected Path: ")
        self.path_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.path_label.setMinimumHeight(25)
        self.path_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        bar_layout.addWidget(self.path_label, 8)

        self.path_select_button = QPushButton("Select Path")
        self.path_select_button.setMinimumHeight(25)
        self.path_select_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        bar_layout.addWidget(self.path_select_button)

        self.path_select_button.clicked.connect(self._on_path_select_button_clicked)

    def _on_path_select_button_clicked(self):
        sourcepath = QFileDialog.getExistingDirectory(self.mainwindow, 'Select Source Path')
        if sourcepath:
            self.path_label.setText(f"Selected Path: {sourcepath}")
            logger.info(f"worker started. Counting Loadable Images in {sourcepath}...")
            QTimer.singleShot(0, lambda: self._start_loadable_count_worker(sourcepath))

    def _start_loadable_count_worker(self, sourcepath):
        self.worker = ExtendedWorker(DataLoader.get_loadable_count, sourcepath)
        self.worker.result.connect(self._on_loadable_counting_finished)
        self.worker.finished.connect(lambda: logger.info("worker finished."))
        self.worker.start()

    def _on_loadable_counting_finished(self, count):
        if count == 0:
            GUISignalManager().emit_on_load_image_empty()
            return
        
        if UserSetting.get('DONT_SHOW_LOAD_CONFIRM') == True:
            logger.info("Auto Load Enabled. Loading Images...")
            self._image_load()
            return
        
        result = PopupFactory(self).create_load_confirm_popup(count).exec_()
        if result == QDialog.Accepted:
            self._image_load()

    def _image_load(self):
        self.worker = ExtendedWorker(DataLoader.load_using_multi)
        self.worker.finished.connect(self._on_load_complete)
        self.worker.start()

    def _on_load_complete(self):
        GUISignalManager().on_load_complete.emit()
        logger.info("Image Load Complete.")