import pandas as pd
from query_processing.pipeline import process_query
from evaluation.evaluator import Evaluator
from retrieval.lexical_bm25 import LexicalRetriever
from retrieval.semantic_embedding import SemanticRetriever
from evaluation.ranking import Ranker


def evaluate_model(model_type="hybrid", queries=None):
    evaluator = Evaluator("evaluation/labels.csv")

    results_all = []

    if model_type == "bm25":
        print("\n🔎 Evaluating BM25...")
        lexical = LexicalRetriever()

    elif model_type == "embedding":
        print("\n🔎 Evaluating Embedding...")
        semantic = SemanticRetriever()

    elif model_type == "hybrid":
        print("\n🔎 Evaluating Hybrid...")
        hybrid = Ranker()

    else:
        raise ValueError("Choose: bm25 | embedding | hybrid")

    for query in queries:
        processed = process_query(query)
        language = processed["language"]

        # -------------------------
        # MODEL SELECTION
        # -------------------------
        if model_type == "bm25":
            results = lexical.search_bm25(
                processed["original"], language, top_k=10
            )
            time_ms = 0

        elif model_type == "embedding":
            results = semantic.search(
                processed["original"], language, top_k=10
            )
            time_ms = 0

        elif model_type == "hybrid":
            results, time_ms = hybrid.search(
                processed["original"], language, top_k=10
            )

        # -------------------------
        # EVALUATION
        # -------------------------
        retrieved_urls = [r["url"] for r in results]

        metrics = evaluator.evaluate_query(query, retrieved_urls)
        metrics["retrieval_time_ms"] = time_ms
        metrics["query"] = query

        results_all.append(metrics)

    df = pd.DataFrame(results_all)
    return df


def compare_models(queries):
    bm25_df = evaluate_model("bm25", queries)
    embed_df = evaluate_model("embedding", queries)
    hybrid_df = evaluate_model("hybrid", queries)

    comparison = pd.DataFrame({
        "Model": ["BM25", "Embedding", "Hybrid"],
        "Precision@10": [
            bm25_df["Precision@10"].mean(),
            embed_df["Precision@10"].mean(),
            hybrid_df["Precision@10"].mean()
        ],
        "Recall@50": [
            bm25_df["Recall@50"].mean(),
            embed_df["Recall@50"].mean(),
            hybrid_df["Recall@50"].mean()
        ],
        "MRR": [
            bm25_df["MRR"].mean(),
            embed_df["MRR"].mean(),
            hybrid_df["MRR"].mean()
        ],
        "nDCG@10": [
            bm25_df["nDCG@10"].mean(),
            embed_df["nDCG@10"].mean(),
            hybrid_df["nDCG@10"].mean()
        ],
        "Avg Retrieval Time (ms)": [
            bm25_df["retrieval_time_ms"].mean(),
            embed_df["retrieval_time_ms"].mean(),
            hybrid_df["retrieval_time_ms"].mean()
        ]
    })

    print("\n📊 MODEL COMPARISON TABLE")
    print(comparison)

    comparison.to_csv("evaluation/model_comparison_results.csv", index=False)
    print("\n✅ Saved to evaluation/model_comparison_results.csv")

    return comparison


if __name__ == "__main__":
    labels = pd.read_csv("evaluation/labels.csv")
    queries = labels["query"].unique().tolist()

    compare_models(queries)
