from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class ArticleSource:
    """
    article source, such as API or website
    """
    id: str
    name: str


@dataclass
class Article:
    """
    an article
    """
    id: str
    source: str
    header: str
    body: str


@dataclass
class NewsParser:
    provider: NotImplementedError
    header_list: [Dict]

    def fetch_news(self):
        raise NotImplementedError

    def fetch_headers(self):
        raise NotImplementedError

    def build_header_list(self):
        raise NotImplementedError

    def get_news_by_header(self):
        raise NotImplementedError
