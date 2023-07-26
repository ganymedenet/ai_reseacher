from dataclasses import dataclass
from session_base import SessionBase
from queue import Queue


@dataclass
class DatabaseDispatcher(SessionBase):
    add_queue = Queue()

    def add(self, data_object):
        self.add_queue.put(data_object)
        item = self.add_queue.get()

        self.db.add(
            item
        )
