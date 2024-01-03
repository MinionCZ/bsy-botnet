import threading
from time import sleep

from master.src.data.context import is_running
from master.src.data.properties import get_properties
from master.src.dropbox_handler import download_and_delete_command_execution_results_from_dropbox


def __fetch_command_results_periodically() -> None:
    while is_running():
        command_execution_results = download_and_delete_command_execution_results_from_dropbox()
        for command in command_execution_results:
            print(command)
        sleep(get_properties().result_fetch_period)


def start_command_results_fetcher_job() -> threading.Thread:
    thread = threading.Thread(target=__fetch_command_results_periodically)
    thread.start()
    return thread
