from PyQt5.QtWidgets import QDialog, QLabel, QCheckBox, QPushButton, QBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt

from ...user_setting import UserSetting

class LoadConfirmPopup(QDialog):
    def __init__(self, parent, count):
        super().__init__(parent)
        self.setWindowTitle("Loading")
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.info_label = QLabel(f"Find {count} loadable images. Do you want to load?")
        self.info_label.setMinimumHeight(50)
        self.info_label.setContentsMargins(5, 5, 5, 5)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        button_layout = QBoxLayout(QBoxLayout.LeftToRight)
        self.load_button = QPushButton("Yes")
        self.load_button.setMinimumHeight(30)
        self.load_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.load_button.clicked.connect(self.accept)

        self.reject_button = QPushButton("No")
        self.reject_button.setMinimumHeight(30)
        self.reject_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.reject_button.clicked.connect(self.reject)

        self.checkbox = QCheckBox("Don't show this message again")
        self.checkbox.setMinimumHeight(20)
        self.checkbox.setStyleSheet("QCheckBox::indicator { width: 10px; height: 10px; }")
        self.checkbox.setContentsMargins(5, 5, 5, 5)

        self.layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.layout.addWidget(self.info_label)
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.reject_button)
        self.layout.addWidget(self.checkbox)
        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)
    
    def accept(self):
        self.result = True
        if self.checkbox.isChecked():
            UserSetting.set("DONT_SHOW_LOAD_CONFIRM", True)
            UserSetting.save()
        super().accept()

    def reject(self):
        self.result = False
        super().reject()