import datetime
import time
import uuid
from dataclasses import dataclass
from mmutils import Instance
from models import CompanyEventModel
from session_base import SessionBase
from models.enums import EventType
from enum import Enum
from typing import List


@dataclass
class RawEvent(Instance):
    name: str
    type: EventType
    title: str
    body: str
    ref: str
    tags: List[str]
    summarized: str

    @property
    def dict(self):
        return dict(
            name=self.name,
            type=self.type,
            title=self.title,
            body=self.body,
            ref=self.link,
            summarized=self.summarized
        )
