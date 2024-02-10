import json
from r3util import r3path

SETTING = {}

DEFALUT_SETTING = {
    'IMAGE_SAVE_DIR' : r3path.get_program_start_path(), # Image save directory
    'SAVE_MODE' : 'True', # True: Copy mode, False: Move mode
}

TAGGER_CONFIG ={
    'IMAGE_TAGGER_INPUT_DIR' : '',
    'IMAGE_TAGGER_CONFIDENCE_THRESHOLD' : 0.5,
}

HF_CONFIG = {
    'HF_REPO_ID' : 'r3dsd/ImageForester',
    'HF_MODEL_DIR' : './module/model'
}

IMAGE_FORMATS = ('.png')

def option_load() -> None:
    if r3path.check_path_exists('option.json'):
        print('option.json exists... loading...')
        with open('option.json', 'r') as f:
            SETTING = json.load(f)

    else:
        print('option.json does not exist... creating...')
        SETTING = DEFALUT_SETTING
        with open('option.json', 'w') as f:
            json.dump(SETTING, f)

def option_save() -> None:
    with open('option.json', 'w') as f:
        json.dump(SETTING, f)

option_load()