import uuid
from typing import List

from pydantic import BaseModel
import enum


class CommandType(enum.Enum):
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
    command: CommandType
    param: str


class CommandExecutionResult(BaseModel):
    bot_id: uuid.UUID
    command: CommandType
    param: str
    status: CommandStatus
    results: List[str]

    def __str__(self) -> str:
        if self.status == CommandStatus.SUCCESS:
            return f"""Bot with ID: {self.bot_id}, successfully executed command: {self.command.value} {self.param} with results: {self.results}"""
        return f"""Bot with ID: {self.bot_id}, executed command: {self.command.value} {self.param} with errors: {self.results}"""
