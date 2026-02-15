import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")

EN_PATH = os.path.join(DATA_DIR, "english.json")
BN_PATH = os.path.join(DATA_DIR, "bangla.json")


class SemanticRetriever:

    def __init__(self):
        self.model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

        self.en_docs = self.load_json(EN_PATH)
        self.bn_docs = self.load_json(BN_PATH)

        self.en_corpus = [doc["content"] for doc in self.en_docs]
        self.bn_corpus = [doc["content"] for doc in self.bn_docs]

        print("🔄 Encoding English docs...")
        self.en_embeddings = self.model.encode(self.en_corpus, show_progress_bar=True)

        print("🔄 Encoding Bangla docs...")
        self.bn_embeddings = self.model.encode(self.bn_corpus, show_progress_bar=True)

    def load_json(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def search(self, query, language="en", top_k=5):
        query_embedding = self.model.encode([query])

        if language == "en":
            sim = cosine_similarity(query_embedding, self.en_embeddings)[0]
            docs = self.en_docs
        else:
            sim = cosine_similarity(query_embedding, self.bn_embeddings)[0]
            docs = self.bn_docs

        top_indices = np.argsort(sim)[::-1][:top_k]
        return [(docs[i]["title"], sim[i]) for i in top_indices]
