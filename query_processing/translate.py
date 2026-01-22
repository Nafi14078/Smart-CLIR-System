from deep_translator import GoogleTranslator

def translate_query(text, src_lang, tgt_lang):
    try:
        return GoogleTranslator(source=src_lang, target=tgt_lang).translate(text)
    except:
        return text
