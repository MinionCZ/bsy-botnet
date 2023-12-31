from datetime import datetime

from common.dataclasses.properties import get_property, Properties


def generate_unique_image_name() -> str:
    actual_date = datetime.now().isoformat()
    if get_property(Properties.IMAGE_MODE) == "random":
        return "modern_art-" + actual_date + ".png"
    elif get_property(Properties.IMAGE_MODE) == "fractal":
        return "really_interesting_fractal-" + actual_date + ".png"
    raise Exception(f"Unknown image mode: {get_property(Properties.IMAGE_MODE)}")


