import math
import threading
import time
from typing import List

from common.dataclasses.heartbeat import Heartbeat
from master.src.dataclasses.context import is_running
from master.src.dataclasses.properties import get_properties
from master.src.dropbox_handler import download_heartbeats


def __is_some_heartbeat_offline(heartbeats: List[Heartbeat]) -> bool:
    for heartbeat in heartbeats:
        if not heartbeat.is_online():
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


def __print_heartbeat_status(heartbeats: List[Heartbeat]) -> None:
    if not heartbeats:
        print("No heartbeats found")
        return
    heartbeats.sort(key=lambda heartbeat: heartbeat.heartbeat_timestamp, reverse=True)
    is_some_heartbeat_offline = __is_some_heartbeat_offline(heartbeats)
    heartbeats_as_table_lines = list(

        map(lambda heartbeat: heartbeat.map_to_table_row(is_some_heartbeat_offline), heartbeats))

    table_delimiter, payload_sizes = __generate_table_delimiter_and_return_fragment_lengths(
        max(heartbeats_as_table_lines))
    __print_header(table_delimiter, payload_sizes)
    for heartbeat_line in heartbeats_as_table_lines:
        print(heartbeat_line)
        print(table_delimiter)


def __download_heartbeats_periodically() -> None:
    while is_running():
        __print_heartbeat_status(download_heartbeats())
        time.sleep(get_properties().heartbeat_fetch_period)


def start_heartbeat_fetcher_job() -> threading.Thread:
    thread = threading.Thread(target=__download_heartbeats_periodically)
    thread.start()
    return thread
