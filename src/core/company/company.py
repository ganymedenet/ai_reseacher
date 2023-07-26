import uuid
from dataclasses import dataclass


@dataclass
class Company:
    id = str(uuid.uuid4())
