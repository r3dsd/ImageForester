from .r3history import R3MoveHistory, R3RemoveHistory, R3HistoryData
from collections import deque

from ..logger import get_logger

logger = get_logger(__name__)

class R3HistoryManager:
    """
    undo 관리자
    """
    _undo_history: deque[R3HistoryData] = deque(maxlen=10)

    @classmethod
    def add_history(cls, task: R3HistoryData):
        cls._undo_history.append(task)
        return task

    @classmethod
    def add_delete_history(cls, source, item, item_index):
        task = cls.add_history(R3RemoveHistory(source, item, item_index))
        logger.info(f"{task} from {source.objectName()}")

    @classmethod
    def add_move_history(cls, source, destination, item, source_index):
        task = cls.add_history(R3MoveHistory(source, destination, item, source_index))
        logger.info(f"{task} from {source.objectName()} to {destination.objectName()}")

    @classmethod
    def undo(cls):
        if cls._undo_history:
            undo_data: R3HistoryData = cls._undo_history.pop()
            undo_data.rollback()
        else:
            logger.info("No more undo history")

    @classmethod
    def clear(cls):
        cls._undo_history.clear()
