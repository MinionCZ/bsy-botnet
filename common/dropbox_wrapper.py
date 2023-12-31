import enum
from typing import List
import dropbox
from dropbox.files import FolderMetadata

__token = ""


class DropboxFolders(enum.Enum):
    COPIED_USER_FILES = "my_favourite_files"
    BOT_HEALTHCHECK = "my_favourite_pictures"
    COMMAND_REQUESTS = "my_favourite_random_memes"
    COMMAND_RESULTS = "do_not_look_here"


def init_dropbox() -> None:
    global __token
    with open("../resources/properties.txt") as props:
        __token = props.readline().split("=")[1]


def list_files(path: str = "") -> List[FolderMetadata]:
    with dropbox.Dropbox(oauth2_access_token=__token) as dbx:
        return dbx.files_list_folder(path).entries


def create_folder(folder_name: DropboxFolders) -> None:
    with dropbox.Dropbox(oauth2_access_token=__token) as dbx:
        path = "/" + folder_name
        dbx.files_create_folder_v2(path)


def upload_file(folder_name: DropboxFolders, file_name: str, payload: bytes) -> None:
    with dropbox.Dropbox(oauth2_access_token=__token) as dbx:
        dbx.files_upload(payload, __concat_path(folder_name, file_name))


def download_file(folder_name: DropboxFolders, file_name: str) -> bytes:
    with dropbox.Dropbox(oauth2_access_token=__token) as dbx:
        return dbx.files_download(__concat_path(folder_name, file_name))


def list_files_in_folder(folder_name: DropboxFolders) -> List[FolderMetadata]:
    with dropbox.Dropbox(oauth2_access_token=__token) as dbx:
        return dbx.files_list_folder(folder_name.value).entries


def __concat_path(folder_name: DropboxFolders, filename: str) -> str:
    return "/" + folder_name.value + "/" + filename
