import json
import time
import uuid
from typing import List
import requests
from dataclasses import dataclass
from session_base import SessionBase
from core import CompanyEvent
from .news_feed import NewsFeed
from models.enums import EventType


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

    def extract_name_and_summarize(self, data):
        article = dict(
            title=data["title"],
            body=data["body"]
        )

        prompt = """       
        Role: You are a hedge fund analyst responsible for analyzing news headlines. You will be provided with a JSON containing a news article.

    
        Goal 1: Identify the company name the article is about.
                
        Goal 2: Summarize the article into an up to 200 words text. 
        
        Goal 3: Generate short up to 3 #tags for the article. Tag must reflect the main topics the article is about.
        
        Return in the following format:
        
        NAME: <identified company name or NONE>

        TAGS: <tags separated by ','>
        
        SUMMARIZED: <summaraized in up to 200 words article>
        
        Next I provide the JSON with the article to be processed: '{article}'
        """.format(article=article)

        string = self.session.llm.query_with_error_callback(
            prompt=prompt,
            max_tokens=1000,
        )

        # print(string)

        res = string.split("NAME:")[1]
        name = res.split("TAGS:")[0].strip()

        tags = string.split("TAGS:")[1]
        tags = tags.split("SUMMARIZED:")[0].strip()

        summaraized = string.split("SUMMARIZED:")[1].strip()

        return dict(
            title=article["title"],
            body=article["body"],
            name=name,
            tags=tags,
            summaraized=summaraized
        )

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
        # time.sleep(3)
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

        for new in self.final:
            print("\n", new["title"])

            # TODO: check title duplicates in CompanyEventManager
            if self.session.company_event_manager.if_title_duplicate(new):
                continue

            extracted = self.extract_name_and_summarize(new)

            print(json.dumps(
                dict(
                    name=extracted["name"],
                    tags=extracted["tags"],
                    summaraized=extracted["summaraized"]
                ), indent=3
            ))

            self.session.company_event_manager.add_company_event(
                **
                dict(
                    name=extracted["name"],
                    event_type=EventType.NEWS,
                    title=extracted["title"],
                    body=extracted["body"],
                    tags=extracted["tags"],
                    summarized=extracted["summaraized"]
                )
            )
            time.sleep(5)
