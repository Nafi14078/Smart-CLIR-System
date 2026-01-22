from langdetect import detect

def detect_language(text: str) -> str:
    try:
        lang = detect(text)
        if lang == "bn":
            return "bangla"
        else:
            return "english"
    except:
        return "unknown"
