# data/crawlers/models.py

from dataclasses import dataclass
from datetime import datetime

@dataclass
class Article:
    title: str
    content: str
    url: str
    date: str
    language: str  # "en" or "bn"

    def to_dict(self):
        return {
            "title": self.title,
            "content": self.content,
            "url": self.url,
            "date": self.date,
            "language": self.language
        }
