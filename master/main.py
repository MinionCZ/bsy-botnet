from common.fractal_image_generator import generate_fractal_image
from common.random_image_generator import generate_random_image


def main():
    generate_fractal_image(640, 480)
    generate_random_image(640, 480)

if __name__ == '__main__':
    main()


