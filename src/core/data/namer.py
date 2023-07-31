from dataclasses import dataclass
from session_base import SessionBase
from models import CompanyModel


@dataclass
class Namer(SessionBase):


    def search_name(self, name):
        raise NotImplementedError

    def validate_name(self, name: str):
        """
        The service must check the name on a database

        if not exist:
            return name

        if aliases exists:
            return canonical name

        if similar exists:
            generate manual review event

        if exists:
            return name

        """
        return name
