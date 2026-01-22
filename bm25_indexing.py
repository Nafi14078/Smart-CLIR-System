import json
import os
import re
import pickle
from rank_bm25 import BM25Okapi
from tqdm import tqdm

# =========================
# Paths
# =========================
ENGLISH_PATH = "data/processed/english_docs.json"
BANGLA_PATH = "data/processed/bangla_docs.json"
OUTPUT_DIR = "data/index"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# Text Preprocessing
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
# Safe Text Extractor
# =========================
def get_text(doc):
    """
    Safely extract article text from different possible keys
    """
    for key in ["content", "text", "body", "article", "full_text"]:
        if key in doc and doc[key]:
            return doc[key]
    return ""


# =========================
# Load Documents
# =========================
def load_documents(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


print("\n📥 Loading documents...")
english_docs = load_documents(ENGLISH_PATH)
bangla_docs = load_documents(BANGLA_PATH)

print(f"✅ English docs: {len(english_docs)}")
print(f"✅ Bangla docs : {len(bangla_docs)}")

# =========================
# Prepare Corpus
# =========================
corpus = []
metadata = []

print("\n🧹 Preprocessing documents...")

for doc in tqdm(english_docs, desc="English"):
    text = get_text(doc)
    tokens = tokenize(text)
    if tokens:
        corpus.append(tokens)
        metadata.append({
            "id": doc.get("id", ""),
            "title": doc.get("title", ""),
            "source": doc.get("source", ""),
            "language": "english"
        })

for doc in tqdm(bangla_docs, desc="Bangla"):
    text = get_text(doc)
    tokens = tokenize(text)
    if tokens:
        corpus.append(tokens)
        metadata.append({
            "id": doc.get("id", ""),
            "title": doc.get("title", ""),
            "source": doc.get("source", ""),
            "language": "bangla"
        })

print(f"\n📊 Total indexed documents: {len(corpus)}")

# =========================
# BM25 Indexing
# =========================
print("\n🚀 Building BM25 index...")
bm25 = BM25Okapi(corpus)

# =========================
# Save Index
# =========================
with open(os.path.join(OUTPUT_DIR, "bm25_index.pkl"), "wb") as f:
    pickle.dump(bm25, f)

with open(os.path.join(OUTPUT_DIR, "doc_metadata.pkl"), "wb") as f:
    pickle.dump(metadata, f)

print("\n✅ BM25 indexing completed!")
print("📁 Saved:")
print(" - data/index/bm25_index.pkl")
print(" - data/index/doc_metadata.pkl")
