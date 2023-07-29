import json
import time
import uuid
from typing import List
import requests
from dataclasses import dataclass
from session_base import SessionBase
from models import CompanyModel
from core.company import CompanyEvent
from .news_feed import NewsFeed


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
class NewsParser(SessionBase):
    """
    https://newsapi.ai/

    sergey@omg.one:cUQ4KwvYnrUsFb@

    https://newsapi.ai/documentation?tab=searchArticles
    https://platform.openai.com/docs/guides/gpt/function-calling
    """
    key = "8af34ff7-fb88-45c4-aff0-7c6e9776082b"
    uri = "http://eventregistry.org/api/v1/article/getArticles"

    feed = NewsFeed()

    final = None
    event_list = list()

    def fetch_news(self):
        self.final = self.feed.fetch_news()

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
        print("TARGET:", self.session.task.target)

        headers = headers[:470]
        print(len(headers))

        prompt = """       
        Role: You are a hedge fund analyst responsible for analyzing news headlines. You will be provided with a JSON containing a list of news headlines.

        To match article titles with the search term, you will receive a search term in the form of a TARGET, consisting of up to 10 words. The Target represents the type of company you are looking for articles about.        
        You must allow for broader matches for the target to avoid overly narrow searches. The search term may not always be explicitly presented in the article title, so try to guess the context.

        TARGET: '{target}' 
        
        Goal 1: Read article titles and identify article that can contain information about the TARGET.
                
        Goal 2: Ignore duplicated headers or very similar headers that can be the same news published by different sources. 
        
        Goal 3: Return the list of identified news headers in the format:

        START
        <"id" from the provided JSON>     
        END
        
        JSON with headers to be processed: {headers}
        """.format(
            target=self.session.task.target,
            headers=headers
        )

        # prompt = """
        # Role: You are a hedge fund analyst responsible for analyzing news headlines. You will be provided with a JSON containing a list of news headlines.
        #
        # To match article titles with the search term, you will receive a search term in the form of a TARGET, consisting of up to 10 words. The Target represents the type of company you are looking for articles about.
        # You must allow for broader matches for the target to avoid overly narrow searches. The search term may not always be explicitly presented in the article title, so try to guess the context.
        #
        # TARGET: '{target}'
        #
        # Goal 1: Read headers and identify article that can contain information about the TARGET.
        #
        # Goal 2: Ignore duplicated headers or very similar headers that can be the same news published by different sources.
        #
        # Goal 3: Return the list of identified news headers in the format:
        #
        # RESULTING LIST:
        # <title> - <up to 20 words reason why you have chosen this title>
        #
        # JSON with headers to be processed: {headers}
        # """.format(
        #     target=self.session.task.target,
        #     headers=headers
        # )

        string = self.session.llm.query_with_error_callback(
            prompt=prompt,
            max_tokens=1000,
        )

        # print(string)

        # print(_raw["choices"][0]["message"]["content"])

        res = string.split("START")[1]
        res = res.split("END")[0]
        res = res.split("\n")
        #
        # print(res)
        res = [x for x in res if x]
        # print(res)
        return res

    def parse_body(self, body):
        prompt = """

        Role: You are a market researcher responsible for analyzing company news. You will be given an article about a company.
        Additionally, you will receive a TARGET - a company type description consisting of up to 20 words that you are looking for articles about.
        Your main goal is to match the article with the target description and determine if the article is about the specified target.
        
        TARGET: '{target}'

        Goal 1: Read the article and identify if article is about the target. 
        Depending of result produce one of the two following possible outcomes.
        Goal 2: Identify the name of the target company, if there is no company name in the article, 
        consider the outcome is Outcome 1.
                
        If article is not about the target please return OUTCOME 1 in the FORMAT: 
        
        SUCCESS: FALSE
        SUMMARIZED ARTICLE: [<summarized strictly in up to 100 words particle in the square brackets]
        
        If article is about the target please return OUTCOME 2 in the FORMAT:
        
        SUCCESS: TRUE 
        
        COMPANY NAME: [<identified name strictly in square brackets>]
            
        SUMMARIZED ARTICLE: [<summarized strictly in up to 100 article in the square brackets]

        Article to be processed: {body}
        """.format(
            target=self.session.task.description,
            body=body
        )

        res = self.session.llm.query_with_error_callback(
            prompt=prompt,
            max_tokens=1000,
        )

        print("\n", res)
        time.sleep(3)
        # if res not in ['NONE']:
        #     name = res.split("COMPANY NAME: [")[1]
        #     name = name.split("]")[0]
        #
        #     structured = res.split("SUMMARIZED ARTICLE: [")[1]
        #     structured = structured.split("]")[0]
        #
        #     # print(_raw["choices"][0]["message"]["content"])
        #     # res = _raw["choices"][0]["message"]["content"]
        #     self.generate_event(
        #         name=name,
        #         body=body,
        #         result=structured
        #     )
        #     time.sleep(3)

    def generate_event(self, name, body, result):
        self.session.company_event_manager(name, body, result)

    def parse_events(self) -> List[CompanyEvent]:
        self.fetch_news()

        headers = self.parse_headers()

        print("INPUT HEADERS:", len(headers))

        valid_headers = self.process_headers(headers)

        print("VALID HEADERS:", len(valid_headers))

        for header_id in valid_headers:
            print(header_id)
            body = [x["body"] for x in self.final if x["id"] == int(header_id)]
            res = [x for x in self.final if x["id"] == int(header_id)]

            # for r in res:
            #     print(r["title"])
            self.parse_body(body)

        print("OUTPUT:", len(valid_headers))

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
