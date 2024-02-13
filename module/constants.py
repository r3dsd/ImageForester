PROGRAM_NAME = 'Image Forester'
PROGRAM_VERSION = '0.0.1'
PROGRAM_AUTHOR = 'r3dsd'

IMAGE_FORMATS = ('.png')

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
                border: 3px solid #111;
                selection-background-color: #888;
            }
            QComboBox::item:selected {
                background: #EEE;
                color: #111;
            }
        """,
    'LIGHT': """
            
        """,
    'EASY': """
            QWidget{
                background-color: #333;
                color: #FFF;
                border-radius: 5px;
                border: 1px solid #F11;
            }
            QLineEdit{
                border-radius: 5px;
                background-color: #444;
                border: 1px solid #F11;
            }
            QListWidget, QLabel {
                border-radius: 5px;
                background-color: #444;
                border: 1px solid #F11;
                padding: 5px;
            }
            QPushButton {
                border-radius: 5px;
                padding: 6px;
                background-color: #555;
                min-width: 80px;
                border: 1px solid #F11;
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
                width:  30px;
                height: 30px;
            }
        """
}