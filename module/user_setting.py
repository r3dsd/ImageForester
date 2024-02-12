from .r3util import r3path
import json

class UserSetting:
    SETTING = {}
    DEFALUT_SETTING = {
        'IMAGE_SOURCE_DIR' : '',
        'IMAGE_SAVE_DIR' : r3path.get_defalut_save_path(), # Image save directory
        'SAVE_MODE' : 'Copy', # Save mode (Copy, Move)
        'STEALTH_MODE' : False, # Stealth mode (True, False)
    }
    @classmethod
    def load(cls) -> None:
        try:
            if r3path.check_path_exists('User_Settings.json'):
                print('User_Settings.json exists... loading...')
                with open('User_Settings.json', 'r') as f:
                    cls.SETTING = json.load(f)
            else:
                print('User_Settings.json does not exist... creating...')
                cls.SETTING = cls.DEFALUT_SETTING
                with open('User_Settings.json', 'w') as f:
                    json.dump(cls.SETTING, f)

            print('successfully loaded User_Settings.json...')
            for key, value in cls.SETTING.items():
                print(f'[{key}] : {value}')
        except Exception as e:
            print(f'UserSetting File is broken... {e} ... creating new UserSetting file...')
            cls.SETTING = cls.DEFALUT_SETTING
            cls.save()
            
    @classmethod
    def save(cls) -> None:
        try:
            with open('User_Settings.json', 'w') as f:
                json.dump(cls.SETTING, f)
                print('User_Settings.json saved...')
        except Exception as e:
            print(f'Error: {e}')

    @classmethod
    def get(cls, key: str) -> str:
        try:
            if key == 'SAVE_MODE':
                assert cls.SETTING[key] == 'Copy' or cls.SETTING[key] == 'Move', f'UserSetting : {key} is not in UserSetting'
            return cls.SETTING[key]
        except:
            RuntimeError(f"UserSetting : {key} is not in UserSetting")
    
    @classmethod
    def set(cls, key: str, value: str) -> None:
        print(f"UserSetting Changed: [{key}] : {cls.SETTING[key]} -> {value}")
        if cls.SETTING.keys().__contains__(key):
            cls.SETTING[key] = value
        else:
            raise RuntimeError(f"UserSetting : {key} is not in UserSetting")