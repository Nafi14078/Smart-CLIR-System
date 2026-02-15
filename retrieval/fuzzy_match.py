import json
import os
from rapidfuzz import fuzz

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EN_PATH = os.path.join(BASE_DIR, "data", "processed", "english_docs.json")
BN_PATH = os.path.join(BASE_DIR, "data", "processed", "bangla_docs.json")


class FuzzyMatcher:
    def __init__(self):
        self.en_docs = self.load_json(EN_PATH)
        self.bn_docs = self.load_json(BN_PATH)

        print(f"EN docs: {len(self.en_docs)}")
        print(f"BN docs: {len(self.bn_docs)}")

    def load_json(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_text(self, doc):
        """
        Robust content extractor.
        Handles different key names safely.
        """
        return (
            doc.get("content")
            or doc.get("text")
            or doc.get("body")
            or ""
        )

    def search(self, query, language="en", top_k=5):
        docs = self.en_docs if language == "en" else self.bn_docs

        results = []

        for doc in docs:
            text = self.get_text(doc)

            if not text:
                continue

            score = fuzz.partial_ratio(
                query.lower(),
                text.lower()
            ) / 100.0

            results.append({
                "title": doc.get("title", ""),
                "url": doc.get("url", ""),
                "score": round(score, 4)
            })

        results = sorted(results, key=lambda x: x["score"], reverse=True)

        return results[:top_k]
