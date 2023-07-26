import uuid
from dataclasses import dataclass
from session_base import SessionBase


@dataclass
class DailyEvent:
    id = str(uuid.uuid4())
