import pickle
import re

# =========================
# Paths
# =========================
BM25_PATH = "../data/index/bm25_index.pkl"
META_PATH = "../data/index/doc_metadata.pkl"

# =========================
# Preprocessing (same as before)
# =========================
def clean_text(text):
    text = text.lower()
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"[^\w\s\u0980-\u09ff]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def tokenize(text):
    return clean_text(text).split()

# =========================
# SIMPLE BANGLA → ENGLISH DICTIONARY
# (Extendable – good for viva)
# =========================
BN_EN_DICT = {
    "নির্বাচন": "election",
    "রাজনীতি": "politics",
    "সরকার": "government",
    "অর্থনীতি": "economy",
    "দুর্নীতি": "corruption",
    "জলবায়ু": "climate",
    "পরিবর্তন": "change",
    "বাজেট": "budget",
    "শিক্ষা": "education",
    "স্বাস্থ্য": "health",
    "সংকট": "crisis",
    "আইন": "law",
    "আদালত": "court",
    "সংসদ": "parliament"
}

# =========================
# Query Translation
# =========================
def translate_bn_to_en(query):
    tokens = tokenize(query)
    translated = []

    for word in tokens:
        translated.append(BN_EN_DICT.get(word, word))

    return " ".join(translated)

# =========================
# Load BM25 Index
# =========================
print("\n📦 Loading BM25 index...")
with open(BM25_PATH, "rb") as f:
    bm25 = pickle.load(f)

with open(META_PATH, "rb") as f:
    metadata = pickle.load(f)

print(f"✅ Loaded {len(metadata)} documents")

# =========================
# CLIR Search
# =========================
def clir_search(bangla_query, top_k=10):
    translated_query = translate_bn_to_en(bangla_query)
    tokens = tokenize(translated_query)
    scores = bm25.get_scores(tokens)

    ranked = sorted(
        enumerate(scores),
        key=lambda x: x[1],
        reverse=True
    )

    results = []
    for idx, score in ranked[:top_k]:
        doc = metadata[idx]
        if doc["language"] == "english":
            results.append({
                "score": round(score, 4),
                "title": doc["title"],
                "source": doc["source"]
            })

    return translated_query, results

# =========================
# Interactive Mode
# =========================
if __name__ == "__main__":
    while True:
        query = input("\n🔎 Enter Bangla query (or 'exit'): ")
        if query.lower() == "exit":
            break

        translated, results = clir_search(query)

        print(f"\n🌐 Translated Query: {translated}")
        print("\n📄 Top English Results:")

        for i, res in enumerate(results, 1):
            print(f"\n{i}. Title : {res['title']}")
            print(f"   Score : {res['score']}")
