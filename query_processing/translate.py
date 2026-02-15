from deep_translator import GoogleTranslator

def translate_query(text: str, source_lang: str) -> str:
    """
    Translate query between Bangla and English.
    """

    if source_lang == "en":
        target = "bn"
    else:
        target = "en"

    try:
        translated = GoogleTranslator(
            source=source_lang,
            target=target
        ).translate(text)

        return translated

    except Exception as e:
        print(f"⚠ Translation error: {e}")
        return text  # fallback
