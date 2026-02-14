import requests
from bs4 import BeautifulSoup
from .base import BaseCrawler, Article


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


# ======================================================
# 1️⃣ PROTHOM ALO
# ======================================================
class ProthomAloCrawler(BaseCrawler):

    def get_language(self):
        return "bn"

    def crawl(self):
        articles = []
        visited_urls = set()

        categories = [
            "politics",
            "economy",
            "sports",
            "world",
            "bangladesh"
        ]

        max_pages = 200

        for category in categories:
            print(f"   🔎 Category: {category}")

            for page in range(1, max_pages + 1):

                url = f"https://www.prothomalo.com/{category}?page={page}"
                html = self.fetch(url)
                if not html:
                    continue

                soup = BeautifulSoup(html, "html.parser")
                links = soup.select('a[data-testid="link"]')

                if not links:
                    break

                for link in links:
                    href = link.get("href")
                    if not href or not href.startswith("/"):
                        continue

                    full_url = "https://www.prothomalo.com" + href

                    if full_url in visited_urls:
                        continue

                    visited_urls.add(full_url)

                    article = self.parse_article(full_url)
                    if article:
                        articles.append(article)

        return articles

# ======================================================
# 2️⃣ BANGLA TRIBUNE
# ======================================================
class BanglaTribuneCrawler(BaseCrawler):

    def get_language(self):
        return "bn"

    def crawl(self):
        articles = []
        visited_urls = set()

        categories = [
            "politics",
            "economy",
            "sports",
            "world",
            "bangladesh"
        ]

        max_pages = 200

        for category in categories:
            print(f"   🔎 Category: {category}")

            for page in range(1, max_pages + 1):

                url = f"https://www.banglatribune.com/{category}?page={page}"
                html = self.fetch(url)
                if not html:
                    continue

                soup = BeautifulSoup(html, "html.parser")
                links = soup.select('a[data-testid="link"]')

                if not links:
                    break

                for link in links:
                    href = link.get("href")
                    if not href or not href.startswith("/"):
                        continue

                    full_url = "https://www.banglatribune.com" + href

                    if full_url in visited_urls:
                        continue

                    visited_urls.add(full_url)

                    article = self.parse_article(full_url)
                    if article:
                        articles.append(article)

        return articles

# ======================================================
# 3️⃣ KALER KANTHO
# ======================================================
class KalerKanthoCrawler(BaseCrawler):

    def get_language(self):
        return "bn"

    def crawl(self):
        articles = []
        visited_urls = set()

        categories = [
            "politics",
            "economy",
            "sports",
            "world",
            "bangladesh"
        ]

        max_pages = 200

        for category in categories:
            print(f"   🔎 Category: {category}")

            for page in range(1, max_pages + 1):

                url = f"https://www.kalerkantho.com/{category}?page={page}"
                html = self.fetch(url)
                if not html:
                    continue

                soup = BeautifulSoup(html, "html.parser")
                links = soup.select('a[data-testid="link"]')

                if not links:
                    break

                for link in links:
                    href = link.get("href")
                    if not href or not href.startswith("/"):
                        continue

                    full_url = "https://www.kalerkantho.com" + href

                    if full_url in visited_urls:
                        continue

                    visited_urls.add(full_url)

                    article = self.parse_article(full_url)
                    if article:
                        articles.append(article)

        return articles