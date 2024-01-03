from datetime import datetime

import pytz

from common.image_generators.image_generator_mode import ImageGeneratorMode


def generate_unique_image_name(image_generator_mode: ImageGeneratorMode) -> str:
    actual_date = datetime.now(tz=pytz.UTC).timestamp()
    if image_generator_mode == ImageGeneratorMode.RANDOM:
        return f"modern_art-{actual_date}.png"
    elif image_generator_mode == ImageGeneratorMode.FRACTAL:
        return f"really_interesting_fractal-{actual_date}.png"
