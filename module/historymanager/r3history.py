from abc import ABC, abstractmethod
from PyQt5.QtWidgets import QListWidget, QListWidgetItem

class R3HistoryData(ABC):
    """
    undo/redo abstract class
    """
    @abstractmethod
    def rollback(self):
        pass

class R3RemoveHistory(R3HistoryData):
    """
    remove history
    """
    def __init__(self, source: QListWidget, item: QListWidgetItem, item_index: int):
        self.source = source
        self.item = item
        self.item_index = item_index

    def rollback(self):
        self.source.insertItem(self.item_index, self.item)
        self.source.setFocus()
        self.source.scrollToItem(self.item)
        self.source.setCurrentItem(self.item)
        super().rollback()

    def __str__(self):
        return f"[deleted] - {self.item.text()}"
    
class R3MoveHistory(R3HistoryData):
    """
    move history
    """
    def __init__(self, source: QListWidget, destination: QListWidget, item: QListWidgetItem, source_index: int):
        self.source = source
        self.destination = destination
        self.item = item
        self.source_index = source_index

    def rollback(self):
        taked_item = self.destination.takeItem(self.destination.row(self.item))
        self.source.insertItem(self.source_index, taked_item)
        self.source.setFocus()
        self.source.scrollToItem(taked_item)
        self.source.setCurrentItem(taked_item)
        super().rollback()

    def __str__(self):
        return f"[moved] - {self.item.text()}"