synonyms_en = {
    "car": ["automobile", "vehicle"],
    "buy": ["purchase", "get"],
    "cheap": ["low cost", "affordable"]
}

synonyms_bn = {
    "গাড়ি": ["যানবাহন", "অটো"],
    "কিনতে": ["ক্রয়", "নিতে"],
    "সস্তা": ["কম দাম", "স্বল্পমূল্য"]
}

def expand_query(tokens, lang):
    expanded = set(tokens)

    if lang == "english":
        for t in tokens:
            if t in synonyms_en:
                expanded.update(synonyms_en[t])

    elif lang == "bangla":
        for t in tokens:
            if t in synonyms_bn:
                expanded.update(synonyms_bn[t])

    return list(expanded)
