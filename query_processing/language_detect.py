import re

def detect_language(text: str) -> str:
    """
    Detect whether query is Bangla or English.
    Returns: 'bn' or 'en'
    """

    # Bangla Unicode range check
    bangla_pattern = re.compile(r'[\u0980-\u09FF]')

    if bangla_pattern.search(text):
        return "bn"
    else:
        return "en"
