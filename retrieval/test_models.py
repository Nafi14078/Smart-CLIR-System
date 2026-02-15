from retrieval.lexical_bm25 import LexicalRetriever
from retrieval.semantic_embedding import SemanticRetriever
from retrieval.fuzzy_match import FuzzyMatcher
from query_processing.pipeline import process_query
import json
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")

EN_PATH = os.path.join(DATA_DIR, "english_docs.json")
BN_PATH = os.path.join(DATA_DIR, "bangla_docs.json")


def load_docs(language="en"):
    path = EN_PATH if language == "en" else BN_PATH
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def test_query(query):

    print("="*60)
    print("🔎 Query:", query)

    processed = process_query(query)
    language = processed["language"]

    lexical = LexicalRetriever()
    semantic = SemanticRetriever()

    print("\n📘 BM25 Results:")
    print(lexical.search_bm25(processed["original"], language))

    print("\n📗 TF-IDF Results:")
    print(lexical.search_tfidf(processed["original"], language))

    print("\n📙 Semantic Results:")
    print(semantic.search(processed["original"], language))

    docs = load_docs(language)
    fuzzy = FuzzyMatcher(docs)

    print("\n📕 Fuzzy Results:")
    print(fuzzy.search(processed["original"]))


if __name__ == "__main__":
    test_query("Bangladesh economy growth")
