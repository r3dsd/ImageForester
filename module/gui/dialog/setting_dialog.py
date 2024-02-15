from PyQt5.QtWidgets import QDialog, QHBoxLayout, QLabel, QVBoxLayout, QPushButton, QFileDialog, QSizePolicy, QComboBox, QCheckBox, QWidget
from PyQt5.QtCore import Qt
from enum import Enum, auto

from ...constants import GUI_STYLE_SHEET
from ...user_setting import UserSetting, SaveModeEnum, GUIModeEnum
from ...logger import get_logger

logger = get_logger(__name__)

class SettingDialog(QDialog):
    def __init__(self, parent=None, full_setting=False):
        super().__init__(parent)
        self.full_setting = full_setting
        self._mainwindow = parent
        logger.debug(f"SettingDialog mainwindow : {self._mainwindow}")
        self._initUI()
        self.exec_()

    def _initUI(self):
        self.setWindowTitle('User Setting')
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint | Qt.CustomizeWindowHint)

        _layout = QVBoxLayout()
        self.setLayout(_layout)

        # Setting 1 - Save Path
        savepath_row = SettingOptionWidget(parent=self._mainwindow, 
                                            option_name='SAVE_PATH', 
                                            option_label_text='Save Path : ', 
                                            tooltip_text='Select Save Directory',
                                            option_mode=OPTION_MODE.PATHSELECT)
        # Setting 2 - Save Mode
        savemode_row = SettingOptionWidget(parent=self._mainwindow,
                                            option_name='SAVE_MODE',
                                            option_label_text='Save Mode : ',
                                            tooltip_text='Copy or Move Image to Save Path',
                                            option_mode=OPTION_MODE.COMBOBOX,
                                            option_list=SaveModeEnum.get_all_enum())
        # Setting 3 - Stealth Mode
        stealthmode_row = SettingOptionWidget(parent=self._mainwindow,
                                            option_name='STEALTH_MODE',
                                            option_label_text='Stealth Mode : ',
                                            tooltip_text='if checked, will be more find description from image pixel',
                                            option_mode=OPTION_MODE.CHECKBOX,
                                            option_value_text='if checked, will be more find description from image pixel')

        _layout.addWidget(savepath_row)
        _layout.addWidget(savemode_row)
        _layout.addWidget(stealthmode_row)

        if self.full_setting:
            self.setWindowTitle('User Setting (Full)')
            # Setting 4 - autoload
            autoload_row = SettingOptionWidget(parent=self._mainwindow,
                                            option_name='AUTO_LOAD',
                                            option_label_text='Auto Load : ',
                                            tooltip_text='Auto Load is for auto load image when path selected immediately',
                                            option_mode=OPTION_MODE.CHECKBOX,
                                            option_value_text='if checked, image will be loaded immediately')
            # Setting 5 - GUI Style
            guistyle_row = SettingOptionWidget(parent=self._mainwindow,
                                            option_name='GUI_STYLE',
                                            option_label_text='GUI Style : ',
                                            tooltip_text='Change GUI Style',
                                            option_mode=OPTION_MODE.COMBOBOX,
                                            option_list=GUIModeEnum.get_all_enum())
            # Setting 6 - AUTO_GENERATE_FOLDER_NAME
            auto_generate_folder_name_row = SettingOptionWidget(parent=self._mainwindow,
                                                                option_name='AUTO_GENERATE_FOLDER_NAME',
                                                                option_label_text='Auto Generate Folder Name : ',
                                                                tooltip_text='Auto Generate Folder Name is for auto generate folder name',
                                                                option_mode=OPTION_MODE.CHECKBOX,
                                                                option_value_text='if checked, folder name will be generated automatically by search keyword')
            # Setting 7 - Disable Open Folder Popup
            disable_open_folder_popup_row = SettingOptionWidget(parent=self._mainwindow,
                                                                option_name='DISABLE_OPEN_FOLDER_POPUP',
                                                                option_label_text='Disable Open Folder Popup : ',
                                                                tooltip_text='Disable Open Folder Popup is for disable open folder popup',
                                                                option_mode=OPTION_MODE.CHECKBOX,
                                                                option_value_text='if checked, don\'t show open folder confirmation')
            # Setting 8 - Force Delete
            force_delete_row = SettingOptionWidget(parent=self._mainwindow,
                                                    option_name='FORCE_DELETE',
                                                    option_label_text='Force Delete : ',
                                                    tooltip_text='Force Delete is for force delete',
                                                    option_mode=OPTION_MODE.CHECKBOX,
                                                    option_value_text='if checked, don\'t show delete confirmation')
            # Setting 9 - Auto Delete After Tagging
            auto_delete_after_tagging_row = SettingOptionWidget(parent=self._mainwindow,
                                                                option_name='AUTO_DELETE_AFTER_TAGGING',
                                                                option_label_text='Auto Delete After Tagging : ',
                                                                tooltip_text='Auto Delete After Tagging is for auto delete after tagging',
                                                                option_mode=OPTION_MODE.CHECKBOX,
                                                                option_value_text='if checked, auto delete after tagging')
            _layout.addWidget(autoload_row)
            _layout.addWidget(guistyle_row)
            _layout.addWidget(auto_generate_folder_name_row)
            _layout.addWidget(disable_open_folder_popup_row)
            _layout.addWidget(force_delete_row)
            _layout.addWidget(auto_delete_after_tagging_row)

        self.setFixedSize(self.sizeHint())

    def closeEvent(self, event):
        UserSetting.save()

class OPTION_MODE(Enum):
    CHECKBOX = auto()
    COMBOBOX = auto()
    PATHSELECT = auto()

class SettingOptionWidget(QWidget):
    def __init__(self,
                parent=None,
                option_name='EMPTY_NAME',
                option_label_text='empty',
                tooltip_text='empty',
                option_mode=OPTION_MODE.CHECKBOX,
                option_list=None,
                option_value_text=''):
        super().__init__(parent)
        self.option_name = option_name
        self._mainwindow = parent
        logger.debug(f"SettingOptionWidget mainwindow : {self._mainwindow}")
        option_row = QHBoxLayout()
        option_row.setContentsMargins(0, 0, 0, 0)
        self.setLayout(option_row)

        self.option_label = QLabel(option_label_text)
        option_row.addWidget(self.option_label)
        self.option_label.setToolTip(tooltip_text)
        self.option_label.setFixedHeight(25)
        self.option_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.option_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        if option_mode == OPTION_MODE.CHECKBOX:
            self.option_value = QCheckBox()
            option_row.addWidget(self.option_value)
            self.option_value.setToolTip(tooltip_text)
            self.option_value.setText(option_value_text)
            self.option_value.setChecked(UserSetting.get(option_name))
            self.option_value.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.option_value.stateChanged.connect(self.on_state_changed)
        elif option_mode == OPTION_MODE.COMBOBOX:
            self.option_value = QComboBox()
            option_row.addWidget(self.option_value)
            self.option_value.setToolTip(tooltip_text)
            self.option_value.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            for option_text in option_list:
                self.option_value.addItem(option_text.get_display_str())
            self.option_value.setCurrentIndex(UserSetting.get(option_name).value - 1)
            self.option_value.activated.connect(self.on_activated)
        elif option_mode == OPTION_MODE.PATHSELECT:
            self.option_value = QLabel(UserSetting.get(option_name))
            option_row.addWidget(self.option_value)
            self.option_value.setToolTip(tooltip_text)
            self.option_value.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            self.option_button = QPushButton('. . .')
            option_row.addWidget(self.option_button)
            self.option_button.setToolTip('Select Save Path')
            self.option_button.setFixedHeight(25)
            self.option_button.setMaximumWidth(30)
            self.option_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.option_button.clicked.connect(self.on_path_button_clicked)

        logger.debug(f'Option_{option_name} : {UserSetting.get(option_name)}')

    def on_state_changed(self, state: int):
        UserSetting.set(self.option_name, True if state else False)

    def on_activated(self, index: int):
        index += 1
        if self.option_name == 'GUI_STYLE':
            UserSetting.set(self.option_name, GUIModeEnum(index).name)
            self._mainwindow.setStyleSheet(GUI_STYLE_SHEET[UserSetting.get('GUI_STYLE').name])
            return
        elif self.option_name == 'SAVE_MODE':
            UserSetting.set(self.option_name, SaveModeEnum(index).name)
            return

    def on_path_button_clicked(self):
        savepath = QFileDialog.getExistingDirectory(self, 'Directory Select')
        if savepath:
            self.option_value.setText(savepath)
            UserSetting.set(self.option_name, savepath)