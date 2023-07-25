import session
import database
import asyncio
import traceback
import datetime
from mmutils import Amount


class SessionBase:
    def __init__(self):
        pass

    @property
    def session(self):
        return session.SESSION

    @property
    def db(self):
        return database.DATASTORAGE

    # def amount(self, value):
    #     return Amount(self.session.decimals, value)

    # def now(self):
    #     mmutils.helpers.now("cme")
    # @property
    # def provider(self):
    #     return self.session.data_provider_router.stock_data_provider

    async def handle_task_result(self, task: asyncio.Task) -> None:
        try:
            res = await task
            return res

        except Exception as e:  # pylint: disable=broad-except
            print('Exception raised by task = %r', task)
            print(e)
            traceback.print_exc()
            await self.send_error(e)
            raise Exception

    async def await_callback(self, task):
        return await self.handle_task_result(task)

    async def send_error(self, e):
        msg = f"{chr(0x26d4)} *Runtime Error*\n"
        msg += f"Session: {self.session.id}\n"
        msg += f"Error: {e}\n"
        msg += f"{datetime.datetime.now()}"

        # if self.session.telegram_log:
        #     await self.session.telegram_client.send_msg(msg)
        #
        #     await self.session.logger.push(
        #         service=self.__class__.__name__,
        #         function=self.send_error.__name__,
        #         level="error",
        #         info=f'ERROR REPORTED: {e}'
        #     )
