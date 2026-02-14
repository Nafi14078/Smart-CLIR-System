# data/crawlers/storage.py

import json
import os

def save_articles(articles, filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            existing = json.load(f)
    else:
        existing = []

    existing_urls = {article["url"] for article in existing}

    new_articles = [
        article.to_dict()
        for article in articles
        if article.url not in existing_urls
    ]

    all_articles = existing + new_articles

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved {len(new_articles)} new articles to {filename}")
    print(f"📊 Total now: {len(all_articles)}")
