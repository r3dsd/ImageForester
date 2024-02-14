import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget, QHBoxLayout, QPushButton, QSizePolicy, QLineEdit, QListWidgetItem
from PyQt5.QtGui import QPixmap
from ..guisignalmanager import GUISignalManager
from ...data.data_container import DataContainer
from ...imagetagger.imagetagger import ImageTagger, add_tag
from ..worker import ExtendedWorker

from ...logger import get_logger

logger = get_logger(__name__)

class ImageTaggerWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Image Tagging")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint | Qt.CustomizeWindowHint)
        
        _layout = QVBoxLayout()
        self.setLayout(_layout)

        middle_layout = QHBoxLayout()
        _layout.addLayout(middle_layout)

        list_layout = QVBoxLayout()
        middle_layout.addLayout(list_layout)

        self.list_name_label = QLabel("No Description File List")
        self.list_name_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.list_name_label.setMinimumSize(300, 25)
        self.list_name_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        list_layout.addWidget(self.list_name_label)

        self.list = QListWidget()
        self.list.setObjectName("No Description File List")
        self.list.setMinimumSize(300, 400)
        self.list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        list_layout.addWidget(self.list)

        self.no_data_label = QLabel("No Description File not found")
        self.no_data_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.no_data_label.setMinimumSize(300, 400)
        self.no_data_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        list_layout.addWidget(self.no_data_label)

        list_button_layout = QHBoxLayout()
        list_layout.addLayout(list_button_layout)
        self.auto_tag_button = QPushButton("Auto Tagging")
        self.auto_tag_button.setToolTip("Auto Tagging is using onnx model to tag images automatically (may take a long time and high memory usage)")
        self.auto_tag_button.clicked.connect(self._on_auto_tag_button_clicked)

        self.tag_edit_button = QPushButton("Add Tag")
        self.tag_edit_button.setToolTip("Add Tagging is user can edit tag")
        self.tag_edit_button.clicked.connect(self._on_tag_edit_button_clicked)

        list_button_layout.addWidget(self.auto_tag_button)
        list_button_layout.addWidget(self.tag_edit_button)

        self.preview_image = QLabel()
        self.preview_image.setAlignment(Qt.AlignCenter)
        self.preview_image.setMinimumSize(512, 512)
        self.preview_image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        middle_layout.addWidget(self.preview_image)

        self._all_hide()
        self.update_ui()  # 초기 UI 상태 업데이트
        self.setFixedSize(self.sizeHint())

        GUISignalManager().on_load_complete.connect(self.update_ui)
        self.list.itemClicked.connect(self._preview_image_update)
        self.list.currentItemChanged.connect(self._preview_image_update)

    def update_ui(self):
        if DataContainer.has_load_failed_data():
            self._update_has_data_ui()
        else:
            self._update_no_data_ui()

    def _update_has_data_ui(self):
        self.list_name_label.show()
        self.list.show()
        self.preview_image.show()
        self.no_data_label.hide()
        self.list.clear()
        for file_path in DataContainer.get_load_failed_data():
            self.list.addItem(file_path)
        self._button_enable()

    def _update_no_data_ui(self):
        self.list_name_label.show()
        self.list.hide()
        self.preview_image.show()
        self.no_data_label.show()
        self._button_disable()

    def _preview_image_update(self, item: QListWidgetItem):
        if item is None:
            return
        image_path = item.text()
        normpath = os.path.normpath(image_path)
        pixmap = QPixmap(normpath)
        scaled_pixmap = pixmap.scaled(self.preview_image.width(), self.preview_image.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.preview_image.setPixmap(scaled_pixmap)

    def _on_auto_tag_button_clicked(self):
        path_list = [self.list.item(i).text() for i in range(self.list.count())]
        logger.info("ImageTagger worker started.")
        self.worker = ExtendedWorker(ImageTagger().auto_tagging, path_list)
        self.worker.finished.connect(self._on_auto_tagging_finished)
        self.worker.start()

    def _on_tag_edit_button_clicked(self):
        if self.list.currentItem() is not None:
            listitem = self.list.currentItem()
            TagEditWindow(self, listitem).exec_()

            self.list.takeItem(self.list.currentRow())
            if self.list.count() > 0:
                self.list.setCurrentRow(0)
                self._preview_image_update(self.list.currentItem())
            else:
                self.update_ui()

    def _on_auto_tagging_finished(self):
        logger.info("ImageTagger worker finished.")
        self.list.clear()
        self.preview_image.clear()
        self._button_disable()
        self._update_no_data_ui()
        DataContainer.clear_load_failed_data()

    def _all_hide(self):
        self.list_name_label.hide()
        self.list.hide()
        self.no_data_label.hide()
        self.preview_image.hide()

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

class TagEditWindow(QDialog):
    def __init__(self, parents, item : QListWidgetItem):
        super().__init__(parents)
        self._item = item

        self.setWindowTitle(f"Add Tagging to {item.text()}")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint | Qt.CustomizeWindowHint)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.tag_input = QLineEdit()
        self.tag_input.setPlaceholderText("Add Tagging (comma separated) ex) tag1, tag2, tag3")
        self.tag_input.setAlignment(Qt.AlignLeft)
        self.tag_input.setMinimumSize(300, 100)
        layout.addWidget(self.tag_input)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        self.clear_button = QPushButton("Clear")
        button_layout.addWidget(self.clear_button)

        self.add_button = QPushButton("Add")
        button_layout.addWidget(self.add_button)

        self.setFixedSize(self.sizeHint())

        self._initSignal()

    def _initSignal(self):
        self.clear_button.clicked.connect(self._on_clear_button_clicked)
        self.add_button.clicked.connect(self._on_add_button_clicked)
        self.tag_input.returnPressed.connect(self._on_add_button_clicked)

    def _on_clear_button_clicked(self):
        self.tag_input.clear()

    def _on_add_button_clicked(self):
        tag = self.tag_input.text()
        add_tag(self._item.text(), tag)
        self.hide()
        self.tag_input.clear()
        super().accept()

    def reject(self) -> None:
        super().reject()