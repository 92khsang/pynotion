from importlib import import_module
from typing import Any, Union

from pydantic import BaseModel, Field, TypeAdapter
from typing_extensions import Annotated  # Python 3.10 이상이면 필요 없음


def _import_model(model_name: str) -> type[BaseModel]:
    module = import_module("pynotion.models")
    return getattr(module, model_name)


def _parse_type_string(type_str: str) -> Any:
    """Parses a string like 'A | B' to Union[A, B]"""
    type_names = [name.strip() for name in type_str.split("|")]
    types = tuple(_import_model(name) for name in type_names)

    if len(types) == 1:
        return types[0]
    return Union[types]  # Union[A, B]


def dump_rx(type_str: str, data: dict, *, discriminator: str | None = None) -> Any:
    parsed_type = _parse_type_string(type_str)

    if discriminator:
        parsed_type = Annotated[parsed_type, Field(discriminator=discriminator)]

    return TypeAdapter(parsed_type).validate_python(data)


def dump_tx(model: BaseModel | None) -> dict | None:
    return model.model_dump(mode="json", exclude_none=True) if model else None
