from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QSizePolicy, QSpacerItem, QCheckBox, QLineEdit, QProgressDialog
from PyQt5.QtCore import Qt, pyqtSignal
from ...user_setting import UserSetting
from ...config import FILEMANAGER_CONFIG
from ..dialog.setting_dialog import SettingDialog
from ..dialog.crashreportdialog import CrashReportDialog

class DialogFactory:
    def __init__(self, parent=None):
        self.parent = parent
    
    def create_input_folder_name_dialog(self):
        return InputFolderNameDialog(self.parent)
    
    def create_load_confirm_dialog(self, count):
        return LoadConfirmDialog(self.parent, count)
    
    def create_confirm_delete_dialog(self, path):
        return ConfirmDeleteDialog(self.parent, path)
    
    def create_folder_open_dialog(self, count):
        return FolderOpenDialog(self.parent, count)
    
    def create_loading_dialog(self):
        return LoadingDialog(self.parent)
    
    def create_setting_dialog(self, full_setting=False):
        return SettingDialog(self.parent, full_setting)
    
    def create_crash_report_dialog(self, error_log=""):
        return CrashReportDialog(self.parent, error_log)

class LoadingDialog(QProgressDialog):
    progress_update = pyqtSignal(int, str)

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Loading")
        self.setWindowModality(Qt.WindowModal)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint | Qt.CustomizeWindowHint)
        self.setLabelText("Loading...")
        self.setCancelButton(None)
        self.setRange(0, 100)
        self.setFixedSize(300, 100)
        self.progress_update.connect(self._progress_update)

    def _progress_update(self, value, message):
        self.setLabelText(message)
        self.setValue(value)

class ConfirmDeleteDialog(QDialog):
    def __init__(self, parent=None, path=""):
        super().__init__(parent)
        self.setWindowTitle("Delete Confirm")
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint | Qt.CustomizeWindowHint)

        layout = QVBoxLayout()
        self.setLayout(layout)
        message_label = QLabel(f"""Are you sure you want to delete [{path}]?
                            <br> <b><font color=\"#F55\">This action cannot be undone.</font></b> 
                            <br>if you want undo, you should be go to trash folder.""")

        message_label.setTextFormat(Qt.RichText)
        message_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        message_label.setStyleSheet("padding: 10px;")
        layout.addWidget(message_label)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        yes_button = QPushButton("Yes")
        yes_button.clicked.connect(self.accept)
        button_layout.addWidget(yes_button)
        no_button = QPushButton("No")
        no_button.clicked.connect(self.reject)
        button_layout.addWidget(no_button)

        under_layout = QHBoxLayout()
        layout.addLayout(under_layout)
        under_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.checkbox = QCheckBox("Don't show this again")
        self.checkbox.setStyleSheet("QCheckBox::indicator { width: 10px; height: 10px; }")
        self.checkbox.setMinimumHeight(20)
        under_layout.addWidget(self.checkbox)

        self.setFixedSize(self.sizeHint())

    def accept(self):
        self.result = True
        if self.checkbox.isChecked():
            UserSetting.set("FORCE_DELETE", True)
            UserSetting.save()
        super().accept()

    def reject(self):
        self.result = False
        super().reject()

class InputFolderNameDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Save Folder Name")
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint | Qt.CustomizeWindowHint)

        layout = QVBoxLayout()
        self.setLayout(layout)

        row = QHBoxLayout()
        layout.addLayout(row)
        label = QLabel("Folder name : ")
        row.addWidget(label)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Folder name.. if empty, use search keyword.")
        self.input.setMinimumWidth(300)
        self.input.setMinimumHeight(25)
        row.addWidget(self.input)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        ok_button = QPushButton("OK")
        button_layout.addWidget(ok_button)

        under_layout = QHBoxLayout()
        layout.addLayout(under_layout)
        under_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.checkbox = QCheckBox("Don't show this again")
        self.checkbox.setStyleSheet("QCheckBox::indicator { width: 10px; height: 10px; }")
        self.checkbox.setMinimumHeight(20)
        under_layout.addWidget(self.checkbox)

        ok_button.clicked.connect(self.accept)
        self.input.returnPressed.connect(self.accept)

    def accept(self):
        self.result = self.input.text()
        if self.checkbox.isChecked():
            UserSetting.set("AUTO_GENERATE_FOLDER_NAME", True)
            UserSetting.save()
        super().accept()

    def reject(self):
        self.result = ''
        super().reject()

class FolderOpenDialog(QDialog):
    def __init__(self, parent=None, count=0):
        super().__init__(parent)
        self.setWindowTitle("Successfully saved")
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint | Qt.CustomizeWindowHint)

        layout = QVBoxLayout()
        self.setLayout(layout)

        row = QHBoxLayout()
        layout.addLayout(row)
        label = QLabel(f"Successfully {count} images saved.\n do you want to open the folder?")
        row.addWidget(label)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        ok_button = QPushButton("It's OK!")
        ok_button.clicked.connect(self.accept)

        open_button = QPushButton("Open folder")
        open_button.clicked.connect(self.open_folder)

        button_layout.addWidget(ok_button)
        button_layout.addWidget(open_button)

        under_layout = QHBoxLayout()
        layout.addLayout(under_layout)
        under_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.checkbox = QCheckBox("Don't show this again")
        self.checkbox.setStyleSheet("QCheckBox::indicator { width: 10px; height: 10px; }")
        self.checkbox.setMinimumHeight(20)
        under_layout.addWidget(self.checkbox)

        self.setFixedSize(self.sizeHint())

        ok_button.setFocus()

    def accept(self):
        if self.checkbox.isChecked():
            UserSetting.set("DISABLE_OPEN_FOLDER_dialog", True)
            UserSetting.save()
        super().accept()

    def reject(self):
        self.accept()

    def open_folder(self):
        import os
        os.startfile(FILEMANAGER_CONFIG['FINAL_SAVE_FOLDER_PATH'])
        super().accept()

class LoadConfirmDialog(QDialog):
    def __init__(self, parent, count):
        super().__init__(parent)
        self.setWindowTitle("Loading")
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint | Qt.CustomizeWindowHint)

        # Design like create_yes_no_dialog
        layout = QVBoxLayout()
        self.setLayout(layout)

        message_label = QLabel(f"Find {count} loadable images. Do you want to load?")
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setStyleSheet("padding: 10px;")
        layout.addWidget(message_label)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        yes_button = QPushButton("Yes")
        yes_button.clicked.connect(self.accept)
        button_layout.addWidget(yes_button)
        no_button = QPushButton("No")
        no_button.clicked.connect(self.reject)
        button_layout.addWidget(no_button)

        under_layout = QHBoxLayout()
        layout.addLayout(under_layout)
        under_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.checkbox = QCheckBox("Don't show this again")
        self.checkbox.setStyleSheet("QCheckBox::indicator { width: 10px; height: 10px; }")
        self.checkbox.setMinimumHeight(20)
        under_layout.addWidget(self.checkbox)

        self.setFixedSize(self.sizeHint())
    
    def accept(self):
        self.result = True
        if self.checkbox.isChecked():
            UserSetting.set("AUTO_LOAD", True)
            UserSetting.save()
        super().accept()

    def reject(self):
        self.result = False
        super().reject()