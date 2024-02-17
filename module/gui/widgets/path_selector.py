from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QSizePolicy, QFileDialog, QDialog
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from ..worker import ExtendedWorker
from ...data import DataLoader
from ..factory.DialogFactory import DialogFactory
from ...user_setting import UserSetting

from ...logger import get_logger

logger = get_logger(__name__)

class PathSelector(QWidget):
    on_load_complete = pyqtSignal()

    def __init__(self, mainwindow, use_DB=False, datastorage=None):
        super().__init__(mainwindow)
        self.use_DB = use_DB
        self.datastorage = datastorage
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
        self.worker = ExtendedWorker(DataLoader.get_loadable_count, sourcepath, self.use_DB)
        self.worker.result.connect(self._on_loadable_counting_finished)
        self.worker.finished.connect(lambda: logger.info("worker finished."))
        self.worker.start()

    def set_path_label(self, text):
        self.path_label.setText(text)

    def _on_loadable_counting_finished(self, count):
        if count == 0:
            self._on_load_complete(0)
            return
        
        if UserSetting.get('AUTO_LOAD') == True:
            logger.info("Auto Load Enabled. Loading Images...")
            self._image_load()
            return
        
        result = DialogFactory(self).create_load_confirm_dialog(count).exec_()
        if result == QDialog.Accepted:
            self._image_load()

    def _image_load(self):
        self.worker = ExtendedWorker(DataLoader.load_using_multi, self.use_DB, self.datastorage)
        self.worker.finished.connect(self._on_load_complete)
        self.worker.start()

    def _on_load_complete(self):
        self.on_load_complete.emit()
        logger.info("Image Load Complete.") 