from typing import Set
from common.dropbox_wrapper import init_dropbox, list_files, DropboxFolders, create_folder


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
