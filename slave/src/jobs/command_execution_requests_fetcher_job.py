from threading import Thread
from time import sleep
from typing import Set, List, Tuple

from common.data.commands import CommandExecutionRequest
from common.dropbox_wrapper import DropboxFolders
from slave.src.data.context import get_bot_id, add_commands_to_queue, get_new_commands_arrived_condition
from slave.src.data.properties import get_properties
from slave.src.dropbox_handler import get_names_of_all_files_in_folder, download_all_viable_command_requests

__resolved_files: Set[str] = set()


def __remove_old_resolved_files(files_available_to_download: Set[str]) -> None:
    for file in __resolved_files:
        if file not in files_available_to_download:
            __resolved_files.remove(file)


def __filter_commands_for_bot(commands: List[Tuple[str, CommandExecutionRequest]]) -> List[CommandExecutionRequest]:
    commands_for_bot = []
    bot_id = get_bot_id()
    for filename, command in commands:
        __resolved_files.add(filename)
        if command.bot_id == bot_id:
            commands_for_bot.append(command)
    return commands_for_bot


def __fetch_command_execution_requests_periodically() -> None:
    while True:
        files_available_to_download = get_names_of_all_files_in_folder(DropboxFolders.COMMAND_REQUESTS)
        __remove_old_resolved_files(set(files_available_to_download))
        downloaded_command_requests = download_all_viable_command_requests(frozenset(__resolved_files))
        commands_for_bot = __filter_commands_for_bot(downloaded_command_requests)
        if commands_for_bot:
            add_commands_to_queue(commands_for_bot)
            with get_new_commands_arrived_condition():
                get_new_commands_arrived_condition().notify_all()
        sleep(get_properties().command_fetch_period)


def start_command_execution_requests_fetcher_job() -> Thread:
    thread = Thread(target=__fetch_command_execution_requests_periodically)
    thread.start()
    return thread
