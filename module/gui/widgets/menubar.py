from PyQt5.QtWidgets import QMenuBar, QAction
from ..factory.DialogFactory import DialogFactory
from ...logger import get_logger

logger = get_logger(__name__)

class MyMenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._mainwindow = parent
        self._initUI()

    def _initUI(self):
        parent = self.parent()
        fileMenu = self.addMenu('File')
        exitAction = QAction('Exit', parent)
        exitAction.triggered.connect(parent.close)
        fileMenu.addAction(exitAction)

        toolsMenu = self.addMenu('Tools')
        settingAction = QAction("Settings", parent)
        settingAction.triggered.connect(self.openSettingDialog)
        
        toolsMenu.addAction(settingAction)

    def openSettingDialog(self):
        DialogFactory(self._mainwindow).create_setting_dialog(full_setting=True)