from dataclasses import dataclass
from session_base import SessionBase
from models import CompanyModel
from typing import List


@dataclass
class Tagger(SessionBase):

    def search_tag(self, tag):
        raise NotImplementedError

    def validate_tags(self, tags: List[str]) -> List[str]:
        """
        The service must check the tags on a database

        if not exist:
            return tags

        if similar exists:
            generate manual review event

        if exists:
            return tag

        """
        return tags
