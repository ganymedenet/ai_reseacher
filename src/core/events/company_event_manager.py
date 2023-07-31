import datetime
import json
import uuid
from typing import List
from dataclasses import dataclass
from core.company import Company
from session_base import SessionBase
# from models.enums import EventType
from models import CompanyEventModel
# from .company_event import CompanyEvent
from core.data import Namer, Tagger
from .raw_event import RawEvent


@dataclass
class CompanyEventManager(SessionBase):
    namer = Namer()
    tagger = Tagger()

    @staticmethod
    def parse_tags(tags):
        tags = tags.replace("#", "").split(",")
        return tags

    def validate_name(self):
        # TODO:
        raise NotImplementedError

    def validate_tags(self):
        # TODO:
        raise NotImplementedError

    def validate_title(self):
        # TODO:
        raise NotImplementedError

    def if_title_duplicated(self, title) -> bool:
        # TODO: check header similarity
        return False

    def add_company_event(
            self,
            raw_event: RawEvent
    ):
        """
        validate name or check if don't exist
        validate tags
        update company summary
        update core products or mindmap
        etc

        """

        name_processed = self.namer(raw_event.name)
        tags_processed = self.tagger(raw_event.tags)

        if name_processed in [
            "OpenAI",
            "AWS",
            "Google",
            "Facebook",
            "Microsoft",
            "Tesla",
            "Apple",
            "Alibaba",
            "NONE"
        ]:
            return

        # TODO: implement pydantic
        event_model = CompanyEventModel(
            **
            dict(
                id=str(uuid.uuid4()),
                name=name_processed,
                type=raw_event.type.value,
                title=raw_event.title,
                body=raw_event.body,
                tags=json.dumps(tags_processed),
                summarized=raw_event.summarized,
                created_at=str(datetime.datetime.now()))
        )

        self.save_event(event_model)

    def save_event(self, event_model):
        self.session.dispatcher.add(
            event_model
        )
        print("EVENT CREATED")

    def check_company(self, company: Company):
        raise NotImplementedError

    def update_company(self, company: Company):
        raise NotImplementedError
