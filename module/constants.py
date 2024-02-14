from enum import Enum

PROGRAM_NAME = 'Image Forester'
PROGRAM_VERSION = 'v0.0.1'
PROGRAM_AUTHOR = 'r3dsd'

IMAGE_FORMATS = ('.png')

class GUI_STYLE(Enum):
    DARK = 0
    LIGHT = 1
    LIGHT_GREEN = 2

GUI_STYLE_SHEET = {
    'DARK': """
            QWidget{
                background-color: #333;
                color: #FFF;
            }
            QLineEdit{
                border-radius: 5px;
                background-color: #444;
            }
            QListWidget, QLabel {
                border-radius: 5px;
                background-color: #444;
                padding: 5px;
            }
            QPushButton {
                border-radius: 5px;
                background-color: #555;
                padding: 5px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #666;
            }
            QPushButton:pressed {
                background-color: #333;
            }
            QPushButton:disabled {
                background-color: #222;
                text-decoration: line-through;
            }
            QCheckBox {
                spacing: 5px;
            }
            QCheckBox::indicator {
                width:  25px;
                height: 25px;
                background-color: #444;
                border : 1px solid #FFF;
            }
            QCheckBox::indicator:unchecked {
                background-color: #444;
            }
            QCheckBox::indicator:checked {
                background-color: #7F7;
            }
            QComboBox:!editable, QComboBox::drop-down:editable {
                background: #444;
            }
            QComboBox QAbstractItemView {
                selection-background-color: #888;
            }
            QComboBox::item:selected {
                background: #EEE;
                color: #111;
            }
            QMenuBar {
                background-color: #333;
                color: #FFF;
                border-bottom: 2px solid #444;
            }
            QMenuBar::item {
                background-color: #333;
                color: #FFF;
                margin: 5px;
                min-width: 80px;
            }
            QMenuBar::item::selected {
                background-color: rgb(30,30,30);
            }
            QMenu {
                background-color: #333;
                color: #FFF;        
            }
            QMenu::item::selected {
                background-color: #111;
            }
            QToolTip {
                background-color: #444;
                color: #FFF;
                border: 1px solid #FFF;
            }
        """,
    'LIGHT': """
            QWidget{
                background-color: #FFF;
                color: #333;
            }
            QLineEdit{
                border-radius: 5px;
                background-color: #EEE;
            }
            QListWidget, QLabel {
                border-radius: 5px;
                background-color: #EEE;
                padding: 5px;
            }
            QPushButton {
                border-radius: 5px;
                background-color: #DDD;
                padding: 5px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #CCC;
            }
            QPushButton:pressed {
                background-color: #AAA;
            }
            QPushButton:disabled {
                background-color: #AAA;
                text-decoration: line-through;
            }
            QCheckBox {
                spacing: 5px;
            }
            QCheckBox::indicator {
                width:  25px;
                height: 25px;
                background-color: #EEE;
                border : 1px solid #333;
            }
            QCheckBox::indicator:unchecked {
                background-color: #EEE;
            }
            QCheckBox::indicator:checked {
                background-color: #7F7;
            }
            QComboBox:!editable, QComboBox::drop-down:editable {
                background: #EEE;
            }
            QComboBox QAbstractItemView {
                border: 3px solid #FFF;
                selection-background-color: #444;
            }
            QComboBox::item:selected {
                background: #111;
                color: #FFF;
            }
            QMenuBar {
                background-color: #FFF;
                color: #333;
                border-bottom: 2px solid #EEE;
            }
            QMenuBar::item {
                background-color: #FFF;
                color: #333;
                margin: 5px;
                min-width: 80px;
            }
            QMenuBar::item::selected {
                background-color: #EEE;
            }
            QMenu {
                background-color: #FFF;
                color: #333;        
            }
            QMenu::item::selected {
                background-color: #EEE;
            }
            QToolTip {
                background-color: #EEE;
                color: #333;
                border: 1px solid #333;
            }
        """,
    'LIGHT_GREEN': """
            QWidget{
                background-color: #AEF6CF;
                color: #333;
            }
            QLineEdit{
                border-radius: 5px;
                background-color: #A2D9CE;
            }
            QListWidget, QLabel {
                border-radius: 5px;
                background-color: #A2D9CE;
                padding: 5px;
            }
            QPushButton {
                border-radius: 5px;
                background-color: #A2D9CE;
                padding: 5px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #A2D9CE;
            }
            QPushButton:pressed {
                background-color: #A2D9CE;
            }
            QPushButton:disabled {
                background-color: #74D3C1;
                text-decoration: line-through;
            }
            QCheckBox {
                spacing: 5px;
            }
            QCheckBox::indicator {
                width:  25px;
                height: 25px;
                background-color: #A2D9CE;
                border : 1px solid #333;
            }
            QCheckBox::indicator:unchecked {
                background-color: #A2D9CE;
            }
            QCheckBox::indicator:checked {
                background-color: #7F7;
            }
            QComboBox:!editable, QComboBox::drop-down:editable {
                background: #A2D9CE;
            }
            QComboBox QAbstractItemView {
                border: 3px solid #FFF;
                selection-background-color: #444;
            }
            QComboBox::item:selected {
                background: #111;
                color: #FFF;
            }
            QMenuBar {
                background-color: #AEF6CF;
                color: #333;
                border-bottom: 2px solid #A2D9CE;
            }
            QMenuBar::item {
                background-color: #AEF6CF;
                color: #333;
                margin: 5px;
                min-width: 80px;
            }
            QMenuBar::item::selected {
                background-color: #A2D9CE;
            }
            QMenu {
                background-color: #AEF6CF;
                color: #333;        
            }
            QMenu::item::selected {
                background-color: #A2D9CE;
            }
            QToolTip {
                background-color: #A2D9CE;
                color: #333;
                border: 1px solid #333;
            }
    """
}