from dataclasses import dataclass
from .company import Company
from session_base import SessionBase
from models import CompanyModel

from .company_event import CompanyEvent


@dataclass
class CompanyEventManager(SessionBase):

    def add_company_event(self, name, body, result):
        event = CompanyEvent(
            name=name,
            unstructured=body,
            structured=result
        )
        event.save()

    def check_company(self, company: Company):
        raise NotImplementedError

    def update_company(self, company: Company):
        raise NotImplementedError
