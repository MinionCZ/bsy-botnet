
import threading
import time

from master.src.data.context import is_running, update_online_bots
from master.src.data.properties import get_properties
from master.src.dropbox_handler import download_and_delete_heartbeats


def __download_heartbeats_periodically() -> None:
    while is_running():
        downloaded_heartbeats = download_and_delete_heartbeats()
        bot_ids = list(map(lambda heartbeat: heartbeat.bot_id, downloaded_heartbeats))
        update_online_bots(bot_ids)
        print("List of active bots updated")
        time.sleep(get_properties().heartbeat_fetch_period)


def start_heartbeat_fetcher_job() -> threading.Thread:
    thread = threading.Thread(target=__download_heartbeats_periodically)
    thread.start()
    return thread
