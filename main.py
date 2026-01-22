from query_processing.language_detect import detect_language
from query_processing.translate import translate_query
from query_processing.expansion import expand_query
from query_processing.ner_mapping import map_named_entities
from query_processing.normalize import normalize


def process_query(query):

    print("Original:", query)

    lang = detect_language(query)
    print("Language:", lang)

    norm = normalize(query)
    print("Normalized:", norm)

    tokens = norm.split()

    tokens = map_named_entities(tokens)
    print("After NE Mapping:", tokens)

    expanded = expand_query(tokens, lang)
    print("After Expansion:", expanded)

    if lang == "bangla":
        translated = translate_query(" ".join(expanded), "bn", "en")
    else:
        translated = translate_query(" ".join(expanded), "en", "bn")

    print("Translated Query:", translated)

    return translated


if __name__ == "__main__":
    q1 = "Cheap car in Bangladesh"
    q2 = "ঢাকায় সস্তা গাড়ি কিনতে চাই"

    process_query(q1)
    print("-" * 40)
    process_query(q2)
