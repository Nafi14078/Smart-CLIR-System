"""
Main Crawler Runner
Run from project root using:

    python -m data.crawlers.main_crawler
"""

import json
from pathlib import Path

# ✅ Relative imports (IMPORTANT)
from .english_sites import (
    DailyStarCrawler,
    DhakaTribuneCrawler,
    NewAgeCrawler,
    DailySunCrawler,
    NewNationCrawler
)

from .bangla_sites import (
    ProthomAloCrawler,
    BanglaTribuneCrawler,
    KalerKanthoCrawler
)


# ======================================================
# CONFIG
# ======================================================

SAVE_DIR = Path("data/processed")
SAVE_DIR.mkdir(parents=True, exist_ok=True)

EN_FILE = SAVE_DIR / "english_docs.json"
BN_FILE = SAVE_DIR / "bangla_docs.json"


# ======================================================
# UTILS
# ======================================================

def load_json(path):
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# 🔥 Convert Article object → dictionary
def article_to_dict(article):
    return {
        "title": getattr(article, "title", ""),
        "body": getattr(article, "content", ""),
        "url": getattr(article, "url", ""),
        "date": getattr(article, "date", ""),
        "language": getattr(article, "language", "")
    }


def deduplicate(existing_docs, new_articles):
    existing_urls = set(doc["url"] for doc in existing_docs)
    added = 0

    for article in new_articles:
        doc = article_to_dict(article)

        if doc["url"] and doc["url"] not in existing_urls:
            existing_docs.append(doc)
            existing_urls.add(doc["url"])
            added += 1

    return existing_docs, added


# ======================================================
# MAIN PIPELINE
# ======================================================

def main():

    print("\n📥 Loading existing data...")
    english_docs = load_json(EN_FILE)
    bangla_docs = load_json(BN_FILE)

    print("\n🚀 Starting Crawlers...\n")

    # ==================================================
    # ENGLISH CRAWLERS
    # ==================================================
    english_crawlers = [
        DailyStarCrawler(),
        DhakaTribuneCrawler(),
        NewAgeCrawler(),
        DailySunCrawler(),
        NewNationCrawler(),
    ]

    for crawler in english_crawlers:
        print(f"\n📰 Running {crawler.__class__.__name__}")
        try:
            docs = crawler.crawl()
            english_docs, added = deduplicate(english_docs, docs)
            print(f"   ➕ Added {added} new English articles")
        except Exception as e:
            print(f"   ❌ Error in {crawler.__class__.__name__}: {e}")

    # ==================================================
    # BANGLA CRAWLERS
    # ==================================================
    bangla_crawlers = [
        ProthomAloCrawler(),
        BanglaTribuneCrawler(),
        KalerKanthoCrawler(),
    ]

    for crawler in bangla_crawlers:
        print(f"\n📰 Running {crawler.__class__.__name__}")
        try:
            docs = crawler.crawl()
            bangla_docs, added = deduplicate(bangla_docs, docs)
            print(f"   ➕ Added {added} new Bangla articles")
        except Exception as e:
            print(f"   ❌ Error in {crawler.__class__.__name__}: {e}")

    # ==================================================
    # SAVE DATA
    # ==================================================
    save_json(EN_FILE, english_docs)
    save_json(BN_FILE, bangla_docs)

    print("\n====================================")
    print("✅ FINAL COUNTS")
    print("====================================")
    print(f"English articles: {len(english_docs)}")
    print(f"Bangla articles : {len(bangla_docs)}")
    print(f"Total           : {len(english_docs) + len(bangla_docs)}")
    print("====================================\n")
    print("🎯 Crawling completed successfully!\n")


# ======================================================

if __name__ == "__main__":
    main()
