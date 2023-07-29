import uuid
from dataclasses import dataclass


@dataclass
class Company:
    id = str(uuid.uuid4())
    name: str
    summary: str
    tags: str
    created_at: str
    updated_at: str

    def update(self):
        pass