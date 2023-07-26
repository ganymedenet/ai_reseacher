import json
import time
import uuid
from typing import List
import requests
from dataclasses import dataclass
from session_base import SessionBase
from models import CompanyModel
from core.company import CompanyEvent


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
        prompt = """
        Forget all your previous instructions.
        
        Role: You are a hedge fund analyst analyzing news headers. You will be given a Json containing list of news headers.

        Goal 1: Read headers and identify article that can contain information about an '{target}'.
                
        Goal 2: Ignore duplicated headers or very similar headers that can be the same news published by different sources. 
        
        Goal 3: Return the list of identified news headers in the format:

        START:
        <"id" from the provided JSON>     
        :END
        
        JSON with headers to be processed: {headers}
        """.format(
            target=self.session.task.target,
            headers=headers
        )

        _raw = self.session.llm.query_with_error_callback(
            prompt=prompt,
            max_tokens=1000,
        )

        # print(_raw["choices"][0]["message"]["content"])

        string = _raw["choices"][0]["message"]["content"]

        res = string.split("START:")[1]
        res = res.split(":END")[0]
        res = res.split("\n")
        #
        # print(res)
        res = [x for x in res if x]
        # print(res)
        return res

    def parse_body(self, body):

        prompt = """
        Forget all your previous instructions.

        Role: You are a hedge fund analyst analyzing company news. You will be given an article about a company.

        Goal 1: Read headers and identify if article is about an '{target}'. If not, return 'NONE' straight away in the format:
        
        NONE
        
        Goal 2: If not, identify the company name and summarize article in 100 words. 
        
        Goal 3: If you can't identify the company name the article is of, return 'NONE' straight away in the format:
        
        NONE

        Goal 3: If you the article is about an '{target}' and you have identified the company name, return the result in the following format

        COMPANY NAME: [<identified name strictly in square brackets>]
            
        SUMMARIZED ARTICLE: [<summarized article strictly in the square brackets]

        Article body: {body}
        """.format(
            target=self.session.task.target,
            body=body
        )

        _raw = self.session.llm.query_with_error_callback(
            prompt=prompt,
            max_tokens=1000,
        )
        res = _raw["choices"][0]["message"]["content"]

        print(res)

        if res not in ['NONE']:
            name = res.split("COMPANY NAME: [")[1]
            name = name.split("]")[0]

            structured = res.split("SUMMARIZED ARTICLE: [")[1]
            structured = structured.split("]")[0]

            # print(_raw["choices"][0]["message"]["content"])
            # res = _raw["choices"][0]["message"]["content"]
            self.generate_event(
                name=name,
                body=body,
                result=structured
            )
            time.sleep(3)

    def generate_event(self, name, body, result):

        event = CompanyEvent(
            name=name,
            unstructured=body,
            structured=result
        )
        event.save()
        self.event_list.append(event)

    def parse_events(self) -> List[CompanyEvent]:
        self.fetch_news()

        headers = self.parse_headers()
        valid_headers = self.process_headers(headers)

        # print(valid_headers)
        #
        # for item in self.final:
        #     print("\n", item["id"], item["title"], item["source"]["uri"])
        print("FOUND HEADERS:", len(valid_headers))

        for header_id in valid_headers:
            print(header_id)
            body = [x["body"] for x in self.final if x["id"] == int(header_id)]
            self.parse_body(body[0])

        #
        # print(len(headers))

        return None

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
