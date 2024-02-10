import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout

class MainGui:
    def __init__(self):
        self.App = QApplication(sys.argv)
        self._initUI()
        sys.exit(self.App.exec_())


    def _initUI(self):
        self._initwindow()

        self._initcentralwidget()

        self._mainwindow.show()

    def _initwindow(self):
        self._mainwindow = QMainWindow()
        self._mainwindow.setWindowTitle("Image Forester")

    def _initcentralwidget(self):
        self._centralwidget = QWidget()
        self._layout = QVBoxLayout(self._centralwidget)
        self._mainwindow.setCentralWidget(self._centralwidget)

if __name__ == "__main__":
    MainGui()
