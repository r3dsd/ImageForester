from PyQt5.QtWidgets import QHBoxLayout, QSizePolicy, QVBoxLayout, QLabel, QPushButton, QListWidgetItem, QLineEdit
from PyQt5.QtCore import Qt
import send2trash

from ....imagetagger.imagetagger import ImageTagger
from ...widgets.components.myqlistwidget import MyQListWidget
from ...widgets.image_viewer import ImageViewer
from ....data import ImageFileDataFactory
from ....gui.guisignalmanager import GUISignalManager
from ...factory.PopupFactory import PopupFactory
from ...worker import ExtendedWorker
from ....imagetagger.imagetagger import add_tag
from ....data import DB
from ....user_setting import UserSetting

from ....logger import get_logger
import traceback

logger = get_logger(__name__)

class MiddleLayout(QVBoxLayout):
    def __init__(self, mainwindow):
        super().__init__()
        self.mainwindow = mainwindow
        self._initUI()
        self._initSignal()

    def _initUI(self):

        middle_layout = QHBoxLayout()
        self.addLayout(middle_layout)

        list_layout = QVBoxLayout()
        middle_layout.addLayout(list_layout)

        list_upper_layout = QHBoxLayout()
        list_layout.addLayout(list_upper_layout)

        self.list_name_label = QLabel("No Description File List")
        list_upper_layout.addWidget(self.list_name_label)
        self.list_name_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.list_name_label.setMinimumSize(300, 25)
        self.list_name_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.load_button = QPushButton("Load")
        list_upper_layout.addWidget(self.load_button)
        self.load_button.setToolTip("Load No Description File List")

        self.list = MyQListWidget()
        self.list.setObjectName("No Description File List")
        self.list.setMinimumSize(300, 400)
        self.list.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        list_layout.addWidget(self.list)

        self.no_data_label = QLabel("No Description File not found")
        self.no_data_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.no_data_label.setMinimumSize(300, 400)
        self.no_data_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        list_layout.addWidget(self.no_data_label)

        list_button_layout = QHBoxLayout()
        list_layout.addLayout(list_button_layout)
        self.auto_tag_button = QPushButton("Auto Tagging")
        list_button_layout.addWidget(self.auto_tag_button)
        self.auto_tag_button.setToolTip("Auto Tagging is using onnx model to tag images automatically (may take a long time and high memory usage)")
        self.auto_tag_button.clicked.connect(self._on_auto_tag_button_clicked)

        view_layout = QVBoxLayout()
        middle_layout.addLayout(view_layout)
        self.image_viewer = ImageViewer(self.parent())
        self.image_viewer.setMinimumSize(512, 512)
        view_layout.addWidget(self.image_viewer)
        self.tag_edit_input = QLineEdit()
        view_layout.addWidget(self.tag_edit_input)
        self.tag_edit_input.setPlaceholderText("Add Tag... ex) cat, dog, ...")
        self.tag_edit_input.setDisabled(True)
        self.tag_edit_input.returnPressed.connect(self._on_tag_add_button_clicked)
        self.tag_edit_input.textChanged.connect(lambda: self.tag_add_button.setDisabled(False) if len(self.tag_edit_input.text()) > 0 else self.tag_add_button.setDisabled(True))
        self.tag_edit_input.setMinimumHeight(100)
        self.tag_edit_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.tag_edit_input.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.tag_add_button = QPushButton("Add Tag")
        self.tag_add_button.setDisabled(True)
        view_layout.addWidget(self.tag_add_button)

        self._all_hide()
        self._update_no_data_ui()

    def _initSignal(self):
        self.load_button.clicked.connect(self._on_load_button_clicked)
        self.auto_tag_button.clicked.connect(self._on_auto_tag_button_clicked)
        self.tag_add_button.clicked.connect(self._on_tag_add_button_clicked)
        self.list.itemClicked.connect(self._on_item_selection_changed)
        self.list.currentItemChanged.connect(self._on_item_selection_changed)
        GUISignalManager().on_load_complete.connect(self.on_load_complete)

    def on_load_complete(self, data=None):
        logger.debug(f"TaggerLayout update_ui")
        if data is None:
            self._update_no_data_ui()
        else:
            self._update_has_data_ui(data)

    def _update_has_data_ui(self, data):
        logger.debug(f"TaggerLayout update has data ui")
        self.list_name_label.show()
        self.list.show()
        self.image_viewer.show()
        self.no_data_label.hide()
        self.list.clear()
        for file_path in data:
            self.list.addItem(file_path)
        self.auto_tag_button.setDisabled(False)

    def _update_no_data_ui(self):
        logger.debug(f"TaggerLayout update no data ui")
        self.list_name_label.show()
        self.list.hide()
        self.image_viewer.show()
        self.no_data_label.show()
        self.auto_tag_button.setDisabled(True)

    def _on_item_selection_changed(self, item: QListWidgetItem):
        if item is not None:
            self.image_viewer.update_image(item.text())
            self.tag_edit_input.setDisabled(False)
        else:
            self.tag_edit_input.setDisabled(True)

    def _on_auto_tag_button_clicked(self):
        path_list = [self.list.item(i).text() for i in range(self.list.count())]
        logger.info("ImageTagger worker started.")
        self.worker = ExtendedWorker(ImageTagger().auto_tagging, path_list)
        self.worker.result.connect(self._on_auto_tagging_finished)
        self.worker.start()

    def _on_auto_tagging_finished(self, result):
        logger.info("ImageTagger worker finished.")
        if result is None:
            PopupFactory.show_error_message(self.mainwindow, "Auto Tagging failed.")
            return
        data = [ImageFileDataFactory.create(path, tag) for path, tag in result]
        count = self.list.count()
        source_path_list = [self.list.item(i).text() for i in range(count)]
        self.image_viewer.clear()
        self.auto_tag_button.setDisabled(True)
        self._update_no_data_ui()
        GUISignalManager().emit_on_tag_added(data, count)
        if UserSetting.check('AUTO_DELETE_AFTER_TAGGING'):
            logger.info(f"AUTO_DELETE_AFTER_TAGGING Enabled... moved to trash {count} images.")
            logger.info(f"Trash targets: {source_path_list}")
            send2trash.send2trash(source_path_list)
            DB("Tagger Data Storage").delete_no_tags_datas(source_path_list)
            logger.info(f"Succesfully moved to trash 1 images.")
        logger.info(f"Auto Tagging finished. {count} images are tagged.")
        PopupFactory.show_info_message(self.mainwindow, f"Auto Tagging finished. {count} images are tagged.")

    def _on_tag_add_button_clicked(self):
        tag = self.tag_edit_input.text()
        item = self.list.currentItem()
        if item is not None:
            source_path = item.text()
            newpath = add_tag(source_path, tag)
            data = ImageFileDataFactory.create(newpath, tag)
            self.tag_edit_input.clear()
            self.tag_edit_input.setDisabled(True)
            self.tag_add_button.setDisabled(True)
            self.list.takeItem(self.list.currentRow())
            self.image_viewer.clear()
            GUISignalManager().emit_on_tag_added(data, 1)
            if UserSetting.check('AUTO_DELETE_AFTER_TAGGING'):
                logger.info(f"AUTO_DELETE_AFTER_TAGGING Enabled... moved to trash 1 images.")
                logger.info(f"Trash targets: {source_path}")
                send2trash.send2trash(source_path)
                DB("Tagger Data Storage").delete_no_tags_datas(source_path)
                logger.info(f"Succesfully moved to trash 1 images.")
            logger.info(f"Tag Added: {data}")
            PopupFactory.show_info_message(self.mainwindow, f"Tag Added: {data}")
        else:
            logger.error(f"Item is None. {traceback.format_exc()}")

    def _on_load_button_clicked(self):
        db = DB("Tagger Data Storage")
        data = db.get_no_tags_datas()
        if len(data) == 0:
            PopupFactory.show_info_message(self.mainwindow, "No Description File not found.")
            return
        self.on_load_complete(data)

    def _all_hide(self):
        self.list_name_label.hide()
        self.list.hide()
        self.no_data_label.hide()
        self.image_viewer.hide()