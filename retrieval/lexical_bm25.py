import json
import os
import numpy as np
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")

EN_PATH = os.path.join(DATA_DIR, "english.json")
BN_PATH = os.path.join(DATA_DIR, "bangla.json")


class LexicalRetriever:
    def __init__(self):
        self.en_docs = self.load_json(EN_PATH)
        self.bn_docs = self.load_json(BN_PATH)

        self.en_corpus = [doc["content"] for doc in self.en_docs]
        self.bn_corpus = [doc["content"] for doc in self.bn_docs]

        self.en_tokens = [doc.split() for doc in self.en_corpus]
        self.bn_tokens = [doc.split() for doc in self.bn_corpus]

        self.bm25_en = BM25Okapi(self.en_tokens)
        self.bm25_bn = BM25Okapi(self.bn_tokens)

        # TF-IDF vectorizers
        self.tfidf_en = TfidfVectorizer()
        self.tfidf_bn = TfidfVectorizer()

        self.tfidf_matrix_en = self.tfidf_en.fit_transform(self.en_corpus)
        self.tfidf_matrix_bn = self.tfidf_bn.fit_transform(self.bn_corpus)

    def load_json(self, path):
        if not os.path.exists(path):
            return []
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    # ---------------- BM25 ----------------
    def search_bm25(self, query, language="en", top_k=5):
        tokens = query.split()

        if language == "en":
            scores = self.bm25_en.get_scores(tokens)
            docs = self.en_docs
        else:
            scores = self.bm25_bn.get_scores(tokens)
            docs = self.bn_docs

        top_indices = np.argsort(scores)[::-1][:top_k]
        results = [(docs[i]["title"], scores[i]) for i in top_indices]

        return results

    # ---------------- TF-IDF ----------------
    def search_tfidf(self, query, language="en", top_k=5):
        if language == "en":
            query_vec = self.tfidf_en.transform([query])
            sim = cosine_similarity(query_vec, self.tfidf_matrix_en).flatten()
            docs = self.en_docs
        else:
            query_vec = self.tfidf_bn.transform([query])
            sim = cosine_similarity(query_vec, self.tfidf_matrix_bn).flatten()
            docs = self.bn_docs

        top_indices = np.argsort(sim)[::-1][:top_k]
        results = [(docs[i]["title"], sim[i]) for i in top_indices]

        return results
