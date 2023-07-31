import time
import uuid
from typing import List, Dict, Tuple
from dataclasses import dataclass
from session_base import SessionBase
from .raw_event import RawEvent


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
    news_events: List[RawEvent] = None
    other_events: List[RawEvent] = None

    def parse_events(self):
        # self.news_events: List[RawEvent] = self.session.news_parser.parse_events()

        self.session.news_parser.parse_events()

    def process_events(self):
        for event in self.news_events:
            self.session.company_event_manager.add_company_event(
                event
            )

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

    def save(self):
        raise NotImplementedError

    def generate_report(self):
        raise NotImplementedError

    def run(self):
        self.parse_events()
        self.process_events()
