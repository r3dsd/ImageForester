import re

from ..logger import get_logger

logger = get_logger(__name__)

def HighlightingText(text: str, keywords: list[str]):
    words = [text.strip() for text in text.split(',')]

    for i in range(len(words)):
        for keyword in keywords:
            if keyword.startswith('~'):
                if words[i] == keyword[1:]:
                    words[i] = "<span style='background-color: #0F0'>" + words[i] + "</span>"
            else:
                if keyword in words[i]:
                    words[i] = words[i].replace(keyword, "<span style='background-color: #F00'>" + keyword + "</span>")
    return ', '.join(words)

def check_save_folder_name(folder_name: str):
    invalid_chars = r'[\<\>:"/\\|?*]'
    if folder_name and not re.search(invalid_chars, folder_name):
        logger.info(f"folder_name: {folder_name} is valid.")
        return True
    logger.info(f"folder_name: {folder_name} is invalid. do not use [\<\>:\"/\\|?*]")
    return False