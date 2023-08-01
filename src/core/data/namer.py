from dataclasses import dataclass
from session_base import SessionBase


@dataclass
class Namer(SessionBase):
    aliases = dict(

    )

    def validate_aliases(self, tag):
        for key, als in self.aliases.items():
            if tag in als:
                return key
        return tag

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
