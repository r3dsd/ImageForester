from PyQt5.QtWidgets import QBoxLayout, QLabel, QPushButton, QHBoxLayout, QSizePolicy, QFileDialog

from ..widgets.settingdialog import SettingDialog
from ...user_setting import UserSetting

class BottomLayout(QBoxLayout):
    def __init__(self, mainwindow):
        super().__init__(QBoxLayout.TopToBottom)
        self.mainwindow = mainwindow

        self._initUI()
        self._initsignal()

    def _initUI(self):
        self.info_console = QLabel()
        self.info_console.setMinimumHeight(100)
        self.addWidget(self.info_console)

        bar_layout = QHBoxLayout()
        self.path_label = QLabel()
        self.path_label.setText("Selected Path: ")
        self.path_label.setMinimumHeight(30)
        self.path_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        bar_layout.addWidget(self.path_label, 7)

        self.path_select_button = QPushButton("Select Path")
        bar_layout.addWidget(self.path_select_button, 1)

        self.option_button = QPushButton("Options")
        bar_layout.addWidget(self.option_button, 1)

        self.save_button = QPushButton("Save")
        bar_layout.addWidget(self.save_button, 1)

        self.addLayout(bar_layout)

    def _initsignal(self):
        self.option_button.clicked.connect(self._on_option_button_clicked)
        self.path_select_button.clicked.connect(self._on_path_select_button_clicked)

    def _on_option_button_clicked(self):
        SettingDialog(self.mainwindow)

    def _on_path_select_button_clicked(self):
        sourcepath = QFileDialog.getExistingDirectory(self.mainwindow, 'Select Source Path')
        if sourcepath:
            self.path_label.setText(f"Selected Path: {sourcepath}")
            UserSetting.set('IMAGE_SOURCE_DIR', sourcepath)