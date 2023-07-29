import datetime
import json
import uuid
from typing import List
from dataclasses import dataclass
from core.company import Company
from session_base import SessionBase
from models.enums import EventType
from models import CompanyEventModel
from .company_event import CompanyEvent


@dataclass
class CompanyEventManager(SessionBase):

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
            name: str,
            event_type: EventType,
            title, body: str,
            tags: str,
            summarized: str
    ):
        """
        validate name or check if don't exist
        validate tags
        update company summary
        update core products or mindmap
        etc

        """

        if name in [
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
                name=name,
                type=event_type.value,
                title=title,
                body=body,
                tags=json.dumps(self.parse_tags(tags)),
                summarized=summarized,
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
