import threading
from time import sleep

from master.src.dataclasses.properties import get_properties
from master.src.dropbox_handler import download_and_delete_command_execution_results_from_dropbox


def __fetch_command_results_periodically() -> None:
    while True:
        command_execution_results = download_and_delete_command_execution_results_from_dropbox()
        for command in command_execution_results:
            print(command)
        sleep(get_properties().result_fetch_period)


def start_command_results_fetcher_job() -> None:
    thread = threading.Thread(target=__fetch_command_results_periodically)
    thread.start()
    thread.join()
