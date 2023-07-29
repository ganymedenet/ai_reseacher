import json
from session import Base
# from database import Base
from sqlalchemy import Column, Integer, String, Float, Boolean


class CompanyModel(Base):
    __tablename__ = 'companies'

    id = Column(String, primary_key=True, nullable=False)
    name = Column(String)
    summary = Column(String)
    tags = Column(String)
    created_at = Column(String)
    updated_at = Column(String)

    # description = Column(String)
    # scope = Column(String)
    # created_at = Column(String)
    # updated_at = Column(String)

    def __repr__(self):
        return json.dumps(self.__dict__, indent=3)
