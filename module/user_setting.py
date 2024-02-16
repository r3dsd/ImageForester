from enum import Enum, auto
import json

from .logger import get_logger
from .r3util import r3path

logger = get_logger(__name__)

class SaveModeEnum(Enum):
    COPY = auto()
    MOVE = auto()
    def get_display_str(self) -> str:
        if self == self.COPY:
            return 'Copy mode'
        elif self == self.MOVE:
            return 'Move mode'
    @staticmethod
    def get_all_enum() -> list[str]:
        return list(SaveModeEnum.__members__.values())

class GUIModeEnum(Enum):
    DARK = auto()
    LIGHT = auto()
    LIGHT_GREEN = auto()
    def get_display_str(self) -> str:
        if self == self.DARK:
            return 'Dark Theme'
        elif self == self.LIGHT:
            return 'Light Theme'
        elif self == self.LIGHT_GREEN:
            return 'Light Green Theme'
    @staticmethod
    def get_all_enum() -> list[str]:
        return list(GUIModeEnum.__members__.values())

# UserSetting
class UserSetting:
    SETTING = {}
    DEFAULT_SETTING = {
        'SAVE_PATH' : r3path.get_defalut_save_path(), # Image save directory
        'SAVE_MODE' : 'COPY', # Save mode ('COPY', 'MOVE') Default: 'COPY'
        'STEALTH_MODE' : False, # Stealth mode (True, False)
        'AUTO_LOAD' : False, # Auto load (True, False) Default: False
        'AUTO_GENERATE_FOLDER_NAME' : False, # Auto typing save folder (True, False) Default: False
        'DISABLE_OPEN_FOLDER_POPUP' : False, # open folder popup show (True, False) Default: False
        'GUI_STYLE' : 'DARK', # GUI Style ('DARK', 'LIGHT', 'LIGHT_GREEN') Default: 'DARK'
        'FORCE_DELETE' : False, # Force delete (True, False) Default: False
        'AUTO_DATABASE' : False, # on program start, auto load database (True, False) Default: False 
        'AUTO_DELETE_AFTER_TAGGING' : False, # Auto delete after tagging (True, False) Default: False
    }
    @classmethod
    def load(cls) -> None:
        try:
            if r3path.check_path_exists('User_Settings.json'):
                logger.info('User_Settings.json exists... loading...')
                with open('User_Settings.json', 'r') as f:
                    cls.SETTING = json.load(f)

                missing_keys = list(set(cls.DEFAULT_SETTING.keys()) - set(cls.SETTING.keys()))
                if missing_keys:
                    logger.info(f'User_Settings.json is missing options: {missing_keys} ... updating...')
                    for key in missing_keys:
                        cls.SETTING[key] = cls.DEFAULT_SETTING[key]
                    with open('User_Settings.json', 'w') as f:
                        json.dump(cls.SETTING, f, indent=4)
                    logger.info('User_Settings.json updated...')
            else:
                logger.info('User_Settings.json does not exists... creating new User_Settings.json...')
                cls.SETTING = cls.DEFAULT_SETTING
                with open('User_Settings.json', 'w') as f:
                    json.dump(cls.SETTING, f, indent=4)

            logger.info("successfully loaded User_Settings.json...")
            for key, value in cls.SETTING.items():
                logger.info(f"UserSetting : [{key}] : {value}")
        except Exception as e:
            logger.warning(f'Error: {e}')
            cls.SETTING = cls.DEFAULT_SETTING
            cls.save()
            
    @classmethod
    def save(cls) -> None:
        try:
            with open('User_Settings.json', 'w') as f:
                json.dump(cls.SETTING, f, indent=4)
            logger.info("successfully saved User_Settings.json...")
        except Exception as e:
            logger.warning(f'Error: {e}')
            logger.info("User_Settings.json is missing... creating defalut User_Settings.json...")
            cls.SETTING = cls.DEFAULT_SETTING
            cls.save()

    @classmethod
    def get(cls, key: str) -> str | bool | Enum:
        try:
            value = cls.SETTING.get(key, cls.DEFAULT_SETTING[key])
            if key == 'SAVE_MODE':
                return SaveModeEnum[value]
            elif key == 'GUI_STYLE':
                return GUIModeEnum[value]
            return value
        except KeyError as e:
            logger.error(f"KeyError in UserSetting.get: '{key}' is not a valid setting. Default setting will be used.")
            return cls.get_default_setting(key)
        except AttributeError as e:
            logger.error(f"AttributeError in UserSetting.get: '{value}' is not a valid value for '{key}'. Using default value.")

    @classmethod
    def check(cls, key: str, match=None) -> bool:
        try:
            value = cls.SETTING.get(key, cls.DEFAULT_SETTING[key])
            if match is None:
                logger.info(f"UserSetting Check : {key} : [{value}]")
                return value
            else:
                logger.info(f"UserSetting Check : {key} : [{value}] == [{match}]")
                return value == match
        except KeyError as e:
            logger.error(f"KeyError in UserSetting.check: '{key}' is not a valid setting.")
        except AttributeError as e:
            logger.error(f"AttributeError in UserSetting.check: '{value}' is not a valid value for '{key}'.")

    @classmethod
    def set(cls, key: str, value: str) -> None:
        logger.info(f"UserSetting Changed: [{key}] : {cls.SETTING[key]} -> {value}")
        if cls.SETTING.keys().__contains__(key):
            cls.SETTING[key] = value
        else:
            logger.error(f"UserSetting : {key} is not in UserSetting")
            raise RuntimeError(f"UserSetting : {key} is not in UserSetting")
        
    @classmethod
    def get_default_setting(cls, key: str) -> str | bool | Enum:
        default_value = cls.DEFAULT_SETTING[key]
        logger.info(f"UserSetting : Using Default Setting [{default_value}]")
        if key == 'SAVE_MODE':
            return SaveModeEnum[default_value]
        elif key == 'GUI_STYLE':
            return GUIModeEnum[default_value]
        return default_value