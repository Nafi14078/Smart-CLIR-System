import json
from pathlib import Path
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ==========================================================
# CONFIG
# ==========================================================

DATA_DIR = Path("data/processed")
EN_FILE = DATA_DIR / "english_docs.json"
BN_FILE = DATA_DIR / "bangla_docs.json"


# ==========================================================
# UTILS
# ==========================================================

def load_json(path):
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def tokenize(text):
    if not text:
        return []
    return text.lower().split()


# ==========================================================
# LEXICAL RETRIEVER (BM25 + TF-IDF)
# ==========================================================

class LexicalRetriever:

    def __init__(self):

        self.en_docs = load_json(EN_FILE)
        self.bn_docs = load_json(BN_FILE)

        print(f"EN docs: {len(self.en_docs)}")
        print(f"BN docs: {len(self.bn_docs)}")

        # Extract text
        self.en_corpus = [doc.get("body", "") for doc in self.en_docs]
        self.bn_corpus = [doc.get("body", "") for doc in self.bn_docs]

        # ---------- BM25 ----------
        self.en_tokens = [tokenize(doc) for doc in self.en_corpus if doc]
        self.bn_tokens = [tokenize(doc) for doc in self.bn_corpus if doc]

        self.bm25_en = BM25Okapi(self.en_tokens) if self.en_tokens else None
        self.bm25_bn = BM25Okapi(self.bn_tokens) if self.bn_tokens else None

        # ---------- TF-IDF ----------
        self.tfidf_en = TfidfVectorizer()
        self.tfidf_bn = TfidfVectorizer()

        self.en_tfidf_matrix = (
            self.tfidf_en.fit_transform(self.en_corpus)
            if self.en_corpus else None
        )

        self.bn_tfidf_matrix = (
            self.tfidf_bn.fit_transform(self.bn_corpus)
            if self.bn_corpus else None
        )


    # ==========================================================
    # BM25 SEARCH
    # ==========================================================

    def search_bm25(self, query, language="en", top_k=5):

        query_tokens = tokenize(query)

        if language == "en" and self.bm25_en:
            scores = self.bm25_en.get_scores(query_tokens)
            docs = self.en_docs

        elif language == "bn" and self.bm25_bn:
            scores = self.bm25_bn.get_scores(query_tokens)
            docs = self.bn_docs

        else:
            return []

        ranked = sorted(
            zip(docs, scores),
            key=lambda x: x[1],
            reverse=True
        )[:top_k]

        return [
            {
                "title": doc.get("title", ""),
                "url": doc.get("url", ""),
                "score": round(float(score), 4)
            }
            for doc, score in ranked
        ]


    # ==========================================================
    # TF-IDF SEARCH
    # ==========================================================

    def search_tfidf(self, query, language="en", top_k=5):

        if language == "en" and self.en_tfidf_matrix is not None:
            query_vec = self.tfidf_en.transform([query])
            sims = cosine_similarity(query_vec, self.en_tfidf_matrix)[0]
            docs = self.en_docs

        elif language == "bn" and self.bn_tfidf_matrix is not None:
            query_vec = self.tfidf_bn.transform([query])
            sims = cosine_similarity(query_vec, self.bn_tfidf_matrix)[0]
            docs = self.bn_docs

        else:
            return []

        ranked = sorted(
            zip(docs, sims),
            key=lambda x: x[1],
            reverse=True
        )[:top_k]

        return [
            {
                "title": doc.get("title", ""),
                "url": doc.get("url", ""),
                "score": round(float(score), 4)
            }
            for doc, score in ranked
        ]
