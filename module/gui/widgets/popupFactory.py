from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QSizePolicy, QSpacerItem, QCheckBox, QLineEdit
from PyQt5.QtCore import Qt
from ...user_setting import UserSetting
import winsound

class PopupFactory:
    def __init__(self, parent):
        self.parent = parent
        winsound.PlaySound("SystemAsterisk", winsound.SND_ASYNC | winsound.SND_ALIAS)

    def create_popup(self, title, message, button_text="OK"):
        return DefalutPopup(self.parent, title, message, button_text)
    
    def create_yes_no_popup(self, title, message, yes_text="Yes", no_text="No"):
        return YesNoPopup(self.parent, title, message, yes_text, no_text)
    
    def create_input_folder_name_popup(self):
        return InputFolderNamePopup(self.parent)
    
    def create_warning_popup(self, message):
        return self.create_popup("Warning", message)
    
    def create_load_confirm_popup(self, count):
        return LoadConfirmPopup(self.parent, count)
    
class DefalutPopup(QDialog):
    def __init__(self, parent, title, message, button_text="OK"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint | Qt.CustomizeWindowHint)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        layout = QVBoxLayout()
        self.setLayout(layout)

        message_label = QLabel(message)
        layout.addWidget(message_label)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        ok_button = QPushButton(button_text)
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)

        self.setFixedSize(self.sizeHint())

class YesNoPopup(QDialog):
    def __init__(self, parent, title, message, yes_text="Yes", no_text="No"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint | Qt.CustomizeWindowHint)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        layout = QVBoxLayout()
        self.setLayout(layout)

        message_label = QLabel(message)
        layout.addWidget(message_label)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        yes_button = QPushButton(yes_text)
        yes_button.clicked.connect(self.accept)
        button_layout.addWidget(yes_button)
        no_button = QPushButton(no_text)
        no_button.clicked.connect(self.reject)
        button_layout.addWidget(no_button)

        self.setFixedSize(self.sizeHint())

class InputFolderNamePopup(QDialog):
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
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)

    def accept(self):
        self.result = self.input.text()
        super().accept()

    def reject(self):
        self.result = ''
        super().reject()

class LoadConfirmPopup(QDialog):
    def __init__(self, parent, count):
        super().__init__(parent)
        self.setWindowTitle("Loading")
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint | Qt.CustomizeWindowHint)

        # Design like create_yes_no_popup
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
            UserSetting.set("DONT_SHOW_LOAD_CONFIRM", True)
            UserSetting.save()
        super().accept()

    def reject(self):
        self.result = False
        super().reject()