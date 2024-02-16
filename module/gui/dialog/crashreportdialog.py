from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QFrame, QPushButton, QHBoxLayout, QTextEdit, QSizePolicy
import winsound

class CrashReportDialog(QDialog):
    def __init__(self, parent=None, error_log=""):
        super().__init__(parent)
        winsound.PlaySound("SystemAsterisk", winsound.SND_ASYNC | winsound.SND_ALIAS)
        self.setWindowTitle("Crash Report")
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint | Qt.CustomizeWindowHint)

        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 오류 메시지 레이블
        message_label = QLabel("<span style='color:#F55;'><b>The program has crashed</b></span>. If you want to send the crash log to the developer, <br><b>Click the 'Send Report' button.</b>")
        message_label.setTextFormat(Qt.RichText)
        message_label.setWordWrap(True)
        message_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        message_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        layout.addWidget(message_label)
        
        # 오류 로그를 표시할 텍스트 영역
        error_log_text_edit = QTextEdit()
        error_log_text_edit.setMinimumSize(500, 200)
        error_log_text_edit.setReadOnly(True)
        error_log_text_edit.setPlainText(error_log)
        error_log_text_edit.setLineWrapMode(QTextEdit.NoWrap)
        error_log_text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(error_log_text_edit)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

        # 버튼 레이아웃
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        send_report_button = QPushButton("Send Report")
        send_report_button.clicked.connect(self.send_report)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(send_report_button)

        self.setFixedSize(self.sizeHint())

    def send_report(self):
        print("not implemented yet.")
        super().accept()