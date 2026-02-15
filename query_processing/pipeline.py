from query_processing.language_detect import detect_language
from query_processing.translate import translate_query
from query_processing.expansion import expand_english, expand_bangla
from query_processing.ner_mapping import map_named_entities


def normalize(text: str) -> str:
    return " ".join(text.lower().strip().split())


def process_query(query: str):
    print(f"\n🔎 Original Query: {query}")

    # 1. Language Detection
    lang = detect_language(query)
    print(f"🌍 Detected Language: {lang}")

    # 2. Normalization
    query = normalize(query)
    print(f"🧹 Normalized: {query}")

    # 3. Named Entity Mapping
    mapped_query = map_named_entities(query)
    print(f"🏷 After NE Mapping: {mapped_query}")

    # 4. Translation
    translated_query = translate_query(mapped_query, lang)
    print(f"🌐 Translated: {translated_query}")

    # 5. Expansion
    if lang == "en":
        expanded_original = expand_english(mapped_query)
        expanded_translated = expand_bangla(translated_query)
    else:
        expanded_original = expand_bangla(mapped_query)
        expanded_translated = expand_english(translated_query)

    print(f"➕ Expanded Original: {expanded_original}")
    print(f"➕ Expanded Translated: {expanded_translated}")

    return {
        "original": expanded_original,
        "translated": expanded_translated,
        "language": lang
    }
