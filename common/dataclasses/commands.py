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


class CommandExecutionRequest(BaseModel):
    bot_id: uuid.UUID
    command: CommandType
    param: str


class CommandExecutionResult(BaseModel):
    bot_id: uuid.UUID
    command: CommandType
    param: str
    results: List[str]

    def __str__(self) -> str:
        return f"""Bot with ID: {self.bot_id}, successfully executed command: {self.command.value} {self.param} with results: {self.results}"""
