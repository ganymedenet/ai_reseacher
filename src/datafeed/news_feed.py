from newsapi import NewsApiClient
from dataclasses import dataclass


# Init
@dataclass
class NewsAPI:
    """
    https://newsapi.org/docs/endpoints/top-headlines
    """
    newsapi = NewsApiClient(api_key='API_KEY')

    # /v2/top-headlines
    def fetch(self):
        top_headlines = self.newsapi.get_top_headlines(q='bitcoin',
                                                  sources='bbc-news,the-verge',
                                                  category='business',
                                                  language='en',
                                                  country='us')

        # /v2/everything
        all_articles = self.newsapi.get_everything(q='bitcoin',
                                              sources='bbc-news,the-verge',
                                              domains='bbc.co.uk,techcrunch.com',
                                              from_param='2017-12-01',
                                              to='2017-12-12',
                                              language='en',
                                              sort_by='relevancy',
                                              page=2)

    # /v2/top-headlines/sources
    sources = newsapi.get_sources()


class NewsFeed:
    pass
