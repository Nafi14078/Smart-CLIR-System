import jellyfish
import numpy as np


class FuzzyMatcher:

    def __init__(self, documents):
        self.documents = documents

    def jaccard_similarity(self, a, b):
        set_a = set(a.split())
        set_b = set(b.split())
        return len(set_a & set_b) / len(set_a | set_b)

    def levenshtein_score(self, a, b):
        dist = jellyfish.levenshtein_distance(a, b)
        return 1 / (1 + dist)

    def search(self, query, top_k=5):
        scores = []

        for doc in self.documents:
            title = doc["title"]
            jaccard = self.jaccard_similarity(query, title)
            levenshtein = self.levenshtein_score(query, title)

            score = 0.5 * jaccard + 0.5 * levenshtein
            scores.append(score)

        top_indices = np.argsort(scores)[::-1][:top_k]
        return [(self.documents[i]["title"], scores[i]) for i in top_indices]
