import enum

from pydantic import BaseModel, field_validator

from common.image_generators.image_generator_mode import ImageGeneratorMode

__properties: "Properties | None" = None


class Properties(BaseModel):
    token: str
    image_generator_mode: ImageGeneratorMode
    result_fetch_period: int
    heartbeat_fetch_period: int
    bot_maximum_heartbeat_delay: int
    copied_files_fetch_interval: int

    @classmethod
    @field_validator("result_fetch_period",
                     "heartbeat_fetch_period",
                     "bot_maximum_heartbeat_delay",
                     "copied_files_fetch_interval")
    def must_be_positive_value(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("Value must not be less than 0")
        return value


def __init_properties() -> Properties:
    with open("./master/resources/properties.json", "r") as properties_file:
        input_json = "".join(properties_file.readlines())
        return Properties.model_validate_json(input_json)


def get_properties() -> Properties:
    global __properties
    if not __properties:
        __properties = __init_properties()
    return __properties
