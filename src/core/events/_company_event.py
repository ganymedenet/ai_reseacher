import datetime
import time
import uuid
from dataclasses import dataclass
from mmutils import Instance
from models import CompanyEventModel
from session_base import SessionBase

from enum import Enum


class CompanyEvent(SessionBase, Instance):
    """

    CompanyEvent
        add to event db
        if no company add to the CompanyList
        for each company build/update the following:
            business summary
            tag cloud
            updated at



    """

    def __init__(self, name, event_type, title, body, summarized, link):
        self.id = str(uuid.uuid4())
        self.name = name
        self.type = event_type.value
        self.title = title
        self.body = body
        self.link = link
        self.summarized = summarized
        self.created_at = str(datetime.datetime.now())

    def save(self):
        self.session.dispatcher.add(
            CompanyEventModel(
                **
                self.dict
            )
        )
        print("EVENT CREATED", self.name, self.created_at)

    @property
    def dict(self):
        return dict(
            id=self.id,
            name=self.name,
            type=self.type,
            title=self.title,
            body=self.body,
            summarized=self.summarized,
            created_at=self.created_at
        )
