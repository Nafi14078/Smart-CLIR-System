import requests
import feedparser
import json
import time
import hashlib
from pathlib import Path
from bs4 import BeautifulSoup
from langdetect import detect
from tqdm import tqdm

# ======================================================
# CONFIG
# ======================================================
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

SAVE_DIR = Path("data/processed")
SAVE_DIR.mkdir(parents=True, exist_ok=True)

EN_FILE = SAVE_DIR / "english_docs.json"
BN_FILE = SAVE_DIR / "bangla_docs.json"

# ---------- RSS (LIMITED BUT CLEAN) ----------
ENGLISH_FEEDS = [
    "https://www.thedailystar.net/frontpage/rss.xml",
    "https://www.thedailystar.net/business/rss.xml",
    "https://www.thedailystar.net/sports/rss.xml"
]

BANGLA_FEEDS = [
    "https://www.prothomalo.com/feed"
]

# ---------- PAGINATION LIMITS ----------
DHAKA_TRIBUNE_PAGES = 500        # ~2000+ English
PROTHOM_ALO_PAGES = 500          # ~3000–4000 Bangla
BANGLA_TRIBUNE_PAGES = 500      # ~2000 Bangla

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

def gen_id(url):
    return hashlib.md5(url.encode()).hexdigest()

def fetch_article_text(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        text = " ".join(p.get_text(strip=True) for p in soup.find_all("p"))
        return text.strip()
    except Exception:
        return ""

def is_valid(text):
    return text and len(text) > 300

# ======================================================
# RSS CRAWLER
# ======================================================
def crawl_rss(feeds, lang_code):
    articles = []
    print("\n📡 RSS crawling...")

    for feed_url in feeds:
        print(f"   → {feed_url}")
        feed = feedparser.parse(feed_url)

        for entry in tqdm(feed.entries):
            url = entry.get("link", "")
            if not url:
                continue

            text = fetch_article_text(url)
            if not is_valid(text):
                continue

            try:
                if detect(text) != lang_code:
                    continue
            except:
                continue

            articles.append({
                "id": gen_id(url),
                "title": entry.get("title", ""),
                "body": text,
                "url": url,
                "date": entry.get("published", ""),
                "language": lang_code,
                "tokens": len(text.split())
            })

            time.sleep(0.3)

    return articles

# ======================================================
# PAGINATION CRAWLERS (FIXED SELECTORS)
# ======================================================
def crawl_dhaka_tribune(pages):
    articles = []
    print("\n📰 Crawling Dhaka Tribune (English)...")

    for page in tqdm(range(1, pages + 1)):
        url = f"https://www.dhakatribune.com/latest?page={page}"
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        links = soup.select("h3 a")
        for link in links:
            href = link.get("href", "")
            if not href.startswith("/"):
                continue

            article_url = "https://www.dhakatribune.com" + href
            text = fetch_article_text(article_url)
            if not is_valid(text):
                continue

            articles.append({
                "id": gen_id(article_url),
                "title": link.get_text(strip=True),
                "body": text,
                "url": article_url,
                "language": "en",
                "tokens": len(text.split())
            })

        time.sleep(0.3)

    return articles

def crawl_prothom_alo(pages):
    articles = []
    print("\n📰 Crawling Prothom Alo (Bangla)...")

    for page in tqdm(range(1, pages + 1)):
        url = f"https://www.prothomalo.com/latest?page={page}"
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        links = soup.select('a[data-testid="link"]')
        for link in links:
            href = link.get("href", "")
            if not href.startswith("/"):
                continue

            article_url = "https://www.prothomalo.com" + href
            text = fetch_article_text(article_url)
            if not is_valid(text):
                continue

            articles.append({
                "id": gen_id(article_url),
                "title": link.get_text(strip=True),
                "body": text,
                "url": article_url,
                "language": "bn",
                "tokens": len(text.split())
            })

        time.sleep(0.3)

    return articles

def crawl_bangla_tribune(pages):
    articles = []
    print("\n📰 Crawling Bangla Tribune (Bangla)...")

    for page in tqdm(range(1, pages + 1)):
        url = f"https://www.banglatribune.com/latest?page={page}"
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        links = soup.select("h2 a")
        for link in links:
            href = link.get("href", "")
            if not href.startswith("/"):
                continue

            article_url = "https://www.banglatribune.com" + href
            text = fetch_article_text(article_url)
            if not is_valid(text):
                continue

            articles.append({
                "id": gen_id(article_url),
                "title": link.get_text(strip=True),
                "body": text,
                "url": article_url,
                "language": "bn",
                "tokens": len(text.split())
            })

        time.sleep(0.3)

    return articles

# ======================================================
# MAIN PIPELINE
# ======================================================
def main():
    print("\n📥 Loading existing data...")
    en_existing = load_json(EN_FILE)
    bn_existing = load_json(BN_FILE)

    en_urls = set(d["url"] for d in en_existing)
    bn_urls = set(d["url"] for d in bn_existing)

    # ---------- RSS ----------
    en_rss = crawl_rss(ENGLISH_FEEDS, "en")
    bn_rss = crawl_rss(BANGLA_FEEDS, "bn")

    # ---------- PAGINATION ----------
    en_pag = crawl_dhaka_tribune(DHAKA_TRIBUNE_PAGES)
    bn_pag1 = crawl_prothom_alo(PROTHOM_ALO_PAGES)
    bn_pag2 = crawl_bangla_tribune(BANGLA_TRIBUNE_PAGES)

    # ---------- MERGE + DEDUPE ----------
    for d in en_rss + en_pag:
        if d["url"] not in en_urls:
            en_existing.append(d)
            en_urls.add(d["url"])

    for d in bn_rss + bn_pag1 + bn_pag2:
        if d["url"] not in bn_urls:
            bn_existing.append(d)
            bn_urls.add(d["url"])

    save_json(EN_FILE, en_existing)
    save_json(BN_FILE, bn_existing)

    print("\n✅ FINAL COUNTS")
    print(f"English articles: {len(en_existing)}")
    print(f"Bangla articles:  {len(bn_existing)}")
    print(f"Total: {len(en_existing) + len(bn_existing)}")

if __name__ == "__main__":
    main()
