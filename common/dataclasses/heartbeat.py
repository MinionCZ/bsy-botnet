import datetime
import uuid

from pydantic import BaseModel

from master.src.dataclasses.properties import get_properties


class Heartbeat(BaseModel):
    bot_id: uuid.UUID
    heartbeat_timestamp: datetime.datetime

    def map_to_table_row(self) -> str:
        formatted_timestamp = self.heartbeat_timestamp.strftime("%d.%m.%Y %H:%M:%S")
        bot_max_delay_datetime = datetime.datetime.now() - datetime.timedelta(
            seconds=get_properties().bot_maximum_heartbeat_delay)
        status = " ONLINE" if self.heartbeat_timestamp > bot_max_delay_datetime else "OFFLINE"
        return f'| {self.bot_id} | {formatted_timestamp} | {status} |'
