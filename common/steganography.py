import io

import stegano


def hide_message_to_image(message: str, image: bytes) -> bytes:
    image_with_secret = stegano.lsb.hide(image, message)
    buffer = io.BytesIO()
    image_with_secret.save(buffer, format="PNG")
    return buffer.getbuffer().tobytes()


def decode_message_from_image(image: bytes) -> str:
    return stegano.lsb.reveal(io.BytesIO(image))
