import datetime
from threading import Thread
from time import sleep

import pytz

from common.data.heartbeat import Heartbeat
from slave.src.data.context import get_bot_id
from slave.src.data.properties import get_properties
from slave.src.dropbox_handler import upload_heartbeat


def __upload_heartbeats_periodically() -> None:
    while True:
        now = datetime.datetime.now(tz=pytz.utc)
        heartbeat = Heartbeat(bot_id=get_bot_id(), heartbeat_timestamp=now)
        upload_heartbeat(heartbeat)
        sleep(get_properties().heartbeat_post_period)


def start_heartbeat_job() -> Thread:
    thread = Thread(target=__upload_heartbeats_periodically)
    thread.start()
    return thread
