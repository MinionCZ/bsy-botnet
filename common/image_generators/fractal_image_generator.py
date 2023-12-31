import io
import random
import numpy
from PIL import Image

__DIVERGING_VALUE = 2.0
__MAX_PIXEL_VALUE = 255


def calculate_pixel_color(x: int,
                          y: int,
                          starting_value: complex,
                          offset: complex,
                          n: int,
                          image_payload: numpy.array) -> None:
    for i in range(n):
        starting_value = starting_value * starting_value + offset
        if abs(starting_value) >= __DIVERGING_VALUE:
            coef = i / n
            red = 9 * (1 - coef) * coef ** 3 * __MAX_PIXEL_VALUE
            green = 15 * (1 - coef) ** 2 * coef ** 2 * __MAX_PIXEL_VALUE
            blue = 8.5 * (1 - coef) ** 3 * coef * __MAX_PIXEL_VALUE
            image_payload[y, x, 0] = red
            image_payload[y, x, 1] = green
            image_payload[y, x, 2] = blue
            return
    image_payload[y, x, 0] = 0
    image_payload[y, x, 1] = 0
    image_payload[y, x, 2] = 0


def generate_fractal_image(horizontal_size: int, vertical_size: int) -> io.BytesIO:
    n = random.randint(10, 30)
    image_payload = numpy.zeros((vertical_size, horizontal_size, 3), dtype="uint8")
    offset = complex(random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0))
    starting_value = complex(random.uniform(-2.0, 0.0), random.uniform(-2.0, 0.0))
    ending_value = complex(random.uniform(0.0, 2.0), random.uniform(0.0, 2.0))
    x_step = abs(starting_value.real - ending_value.real) / horizontal_size
    i_step = abs(starting_value.imag - ending_value.imag) / vertical_size
    for x in range(horizontal_size):
        for i in range(vertical_size):
            calculation_starting_point = starting_value + complex(x * x_step, i * i_step)
            calculate_pixel_color(x, i, calculation_starting_point, offset, n, image_payload)
    i = Image.fromarray(numpy.asarray(image_payload)).convert("RGBA")
    output_stream = io.BytesIO()
    i.save(output_stream, "png")
    return output_stream
