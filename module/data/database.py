import os
import sqlite3
from collections.abc import Iterable
from .imagefiledata import ImageFileData, ImageFileDataFactory

from ..logger import get_logger

logger = get_logger(__name__)

IMAGE_FILE_TABLE = '''
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        path TEXT NOT NULL UNIQUE,
        tags TEXT NOT NULL
    )
'''

NO_TAGS_IMAGE_FILE_TABLE = '''
    CREATE TABLE IF NOT EXISTS no_tags_images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        path TEXT NOT NULL UNIQUE
    )
'''

SELECT_ALL = '''
    SELECT * FROM images
'''

SELECT_PATH = '''
    SELECT path FROM images
'''

SELECT_TAGS = '''
    SELECT tags FROM images
'''

SELECT_IMAGE_DATA = '''
    SELECT path, tags FROM images
'''

SELECT_ID_PATH = '''
    SELECT id, path FROM images
'''

DELETE_USING_PATH = '''
    DELETE FROM images WHERE path=?
'''

INSERT_IMAGE_DATA = '''
    INSERT OR IGNORE INTO images (path, tags) VALUES (?, ?)
'''

class DB:
    def __init__(self, db_path='database.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        logger.debug(f"Succesfully connected to {db_path}")
        self.cursor = self.conn.cursor()
        self._initialize_database()

    def _initialize_database(self):
        self.cursor.execute(IMAGE_FILE_TABLE)
        self.cursor.execute(NO_TAGS_IMAGE_FILE_TABLE)
        self.conn.commit()

    def get_db_paths(self) -> set[str]:
        logger.debug("Get Paths from DB")
        self.cursor.execute(SELECT_PATH)
        data = self.cursor.fetchall()
        return set([path for path, in data])

    def get_data(self) -> set[ImageFileData]:
        logger.debug("Get Data from DB")
        self._verify_check_db()
        self.cursor.execute(SELECT_IMAGE_DATA)
        data = self.cursor.fetchall()
        result = set([ImageFileDataFactory.create(path, tags) for path, tags in data])
        return result

    def add_data(self, data: ImageFileData) -> None:
        logger.debug(f"Add Data: {data.file_path}")
        self.cursor.execute(INSERT_IMAGE_DATA, (data.file_path, data.file_tags_text))
        self.conn.commit()
        logger.debug(f"Database Updated: {self._get_image_count()} images")
    
    def add_datas(self, datas: Iterable) -> None:
        if isinstance(datas, Iterable):
            logger.debug(f"Add Datas: {len(datas)}")
            self.cursor.executemany(INSERT_IMAGE_DATA, [(data.file_path, data.file_tags_text) for data in datas])
            self.conn.commit()
            logger.debug(f"Database Updated: {self._get_image_count()} images")
        else:
            logger.error(f"Add Datas: Not Iterable Type: '{type(datas)}'")

    def delete_data(self, data: ImageFileData) -> None:
        logger.debug(f"Delete Data: {data.file_path}")
        self.cursor.execute(DELETE_USING_PATH, (data.file_path,))
        self.conn.commit()
        logger.debug(f"Database Updated: {self._get_image_count()} images")

    def delete_datas(self, datas: Iterable) -> None:
        if isinstance(datas, Iterable):
            logger.debug(f"Delete Datas: {len(datas)}")
            self.cursor.executemany(DELETE_USING_PATH, [(data.file_path,) for data in datas])
            self.conn.commit()
            logger.debug(f"Database Updated: {self._get_image_count()} images")
        else:
            logger.error(f"Delete Datas: Not Iterable Type: '{type(datas)}'")

    def add_no_tags_data(self, path: str) -> None:
        logger.debug(f"Add No Tags Data: {path}")
        self.cursor.execute('INSERT INTO no_tags_images (path) VALUES (?)', (path,))
        self.conn.commit()

    def add_no_tags_datas(self, paths: Iterable) -> None:
        if isinstance(paths, Iterable):
            logger.debug(f"Add No Tags Datas: {len(paths)}")
            self.cursor.executemany('INSERT INTO no_tags_images (path) VALUES (?)', [(path,) for path in paths])
            self.conn.commit()
        else:
            logger.error(f"Add No Tags Datas: Not Iterable Type: '{type(paths)}'")

    def delete_no_tags_data(self, path: str) -> None:
        logger.debug(f"Delete No Tags Data: {path}")
        self.cursor.execute('DELETE FROM no_tags_images WHERE path=?', (path,))
        self.conn.commit()

    def delete_no_tags_datas(self, paths: Iterable) -> None:
        if isinstance(paths, Iterable):
            logger.debug(f"Delete No Tags Datas: {len(paths)}")
            self.cursor.executemany('DELETE FROM no_tags_images WHERE path=?', [(path,) for path in paths])
            self.conn.commit()
        else:
            logger.error(f"Delete No Tags Datas: Not Iterable Type: '{type(paths)}'")

    def get_no_tags_data(self) -> set[str]:
        logger.debug("Get No Tags Data from DB")
        self.cursor.execute('SELECT path FROM no_tags_images')
        data = self.cursor.fetchall()
        return set([path for path, in data])

    def _verify_check_db(self):
        logger.debug("Verify Check DB Start")
        self.cursor.execute(SELECT_ID_PATH)
        data = self.cursor.fetchall()
        if not data:
            logger.debug("No Data in DB")
            return
        for id, path in data:
            if not os.path.exists(path):
                logger.warning(f"Found Invalid Path: {path} will be deleted from DB")
                self.cursor.execute('DELETE FROM images WHERE id=?', (id,))
        self.conn.commit()
        logger.debug("Verify Check DB End")

    def _get_image_count(self) -> int:
        self.cursor.execute('SELECT COUNT(*) FROM images')
        return self.cursor.fetchone()[0]