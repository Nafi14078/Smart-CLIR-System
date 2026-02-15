from nltk.corpus import wordnet


# ==============================
# English Expansion (Controlled)
# ==============================
def expand_english(query: str) -> str:
    words = query.split()
    expanded = set(words)

    for word in words:
        synsets = wordnet.synsets(word)
        if not synsets:
            continue

        # Take only first synset (most common meaning)
        syn = synsets[0]

        count = 0
        for lemma in syn.lemmas():
            candidate = lemma.name().replace("_", " ")

            # Skip long noisy phrases
            if len(candidate.split()) > 2:
                continue

            expanded.add(candidate)
            count += 1

            if count >= 2:
                break

    return " ".join(expanded)


# ==============================
# Bangla Expansion (Simple Root Based)
# ==============================
def expand_bangla(query: str) -> str:
    words = query.split()
    expanded = set(words)

    # Simple rule-based stemming / variants
    suffixes = ["ের", "তে", "রা", "গুলি", "দের"]

    for word in words:
        for suf in suffixes:
            if word.endswith(suf):
                root = word.replace(suf, "")
                if len(root) > 2:
                    expanded.add(root)

    return " ".join(expanded)
