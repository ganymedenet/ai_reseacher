from dataclasses import dataclass
from session_base import SessionBase
from .daily_event import DailyEvent
from typing import List


@dataclass
class Reporter:
    daily_events: List[DailyEvent] = None
