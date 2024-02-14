# Module configuration file

FILEMANAGER_CONFIG = {
    'SAVE_FILE_NAME' : '',
    'FINAL_SAVE_FOLDER_PATH' : ''
}

TAGGER_CONFIG ={
    'IMAGE_TAGGER_INPUT_DIR' : '',
    'IMAGE_TAGGER_CONFIDENCE_THRESHOLD' : 0.5,
    'MODEL_NAME' : 'model.onnx',
    'TAGS_FILE_NAME': 'selected_tags.csv'
}

HF_CONFIG = {
    'HF_REPO_ID' : 'r3dsd/ImageForester',
    'HF_MODEL_DIR' : './module/model'
}