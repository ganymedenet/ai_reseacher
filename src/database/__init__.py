from dataclasses import dataclass


@dataclass
class DataStorage:
    db: str


DATASTORAGE = DataStorage()
