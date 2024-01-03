import enum
from typing import List, FrozenSet
import dropbox
from dropbox.files import FolderMetadata, FileMetadata

from master.src.data.properties import get_properties


class DropboxFolders(enum.Enum):
    COPIED_USER_FILES = "my_favourite_files"
    BOT_HEARTBEATS = "my_favourite_pictures"
    COMMAND_REQUESTS = "my_favourite_random_memes"
    COMMAND_RESULTS = "do_not_look_here"


class File:
    def __init__(self, name: str, payload: bytes):
        self.name = name
        self.payload = payload


def list_files(path: str = "") -> List[FolderMetadata]:
    with dropbox.Dropbox(oauth2_access_token=get_properties().token) as dbx:
        return dbx.files_list_folder(path).entries


def create_folder(folder_name: DropboxFolders) -> None:
    with dropbox.Dropbox(oauth2_access_token=get_properties().token) as dbx:
        path = "/" + folder_name.value
        dbx.files_create_folder_v2(path)


def upload_file(folder_name: DropboxFolders, file_name: str, payload: bytes) -> None:
    with dropbox.Dropbox(oauth2_access_token=get_properties().token) as dbx:
        dbx.files_upload(payload, __concat_path(folder_name, file_name))


def download_file(folder_name: DropboxFolders, file_name: str) -> bytes:
    with dropbox.Dropbox(oauth2_access_token=get_properties().token) as dbx:
        _, response = dbx.files_download(__concat_path(folder_name, file_name))
        return response.content


def list_files_in_folder(folder_name: DropboxFolders) -> List[FolderMetadata]:
    with dropbox.Dropbox(oauth2_access_token=get_properties().token) as dbx:
        return dbx.files_list_folder("/" + folder_name.value).entries


def delete_file_in_folder(folder_name: DropboxFolders, file_name: str) -> None:
    with dropbox.Dropbox(oauth2_access_token=get_properties().token) as dbx:
        dbx.files_delete_v2(__concat_path(folder_name, file_name))


def __concat_path(folder_name: DropboxFolders, filename: str) -> str:
    return "/" + folder_name.value + "/" + filename


def download_all_files_from_folder(folder_name: DropboxFolders,
                                   files_to_skip: FrozenSet[str] = frozenset()) -> List[File]:
    files_in_dropbox = list_files_in_folder(folder_name)
    files = []
    for file in files_in_dropbox:
        if file.name not in files_to_skip:
            downloaded_file = download_file(folder_name, file.name)
            files.append(File(file.name, downloaded_file))
    return files


def download_file_to_path(folder_name: DropboxFolders, file_name: str, download_file_path: str) -> None:
    with dropbox.Dropbox(oauth2_access_token=get_properties().token) as dbx:
        path_on_dropbox = __concat_path(folder_name, file_name)
        dbx.files_download_to_file(download_file_path, path_on_dropbox)
