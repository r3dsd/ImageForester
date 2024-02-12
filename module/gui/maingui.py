import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout

from module.constants import GUI_STYLE_SHEET, PROGRAM_NAME, PROGRAM_VERSION
from ..user_setting import UserSetting
from . import layout as MyLayout
from ..imagetagger import imagetagger
from .guisignalmanager import GUISignalManager

class MainGui:
    def __init__(self):
        App = QApplication(sys.argv)
        App.setStyle('Fusion')
        UserSetting.load()
        a = GUISignalManager()
        self._initUI()
        print(f"{PROGRAM_NAME} {PROGRAM_VERSION} started.")
        sys.exit(App.exec_())

    def _initUI(self):
        self._init_window()

        self._init_central_widget()

        self._mainwindow.show()

    def _init_window(self):
        self._mainwindow = QMainWindow()
        self._mainwindow.setWindowTitle(f"{PROGRAM_NAME} {PROGRAM_VERSION}")
        self._mainwindow.setGeometry(100, 100, 1280, 720)
        self._mainwindow.setStyleSheet(GUI_STYLE_SHEET['EASY']) # for debugging, use 'DARK' or 'LIGHT'

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



if __name__ == "__main__":
    MainGui()
