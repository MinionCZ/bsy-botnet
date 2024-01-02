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

