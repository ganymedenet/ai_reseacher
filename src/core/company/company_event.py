import datetime
import time
import uuid
from dataclasses import dataclass
from mmutils import Instance
from models import CompanyEventModel
from session_base import SessionBase


class CompanyEvent(SessionBase, Instance):
    def __init__(self, name, unstructured, structured):
        self.id = str(uuid.uuid4())
        self.name = name
        self.unstructured = unstructured
        self.structured = structured
        self.processed = False
        self.created_at = str(datetime.datetime.now())
        print(self.id)

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
            unstructured=self.unstructured,
            structured=self.structured,
            processed=self.processed,
            created_at=self.created_at
        )
