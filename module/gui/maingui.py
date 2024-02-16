import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon

from module.constants import GUI_STYLE_SHEET, PROGRAM_NAME, PROGRAM_VERSION
from ..user_setting import UserSetting
from . import layout as MyLayout
from .guisignalmanager import GUISignalManager
from .factory.DialogFactory import DialogFactory
from .widgets.menubar import MyMenuBar
from ..logger import get_logger
from ..r3util.r3path import get_resource_path
from ..data.data_loader import DataLoader
from .worker import ExtendedWorker

logger = get_logger(__name__)

class MainGui:
    def __init__(self):
        self.App = QApplication(sys.argv)
        self.App.setStyle('Fusion')
        logger.info(f"{PROGRAM_NAME} {PROGRAM_VERSION} Started.")
        UserSetting.load()
        GUISignalManager().on_crashed_program.connect(self.on_crashed_program)
        self._initUI()
        if UserSetting.get('AUTO_DATABASE'):
            GUISignalManager().emit_on_database_load_started()
            worker = ExtendedWorker(DataLoader.load_from_DB)
            worker.finished.connect(self.on_database_loaded)
            worker.start()
        sys.exit(self.App.exec_())

    def _initUI(self):
        self._init_window()

        self._init_central_widget()

        self._mainwindow.show()

    def _init_window(self):
        self._mainwindow = QMainWindow()
        self._mainwindow.setWindowTitle(f"{PROGRAM_NAME} {PROGRAM_VERSION}")
        self._mainwindow.setWindowIcon(QIcon(get_resource_path('icon.ico')))
        self._mainwindow.setGeometry(100, 100, 1280, 720)
        self._mainwindow.setStyleSheet(GUI_STYLE_SHEET[UserSetting.get('GUI_STYLE').name])

        self.menubar = MyMenuBar(self._mainwindow)
        self._mainwindow.setMenuBar(self.menubar)

    def _init_central_widget(self):
        _central_widget = QWidget()
        _central_Layout = QVBoxLayout()
        _central_widget.setLayout(_central_Layout)
        self._mainwindow.setCentralWidget(_central_widget)

        top_layout = MyLayout.TopLayout(self._mainwindow)
        middle_layout = MyLayout.MiddleLayout(self._mainwindow)
        bottom_layout = MyLayout.BottomLayout(self._mainwindow)

        _central_Layout.addLayout(top_layout)
        _central_Layout.addLayout(middle_layout)
        _central_Layout.addLayout(bottom_layout)

    def on_crashed_program(self, error_log: str):
        DialogFactory(self._mainwindow).create_crash_report_dialog(error_log=error_log).exec_()

    def on_database_loaded(self):
        GUISignalManager().emit_on_database_loaded()