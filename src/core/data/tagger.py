from dataclasses import dataclass
from session_base import SessionBase
from models import CompanyModel
from typing import List


@dataclass
class Tagger(SessionBase):
    aliases = dict(
        AI=["artificialintelligence", "ai"],
        technology=["technology", "tech"]
    )

    def validate_aliases(self, tag):
        for key, als in self.aliases.items():
            if tag in als:
                return key
        return tag

    def validate_tags(self, tags: str) -> List[str]:

        # print("TAGS:", tags)
        final_tags = []

        _split = tags.split(",")

        for i in range(len(_split)):
            _split[i] = _split[i].replace("-", "")
            _split[i] = _split[i].replace("#", "")
            _split[i] = _split[i].replace(" ", "")
            _split[i] = _split[i].lower()
            _split[i] = _split[i].strip()

            tag = self.validate_aliases(_split[i])

            if tag not in final_tags:
                final_tags.append(tag)

        # print("TAGS FINAL:", final_tags)

        """
        The service must check the tags on a database

        if not exist:
            return tags

        if similar exists:
            generate manual review event

        if exists:
            return tag

        """
        return final_tags
