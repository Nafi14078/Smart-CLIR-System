import os
import pandas as pd
import matplotlib.pyplot as plt

PLOTS_DIR = "evaluation/plots"
os.makedirs(PLOTS_DIR, exist_ok=True)


def generate_model_comparison_plots(comparison_csv_path):
    """
    Generate and save comparison charts from model_comparison output CSV
    """

    df = pd.read_csv(comparison_csv_path)

    print("📊 Generating plots...")

    # -----------------------------
    # 1️⃣ Precision, Recall, nDCG, MRR Comparison
    # -----------------------------
    metrics = ["Precision@10", "Recall@50", "MRR", "nDCG@10"]

    for metric in metrics:
        plt.figure(figsize=(8, 5))
        plt.bar(df["Model"], df[metric])
        plt.title(f"{metric} Comparison")
        plt.ylabel(metric)
        plt.ylim(0, 1)
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        save_path = os.path.join(PLOTS_DIR, f"{metric}_comparison.png")
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()

        print(f"✅ Saved {save_path}")

    # -----------------------------
    # 2️⃣ All Metrics Combined Chart
    # -----------------------------
    plt.figure(figsize=(10, 6))

    x = range(len(df["Model"]))

    plt.plot(x, df["Precision@10"], marker="o", label="Precision@10")
    plt.plot(x, df["Recall@50"], marker="o", label="Recall@50")
    plt.plot(x, df["MRR"], marker="o", label="MRR")
    plt.plot(x, df["nDCG@10"], marker="o", label="nDCG@10")

    plt.xticks(x, df["Model"])
    plt.ylim(0, 1)
    plt.title("Overall Model Comparison")
    plt.legend()
    plt.grid(True)

    save_path = os.path.join(PLOTS_DIR, "overall_model_comparison.png")
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()

    print(f"✅ Saved {save_path}")

    # -----------------------------
    # 3️⃣ Retrieval Time Comparison
    # -----------------------------
    if "Avg Retrieval Time (ms)" in df.columns:
        plt.figure(figsize=(8, 5))
        plt.bar(df["Model"], df["Avg Retrieval Time (ms)"])
        plt.title("Average Retrieval Time Comparison")
        plt.ylabel("Time (ms)")
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        save_path = os.path.join(PLOTS_DIR, "retrieval_time_comparison.png")
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()

        print(f"✅ Saved {save_path}")

    print("\n🎉 All plots generated successfully!")


if __name__ == "__main__":
    # Update this if your file name is different
    generate_model_comparison_plots("evaluation/model_comparison_results.csv")
