import json
import time
import uuid
from typing import List
import requests
from dataclasses import dataclass
from session_base import SessionBase



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
class NewsFeed(SessionBase):
    """
    https://newsapi.ai/

    sergey@omg.one:cUQ4KwvYnrUsFb@

    https://newsapi.ai/documentation?tab=searchArticles
    https://platform.openai.com/docs/guides/gpt/function-calling
    """
    key = "8af34ff7-fb88-45c4-aff0-7c6e9776082b"
    uri = "http://eventregistry.org/api/v1/article/getArticles"

    final = list()
    event_list = list()

    def fetch_news(self):

        for i in range(1, 4, 1):
            _json = {
                "action": "getArticles",
                "keyword": ["AI"],
                "articlesPage": i,
                "articlesCount": 200,
                "articlesSortBy": "date",
                "articlesSortByAsc": False,
                "articlesArticleBodyLen": -1,
                "resultType": "articles",
                "lang": "eng",
                "dataType": [
                    "news",
                    "pr",
                    "blog"
                ],
                "apiKey": self.key,
                "forceMaxDataTimeWindow": 31
            }

            res = requests.get(
                self.uri,
                params=_json
            ).json()

            res = res["articles"]["results"]

            if not res:
                break

            # print(f"Page {i}:", len(res), "\n")

            self.final.extend(res)

        _final = list()
        titles = list()
        _id = 1
        for item in self.final:

            if item["title"] not in titles:
                item["id"] = _id
                titles.append(item["title"])
                _final.append(item)
                _id += 1

        self.final = _final

        return self.final
