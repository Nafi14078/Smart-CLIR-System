import numpy as np
from retrieval.lexical_bm25 import LexicalRetriever
from retrieval.semantic_embedding import SemanticRetriever
from retrieval.fuzzy_match import FuzzyMatcher


class HybridRanker:
    def __init__(self, w_bm25=0.4, w_semantic=0.5, w_fuzzy=0.1):
        print("🔄 Initializing Hybrid Ranker...")
        self.lexical = LexicalRetriever()
        self.semantic = SemanticRetriever()
        self.fuzzy = FuzzyMatcher()

        self.w_bm25 = w_bm25
        self.w_semantic = w_semantic
        self.w_fuzzy = w_fuzzy

    def normalize_scores(self, results):
        scores = np.array([r["score"] for r in results])
        if len(scores) == 0:
            return results

        min_s = scores.min()
        max_s = scores.max()

        if max_s - min_s == 0:
            return results

        for r in results:
            r["score"] = (r["score"] - min_s) / (max_s - min_s)

        return results

    def search(self, query, language="en", top_k=5):
        bm25_results = self.lexical.search_bm25(query, language, top_k=20)
        semantic_results = self.semantic.search(query, language, top_k=20)
        fuzzy_results = self.fuzzy.search(query, language, top_k=20)

        bm25_results = self.normalize_scores(bm25_results)
        semantic_results = self.normalize_scores(semantic_results)
        fuzzy_results = self.normalize_scores(fuzzy_results)

        combined = {}

        def add_results(results, weight):
            for r in results:
                key = r["url"]
                if key not in combined:
                    combined[key] = {
                        "title": r["title"],
                        "url": r["url"],
                        "score": 0
                    }
                combined[key]["score"] += weight * r["score"]

        add_results(bm25_results, self.w_bm25)
        add_results(semantic_results, self.w_semantic)
        add_results(fuzzy_results, self.w_fuzzy)

        ranked = sorted(combined.values(), key=lambda x: x["score"], reverse=True)

        return ranked[:top_k]
