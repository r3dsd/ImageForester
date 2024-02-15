import os
from PyQt5.QtWidgets import QLabel, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class ImageViewer(QLabel):
    def __init__(self, parent=None):
        super(ImageViewer, self).__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(512, 512)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setText("No Image")

    def update_image(self, image_path: str):
        if image_path is None:
            return
        normpath = os.path.normpath(image_path)
        pixmap = QPixmap(normpath)
        scaled_pixmap = pixmap.scaled(self.width(), self.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(scaled_pixmap)