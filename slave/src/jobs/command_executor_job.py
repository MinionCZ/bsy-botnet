from threading import Thread

from slave.src.data.context import get_number_of_commands_inside_queue, get_new_commands_arrived_condition, \
    get_commands_from_queue


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
