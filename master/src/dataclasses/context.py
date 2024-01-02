import copy
import threading
import uuid
from typing import List

__lock = threading.Lock()
__online_bots: List[uuid.UUID] = []


def update_online_bots(online_bots: List[uuid.UUID]) -> None:
    with __lock:
        global __online_bots
        __online_bots = copy.deepcopy(online_bots)


def get_online_bots() -> List[uuid.UUID]:
    with __lock:
        return copy.deepcopy(__online_bots)
