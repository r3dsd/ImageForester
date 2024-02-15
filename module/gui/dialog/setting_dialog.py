from PyQt5.QtWidgets import QDialog, QHBoxLayout, QLabel, QVBoxLayout, QPushButton, QFileDialog, QSizePolicy, QComboBox, QCheckBox
from PyQt5.QtCore import Qt

from ...constants import GUI_STYLE_SHEET, GUI_STYLE
from ...user_setting import UserSetting

class SettingDialog(QDialog):
    def __init__(self, parent=None, full_setting=False):
        super().__init__(parent)
        self.full_setting = full_setting
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
        self.savepath_label.setToolTip('Save Path for Selected Image')
        self.savepath_label.setFixedHeight(30)
        self.savepath_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.savepath_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.savepath_value = QLabel(UserSetting.get('IMAGE_SAVE_DIR'))
        self.savepath_value.setToolTip('Save Path for Selected Image')
        self.savepath_value.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.savepath_value.setFixedHeight(30)
        self.savepath_value.setMinimumWidth(300)
        self.savepath_value.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.savepath_button = QPushButton('. . .')
        self.savepath_button.setToolTip('Select Save Path')
        self.savepath_button.setFixedHeight(30)
        self.savepath_button.setMaximumWidth(30)
        self.savepath_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        savepath_row.addWidget(self.savepath_label)
        savepath_row.addWidget(self.savepath_value)
        savepath_row.addWidget(self.savepath_button)
        # Setting 2 - Save Mode
        savemode_row = QHBoxLayout()
        self.savemode_label = QLabel('Save Mode : ')
        self.savemode_label.setToolTip('Save Mode for Selected Image (Copy, Move)')
        self.savemode_label.setFixedHeight(30)
        self.savemode_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.savemode_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.savemode_value = QComboBox()
        self.savemode_value.setToolTip('Save Mode for Selected Image (Copy, Move)')
        self.savemode_value.addItem('Copy Mode')
        self.savemode_value.addItem('Move Mode')
        self.savemode_value.setCurrentIndex(self._get_savemode_from_user_setting())
        self.savemode_value.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        savemode_row.addWidget(self.savemode_label)
        savemode_row.addWidget(self.savemode_value)
        # Setting 3 - Stealth Mode
        stealthmode_row = QHBoxLayout()
        self.stealthmode_label = QLabel('Stealth Mode : ')
        self.stealthmode_label.setToolTip('Stealth Mode is for more powerful image discription extraction (It may take ! SUPER ! longer time)')
        self.stealthmode_label.setFixedHeight(30)
        self.stealthmode_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.stealthmode_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.stealthmode_value = QCheckBox()
        self.stealthmode_value.setToolTip('Stealth Mode is for more powerful image discription extraction (It may take ! SUPER ! longer time)')
        self.stealthmode_value.setChecked(UserSetting.get('STEALTH_MODE'))
        self.stealthmode_value.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        stealthmode_row.addWidget(self.stealthmode_label)
        stealthmode_row.addWidget(self.stealthmode_value)

        _layout.addLayout(savepath_row)
        _layout.addLayout(savemode_row)
        _layout.addLayout(stealthmode_row)

        if self.full_setting:
            self.setWindowTitle('User Setting (Full)')
            # Setting 4 - autoload
            autoload_row = QHBoxLayout()
            self.autoload_label = QLabel('Auto Load : ')
            self.autoload_label.setToolTip('Auto Load is for auto load image when path selected immediately')
            self.autoload_label.setFixedHeight(30)
            self.autoload_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.autoload_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            self.autoload_value = QCheckBox()
            self.autoload_value.setToolTip('Auto Load is for auto load image when path selected immediately')
            self.autoload_value.setChecked(UserSetting.get('AUTO_LOAD'))
            self.autoload_value.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            autoload_row.addWidget(self.autoload_label)
            autoload_row.addWidget(self.autoload_value)
            # Setting 5 - GUI Style
            guistyle_row = QHBoxLayout()
            self.guistyle_label = QLabel('GUI Style : ')
            self.guistyle_label.setToolTip('GUI Style for Image Forester')
            self.guistyle_label.setFixedHeight(30)
            self.guistyle_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.guistyle_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            self.guistyle_value = QComboBox()
            self.guistyle_value.setToolTip('GUI Style for Image Forester')
            self.guistyle_value.addItem('DARK')
            self.guistyle_value.addItem('LIGHT')
            self.guistyle_value.addItem('LIGHT_GREEN')
            self.guistyle_value.setCurrentIndex(GUI_STYLE[UserSetting.get('GUI_STYLE')].value)
            self.guistyle_value.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            guistyle_row.addWidget(self.guistyle_label)
            guistyle_row.addWidget(self.guistyle_value)
            # Setting 6 - AUTO_GENERATE_FOLDER_NAME
            auto_generate_folder_name_row = QHBoxLayout()
            self.auto_generate_folder_name_label = QLabel('Auto Generate Folder Name : ')
            self.auto_generate_folder_name_label.setToolTip('Auto Generate Folder Name is for auto generate folder name using search keywords')
            self.auto_generate_folder_name_label.setFixedHeight(30)
            self.auto_generate_folder_name_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.auto_generate_folder_name_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            self.auto_generate_folder_name_value = QCheckBox()
            self.auto_generate_folder_name_value.setToolTip('Auto Generate Folder Name is for auto generate folder name using search keywords')
            self.auto_generate_folder_name_value.setChecked(UserSetting.get('AUTO_GENERATE_FOLDER_NAME'))
            self.auto_generate_folder_name_value.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            auto_generate_folder_name_row.addWidget(self.auto_generate_folder_name_label)
            auto_generate_folder_name_row.addWidget(self.auto_generate_folder_name_value)
            # Setting 7 - Disable Open Folder Popup
            disable_open_folder_popup_row = QHBoxLayout()
            self.disable_open_folder_popup_label = QLabel('Auto Open Folder : ')
            self.disable_open_folder_popup_label.setToolTip('Auto Open Folder is for auto open folder after save')
            self.disable_open_folder_popup_label.setFixedHeight(30)
            self.disable_open_folder_popup_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.disable_open_folder_popup_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            self.disable_open_folder_popup_value = QCheckBox()
            self.disable_open_folder_popup_value.setToolTip('Auto Open Folder is for auto open folder after save')
            self.disable_open_folder_popup_value.setChecked(UserSetting.get('DISABLE_OPEN_FOLDER_POPUP'))
            self.disable_open_folder_popup_value.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            disable_open_folder_popup_row.addWidget(self.disable_open_folder_popup_label)
            disable_open_folder_popup_row.addWidget(self.disable_open_folder_popup_value)
            # Setting 8 - Force Delete
            force_delete_row = QHBoxLayout()
            self.force_delete_label = QLabel('Force Delete : ')
            self.force_delete_label.setToolTip('Force Delete is The file is actually deleted, not just removed from the list.')
            self.force_delete_label.setFixedHeight(30)
            self.force_delete_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.force_delete_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            self.force_delete_value = QCheckBox()
            self.force_delete_value.setToolTip('Force Delete is The file is actually deleted, not just removed from the list.')
            self.force_delete_value.setChecked(UserSetting.get('FORCE_DELETE'))
            self.force_delete_value.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            force_delete_row.addWidget(self.force_delete_label)
            force_delete_row.addWidget(self.force_delete_value)
            # Setting 9 - Auto Delete After Tagging
            auto_delete_after_tagging_row = QHBoxLayout()
            self.auto_delete_after_tagging_label = QLabel('Auto Delete After Tagging : ')
            self.auto_delete_after_tagging_label.setToolTip('Auto Delete After Tagging')
            self.auto_delete_after_tagging_label.setFixedHeight(30)
            self.auto_delete_after_tagging_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.auto_delete_after_tagging_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            self.auto_delete_after_tagging_value = QCheckBox()
            self.auto_delete_after_tagging_value.setToolTip('Auto Delete After Tagging')
            self.auto_delete_after_tagging_value.setChecked(UserSetting.get('AUTO_DELETE_AFTER_TAGGING'))
            self.auto_delete_after_tagging_value.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            auto_delete_after_tagging_row.addWidget(self.auto_delete_after_tagging_label)
            auto_delete_after_tagging_row.addWidget(self.auto_delete_after_tagging_value)

            _layout.addLayout(autoload_row)
            _layout.addLayout(guistyle_row)
            _layout.addLayout(auto_generate_folder_name_row)
            _layout.addLayout(disable_open_folder_popup_row)
            _layout.addLayout(force_delete_row)
            _layout.addLayout(auto_delete_after_tagging_row)

            self._initSignaladditional()

        self.setFixedSize(self.sizeHint())
    
    def _initSignal(self):
        self.savepath_button.clicked.connect(self._on_savepath_button_clicked)
        self.savemode_value.activated.connect(self._on_savemode_value_activated)
        self.stealthmode_value.stateChanged.connect(self._on_stealthmode_value_stateChanged)

    def _initSignaladditional(self):
        self.autoload_value.stateChanged.connect(self._on_autoload_value_statechanged)
        self.guistyle_value.activated.connect(self._on_guistyle_value_activated)
        self.auto_generate_folder_name_value.stateChanged.connect(self._on_auto_generated_folder_name_value_statechanged)
        self.disable_open_folder_popup_value.stateChanged.connect(self._on_disable_open_folder_popup_value_stateChanged)

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
        
    def _on_autoload_value_statechanged(self, state: int):
        UserSetting.set('AUTO_LOAD', True if state else False)

    def _on_guistyle_value_activated(self, index: int):
        UserSetting.set('GUI_STYLE', GUI_STYLE(index).name)
        self.parent().setStyleSheet(GUI_STYLE_SHEET[UserSetting.get('GUI_STYLE')])

    def _on_auto_generated_folder_name_value_statechanged(self, state: int):
        UserSetting.set('AUTO_GENERATE_FOLDER_NAME', True if state else False)

    def _on_disable_open_folder_popup_value_stateChanged(self, state: int):
        UserSetting.set('DISABLE_OPEN_FOLDER_POPUP', True if state else False)