import enum
from typing import List
import dropbox
from dropbox.files import FolderMetadata

__token = ""


class DropboxFolder(enum.Enum):
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


def create_folder(folder_name: DropboxFolder) -> None:
    with dropbox.Dropbox(oauth2_access_token=__token) as dbx:
        dbx.files_create_folder_v2(folder_name.value)


def upload_file(folder_name: DropboxFolder, file_name: str, payload: bytes) -> None:
    with dropbox.Dropbox(oauth2_access_token=__token) as dbx:
        path = folder_name.value + "/" + file_name
        dbx.files_upload(payload, path)


def download_file(folder_name: DropboxFolder, file_name: str) -> bytes:
    with dropbox.Dropbox(oauth2_access_token=__token) as dbx:
        path = folder_name.value + "/" + file_name
        return dbx.files_download(path)


def list_files_in_folder(folder_name: DropboxFolder) -> List[FolderMetadata]:
    with dropbox.Dropbox(oauth2_access_token=__token) as dbx:
        return dbx.files_list_folder(folder_name.value).entries
