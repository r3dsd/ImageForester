from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QSizePolicy, QSpacerItem, QCheckBox
from PyQt5.QtCore import Qt
from ...user_setting import UserSetting

class PopupFactory:
    def __init__(self, parent):
        self.parent = parent

    def create_popup(self, title, message, button_text="OK"):
        popup = QDialog(self.parent)
        popup.setWindowTitle(title)
        popup.setWindowFlags(popup.windowFlags() & ~Qt.WindowContextHelpButtonHint | Qt.CustomizeWindowHint)
        popup.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        layout = QVBoxLayout()
        popup.setLayout(layout)

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
        ok_button.clicked.connect(popup.accept)
        button_layout.addWidget(ok_button)

        popup.setFixedSize(popup.sizeHint())
        return popup
    
    def create_yes_no_popup(self, title, message, yes_text="Yes", no_text="No"):
        popup = QDialog(self.parent)
        popup.setWindowTitle(title)
        layout = QVBoxLayout()
        popup.setLayout(layout)

        message_label = QLabel(message)
        message_label.setWordWrap(True)
        layout.addWidget(message_label)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        yes_button = QPushButton(yes_text)
        yes_button.clicked.connect(popup.accept)
        button_layout.addWidget(yes_button)
        no_button = QPushButton(no_text)
        no_button.clicked.connect(popup.reject)
        button_layout.addWidget(no_button)

        return popup
    
    def create_warning_popup(self, message):
        return self.create_popup("Warning", message)
    
    def create_load_confirm_popup(self, count):
        return LoadConfirmPopup(self.parent, count)


class LoadConfirmPopup(QDialog):
    def __init__(self, parent, count):
        super().__init__(parent)
        self.setWindowTitle("Loading")
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

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