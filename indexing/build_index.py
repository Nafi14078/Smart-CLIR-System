"""
Build BM25 Index
Run from root:

    python -m indexing.build_index
"""

import json
import math
import re
from pathlib import Path
from collections import defaultdict
from tqdm import tqdm


# ======================================================
# CONFIG
# ======================================================

DATA_DIR = Path("data/processed")
EN_FILE = DATA_DIR / "english_docs.json"
BN_FILE = DATA_DIR / "bangla_docs.json"

INDEX_DIR = Path("data/index")
INDEX_DIR.mkdir(parents=True, exist_ok=True)

EN_INDEX_FILE = INDEX_DIR / "english_index.json"
BN_INDEX_FILE = INDEX_DIR / "bangla_index.json"


# ======================================================
# PREPROCESSING
# ======================================================

def tokenize(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    return text.split()


# ======================================================
# BM25 INDEX BUILDER
# ======================================================

def build_bm25_index(docs):

    inverted_index = defaultdict(dict)
    doc_lengths = {}
    total_docs = len(docs)

    print("\n🧹 Preprocessing + Indexing...")

    for doc_id, doc in tqdm(enumerate(docs), total=total_docs):

        text = doc.get("body", "")
        tokens = tokenize(text)

        doc_lengths[str(doc_id)] = len(tokens)

        term_freq = defaultdict(int)
        for token in tokens:
            term_freq[token] += 1

        for term, freq in term_freq.items():
            inverted_index[term][str(doc_id)] = freq

    avg_doc_len = sum(doc_lengths.values()) / total_docs

    return {
        "inverted_index": inverted_index,
        "doc_lengths": doc_lengths,
        "avg_doc_len": avg_doc_len,
        "total_docs": total_docs
    }


# ======================================================
# MAIN
# ======================================================

def main():

    print("\n📥 Loading documents...")

    with open(EN_FILE, "r", encoding="utf-8") as f:
        en_docs = json.load(f)

    with open(BN_FILE, "r", encoding="utf-8") as f:
        bn_docs = json.load(f)

    print(f"✅ English docs: {len(en_docs)}")
    print(f"✅ Bangla docs : {len(bn_docs)}")

    # ------------------------
    # English Index
    # ------------------------
    en_index = build_bm25_index(en_docs)

    with open(EN_INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(en_index, f)

    print("✅ English index saved.")

    # ------------------------
    # Bangla Index
    # ------------------------
    bn_index = build_bm25_index(bn_docs)

    with open(BN_INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(bn_index, f)

    print("✅ Bangla index saved.")

    print("\n🎯 Indexing Completed Successfully!")


if __name__ == "__main__":
    main()
