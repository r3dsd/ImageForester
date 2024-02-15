from PyQt5.QtWidgets import QMessageBox
import winsound

class PopupFactory:
    @staticmethod
    def show_error_message(parent, message):
        winsound.PlaySound("SystemAsterisk", winsound.SND_ASYNC | winsound.SND_ALIAS)
        QMessageBox.critical(parent, "Error", message)

    @staticmethod
    def show_info_message(parent, message):
        winsound.PlaySound("SystemAsterisk", winsound.SND_ASYNC | winsound.SND_ALIAS)
        QMessageBox.information(parent, "Info", message)
    
    @staticmethod
    def show_warning_message(parent, message):
        winsound.PlaySound("SystemAsterisk", winsound.SND_ASYNC | winsound.SND_ALIAS)
        QMessageBox.warning(parent, "Warning", message)

    @staticmethod
    def show_question_message(parent, title, message):
        winsound.PlaySound("SystemAsterisk", winsound.SND_ASYNC | winsound.SND_ALIAS)
        return QMessageBox.question(parent, title, message, QMessageBox.Yes | QMessageBox.No)
    
    @staticmethod
    def show_yes_no_cancel_message(parent, title, message):
        winsound.PlaySound("SystemAsterisk", winsound.SND_ASYNC | winsound.SND_ALIAS)
        return QMessageBox.question(parent, title, message, QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)