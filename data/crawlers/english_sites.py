import requests
from bs4 import BeautifulSoup
from .base import BaseCrawler, Article


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


# ======================================================
# 1️⃣ DAILY STAR
# ======================================================
class DailyStarCrawler(BaseCrawler):

    def get_language(self):
        return "en"

    def crawl(self):
        articles = []
        visited_urls = set()

        categories = [
            "news",
            "business",
            "sports",
            "opinion",
            "world"
        ]

        max_pages = 200  # Increase if needed

        for category in categories:
            print(f"   🔎 Category: {category}")

            for page in range(1, max_pages + 1):

                url = f"https://www.thedailystar.net/{category}?page={page}"
                html = self.fetch(url)
                if not html:
                    continue

                soup = BeautifulSoup(html, "html.parser")
                links = soup.select("h3 a")

                if not links:
                    break  # stop if no more pages

                for link in links:
                    href = link.get("href")
                    if not href:
                        continue

                    full_url = "https://www.thedailystar.net" + href

                    if full_url in visited_urls:
                        continue

                    visited_urls.add(full_url)

                    article = self.parse_article(full_url)
                    if article:
                        articles.append(article)

        return articles

# ======================================================
# 2️⃣ DHAKA TRIBUNE
# ======================================================
class DhakaTribuneCrawler(BaseCrawler):

    def get_language(self):
        return "en"

    def crawl(self):
        articles = []
        visited_urls = set()

        categories = [
            "news",
            "business",
            "sports",
            "opinion",
            "world"
        ]

        max_pages = 200  # Increase if needed

        for category in categories:
            print(f"   🔎 Category: {category}")

            for page in range(1, max_pages + 1):

                url = f"https://www.dhakatribune.com/{category}?page={page}"
                html = self.fetch(url)
                if not html:
                    continue

                soup = BeautifulSoup(html, "html.parser")
                links = soup.select("h3 a")

                if not links:
                    break  # stop if no more pages

                for link in links:
                    href = link.get("href")
                    if not href:
                        continue

                    full_url = "https://www.dhakatribune.com" + href

                    if full_url in visited_urls:
                        continue

                    visited_urls.add(full_url)

                    article = self.parse_article(full_url)
                    if article:
                        articles.append(article)

        return articles


# ======================================================
# 3️⃣ NEW AGE
# ======================================================
class NewAgeCrawler(BaseCrawler):

    def get_language(self):
        return "en"

    def crawl(self):
        articles = []
        visited_urls = set()

        categories = [
            "news",
            "business",
            "sports",
            "opinion",
            "world"
        ]

        max_pages = 200  # Increase if needed

        for category in categories:
            print(f"   🔎 Category: {category}")

            for page in range(1, max_pages + 1):

                url = f"https://www.newagebd.net/{category}?page={page}"
                html = self.fetch(url)
                if not html:
                    continue

                soup = BeautifulSoup(html, "html.parser")
                links = soup.select("h3 a")

                if not links:
                    break  # stop if no more pages

                for link in links:
                    href = link.get("href")
                    if not href:
                        continue

                    full_url = "https://www.newagebd.net" + href

                    if full_url in visited_urls:
                        continue

                    visited_urls.add(full_url)

                    article = self.parse_article(full_url)
                    if article:
                        articles.append(article)

        return articles
# ======================================================
# 4️⃣ DAILY SUN
# ======================================================
class DailySunCrawler(BaseCrawler):

    def get_language(self):
        return "en"

    def crawl(self):
        articles = []
        visited_urls = set()

        categories = [
            "news",
            "business",
            "sports",
            "opinion",
            "world"
        ]

        max_pages = 200  # Increase if needed

        for category in categories:
            print(f"   🔎 Category: {category}")

            for page in range(1, max_pages + 1):

                url = f"https://www.daily-sun.com/{category}?page={page}"
                html = self.fetch(url)
                if not html:
                    continue

                soup = BeautifulSoup(html, "html.parser")
                links = soup.select("h3 a")

                if not links:
                    break  # stop if no more pages

                for link in links:
                    href = link.get("href")
                    if not href:
                        continue

                    full_url = "https://www.daily-sun.com" + href

                    if full_url in visited_urls:
                        continue

                    visited_urls.add(full_url)

                    article = self.parse_article(full_url)
                    if article:
                        articles.append(article)

        return articles
# ======================================================
# 5️⃣ THE NEW NATION
# ======================================================
class NewNationCrawler(BaseCrawler):

    def get_language(self):
        return "en"

    def crawl(self):
        articles = []
        visited_urls = set()

        categories = [
            "news",
            "business",
            "sports",
            "opinion",
            "world"
        ]

        max_pages = 200  # Increase if needed

        for category in categories:
            print(f"   🔎 Category: {category}")

            for page in range(1, max_pages + 1):

                url = f"https://thedailynewnation.com/{category}?page={page}"
                html = self.fetch(url)
                if not html:
                    continue

                soup = BeautifulSoup(html, "html.parser")
                links = soup.select("h3 a")

                if not links:
                    break  # stop if no more pages

                for link in links:
                    href = link.get("href")
                    if not href:
                        continue

                    full_url = "https://thedailynewnation.com" + href

                    if full_url in visited_urls:
                        continue

                    visited_urls.add(full_url)

                    article = self.parse_article(full_url)
                    if article:
                        articles.append(article)

        return articles