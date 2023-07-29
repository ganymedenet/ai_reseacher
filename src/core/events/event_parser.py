import uuid
from typing import List, Dict, Tuple
from dataclasses import dataclass
from session_base import SessionBase
from core.events.company_event import CompanyEvent


@dataclass
class EventParser(SessionBase):
    """
    proposed data source

    - news api
    - linkedin feed
    - crunchbase feed
    - producthunt feed
    - twitter feed
    """
    news_events: List[CompanyEvent] = None
    other_events: List[CompanyEvent] = None

    def parse_events(self):
        self.news_events = self.session.news_parser.parse_events()

    def process_events(self):
        """
        CompanyManager
            - check if company exist
            - if no:
                add
                generate_daily_event()
            - if yes:
                if new info:
                    update
                else:
                    add info to scope
                    generate_daily_event()
        """

    def generate_report(self):
        raise NotImplementedError

    def run(self):
        self.parse_events()
        self.process_events()
