from dataclasses import dataclass
from .company import Company
from session_base import SessionBase
from models import CompanyModel


@dataclass
class CompanyManager(SessionBase):

    def add_company(self, data: Company):
        self.session.dispatcher.add(
            CompanyModel(
                **
                dict(
                    id="123",
                    name="123"
                )
            )
        )

    def check_company(self, company: Company):
        raise NotImplementedError

    def update_company(self, company: Company):
        raise NotImplementedError
