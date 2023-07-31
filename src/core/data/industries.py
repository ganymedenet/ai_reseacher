from dataclasses import dataclass
from session_base import SessionBase


@dataclass
class Industries(SessionBase):
    industries = dict(
        technology=[
            "Artificial Intelligence"
        ]
    )

    @property
    def list(self):
        return self.industries
