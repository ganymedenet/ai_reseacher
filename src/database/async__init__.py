import asyncio
import session
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy import update, delete
from sqlalchemy import func, select
from sqlalchemy.sql import text as sa_text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import async_scoped_session, async_sessionmaker

Base = session.Base


class DataStorage:
    def __init__(self):
        self.session = None
        self.db_file = "sqlite+aiosqlite:///database/researcher.db"
        self.engine = create_async_engine(self.db_file, echo=False, connect_args={'timeout': 15})
        self.active = False

    async def init_models(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            self.active = True

    async def bind_all(self):
        # _session = sessionmaker(bind=self.engine)
        _session = async_sessionmaker(bind=self.engine, expire_on_commit=False)
        self.session = _session()
        Base.metadata.bind = self.engine
        # Base.metadata.create_all(bind=self.engine)
        asyncio.create_task(self.init_models())

    # async def truncate_klines(self):
    #     table = sqlalchemy.Table("klines", Base.metadata, autoload=True)
    #     # to_delete = self.session.query(table)
    #     # to_delete.delete(synchronize_session=False)
    #     q = delete(table)
    #     await self.session.execute(q)
    #     await self.session.commit()

    async def add(self, obj):
        async with AsyncSession(self.engine) as session:
            async with session.begin():
                await session.merge(
                    obj
                )
        await session.commit()

    async def add_all(self, object_list):
        async with AsyncSession(self.engine) as session:
            async with session.begin():
                session.add_all(
                    object_list
                )

            await session.commit()

    async def update(self, table_name, obj):
        table = sqlalchemy.Table(table_name, Base.metadata, autoload=True)

        async with AsyncSession(self.engine) as session:
            async with session.begin():
                await session.execute(
                    table.update().where(table.c.id == obj["id"]).values(**obj)
                )
        await session.commit()

    async def insert_or_replace(self, table_name, obj):
        table = sqlalchemy.Table(table_name, Base.metadata, autoload=True)

        async with AsyncSession(self.engine) as session:
            async with session.begin():
                await session.execute(
                    table.insert().prefix_with('OR REPLACE').values(**obj)
                )
        await session.commit()

    async def insert_or_ignore(self, table_name, obj):
        table = sqlalchemy.Table(table_name, Base.metadata, autoload=True)

        async with AsyncSession(self.engine) as session:
            async with session.begin():
                await session.execute(
                    table.insert().prefix_with('OR IGNORE').values(**obj)
                )
        await session.commit()

    async def get_klines(self, symbol, depth):
        klines = sqlalchemy.Table("klines", Base.metadata, autoload=True)

        async with AsyncSession(self.engine) as session:
            async with session.begin():
                statement = (
                    select(klines).
                    where(
                        klines.c.symbol == symbol
                    ).order_by(klines.c.start.desc()).limit(depth)
                )
            res = await session.execute(statement)

        return res.fetchall()

    # async def get_positions(self):
    #     # positions = sqlalchemy.Table("positions", Base.metadata, autoload=True)
    #
    #     async with AsyncSession(self.engine) as session:
    #         async with session.begin():
    #             positions = select(PositionModel)
    #
    #             res = await session.scalars(positions)
    #             return [p.dict for p in res]
    #             # res = await session.query(PositionModel).all()
    #             # res = PositionModel.query.all()
    #         # res = await session.execute(statement)
    #
    #     # return res
    #
    # async def get_orders(self):
    #     async with AsyncSession(self.engine) as session:
    #         async with session.begin():
    #             orders = select(OrderModel)
    #             res = await session.scalars(orders)
    #
    #             return [o.dict for o in res]
    #
    # async def get_position(self, symbol):
    #     positions = sqlalchemy.Table("positions", Base.metadata, autoload=True)
    #
    #     async with AsyncSession(self.engine) as session:
    #         async with session.begin():
    #             statement = (
    #                 select(positions).
    #                 where(
    #                     positions.c.symbol == symbol,
    #                     positions.c.active == True
    #                 )
    #             )
    #         res = await session.execute(statement)
    #
    #     return res.fetchone()


DATASTORAGE = DataStorage()
