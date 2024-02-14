from PyQt5.QtWidgets import QMenuBar, QAction
from .settingdialog import SettingDialog
from ..widgets.popupFactory import PopupFactory

class MyMenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
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
        SettingDialog(self.parent(), full_setting=True)