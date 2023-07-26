import asyncio
from session_base import SessionBase


class DatabaseDispatcher(SessionBase):
    def __init__(self):
        super().__init__()

        self.db_queue = asyncio.Queue()

        asyncio.create_task(
            self.session.logger.push(
                service=self.__class__.__name__,
                function=self.__init__.__name__,
                info=f"{self.__class__.__name__} INITIALIZED"
            )
        )

    # async def push_signal(self, signal: Signal):
    #     # print("push signal ", signal.data)
    #     # print(s)
    #     self._last_signal = signal
    #     self._signals.append(self._last_signal)

    async def write_to_db(self, msg):
        retries = 5

        for attempt in range(1, retries):
            try:
                if msg.get("table"):
                    await self.db.insert_or_replace(
                        table_name=msg.get("table"),
                        obj=msg["data_object"]
                    )
                else:
                    await self.db.add(msg["data_object"])
                return

            except Exception as e:
                print(f"{self.__class__.__name__}: {self.write_to_db.__name__} attempt error")
                print(e)
                await asyncio.sleep(2)
                continue

    async def run_db_queue(self):
        # print("db")
        while True:
            if self.db.active:
                msg = await self.db_queue.get()
                # print(msg)
                await self.write_to_db(msg)
                # raise
            await asyncio.sleep(0.001)

            # await asyncio.sleep(0.01)
            #
            # if msg["table"]:
            #     self.db.update("orders", msg["data_object"])
            # else:
            #     self.db.add(msg["data_object"])

            # await asyncio.sleep(0.001)

    async def push_msg_to_db(self, data_object, table=None):
        msg = dict(
            table=table,
            data_object=data_object
        )
        await self.db_queue.put(msg)

        # print("PUSHED")
    # @property
    # def signal(self):
    #     return self._last_signal

#
# DB_DISPATCHER = DatabaseDispatcher()
