from dataclasses import dataclass
from session_base import SessionBase
import session
from dispatcher import DatabaseDispatcher
from datafeed import NewsParser
from llm.openai import OpenAI
from core import Task, DataParser, CompanyManager, Reporter, TaskA, CompanyEventManager
from models import CompanyModel
from dispatcher import DatabaseDispatcher


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

    news: NotImplementedError
    news_headers: NotImplementedError
    result: NotImplementedError

    def initialize(self):
        session.SESSION = session.Session()
        self.initialize_database()
        self.session.dispatcher = DatabaseDispatcher()
        self.session.llm = OpenAI()
        self.session.news_parser = NewsParser()

        self.session.company_manager = CompanyManager()
        self.session.company_event_manager = CompanyEventManager()

        self.session.data_parser = DataParser()
        self.session.reporter = Reporter()

    def initialize_database(self):
        self.db.bind_all()

    def load_task(self):
        # self.session.task = Task(
        #     # raw="gaming company developing play-to-earn games",
        #     raw="AI startup"
        # )

        self.session.task = TaskA()

    def run(self):
        self.initialize()
        self.load_task()
        self.session.data_parser.run()

        # TODO: analyze events
        # TODO: research companies


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
