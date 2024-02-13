from PyQt5.QtWidgets import QToolBar, QMenu, QAction

class MyToolBar(QToolBar):
    def __init__(self, parent=None):
        super(MyToolBar, self).__init__(parent)

        self.action1 = QAction("Test", self)
        self.action1.triggered.connect(self.action1_triggered)
        self.addAction(self.action1)

    def action1_triggered(self):
        self.showContextMenuForAction(self.action1)

    def showContextMenuForAction(self, action):
        menu = QMenu()
        menu.addAction("Detail 1")
        menu.addAction("Detail 2")
        
        actionWidget = self.widgetForAction(action)
        if actionWidget:
            pos = actionWidget.mapToGlobal(actionWidget.rect().bottomLeft())
            menu.exec_(pos)