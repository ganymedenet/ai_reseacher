import json
import uuid
import requests
from dataclasses import dataclass
from session_base import SessionBase


@dataclass
class NewsFeed(SessionBase):
    """
    https://newsapi.ai/

    sergey@omg.one:cUQ4KwvYnrUsFb@

    https://newsapi.ai/documentation?tab=searchArticles
    """
    key = "8af34ff7-fb88-45c4-aff0-7c6e9776082b"
    uri = "http://eventregistry.org/api/v1/article/getArticles"
    final = []

    def fetch_news(self):

        for i in range(1, 3, 1):
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

            print(f"Page {i}:", len(res), "\n")

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

    def parse_headers(self):
        headers = [
            dict(
                id=item["id"],
                title=item["title"],
            )
            for item in self.final
        ]
        return headers

    def process_headers(self, headers):
        target = "AI startup"
        prompt = """
        Forget all your previous instructions.
        
        Role: You are a hedge fund analyst analyzing news headers. You will be given a Json containing list of news headers.

        Goal 1: Read headers and identify article that can contain information about an '{target}'.
                
        Goal 2: Ignore duplicated headers or very similar headers that can be the same news published by different sources. 
        
        Goal 3: Return the list of identified news headers in the format:

        HEADERS:
        <"id" from the provided JSON>     
        
        JSON with headers to be processed: {headers}
        """.format(
            target=target,
            headers=headers
        )

        _raw = self.session.llm.query_with_error_callback(
            prompt=prompt,
            max_tokens=1000,
        )

        print(_raw["choices"][0]["message"]["content"])

    def fetch(self):

        # print(res)
        self.fetch_news()

        headers = self.parse_headers()

        for item in self.final:
            print("\n", item["id"], item["title"], item["source"]["uri"])

        print(len(headers))

        self.process_headers(headers)
        # headers = [
        #     dict(
        #         ts=f'{item["date"]} {item["time"]}',
        #         title=item["title"],
        #         source=item["source"]["uri"],
        #         url=item["url"]
        #     )
        #     for item in self.final
        # ]

        # s = list()
        # f = list()
        # for h in headers:
        #     print(h["title"])
        #
        #     if h["title"] not in s:
        #         f.append(h)
        #         s.append(h["title"])

        # for item in f:
        #     print(json.dumps(item, indent=3))

        # print(len(headers), len(f))

#
# client = NewsAPI()
# client.fetch()
