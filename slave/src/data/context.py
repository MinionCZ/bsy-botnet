import copy
import threading
import uuid
from typing import List

from common.data.commands import CommandExecutionRequest

__context_lock = threading.Lock()

__bot_id: uuid.UUID = uuid.uuid4()
__command_queue: List[CommandExecutionRequest] = []
__new_commands_arrived: threading.Condition = threading.Condition()


def add_commands_to_queue(commands: List[CommandExecutionRequest]) -> None:
    with __context_lock:
        global __command_queue
        __command_queue += commands


def get_number_of_commands_inside_queue() -> int:
    with __context_lock:
        global __command_queue
        return len(__command_queue)


def get_commands_from_queue() -> List[CommandExecutionRequest]:
    with __context_lock:
        global __command_queue
        commands = copy.deepcopy(__command_queue)
        __command_queue = []
        return commands


def get_new_commands_arrived_condition() -> threading.Condition:
    global __new_commands_arrived
    return __new_commands_arrived


def get_bot_id() -> uuid.UUID:
    global __bot_id
    return copy.deepcopy(__bot_id)
