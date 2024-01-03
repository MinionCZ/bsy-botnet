from master.src.dropbox_handler import init_dropbox_handler
from master.src.input.input_handler import handle_user_input
from master.src.jobs.command_results_fetcher_job import start_command_results_fetcher_job
from master.src.jobs.heartbeat_fetcher_job import start_heartbeat_fetcher_job


# Need to run as module python -m master.src.main from
def main():
    init_dropbox_handler()
    threads = [start_command_results_fetcher_job(), start_heartbeat_fetcher_job()]
    handle_user_input()
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()
