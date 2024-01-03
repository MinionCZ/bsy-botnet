from slave.src.jobs.command_execution_requests_fetcher_job import start_command_execution_requests_fetcher_job
from slave.src.jobs.command_executor_job import start_executor_job
from slave.src.jobs.heartbeat_job import start_heartbeat_job


def main():
    threads = [start_heartbeat_job(), start_command_execution_requests_fetcher_job(), start_executor_job()]
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()
