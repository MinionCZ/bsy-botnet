import uuid

from common.dataclasses.commands import CommandExecutionRequest, CommandType

from master.src.dropbox_handler import init_dropbox_handler, upload_command_to_dropbox


def main():
    init_dropbox_handler()
    upload_command_to_dropbox(CommandExecutionRequest(command=CommandType.W, bot_id=uuid.uuid4(), param=""))


if __name__ == '__main__':
    main()
