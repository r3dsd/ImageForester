from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QSizePolicy, QFileDialog, QDialog
from PyQt5.QtCore import QThread
from ..worker import Worker
from ...data.data_loader import DataLoader
from ..widgets.loadconfirmpopup import LoadConfirmPopup
from ...user_setting import UserSetting
from ..guisignalmanager import GUISignalManager

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
        self.path_label.setMinimumHeight(30)
        self.path_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        bar_layout.addWidget(self.path_label, 8)

        self.path_select_button = QPushButton("Select Path")
        self.path_select_button.setMinimumHeight(30)
        bar_layout.addWidget(self.path_select_button, 1)

        self.path_select_button.clicked.connect(self._on_path_select_button_clicked)

    
    def _on_path_select_button_clicked(self):
        sourcepath = QFileDialog.getExistingDirectory(self.mainwindow, 'Select Source Path')
        if sourcepath:
            self.path_label.setText(f"Selected Path: {sourcepath}")
            
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
        if count == 0:
            GUISignalManager().emit_on_load_image_empty()
            return
        
        if UserSetting.get('DONT_SHOW_LOAD_CONFIRM') == True:
            print("Auto Load Confirm is Enabled. Loading...")
            self._image_load()
            return
        
        result = LoadConfirmPopup(self.mainwindow, count).exec_()
        if result == QDialog.Accepted:
            self._image_load()

    def _image_load(self):
        if self.background_thread is not None and self.background_thread.isRunning():
            self.background_thread.quit()
            self.background_thread.wait()
        self.background_thread = QThread()
        self.worker = Worker(DataLoader.load_using_multi)
        self.worker.moveToThread(self.background_thread)
        self.worker.finished.connect(self._on_load_complete)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.background_thread.quit)
        self.background_thread.started.connect(self.worker.run)
        self.background_thread.finished.connect(self.background_thread.deleteLater)
        self.background_thread.start()

    def _on_load_complete(self):
        GUISignalManager().on_load_complete.emit()