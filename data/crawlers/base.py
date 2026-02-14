# data/crawlers/base.py
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass


# ======================================================
# ARTICLE DATA STRUCTURE
# ======================================================

@dataclass
class Article:
    title: str
    content: str
    url: str
    date: str = ""
    language: str = ""


# ======================================================
# BASE CRAWLER
# ======================================================

class BaseCrawler:

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    def fetch(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            return response.text
        except Exception:
            return None

    def parse_article(self, url):
        html = self.fetch(url)
        if not html:
            return None

        soup = BeautifulSoup(html, "html.parser")

        # Generic title extraction
        title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else ""

        # Generic content extraction
        paragraphs = soup.find_all("p")
        content = " ".join(p.get_text(strip=True) for p in paragraphs)

        if len(content) < 300:
            return None  # filter very small articles

        return Article(
            title=title,
            content=content,
            url=url,
            language=self.get_language()
        )

    # Each crawler overrides this
    def get_language(self):
        return ""
