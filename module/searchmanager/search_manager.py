from ..data.data_container import DataContainer
from ..data.imagefiledata import ImageFileData

class SearchManager:
    @staticmethod
    def search(search_keywords: list[str]):
        result: set[ImageFileData] = set()

        normal_keywords = []
        negated_keywords = []
        exact_keywords = []
        negated_exact_keywords = []

        while search_keywords:
            keyword = search_keywords.pop(0)
            if keyword.startswith('~!'):
                negated_exact_keywords.append(keyword[2:])
            elif keyword.startswith('~'):
                exact_keywords.append(keyword[1:])
            elif keyword.startswith('!'):
                negated_keywords.append(keyword[1:])
            else:
                normal_keywords.append(keyword)

        print(f'Normal Keywords: {normal_keywords}')
        print(f'Negated Keywords: {negated_keywords}')
        print(f'Exact Keywords: {exact_keywords}')
        print(f'Negated Exact Keywords: {negated_exact_keywords}')

        for image_info in DataContainer.get_loaded_data():
            match = True

            # Normal keyword search
            for keyword in normal_keywords:
                if keyword and not boyer_moore(image_info.file_tags_text, keyword):
                    match = False
                    break

            if match:
                # Negated keyword search
                for keyword in negated_keywords:
                    if boyer_moore(image_info.file_tags_text, keyword):
                        match = False
                        break

            if match:
                # Exact keyword search
                for keyword in exact_keywords:
                    if not perfect_match(image_info.file_tags_list, keyword):
                        match = False
                        break

            if match:
                # Negated exact keyword search
                for keyword in negated_exact_keywords:
                    if perfect_match(image_info.file_tags_list, keyword):
                        match = False
                        break
            if match:
                    result.add(image_info)
        print(f'result: {len(result)}')
        return result

def boyer_moore(text: str, pattern: str):
    text_length = len(text)
    pattern_length = len(pattern)
    skip = []
    if pattern_length == 0:
        return False
    for i in range(256):
        skip.append(pattern_length)
    for i in range(pattern_length - 1):
        skip[ord(pattern[i])] = pattern_length - i - 1
    i = pattern_length - 1
    while i < text_length:
        j = pattern_length - 1
        k = i
        while j >= 0 and text[k] == pattern[j]:
            j -= 1
            k -= 1
        if j == -1:
            return True
        i += skip[ord(text[i])]
    return False

def perfect_match(text_list: list[str], pattern: str):
    for text in text_list:
        if text == pattern:
            return True
    return False