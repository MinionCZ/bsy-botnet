import io

import numpy
from PIL import Image


def generate_random_image(horizontal_size: int, vertical_size: int) -> io.BytesIO:
    imarray = numpy.random.rand(vertical_size, horizontal_size, 3) * 255
    im = Image.fromarray(imarray.astype('uint8')).convert('RGBA')
    buffer = io.BytesIO()
    im.save(buffer, 'png')
    return buffer


