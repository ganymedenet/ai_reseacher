import json
import os

import sqlalchemy
import session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import update
from sqlalchemy import func, select

Base = session.Base


class DataStorage:
    def __init__(self):
        self.db_file = "sqlite:///database/researcher.db"
        self.engine = create_engine(self.db_file, echo=False)
        self.session = None

        # Base.metadata.bind = self.engine
        # Base.metadata.create_all(bind=self.engine)
        # print("CONNECTED")
        # self.bind_all()

    def bind_all(self):
        _session = sessionmaker(bind=self.engine)
        self.session = _session()
        Base.metadata.bind = self.engine
        Base.metadata.drop_all(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

    def add(self, obj):
        self.session.add(obj)
        self.session.commit()
        return True

    # def update(self, table_name, obj):
    #     table = sqlalchemy.Table(table_name, Base.metadata, autoload=True)
    #
    #     self.session.execute(
    #         table.update().where(table.c.id == obj["id"]).values(**obj)
    #     )
    #     self.session.commit()
    #
    # def get_kappa(self, spread):
    #     kappas = sqlalchemy.Table("kappas", Base.metadata, autoload=True)
    #
    #     statement = (
    #         select(kappas.c.kappa).
    #         where(
    #             kappas.c.spread == spread
    #         )
    #     )
    #     # print(statement.compile(self.engine, compile_kwargs={"literal_binds": True}))
    #     return self.session.execute(statement).scalar()
    #
    # @property
    # def total_bought(self):
    #     orders = sqlalchemy.Table("orders", Base.metadata, autoload=True)
    #     positions = sqlalchemy.Table("positions", Base.metadata, autoload=True)
    #
    #     statement = (
    #         select(func.sum(orders.c.executed_quantity * orders.c.execution_price)).
    #         join(positions, positions.c.id == orders.c.position_id).
    #         where(
    #             orders.c.side == "BUY",
    #             # orders.c.status.in_((OrderStatus.FILLED.value, OrderStatus.PARTIALLY_FILLED.value)),
    #             positions.c.session_id == cfg.SESSION.id
    #         )
    #     )
    #     # print(statement.compile(self.engine, compile_kwargs={"literal_binds": True}))
    #     # raise
    #     return self.session.execute(statement).scalar()

    # @property
    # def total_sold(self):
    #     orders = sqlalchemy.Table("orders", Base.metadata, autoload=True)
    #     positions = sqlalchemy.Table("positions", Base.metadata, autoload=True)
    #
    #     statement = (
    #         select(func.sum(orders.c.executed_quantity * orders.c.execution_price)).
    #         join(positions, positions.c.id == orders.c.position_id).
    #         where(
    #             orders.c.side == "SELL",
    #             # orders.c.status.in_((OrderStatus.FILLED.value, OrderStatus.PARTIALLY_FILLED.value)),
    #             positions.c.session_id == cfg.SESSION.id
    #         )
    #     )
    #     # print(str(statement))
    #     return self.session.execute(statement).scalar()
    #
    # def get_inventory(self, position_id=None):
    #     """
    #     Implement fetching inventory by position ID later
    #     """
    #
    #     orders = sqlalchemy.Table("orders", Base.metadata, autoload=True)
    #     positions = sqlalchemy.Table("positions", Base.metadata, autoload=True)
    #
    #     statement = (
    #         select(func.sum(orders.c.executed_quantity)).
    #         join(positions, positions.c.id == orders.c.position_id).
    #         where(
    #             orders.c.side == "BUY",
    #             # orders.c.status.in_((OrderStatus.FILLED.value, OrderStatus.PARTIALLY_FILLED.value)),
    #             positions.c.session_id == cfg.SESSION.id
    #         )
    #     )
    #     buy_sum = self.session.execute(statement).scalar()
    #
    #     statement = (
    #         select(func.sum(orders.c.executed_quantity)).
    #         join(positions, positions.c.id == orders.c.position_id).
    #         where(
    #             orders.c.side == "SELL",
    #             # orders.c.status.in_((OrderStatus.FILLED.value, OrderStatus.PARTIALLY_FILLED.value)),
    #             positions.c.session_id == cfg.SESSION.id
    #         )
    #     )
    #     sell_sum = self.session.execute(statement).scalar()
    #
    #     if not buy_sum:
    #         buy_sum = 0
    #
    #     if not sell_sum:
    #         sell_sum = 0
    #
    #     return buy_sum - sell_sum

    # def start_engine(self):
    #     return create_engine(self.db_file, echo=False)
    #     # Session = sessionmaker(bind=engine)

    # def start_session(self):
    #     _session = sessionmaker(bind=self.engine)
    #     return _session()

    # @property
    # def total_sold(self):
    #     table = sqlalchemy.Table("orders", Base.metadata, autoload=True)
    #     return self.session.execute(
    #         select(func.sum(table.c.quantity_executed * table.c.price)).where(
    #             table.c.side == "SELL",
    #             table.c.status.in_((OrderStatus.FILLED.value, OrderStatus.PARTIALLY_FILLED.value))
    #         )
    #     ).scalar()

    # def get_position_inventory(self, position_id):
    #     table = sqlalchemy.Table("orders", Base.metadata, autoload=True)
    #
    #     buy_sum = self.session.execute(
    #         select(func.sum(table.c.quantity)).where(
    #             table.c.position_id  == position_id,
    #             table.c.side == "BUY",
    #             table.c.executed == 1
    #         )
    #     ).scalar()
    #
    #     sell_sum = self.session.execute(
    #         select(func.sum(table.c.quantity)).where(
    #             table.c.position_id == position_id,
    #             table.c.side == "SELL",
    #             table.c.executed == 1
    #         )
    #     ).scalar()
    #
    #     if not buy_sum:
    #         buy_sum = 0
    #
    #     if not sell_sum:
    #         sell_sum = 0
    #
    #     return buy_sum - sell_sum


DATASTORAGE = DataStorage()

# class Trade(Base):
#     __tablename__ = 'trades2'
#
#     id = Column(String, primary_key=True)
#     symbol = Column(String)
#
#     def __repr__(self):
#         return json.dumps(self.__dict__)
#
# Base.metadata.create_all(self.engine)
# message = Trade(id=str(uuid.uuid4()), symbol="ETHUSDT")
# self.session.add(message)
# self.session.commit()
