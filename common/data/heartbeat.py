import datetime
import uuid

from pydantic import BaseModel


class Heartbeat(BaseModel):
    bot_id: uuid.UUID
    heartbeat_timestamp: datetime.datetime

    def __hash__(self):
        return hash(self.bot_id)

    def __eq__(self, other):
        if other is None:
            return False
        if isinstance(other, self.__class__):
            return self.bot_id == other.bot_id
        return False
