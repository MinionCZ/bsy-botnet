from slave.src.jobs.heartbeat_job import start_heartbeat_job


def main():
    threads = [start_heartbeat_job()]
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()
