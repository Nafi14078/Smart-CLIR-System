from query_processing.pipeline import process_query
from evaluation.ranking import Ranker

# Your evaluation queries
queries = [
    "Bangladesh economy growth",
    "বাংলাদেশ অর্থনীতি প্রবৃদ্ধি",
    "Dhaka education policy",
    "ঢাকা শিক্ষা নীতি",
    "flood disaster Bangladesh",
    "Bangladesh নির্বাচন crisis",
    "Climate change impact Bangladesh",
    "Renewable energy Bangladesh",
    "Bangladesh export to US",
    "COVID-19 vaccination Bangladesh",
    "Digital Bangladesh progress",
    "Bangladesh inflation rate",
    "Bangladesh foreign investment",
    "Dhaka traffic problem",
    "বাংলাদেশ কৃষি উন্নয়ন",
    "Bangladesh stock market crash",
    "Bangladesh poverty reduction",
    "Bangladesh election violence",
    "Bangladesh banking sector reform",
    "Bangladesh garment industry"
]

ranker = Ranker(threshold=0.20)

for query in queries:
    print("\n" + "=" * 80)
    print("QUERY:", query)

    processed = process_query(query)

    results, _ = ranker.search(
        processed["original"],
        processed["language"],
        top_k=10
    )

    for i, r in enumerate(results, start=1):
        print(f"{i}. {r['url']}  |  Score: {round(r['score'], 4)}")
