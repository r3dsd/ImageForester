from PyQt5.QtWidgets import QMenuBar, QAction
from ..dialog.image_tagger_dialog import ImageTaggerDialog
from ..factory.DialogFactory import DialogFactory
from ...logger import get_logger

logger = get_logger(__name__)

class MyMenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image_tagger_window: ImageTaggerDialog = None
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

        image_tagging_action = QAction("Image Tagging", parent)
        image_tagging_action.triggered.connect(self.openImageTaggerwindow)

        toolsMenu.addAction(image_tagging_action)
        toolsMenu.addAction(settingAction)

    def openSettingDialog(self):
        DialogFactory(self.parent()).create_setting_dialog(full_setting=True)

    def openImageTaggerwindow(self):
        if self.image_tagger_window and not self.image_tagger_window.isVisible():
            logger.debug("ImageTaggerWindow is already opened")
            self.image_tagger_window.show()
            self.image_tagger_window.raise_()
            self.image_tagger_window.activateWindow()
        else:
            logger.debug("Open ImageTaggerWindow")
            self.image_tagger_window = ImageTaggerDialog(self.parent())
            self.image_tagger_window.show()