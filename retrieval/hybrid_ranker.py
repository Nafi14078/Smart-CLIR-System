import numpy as np


class HybridRanker:

    def __init__(self, bm25_scores, semantic_scores, fuzzy_scores):
        self.bm25_scores = bm25_scores
        self.semantic_scores = semantic_scores
        self.fuzzy_scores = fuzzy_scores

    def normalize(self, scores):
        scores = np.array(scores)
        return (scores - scores.min()) / (scores.max() - scores.min() + 1e-9)

    def rank(self, top_k=5):
        bm25 = self.normalize(self.bm25_scores)
        semantic = self.normalize(self.semantic_scores)
        fuzzy = self.normalize(self.fuzzy_scores)

        final = 0.3 * bm25 + 0.5 * semantic + 0.2 * fuzzy

        top_indices = np.argsort(final)[::-1][:top_k]
        return top_indices, final[top_indices]
