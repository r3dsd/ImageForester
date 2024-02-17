from PyQt5.QtWidgets import QHBoxLayout, QSizePolicy, QVBoxLayout, QLabel, QPushButton, QListWidgetItem
from PyQt5.QtCore import Qt

from ....imagetagger.imagetagger import ImageTagger
from ...widgets.components.myqlistwidget import MyQListWidget
from ...widgets.image_viewer import ImageViewer
from ....data import DataStorage, ImageFileDataFactory
from ....gui.guisignalmanager import GUITaggerSignalManager, GUISignalManager
from ...factory.PopupFactory import PopupFactory
from ...worker import ExtendedWorker
from ....imagetagger.imagetagger import add_tag

from ....logger import get_logger

logger = get_logger(__name__)

class MiddleLayout(QVBoxLayout):
    def __init__(self, mainwindow, datastorage: DataStorage):
        super().__init__()
        self.mainwindow = mainwindow
        self.datastorage = datastorage
        self._initUI()

    def _initUI(self):

        middle_layout = QHBoxLayout()
        self.addLayout(middle_layout)

        list_layout = QVBoxLayout()
        middle_layout.addLayout(list_layout)

        self.list_name_label = QLabel("No Description File List")
        self.list_name_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.list_name_label.setMinimumSize(300, 25)
        self.list_name_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        list_layout.addWidget(self.list_name_label)

        self.list = MyQListWidget()
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

        list_button_layout.addWidget(self.auto_tag_button)
        list_button_layout.addWidget(self.tag_edit_button)

        self.image_viewer = ImageViewer(self.parent())
        middle_layout.addWidget(self.image_viewer)

        self._all_hide()
        self.update_ui()  # 초기 UI 상태 업데이트

    def _initSignal(self):
        self.list.itemClicked.connect(self._on_item_selection_changed)
        self.list.currentItemChanged.connect(self._on_item_selection_changed)
        GUITaggerSignalManager().on_load_complete.connect(self.update_ui)

    def update_ui(self):
        if self.datastorage.has_load_failed_data():
            self._update_has_data_ui()
        else:
            self._update_no_data_ui()

    def _update_has_data_ui(self):
        self.list_name_label.show()
        self.list.show()
        self.image_viewer.show()
        self.no_data_label.hide()
        self.list.clear()
        for file_path in self.datastorage.get_load_failed_data():
            self.list.addItem(file_path)
        self._button_enable()

    def _update_no_data_ui(self):
        self.list_name_label.show()
        self.list.hide()
        self.image_viewer.show()
        self.no_data_label.show()
        self._button_disable()

    def _on_item_selection_changed(self, item: QListWidgetItem):
        if item is not None:
            self.image_viewer.update_image(item.text())

    def _on_auto_tag_button_clicked(self):
        path_list = [self.list.item(i).text() for i in range(self.list.count())]
        logger.info("ImageTagger worker started.")
        self.worker = ExtendedWorker(ImageTagger().auto_tagging, path_list)
        self.worker.result.connect(self._on_auto_tagging_finished)
        self.worker.start()

    def _on_auto_tagging_finished(self, result):
        logger.info("ImageTagger worker finished.")
        if result is not None:
            data = [ImageFileDataFactory.create(path, tag) for path, tag in result]
            self.datastorage.add_loaded_data(data)
        self.datastorage.clear_load_failed_data()
        count = self.list.count()
        self.list.clear()
        self.image_viewer.clear()
        self._button_disable()
        self._update_no_data_ui()
        GUISignalManager().emit_on_auto_tagging_finished(count)
        PopupFactory.show_info_message(self.mainwindow, f"Auto Tagging finished. {count} images are tagged.")

    def _all_hide(self):
        self.list_name_label.hide()
        self.list.hide()
        self.no_data_label.hide()
        self.image_viewer.hide()

    def _button_disable(self):
        self.auto_tag_button.setDisabled(True)
        self.tag_edit_button.setDisabled(True)

    def _button_enable(self):
        self.auto_tag_button.setDisabled(False)
        self.tag_edit_button.setDisabled(False)

    # def _on_add_button_clicked(self):
    #     tag = self.tag_input.text()
    #     newpath = add_tag(self._item.text(), tag)
    #     data = ImageFileDataFactory.create(newpath, tag)
    #     self.datastorage.add_loaded_data(data)
    #     GUISignalManager().on_tag_added.emit(data.file_path)
    #     super().accept()