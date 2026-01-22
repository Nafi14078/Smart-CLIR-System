import pickle
import re

# =========================
# Paths
# =========================
BM25_PATH = "../data/index/bm25_index.pkl"
META_PATH = "../data/index/doc_metadata.pkl"

# =========================
# Preprocessing (MUST MATCH INDEXING)
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
# Load Index
# =========================
print("\n📦 Loading BM25 index...")
with open(BM25_PATH, "rb") as f:
    bm25 = pickle.load(f)

with open(META_PATH, "rb") as f:
    metadata = pickle.load(f)

print(f"✅ Loaded {len(metadata)} documents")

# =========================
# Search Function
# =========================
def bm25_search(query, top_k=10):
    tokens = tokenize(query)
    scores = bm25.get_scores(tokens)

    ranked = sorted(
        enumerate(scores),
        key=lambda x: x[1],
        reverse=True
    )

    results = []
    for idx, score in ranked[:top_k]:
        doc = metadata[idx]
        results.append({
            "score": round(score, 4),
            "title": doc["title"],
            "source": doc["source"],
            "language": doc["language"]
        })

    return results


# =========================
# Interactive Query
# =========================
if __name__ == "__main__":
    while True:
        query = input("\n🔎 Enter your query (or type 'exit'): ")
        if query.lower() == "exit":
            break

        results = bm25_search(query, top_k=10)

        print("\n📄 Top Results:")
        for i, res in enumerate(results, 1):
            print(f"\n{i}. [{res['language'].upper()}]")
            print(f"   Title : {res['title']}")
            print(f"   Source: {res['source']}")
            print(f"   Score : {res['score']}")
