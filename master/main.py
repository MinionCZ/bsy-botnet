import uuid

from common.dataclasses.commands import CommandExecutionRequest, CommandType, CommandExecutionResult
from common.dataclasses.properties import init_properties
from common.image_generators.fractal_image_generator import generate_fractal_image
from common.image_generators.random_image_generator import generate_random_image
from master.dropbox_handler import init_dropbox_handler, upload_command_to_dropbox


def main():
    init_properties()
    fractal_image = generate_fractal_image(640, 480)
    rnd_image = generate_random_image(640, 480)
    init_dropbox_handler()
    upload_command_to_dropbox(CommandExecutionRequest(command=CommandType.W, bot_id=uuid.uuid4(), param=""))


if __name__ == '__main__':
    main()
