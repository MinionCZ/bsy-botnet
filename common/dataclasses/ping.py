import datetime
import uuid

from pydantic import BaseModel


class Ping(BaseModel):
    bot_id: uuid.UUID
    ping_timestamp: datetime.datetime



