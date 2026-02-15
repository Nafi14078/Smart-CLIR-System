import csv
from evaluation.metrics import *


class Evaluator:

    def __init__(self, label_file):
        self.label_file = label_file
        self.labels = self.load_labels()

    def load_labels(self):
        labels = {}
        with open(self.label_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                query = row["query"]
                url = row["doc_url"]
                relevant = row["relevant"].lower() == "yes"

                if query not in labels:
                    labels[query] = {"relevant": set()}

                if relevant:
                    labels[query]["relevant"].add(url)

        return labels

    def evaluate_query(self, query, retrieved_urls):

        if query not in self.labels:
            print("⚠ No labels found for this query.")
            return None

        relevant = self.labels[query]["relevant"]

        p10 = precision_at_k(retrieved_urls, relevant, 10)
        r50 = recall_at_k(retrieved_urls, relevant, 50)
        mrr_score = mrr(retrieved_urls, relevant)
        ndcg = ndcg_at_k(retrieved_urls, relevant, 10)

        return {
            "Precision@10": round(p10, 3),
            "Recall@50": round(r50, 3),
            "MRR": round(mrr_score, 3),
            "nDCG@10": round(ndcg, 3)
        }
