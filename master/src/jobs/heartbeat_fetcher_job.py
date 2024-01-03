import datetime
import math
import threading
import time
from typing import List, Tuple

from common.data.heartbeat import Heartbeat
from master.src.data.context import is_running, update_online_bots
from master.src.data.properties import get_properties
from master.src.dropbox_handler import download_heartbeats


def __mark_heartbeats_with_bot_status(heartbeats: List[Heartbeat]) -> List[Tuple[Heartbeat, bool]]:
    cutoff_timestamp = datetime.datetime.now() - datetime.timedelta(
        seconds=get_properties().bot_maximum_heartbeat_delay)

    def check_if_bot_is_online(heartbeat: Heartbeat) -> bool:
        return heartbeat.heartbeat_timestamp > cutoff_timestamp

    return list(map(lambda hb: (hb, check_if_bot_is_online(hb)), heartbeats))


def __check_if_some_bot_is_offline(bots_with_statuses: List[Tuple[Heartbeat, bool]]) -> bool:
    for _, is_online in bots_with_statuses:
        if not is_online:
            return True
    return False


def __generate_table_delimiter_and_return_fragment_lengths(table_row: str) -> (str, List[int]):
    buffer = "+"
    payload_sizes = map(lambda x: len(x), table_row.split("|"))
    payload_sizes = list(filter(lambda x: x > 0, payload_sizes))
    for payload_size in payload_sizes:
        buffer += "-" * payload_size
        buffer += "+"
    return buffer, payload_sizes


def __format_word_to_fit_gap(word: str, gap_width: int) -> str:
    spaces_before_word = math.floor((gap_width - len(word)) / 2)
    spaces_after_word = math.ceil((gap_width - len(word)) / 2)
    return " " * spaces_before_word + word + " " * spaces_after_word


def __print_header(table_delimiter: str, payload_sizes: List[int]) -> None:
    print("+" + "-" * (len(table_delimiter) - 2) + "+")
    print("|" + __format_word_to_fit_gap("Bot Heartbeat Statistics", len(table_delimiter) - 2) + "|")
    print(table_delimiter)
    payload = "|" + __format_word_to_fit_gap("Bot ID", payload_sizes[0])
    payload += "|" + __format_word_to_fit_gap("Last Heartbeat", payload_sizes[1])
    payload += "|" + __format_word_to_fit_gap("Status", payload_sizes[2]) + "|"
    print(payload)
    print(table_delimiter)


def __get_correct_version_of_online(is_some_heartbeat_offline: bool) -> str:
    return "ONLINE " if is_some_heartbeat_offline else "ONLINE"


def __map_to_table_row(heartbeat: Heartbeat, is_bot_online: bool, is_some_bot_offline: bool) -> str:
    formatted_timestamp = heartbeat.heartbeat_timestamp.strftime("%d.%m.%Y %H:%M:%S")
    status = __get_correct_version_of_online(
        is_some_bot_offline) if is_bot_online else "OFFLINE"
    return f'| {heartbeat.bot_id} | {formatted_timestamp} | {status} |'


def __print_heartbeat_status(heartbeats: List[Heartbeat]) -> None:
    if not heartbeats:
        print("No heartbeats found")
        return
    heartbeats.sort(key=lambda hb: hb.heartbeat_timestamp, reverse=True)
    heartbeats_with_statuses = __mark_heartbeats_with_bot_status(heartbeats)
    is_some_bot_offline = __check_if_some_bot_is_offline(heartbeats_with_statuses)
    heartbeats_as_table_lines = []
    for heartbeat, online in heartbeats_with_statuses:
        heartbeats_as_table_lines.append(__map_to_table_row(heartbeat, online, is_some_bot_offline))

    table_delimiter, payload_sizes = __generate_table_delimiter_and_return_fragment_lengths(
        max(heartbeats_as_table_lines))
    __print_header(table_delimiter, payload_sizes)
    for heartbeat_line in heartbeats_as_table_lines:
        print(heartbeat_line)
        print(table_delimiter)


def __download_heartbeats_periodically() -> None:
    while is_running():
        downloaded_heartbeats = download_heartbeats()
        bots_ids = list(map(lambda heartbeat: heartbeat.bot_id, downloaded_heartbeats))
        update_online_bots(bots_ids)
        __print_heartbeat_status(downloaded_heartbeats)
        time.sleep(get_properties().heartbeat_fetch_period)


def start_heartbeat_fetcher_job() -> threading.Thread:
    thread = threading.Thread(target=__download_heartbeats_periodically)
    thread.start()
    return thread
