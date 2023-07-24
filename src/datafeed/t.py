import json

from dataclasses import dataclass
import requests


# Init
@dataclass
class NewsAPI:
    """
    https://newsapi.ai/

    sergey@omg.one:cUQ4KwvYnrUsFb@

    https://newsapi.ai/documentation?tab=searchArticles
    """
    key = "8af34ff7-fb88-45c4-aff0-7c6e9776082b"
    uri = "http://eventregistry.org/api/v1/article/getArticles"

    def fetch(self):
        _json = {
            "action": "getArticles",
            "keyword": "AI startup",
            "articlesPage": 3,
            "articlesCount": 200,
            "articlesSortBy": "date",
            "articlesSortByAsc": False,
            "articlesArticleBodyLen": -1,
            "resultType": "articles",
            "dataType": [
                "news",
                "pr"
            ],
            "apiKey": self.key,
            "forceMaxDataTimeWindow": 31
        }

        res = requests.get(
            self.uri,
            params=_json
        ).json()

        # print(res)
        headers = [
            dict(
                ts=f'{item["date"]} {item["time"]}',
                title=item["title"],
                source=item["source"]["uri"],
                url=item["url"]
            )
            for item in res["articles"]["results"]
        ]

        s = list()
        f = list()
        for h in headers:
            print(h["title"])

            if h["title"] not in s:
                f.append(h)
                s.append(h["title"])

        for item in f:
            print(json.dumps(item, indent=3))

        # for item in res["articles"]["results"]:
        #     print("\n", item["date"], item["time"], item["title"], item["source"]["uri"])

        print(len(headers), len(f))


client = NewsAPI()
client.fetch()
