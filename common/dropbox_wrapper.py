import dropbox

__token = ""


def init_dropbox() -> None:
    global __token
    with open("../resources/properties.txt") as props:
        __token = props.readline().split("=")[1]


def list_files():
    with dropbox.Dropbox(oauth2_access_token=__token) as dbx:
        print(dbx.files_list_folder("").entries)
