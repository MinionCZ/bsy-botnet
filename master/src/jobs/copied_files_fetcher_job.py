import threading
from time import sleep

from master.src.data.context import is_running
from master.src.data.properties import get_properties
from master.src.dropbox_handler import download_copied_files_from_dropbox


def __fetch_command_results_periodically() -> None:
    while is_running():
        downloaded_files = download_copied_files_from_dropbox()
        if downloaded_files:
            print("These requested user files were downloaded:")
            for file in downloaded_files:
                print(f"- {file}")
        sleep(get_properties().copied_files_fetch_interval)


def start_copied_files_fetcher_job() -> threading.Thread:
    thread = threading.Thread(target=__fetch_command_results_periodically)
    thread.start()
    return thread
