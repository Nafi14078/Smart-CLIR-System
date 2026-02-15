import json
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# ==========================================================
# CONFIG
# ==========================================================

DATA_DIR = Path("data/processed")
EN_PATH = DATA_DIR / "english_docs.json"
BN_PATH = DATA_DIR / "bangla_docs.json"


# ==========================================================
# SEMANTIC RETRIEVER
# ==========================================================

class SemanticRetriever:

    def __init__(self):

        print("🔄 Loading multilingual embedding model...")
        self.model = SentenceTransformer(
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )

        self.en_docs = self.load_json(EN_PATH)
        self.bn_docs = self.load_json(BN_PATH)

        print(f"EN docs: {len(self.en_docs)}")
        print(f"BN docs: {len(self.bn_docs)}")

        self.en_texts = [doc.get("body", "") for doc in self.en_docs]
        self.bn_texts = [doc.get("body", "") for doc in self.bn_docs]

        print("🔄 Encoding English documents...")
        self.en_embeddings = self.model.encode(
            self.en_texts, convert_to_numpy=True, show_progress_bar=True
        )

        print("🔄 Encoding Bangla documents...")
        self.bn_embeddings = self.model.encode(
            self.bn_texts, convert_to_numpy=True, show_progress_bar=True
        )


    def load_json(self, path):
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []


    # ==========================================================
    # SEARCH
    # ==========================================================

    def search(self, query, language="en", top_k=5):

        query_embedding = self.model.encode(
            [query], convert_to_numpy=True
        )

        if language == "en":
            sims = cosine_similarity(query_embedding, self.en_embeddings)[0]
            docs = self.en_docs

        elif language == "bn":
            sims = cosine_similarity(query_embedding, self.bn_embeddings)[0]
            docs = self.bn_docs

        else:
            print("⚠ Invalid language.")
            return []

        ranked = sorted(
            zip(docs, sims),
            key=lambda x: x[1],
            reverse=True
        )[:top_k]

        results = []
        for doc, score in ranked:
            results.append({
                "title": doc.get("title", ""),
                "url": doc.get("url", ""),
                "score": round(float(score), 4)
            })

        return results
