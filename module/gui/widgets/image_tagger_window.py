from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget, QFrame, QHBoxLayout, QPushButton
from ..guisignalmanager import GUISignalManager
from ...data.data_container import DataContainer

class ImageTaggerWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Image Tagging")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint | Qt.CustomizeWindowHint)
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.message_label = QLabel("No Description File List")
        self.message_label.setAlignment(Qt.AlignHCenter)
        self.message_label.setMinimumSize(300, 25)
        self.layout.addWidget(self.message_label)

        self.no_data_label = QLabel("No Description File not found")
        self.no_data_label.setAlignment(Qt.AlignCenter)
        self.no_data_label.setMinimumHeight(300)
        self.layout.addWidget(self.no_data_label)

        self.list = QListWidget()
        self.list.setObjectName("No Description File List")
        self.list.setMinimumHeight(300)
        self.layout.addWidget(self.list)

        self._add_common_ui_elements()
        self._all_hide()
        self.update_ui()  # 초기 UI 상태 업데이트
        self.setFixedSize(self.sizeHint())

        GUISignalManager().on_load_complete.connect(self.update_ui)

    def update_ui(self):
        if DataContainer.has_load_failed_data():
            self._update_has_data_ui()
        else:
            self._update_no_data_ui()

    def _update_has_data_ui(self):
        self.message_label.show()
        self.list.show()
        self.no_data_label.hide()
        self.list.clear()
        for file_path in DataContainer.get_load_failed_data():
            self.list.addItem(file_path)
        self._button_enable()

    def _update_no_data_ui(self):
        self.message_label.show()
        self.list.hide()
        self.no_data_label.show()
        self._button_disable()

    def _add_common_ui_elements(self):
        list_button_layout = QHBoxLayout()

        self.auto_tag_button = QPushButton("Auto Tagging")
        self.auto_tag_button.setToolTip("Auto Tagging is using onnx model to tag images automatically (may take a long time and high memory usage)")
        self.auto_tag_button.clicked.connect(self._on_auto_tag_button_clicked)

        self.tag_edit_button = QPushButton("Edit Tag")
        self.tag_edit_button.setToolTip("Edit Tagging is user can edit tag")
        self.tag_edit_button.clicked.connect(self._on_tag_edit_button_clicked)

        list_button_layout.addWidget(self.auto_tag_button)
        list_button_layout.addWidget(self.tag_edit_button)

        self.layout.addLayout(list_button_layout)
        
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(line)

        under_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        under_layout.addWidget(ok_button)
        self.layout.addLayout(under_layout)

    def _on_auto_tag_button_clicked(self):
        pass

    def _on_tag_edit_button_clicked(self):
        pass

    def _all_hide(self):
        self.message_label.hide()
        self.list.hide()
        self.no_data_label.hide()

    def _button_disable(self):
        self.auto_tag_button.setDisabled(True)
        self.tag_edit_button.setDisabled(True)

    def _button_enable(self):
        self.auto_tag_button.setDisabled(False)
        self.tag_edit_button.setDisabled(False)

    def accept(self) -> None:
        self.hide()
    
    def reject(self) -> None:
        self.hide()
