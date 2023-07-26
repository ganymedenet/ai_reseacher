import statistics
import mmutils
from mmutils import Amount
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# config = mmutils.helpers.get_config()

class Session:
    def __init__(
            self,
            log=True
    ):
        # self.env = config["env"]
        self.id = mmutils.helpers.get_letnum_id(6)
        self.log = log

        # MODULES
        self.db_dispatcher = None

        self._delay = None
        self._decimals = None


SESSION = None
