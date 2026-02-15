import time
import numpy as np
from retrieval.hybrid_ranker import HybridRanker


class Ranker:
    def __init__(self, threshold=0.20):
        print("🔄 Initializing Ranking System...")
        self.hybrid = HybridRanker()
        self.threshold = threshold

    def normalize_scores(self, results):
        if not results:
            return results

        scores = np.array([r["score"] for r in results])
        min_s = scores.min()
        max_s = scores.max()

        if max_s - min_s == 0:
            for r in results:
                r["score"] = 1.0
            return results

        for r in results:
            r["score"] = (r["score"] - min_s) / (max_s - min_s)

        return results

    def search(self, query, language, top_k=10):
        start = time.time()

        results = self.hybrid.search(query, language, top_k=top_k)
        results = self.normalize_scores(results)

        end = time.time()
        total_time = (end - start) * 1000  # ms

        print(f"\n⏱ Retrieval Time: {round(total_time,2)} ms")

        if results and results[0]["score"] < self.threshold:
            print(f"\n⚠ Warning: Retrieved results may not be relevant.")
            print(f"Matching confidence is low (score: {round(results[0]['score'],3)})")
            print("Consider rephrasing your query or checking translation quality.")

        return results, total_time
