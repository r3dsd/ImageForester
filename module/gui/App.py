import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from PyQt5.QtGui import QIcon

from module.constants import GUI_STYLE_SHEET, PROGRAM_NAME, PROGRAM_VERSION
from ..user_setting import UserSetting
from .tab import SearchTab, SortTab, TaggerTab
from .guisignalmanager import GUISignalManager, GUISearchSignalManager
from .factory.DialogFactory import DialogFactory
from .widgets.menubar import MyMenuBar
from ..logger import get_logger
from ..r3util.r3path import get_resource_path
from ..data import DataLoader
from .worker import ExtendedWorker

logger = get_logger(__name__)

class App:
    def __init__(self):
        self.App = QApplication(sys.argv)
        self.App.setStyle('Fusion')
        logger.info(f"{PROGRAM_NAME} {PROGRAM_VERSION} Started.")
        UserSetting.load()
        GUISignalManager().on_crashed_program.connect(self.on_crashed_program)
        self._initUI()
        if UserSetting.get('AUTO_DATABASE'):
            GUISearchSignalManager().emit_on_auto_database_load_started()
            worker = ExtendedWorker(DataLoader.load_from_DB)
            worker.finished.connect(self.emit_auto_database_load_finished)
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
        _central_widget = QTabWidget()
        self._mainwindow.setCentralWidget(_central_widget)

        _central_widget.addTab(SearchTab(self._mainwindow), "Search")
        _central_widget.addTab(SortTab(self._mainwindow), "Sort")
        _central_widget.addTab(TaggerTab(self._mainwindow), "Tagger")

    def on_crashed_program(self, error_log: str):
        DialogFactory(self._mainwindow).create_crash_report_dialog(error_log=error_log).exec_()

    def emit_auto_database_load_finished(self):
        GUISearchSignalManager().emit_on_auto_database_load_finished()