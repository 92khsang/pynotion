from importlib import import_module
from typing import Any, Optional

from .base_model import BaseNotionModel

__all__ = [
    "get_value_for_discriminator",
    "discriminate_field",
]


def get_value_for_discriminator(values, key: str):
    if isinstance(values, dict):
        return values.get(key, None)
    else:
        return getattr(values, key, None)


def discriminate_field(
    value: Optional[dict | BaseNotionModel],
    discriminator: str,
    class_name_map: dict[str, str],
) -> Any:
    if isinstance(value, dict) or isinstance(value, BaseNotionModel):
        discriminator_value = get_value_for_discriminator(value, discriminator)

        if discriminator_value not in class_name_map:
            raise ValueError(f"Unknown {discriminator}: {discriminator_value}")

        module = import_module("pynotion.models")
        clz = getattr(module, class_name_map[discriminator_value])

        return clz.model_validate(value)

    raise ValueError(f"Expected dict or BaseNotionModel, got {type(value)}")
