import uuid
from dataclasses import dataclass
from mmutils import Instance


@dataclass
class Task(Instance):
    id = str(uuid.uuid4())
    raw: str
    target: str

    def load(self):
        raise NotImplementedError

    @property
    def dict(self):
        return dict(
            id=self.id,
            raw=self.raw,
            target=self.target
        )
