from __future__ import annotations as _annotations

from abc import ABC
from collections import OrderedDict
from enum import StrEnum
from typing import (
    TypeAlias,
    Any,
    get_args,
    Literal,
    Type,
    get_origin,
)

from pydantic import (
    model_validator,
    model_serializer,
    PrivateAttr,
)
from pydantic_core import ArgsKwargs, PydanticUndefined

from .base_model import BaseNotionModel
from .validate import validate_enum_value

# Type aliases
NotionType: TypeAlias = StrEnum


class TypeObjectRegistry:
    """Manages Notion type-object mappings and ensures validation."""

    __type_object_map__: dict[NotionType, Type | set[Type]] = {}

    @classmethod
    def _validate_type_object_map(cls):
        if not cls.__type_object_map__:
            raise ValueError(f"TypeObjectModel is not registered with any Notion types")

    @classmethod
    def _validate_notion_type(cls, notion_type: NotionType) -> None:
        """Ensure that the given Notion type is registered."""
        if notion_type not in cls.__type_object_map__:
            raise ValueError(f"Type '{notion_type}' is not registered")

    @classmethod
    def _get_registered_types(cls) -> set[NotionType]:
        """Returns all registered Notion types."""
        return set(cls.__type_object_map__.keys())

    @classmethod
    def _get_type_classes(cls, notion_type: NotionType) -> set[Type]:
        """Retrieve the set of classes associated with a Notion type."""
        cls._validate_notion_type(notion_type)
        type_classes = cls.__type_object_map__[notion_type]
        return {type_classes} if not isinstance(type_classes, set) else type_classes


class BaseTypeObjectModel(BaseNotionModel, ABC):
    """Abstract base class for Notion models that involve type-object relationships."""

    __type_field_set__ = ("type", "type_object")

    @classmethod
    def _extract_kwargs(cls, values: Any) -> dict | None:
        """Extracts keyword arguments from input values."""
        return (
            values.kwargs
            if isinstance(values, ArgsKwargs)
            else values if isinstance(values, dict) else None
        )

    @classmethod
    def _get_type_field(cls) -> str:
        return cls.__type_field_set__[0]

    @classmethod
    def _get_type_object_field(cls) -> str:
        return cls.__type_field_set__[1]


class TypeObjectModel(BaseTypeObjectModel, TypeObjectRegistry):
    """Handles type-object validation and transformation."""

    def __new__(cls, *args, **kwargs):
        if cls is TypeObjectModel:
            raise TypeError(f"{cls.__name__} cannot be instantiated directly")
        return super().__new__(cls)

    @classmethod
    def _validate_subclass(cls):
        type_set = {type(t) for t in cls.__type_object_map__}
        if len(type_set) > 1:
            raise ValueError(
                f"TypeObjectModel is registered with multiple Notion types: {type_set}"
            )

        declared_fields = set(cls._collect_all_annotation())
        type_field = cls._get_type_field()
        type_object_field = cls._get_type_object_field()

        missing_fields = [
            f for f in (type_field, type_object_field) if f not in declared_fields
        ]
        if missing_fields:
            raise ValueError(
                f"TypeObjectModel is missing fields: {', '.join(map(repr, missing_fields))}"
            )

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs):
        super().__pydantic_init_subclass__(**kwargs)
        cls._validate_subclass()

    @model_validator(mode="before")
    @classmethod
    def _pre_init(cls, values: Any) -> Any:
        """Pre-process input values to populate type and type_object fields."""
        data = cls._extract_kwargs(values)
        if not data:
            return values

        type_field = cls._get_type_field()
        type_object_field = cls._get_type_object_field()

        type_value = data.get("type") or data.get(type_field)
        if type_value:
            type_value = validate_enum_value(type_value, cls._get_registered_types())
            data[type_field] = type_value
            data.setdefault(type_object_field, data.pop(str(type_value), None))

        return values

    @model_validator(mode="after")
    def _validate_model(self) -> TypeObjectModel:
        """Ensures type and type_object consistency after initialization."""
        type_field = self._get_type_field()
        type_object_field = self._get_type_object_field()

        _type = getattr(self, type_field, None)
        _type_object = getattr(self, type_object_field, None)

        if _type and _type_object:
            object.__setattr__(
                self, type_object_field, self._convert_type_object(_type, _type_object)
            )

        return self

    @classmethod
    def _convert_type_object(cls, notion_type: NotionType, type_object: Any) -> Any:
        """Converts a raw type_object into a registered class instance."""
        type_classes = cls._get_type_classes(notion_type)

        for type_class in type_classes:
            if get_origin(type_class) is Literal and type_object in get_args(
                type_class
            ):
                return type_object
            if type(type_object) is type_class:
                return type_object
            if isinstance(type_object, dict):
                try:
                    return type_class(**type_object)
                except TypeError:
                    continue

        raise ValueError(
            f"Invalid type_object '{type_object}' for type '{notion_type}'"
        )

    @model_serializer(mode="wrap")
    def serialize_model(self, nxt) -> dict:
        """Custom serialization logic."""
        data = OrderedDict(super().serialize_model(nxt))
        type_field = self._get_type_field()
        type_object_field = self._get_type_object_field()

        if type_object_field in data:
            _type = data.get(type_field) or object.__getattribute__(self, type_field)
            if _type:
                new_data = OrderedDict()
                for k, v in data.items():
                    new_key = k if k != type_object_field else str(_type)
                    new_data[new_key] = v
                data = new_data

        return data

    def __getattr__(self, item: str) -> Any:
        """Enables access to type_object via the type name."""
        if self._get_type_field() in self.__dict__:
            type_value = self.__dict__.get(self._get_type_field())
            if type_value and item == str(type_value):
                return self.__dict__[self._get_type_object_field()]

        raise AttributeError(
            f"{type(self).__name__!r} object has no attribute {item!r}"
        )


class FixedTypeObjectModel(TypeObjectModel, ABC):
    """Type object model with a fixed type stored as a private attribute."""

    __type_field_set__ = ("_type", "type_object")
    __serializable_private_attrs__ = {"_type": "type"}

    _type: NotionType = PrivateAttr()
    type_object: Any

    def __new__(cls, *args, **kwargs):
        if cls is FixedTypeObjectModel:
            raise TypeError(f"{cls.__name__} cannot be instantiated directly")
        return super().__new__(cls)

    def __init__(self, /, **data):
        """Initialize with a fixed type."""
        # Get a default type
        default_value = self.__private_attributes__.get("_type").default

        # Extract and validate type
        _type = data.pop("type", None) or default_value
        _type = validate_enum_value(_type, {default_value})

        super().__init__(**data)
        object.__setattr__(self, "_type", _type)

    @classmethod
    def _validate_type_exists(cls) -> None:
        private_attr = cls.__private_attributes__.get("_type")
        if private_attr.default is PydanticUndefined:
            raise ValueError("_type must have a default value")

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs):
        cls._validate_type_object_map()
        cls._validate_type_exists()

        super().__pydantic_init_subclass__(**kwargs)

    @classmethod
    def _get_default_type(cls) -> NotionType:
        return cls.__private_attributes__.get("_type").default

    @model_validator(mode="before")
    @classmethod
    def _pre_init(cls, values: Any) -> Any:
        """Pre-processes input values to handle type and type_object fields."""
        data = cls._extract_kwargs(values)
        if not data:
            return values

        # Handle type_object from a type-specific field
        if "type_object" not in data:
            type_str = str(cls._get_default_type())
            if type_str in data:
                data["type_object"] = data.pop(type_str)

        return values

    def __getattr__(self, item: str) -> Any:
        """Special attribute access for fixed type models."""
        private_attr_default = self._get_default_type()

        if item == "_type":
            return private_attr_default
        elif item == str(private_attr_default):
            return self.type_object

        raise AttributeError(
            f"{type(self).__name__!r} object has no attribute {item!r}"
        )

    @property
    def type(self) -> NotionType:
        """Accessor for the private _type attribute."""
        return self._type
