import enum
from typing import Dict

__properties: Dict[str, str] = {}


class Properties(enum.Enum):
    TOKEN = "token"
    IMAGE_MODE = "image_mode"


def init_properties() -> None:
    with open("../resources/properties.txt", "r") as properties_file:
        for line in properties_file.readlines():
            split_line = line.replace("\n", "").split("=")
            if len(split_line) != 2:
                raise Exception(f"Unable to parse properties, line {line} is invalid")
            __properties[split_line[0]] = split_line[1]


def get_property(name: Properties) -> str:
    return __properties[name.value]
