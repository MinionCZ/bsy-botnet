import copy
import threading
import uuid
from typing import List

__bots_lock = threading.Lock()
__running_lock = threading.Lock()
__online_bots: List[uuid.UUID] = []
__running: bool = True


def update_online_bots(online_bots: List[uuid.UUID]) -> None:
    with __bots_lock:
        global __online_bots
        __online_bots = copy.deepcopy(online_bots)


def get_online_bots() -> List[uuid.UUID]:
    with __bots_lock:
        return copy.deepcopy(__online_bots)


def turn_off_master() -> None:
    global __running
    with __running_lock:
        __running = False


def is_running() -> bool:
    with __running_lock:
        global __running
        return __running
