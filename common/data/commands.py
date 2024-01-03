import uuid
from typing import List

from pydantic import BaseModel
import enum


class CommandTypes(enum.Enum):
    LS = "ls"
    ID = "id"
    W = "w"
    COPY = "copy"
    EXEC = "exec"


class CommandStatus(enum.Enum):
    SUCCESS = "success"
    ERROR = "error"


class CommandExecutionRequest(BaseModel):
    bot_id: uuid.UUID
    command: CommandTypes
    param: str


class CommandExecutionResult(BaseModel):
    bot_id: uuid.UUID
    command: CommandTypes
    param: str
    status: CommandStatus
    results: List[str]

    def __format_results(self) -> str:
        return "".join(self.results)

    def __str__(self) -> str:
        if self.status == CommandStatus.SUCCESS:
            return f"Bot with ID: {self.bot_id}, successfully executed command: {self.command.value} {self.param} with results: \n{self.__format_results()}"
        return f"""Bot with ID: {self.bot_id}, executed command: {self.command.value} {self.param} with errors: \n{self.__format_results()}"""
