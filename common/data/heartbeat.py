import datetime
import uuid

from pydantic import BaseModel


class Heartbeat(BaseModel):
    bot_id: uuid.UUID
    heartbeat_timestamp: datetime.datetime
