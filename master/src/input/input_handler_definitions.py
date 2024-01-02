import enum


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


class InputHandlerState:
    def __init__(self):
        self.command: InputCommandTypes | None = None
        self.param: str | None = None
        self.state: InputStates = InputStates.COMMAND_SELECT
