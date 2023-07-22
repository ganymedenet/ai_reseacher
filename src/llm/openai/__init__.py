from typing import List, Dict, Tuple
from dataclasses import dataclass


class OpenAI:
    client: NotImplementedError

    def analyze_header(self):
        raise NotImplementedError

    def analyze_article(self):
        raise NotImplementedError
