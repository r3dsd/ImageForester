PROGRAM_NAME = 'Image Forester'
PROGRAM_VERSION = '0.0.1'
PROGRAM_AUTHOR = 'r3dsd'

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
            }
            QPushButton {
                border-radius: 5px;
                padding: 6px;
                background-color: #DDD;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #CCC;
            }
            QPushButton:pressed {
                background-color: #FFF;
            }
            QPushButton:disabled {
                background-color: #EEE;
                text-decoration: line-through;
            }
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