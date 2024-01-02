from master.src.dropbox_handler import init_dropbox_handler
from master.src.jobs.command_results_fetcher_job import start_command_results_fetcher_job
from master.src.jobs.heartbeat_fetcher_job import start_heartbeat_fetcher_job


def main():
    init_dropbox_handler()
    threads = [start_command_results_fetcher_job(), start_heartbeat_fetcher_job()]


if __name__ == '__main__':
    main()
