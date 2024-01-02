from datetime import datetime

from common.image_generators.image_generator_mode import ImageGeneratorMode
from master.src.dataclasses.properties import get_properties


def generate_unique_image_name() -> str:
    actual_date = datetime.now().isoformat()
    if get_properties().image_generator_mode == ImageGeneratorMode.RANDOM:
        return "modern_art-" + actual_date + ".png"
    elif get_properties().image_generator_mode == ImageGeneratorMode.FRACTAL:
        return "really_interesting_fractal-" + actual_date + ".png"
