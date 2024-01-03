import threading
import uuid
from typing import List

from common.data.commands import CommandExecutionRequest

__context: "Context | None" = None
__context_lock = threading.Lock()


class Context:
    def __init__(self):
        self.bot_id: uuid.UUID = uuid.uuid4()
        self.command_queue: List[CommandExecutionRequest] = []


def add_commands_to_queue(commands: List[CommandExecutionRequest]) -> None:
    with __context_lock:
        __context.command_queue += commands


def get_number_of_commands_inside_queue() -> int:
    with __context_lock:
        return len(__context.command_queue)


def get_commands_from_queue() -> List[CommandExecutionRequest]:
    with __context_lock:
        commands = __context.command_queue
        __context.command_queue = []
        return commands
