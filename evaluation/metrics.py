import math


def precision_at_k(retrieved, relevant, k=10):
    retrieved_k = retrieved[:k]
    relevant_count = sum([1 for doc in retrieved_k if doc in relevant])
    return relevant_count / k


def recall_at_k(retrieved, relevant, k=50):
    retrieved_k = retrieved[:k]
    relevant_count = sum([1 for doc in retrieved_k if doc in relevant])
    if len(relevant) == 0:
        return 0
    return relevant_count / len(relevant)


def mrr(retrieved, relevant):
    for idx, doc in enumerate(retrieved):
        if doc in relevant:
            return 1 / (idx + 1)
    return 0


def ndcg_at_k(retrieved, relevant, k=10):
    dcg = 0
    for i, doc in enumerate(retrieved[:k]):
        if doc in relevant:
            dcg += 1 / math.log2(i + 2)

    ideal_dcg = sum([1 / math.log2(i + 2) for i in range(min(len(relevant), k))])

    if ideal_dcg == 0:
        return 0

    return dcg / ideal_dcg
