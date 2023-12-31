from common.image_generators.fractal_image_generator import generate_fractal_image
from common.image_generators.random_image_generator import generate_random_image
from common.steganography import hide_message_to_image, decode_message_from_image


def main():
    fractal_image = generate_fractal_image(640, 480)
    rnd_image = generate_random_image(640, 480)
    hidden_image = hide_message_to_image("Hello World!", fractal_image)



if __name__ == '__main__':
    main()


