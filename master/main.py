import uuid

from common.dataclasses.commands import CommandExecutionRequest, CommandType, CommandExecutionResult
from common.dataclasses.properties import init_properties
from common.image_generators.fractal_image_generator import generate_fractal_image
from common.image_generators.random_image_generator import generate_random_image
from common.steganography import insert_command_request_into_image, read_command_request_from_image, \
    insert_command_result_into_image, read_command_result_from_image
import common.dropbox_wrapper as dw
from master.dropbox_handler import init_dropbox_handler


def main():
    init_properties()
    fractal_image = generate_fractal_image(640, 480)
    rnd_image = generate_random_image(640, 480)
    init_dropbox_handler()


if __name__ == '__main__':
    main()
