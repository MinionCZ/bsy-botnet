from common.data.heartbeat import Heartbeat
from common.dropbox_wrapper import upload_file, DropboxFolders
from common.image_generators.image_generator import generate_image
from common.steganography import insert_heartbeat_into_image
from common.utils.string_utils import generate_unique_image_name
from slave.src.data.properties import get_properties

__IMAGE_HORIZONTAL_DIMENSION = 640
__IMAGE_VERTICAL_DIMENSION = 480


def upload_heartbeat(heartbeat: Heartbeat) -> None:
    heartbeat_image = generate_image(__IMAGE_HORIZONTAL_DIMENSION, __IMAGE_VERTICAL_DIMENSION)
    image_with_heartbeat = insert_heartbeat_into_image(heartbeat_image, heartbeat)
    heartbeat_name = generate_unique_image_name(get_properties().image_generator_mode)
    upload_file(DropboxFolders.BOT_HEARTBEATS, heartbeat_name, image_with_heartbeat)
