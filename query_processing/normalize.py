import re

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s\u0980-\u09ff]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text
