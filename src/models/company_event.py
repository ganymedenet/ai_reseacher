import json
from session import Base
# from database import Base
from sqlalchemy import Column, Integer, String, Float, Boolean


class CompanyEventModel(Base):
    __tablename__ = 'company_events'

    id = Column(String, primary_key=True, nullable=False)
    name = Column(String)
    type = Column(String)
    industry = Column(String)
    tags = Column(String)
    title = Column(String)
    summarized = Column(String)
    meta = Column(String)
    created_at = Column(String)

    def __repr__(self):
        return json.dumps(self.__dict__, indent=3)
