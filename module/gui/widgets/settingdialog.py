from PyQt5.QtWidgets import QDialog, QHBoxLayout, QLabel, QVBoxLayout, QPushButton, QFileDialog, QSizePolicy, QComboBox, QCheckBox
from PyQt5.QtCore import Qt
from ...user_setting import UserSetting

class SettingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._initUI()
        self._initSignal()
        self.exec_()

    def accept(self) -> None:
        UserSetting.save()
        return super().accept()
    
    def reject(self) -> None:
        UserSetting.save()
        return super().reject()

    def _initUI(self):
        self.setWindowTitle('User Setting')
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint | Qt.CustomizeWindowHint)

        _layout = QVBoxLayout()
        self.setLayout(_layout)

        # Setting 1 - Save Path
        savepath_row = QHBoxLayout()
        self.savepath_label = QLabel('Save Path : ')
        self.savepath_label.setFixedHeight(30)
        self.savepath_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.savepath_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.savepath_value = QLabel(UserSetting.get('IMAGE_SAVE_DIR'))
        self.savepath_value.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.savepath_value.setFixedHeight(30)
        self.savepath_value.setMinimumWidth(300)
        self.savepath_value.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.savepath_button = QPushButton('. . .')
        self.savepath_button.setFixedHeight(30)
        self.savepath_button.setMaximumWidth(30)
        self.savepath_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        savepath_row.addWidget(self.savepath_label)
        savepath_row.addWidget(self.savepath_value)
        savepath_row.addWidget(self.savepath_button)
        # Setting 2 - Save Mode
        savemode_row = QHBoxLayout()
        self.savemode_label = QLabel('Save Mode : ')
        self.savemode_label.setFixedHeight(30)
        self.savemode_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.savemode_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.savemode_value = QComboBox()
        self.savemode_value.addItem('Copy Mode')
        self.savemode_value.addItem('Move Mode')
        self.savemode_value.setCurrentIndex(self._get_savemode_from_user_setting())
        self.savemode_value.setFixedHeight(30)
        self.savemode_value.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        savemode_row.addWidget(self.savemode_label)
        savemode_row.addWidget(self.savemode_value)
        # Setting 3 - Stealth Mode
        stealthmode_row = QHBoxLayout()
        self.stealthmode_label = QLabel('Stealth Mode : ')
        self.stealthmode_label.setFixedHeight(30)
        self.stealthmode_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.stealthmode_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.stealthmode_value = QCheckBox()
        self.stealthmode_value.setChecked(UserSetting.get('STEALTH_MODE'))
        self.stealthmode_value.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        stealthmode_row.addWidget(self.stealthmode_label)
        stealthmode_row.addWidget(self.stealthmode_value)

        _layout.addLayout(savepath_row)
        _layout.addLayout(savemode_row)
        _layout.addLayout(stealthmode_row)
    
    def _initSignal(self):
        self.savepath_button.clicked.connect(self._on_savepath_button_clicked)
        self.savemode_value.activated.connect(self._on_savemode_value_activated)
        self.stealthmode_value.stateChanged.connect(self._on_stealthmode_value_stateChanged)

    def _on_savepath_button_clicked(self):
        savepath = QFileDialog.getExistingDirectory(self, 'Save Path')
        if savepath:
            self.savepath_value.setText(savepath)
            UserSetting.set('IMAGE_SAVE_DIR', savepath)

    def _on_savemode_value_activated(self, index: int):
        if index == 0:
            UserSetting.set('SAVE_MODE', 'Copy')
        else:
            UserSetting.set('SAVE_MODE', 'Move')

    def _on_stealthmode_value_stateChanged(self, state: int):
        UserSetting.set('STEALTH_MODE', True if state else False)

    def _get_savemode_from_user_setting(self) -> int:
        if UserSetting.get('SAVE_MODE') == 'Copy':
            return 0
        else:
            return 1