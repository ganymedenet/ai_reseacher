from dataclasses import dataclass
from session_base import SessionBase


@dataclass
class Industries(SessionBase):
    industries = dict(
        technology=[
            "Artificial Intelligence",
            "BioTech",
            "AgriTech",
            "Fintech",
            "EdTech",
            "FoodTech",
            "CleanTech",
            "Gaming",
            "Hardware"
        ]
    )

    @property
    def list(self):
        lst = "', '".join(self.industries["technology"])
        lst = f"'{lst}'"
        return lst
