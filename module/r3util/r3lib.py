
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