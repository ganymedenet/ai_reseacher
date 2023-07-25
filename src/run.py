from dataclasses import dataclass
from session_base import SessionBase
import session
from dispatcher import DatabaseDispatcher
from llm.openai import OpenAI
from core.news_parser import NewsParser
from datafeed import NewsFeed


class Researcher(SessionBase):
    """
    Task Definition

    DataSources:
        -> News APIs

        Company
            website parsing
            social media
        Public Social Media
        Public website parsing

    Main Flow:

        NewsParser fetches news from NewsFeed
        NewsParser build header list
        Main analyzes headers (LLM)

        Main request articles by headers
        NewsParser marks news as read
        NewsParser fetches articles by headers
        Main analyzes articles (LLM)
            Identify companies
                search for company website
                search for other info
            Check if already exist
            Update current list item
        Main build daily summary

        identify companies
        add to lists

    LLM:
        Functions:
            add to list
            get company info
                meta
                bullet points

    ListManager:
        build List

    List:
        add item to list
        update list item

    Company
        meta
        bullet points
        news feed
    """
    task: NotImplementedError
    news: NotImplementedError
    news_headers: NotImplementedError
    result: NotImplementedError

    def initialize(self):
        session.SESSION = session.Session()
        # self.session.dispatcher = DatabaseDispatcher()
        self.session.llm = OpenAI()
        self.session.news_feed = NewsFeed()
        # self.session.news_parser = NewsParser()

    def fetch_news(self):
        """
        NewsParser fetches news from NewsFeed
        """
        raise NotImplementedError

    def analyze_headers(self):
        """
        get headers from NewsParser
        user LLM
        """
        raise NotImplementedError

    def analyze_articles(self):
        """
        fetch articles by header id from NewsParser
        analyze articles with LLM
        return result
        """


    def run(self):
        self.initialize()
        self.session.news_feed.fetch()


if __name__ == "__main__":

    researcher = Researcher()
    researcher.run()
    """
    
    
    """
    """
    TASK
      create
      
    SEARCH
        fetch news
        check for matches each article
            if match:
                if exist in the LIST:
                    get current desc bullet points
                        if new info:
                            add to company info
                            save
                else:
                    add company to LIST:
                      add meta data
                      decompose to bullet points
                      save
        
    
    - LIST
      - Design structure
    
    - COMPANY
      - design structure
    
    """
