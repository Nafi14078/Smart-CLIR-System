from query_processing.pipeline import process_query
from evaluation.ranking import Ranker
from evaluation.evaluator import Evaluator
import pandas as pd
import time

# Load labels
labels_file = "evaluation/labels.csv"
labels = pd.read_csv(labels_file)

# Initialize Ranker
ranker = Ranker(threshold=0.20)

# Unique queries
queries = labels["query"].unique()

# Store metrics
all_metrics = []

for q in queries:
    processed = process_query(q)
    start = time.time()
    results, _ = ranker.search(
        processed["original"],
        processed["language"],
        top_k=10
    )
    elapsed_ms = (time.time() - start) * 1000
    retrieved_urls = [r["url"] for r in results]

    evaluator = Evaluator(labels_file)
    metrics = evaluator.evaluate_query(q, retrieved_urls)
    metrics["query"] = q
    metrics["retrieval_time_ms"] = elapsed_ms
    all_metrics.append(metrics)

# Create DataFrame
df_metrics = pd.DataFrame(all_metrics)

# Average metrics
avg_metrics = df_metrics.mean(numeric_only=True)
print("\n📊 Multi-query Evaluation Metrics (per query):")
print(df_metrics)
print("\n📊 Average Metrics Across 20 Queries:")
print(avg_metrics)
