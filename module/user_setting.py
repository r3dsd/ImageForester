from enum import Enum, auto
import json
from .logger import get_logger
from .r3util import r3path

logger = get_logger(__name__)

class Savemode(Enum):
    Copy = "Copy"
    Move = "Move"

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name

# UserSetting
class UserSetting:
    SETTING = {}
    DEFALUT_SETTING = {
        'IMAGE_SAVE_DIR' : r3path.get_defalut_save_path(), # Image save directory
        'SAVE_MODE' : 'Copy', # Save mode ('Copy', 'Move')
        'STEALTH_MODE' : False, # Stealth mode (True, False)
        'AUTO_LOAD' : False, # Auto load (True, False) Default: False
        'AUTO_GENERATE_FOLDER_NAME' : False, # Auto typing save folder (True, False) Default: False
        'DISABLE_OPEN_FOLDER_POPUP' : False, # open folder popup show (True, False) Default: False
        'GUI_STYLE' : 'DARK', # GUI Style ('DARK', 'LIGHT')
        'FORCE_DELETE' : False, # Force delete (True, False) Default: False
        'AUTO_DELETE_AFTER_TAGGING' : False, # Auto delete after tagging (True, False) Default: False
    }
    @classmethod
    def load(cls) -> None:
        try:
            if r3path.check_path_exists('User_Settings.json'):
                logger.info('User_Settings.json exists... loading...')
                with open('User_Settings.json', 'r') as f:
                    cls.SETTING = json.load(f)

                missing_keys = list(set(cls.DEFALUT_SETTING.keys()) - set(cls.SETTING.keys()))
                if missing_keys:
                    logger.info(f'User_Settings.json is missing options: {missing_keys} ... updating...')
                    for key in missing_keys:
                        cls.SETTING[key] = cls.DEFALUT_SETTING[key]
                    with open('User_Settings.json', 'w') as f:
                        json.dump(cls.SETTING, f, indent=4)
                    logger.info('User_Settings.json updated...')
            else:
                logger.info('User_Settings.json does not exists... creating new User_Settings.json...')
                cls.SETTING = cls.DEFALUT_SETTING
                with open('User_Settings.json', 'w') as f:
                    json.dump(cls.SETTING, f, indent=4)

            logger.info("successfully loaded User_Settings.json...")
            for key, value in cls.SETTING.items():
                logger.info(f"UserSetting : [{key}] : {value}")
        except Exception as e:
            logger.warning(f'Error: {e}')
            cls.SETTING = cls.DEFALUT_SETTING
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
            cls.SETTING = cls.DEFALUT_SETTING
            cls.save()

    @classmethod
    def get(cls, key: str) -> str | bool:
        try:
            if key == 'SAVE_MODE':
                assert cls.SETTING[key] == 'Copy' or cls.SETTING[key] == 'Move', f'UserSetting : {key} is not in UserSetting'
                return Savemode[cls.SETTING[key]]
            elif key == 'GUI_STYLE':
                assert cls.SETTING[key] == 'DARK' or cls.SETTING[key] == 'LIGHT' or cls.SETTING[key] == 'LIGHT_GREEN', f'UserSetting : {key} is not in UserSetting'
            return cls.SETTING[key]
        except:
            logger.error(f"UserSetting : {key} is not in UserSetting")
            RuntimeError(f"UserSetting : {key} is not in UserSetting")
    
    @classmethod
    def set(cls, key: str, value: str) -> None:
        logger.info(f"UserSetting Changed: [{key}] : {cls.SETTING[key]} -> {value}")
        if cls.SETTING.keys().__contains__(key):
            cls.SETTING[key] = value
        else:
            logger.error(f"UserSetting : {key} is not in UserSetting")
            raise RuntimeError(f"UserSetting : {key} is not in UserSetting")