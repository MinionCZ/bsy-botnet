import datetime
import uuid

from pydantic import BaseModel

from master.src.dataclasses.properties import get_properties


def _get_correct_version_of_online(is_some_heartbeat_offline: bool) -> str:
    return "ONLINE " if is_some_heartbeat_offline else "ONLINE"


class Heartbeat(BaseModel):
    bot_id: uuid.UUID
    heartbeat_timestamp: datetime.datetime

    def is_online(self) -> bool:
        bot_max_delay_datetime = datetime.datetime.now() - datetime.timedelta(
            seconds=get_properties().bot_maximum_heartbeat_delay)
        return self.heartbeat_timestamp > bot_max_delay_datetime

    def map_to_table_row(self, is_some_heartbeat_offline: bool) -> str:
        formatted_timestamp = self.heartbeat_timestamp.strftime("%d.%m.%Y %H:%M:%S")
        status = _get_correct_version_of_online(
            is_some_heartbeat_offline) if self.is_online() else "OFFLINE"
        return f'| {self.bot_id} | {formatted_timestamp} | {status} |'
