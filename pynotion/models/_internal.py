from __future__ import annotations as _annotations

from abc import ABC
from collections import OrderedDict
from datetime import datetime
from enum import StrEnum
from typing import (
    TypeAlias,
    Any,
    get_args,
    Literal,
    Type,
    get_origin,
)
from uuid import UUID

from pydantic import (
    model_validator,
    model_serializer,
    ConfigDict,
    UUID4,
    BaseModel,
    PrivateAttr,
    Field,
)
from pydantic_core import ArgsKwargs, PydanticUndefined

# Type aliases
NotionType: TypeAlias = StrEnum


def create_read_only_alias(field_name: str) -> str:
    """Generates alias by removing 'read_only_' prefix if present."""
    return field_name.removeprefix("read_only_")


def remove_read_only_prefix(field_name: str) -> str:
    """Removes 'read_only_' prefix if present."""
    return field_name.removeprefix("read_only_")


class BaseNotionModel(BaseModel, ABC):
    """Base class for Notion-like models with special read-only field handling."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        validate_default=True,
        populate_by_name=True,
        alias_generator=create_read_only_alias,
    )

    # Class variable for serializable private attributes
    __serializable_private_attrs__: dict = {}

    def __new__(cls, *args, **kwargs):
        if cls is BaseNotionModel:
            raise TypeError(f"{cls.__name__} cannot be instantiated directly")
        return super().__new__(cls)

    @staticmethod
    def _remove_read_only_prefix(data: dict) -> OrderedDict:
        """Transforms field names by removing 'read_only_' prefix."""
        new_data = OrderedDict()
        for k, v in data.items():
            new_data[remove_read_only_prefix(k)] = v
        return new_data

    @classmethod
    def _collect_all_annotation(cls) -> dict:
        """Returns a list of all annotations for the class."""
        all_annotations = {}
        for clz in reversed(cls.__mro__):
            if hasattr(clz, '__annotations__'):
                all_annotations.update(clz.__annotations__)

        return all_annotations

    @model_serializer(mode="wrap")
    def serialize_model(self, nxt) -> OrderedDict:
        """Ensures private attributes are included and field order is preserved."""
        data = nxt(self)

        # Get private attributes that should be serialized
        private_attrs = {
            attr: getattr(self, attr)
            for attr in self.__serializable_private_attrs__
            if attr in self.__private_attributes__
        }

        # Maintain field declaration order
        all_annotations = self._collect_all_annotation()

        # Use the collected fields for ordering
        declared_fields = list(all_annotations.keys())
        ordered_data = OrderedDict()

        # Process fields in their declaration order
        for field in declared_fields:
            if field in private_attrs:
                alias = self.__serializable_private_attrs__[field]
                ordered_data[alias] = private_attrs.pop(field)
            elif field in data:
                ordered_data[field] = data[field]
            else:
                no_prefix_field = remove_read_only_prefix(field)
                if no_prefix_field in data:
                    ordered_data[field] = data[no_prefix_field]

        # Add any remaining private attributes
        ordered_data.update(
            {
                self.__serializable_private_attrs__[k]: v
                for k, v in private_attrs.items()
                if k not in ordered_data
            }
        )

        return self._remove_read_only_prefix(ordered_data)


def validate_uuid4(value: UUID | str | bytes | int) -> UUID:
    """
    Converts various types to a UUID4-compatible value.
    """
    if isinstance(value, UUID):
        return UUID4(value.hex)
    if isinstance(value, str):
        return UUID4(value)
    if isinstance(value, bytes):
        return UUID4(UUID(bytes=value).hex)
    if isinstance(value, int):
        return UUID4(UUID(int=value).hex)
    raise ValueError(f"Cannot convert {type(value)} to UUID4")


def validate_enum(
    value: str | NotionType, enum_types: tuple[Type[NotionType], ...]
) -> NotionType:
    """
    Convert a string value to one of the provided StrEnum types.

    - If value is already an instance of a provided enum, return it.
    - If value is a string, attempt to convert it to one of the provided enums.
    - Raise ValueError if the string doesn't match any enum member.
    """
    if any(isinstance(value, enum_type) for enum_type in enum_types):
        return value

    for enum_type in enum_types:
        try:
            return enum_type(value)
        except ValueError:
            continue

    valid_values = [item.value for enum_type in enum_types for item in enum_type]
    raise ValueError(f"Invalid value '{value}'. Expected one of: {valid_values}")


def validate_enum_value(
    actual_val: str | NotionType, expected_values: set[NotionType]
) -> NotionType:
    """
    Validates that 'actual_val' matches one of the NotionTypes in 'expected_values'.
    If 'actual_val' is a string, attempts to convert it via 'validate_enum'.
    """
    if isinstance(actual_val, str):
        actual_val = validate_enum(
            actual_val, tuple([type(ev) for ev in expected_values])
        )

    if actual_val not in expected_values:
        raise ValueError(f"Invalid value '{actual_val}'. Expected '{expected_values}'")

    return actual_val


def validate_timezone(value: str) -> str:
    """
    Validates that the given timezone string is a valid IANA timezone.
    """
    from zoneinfo import available_timezones

    if value not in available_timezones():
        raise ValueError(f"Invalid IANA timezone: {value}")
    return value


def validate_datetime(value: str | datetime) -> datetime:
    """
    Validates and converts a given value to a datetime object.
    Accepts a string in ISO 8601 format or a datetime object.
    """
    if isinstance(value, datetime):
        return value
    elif isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError(f"Invalid ISO 8601 format: {value}")
    raise ValueError(f"Expected str or datetime, got {type(value).__name__}")


def validate_url(url: str) -> str:
    """
    Validates and returns a given URL. Only 'http' or 'https' schemes are allowed.
    """
    if not url:
        raise ValueError("URL can't be None or empty")

    from urllib.parse import urlparse

    parsed = urlparse(url)
    if parsed.scheme not in ['http', 'https']:
        raise ValueError(
            f"Invalid URL scheme. Only http and https are allowed. Got: {parsed.scheme}"
        )
    if not parsed.netloc:
        raise ValueError("URL must contain a valid domain")

    return url


class TypeObjectModel(BaseNotionModel, ABC):

    __type_object_map__: dict[NotionType, Type | set[Type]] = {}
    __type_field_set__ = ("type", "type_object")

    def __new__(cls, *args, **kwargs):
        if cls is TypeObjectModel:
            raise TypeError(f"{cls.__name__} cannot be instantiated directly")
        return super().__new__(cls)

    @classmethod
    def _validate_type_object_map(cls):
        if not cls.__type_object_map__:
            raise ValueError(f"TypeObjectModel is not registered with any Notion types")

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

    @classmethod
    def _get_type_field(cls) -> str:
        return cls.__type_field_set__[0]

    @classmethod
    def _get_type_object_field(cls) -> str:
        return cls.__type_field_set__[1]

    @staticmethod
    def _extract_kwargs(values: Any) -> dict | None:
        """Extracts keyword arguments from input values."""
        if isinstance(values, dict):
            return values
        elif isinstance(values, ArgsKwargs):
            return values.kwargs
        return None

    @model_validator(mode="before")
    @classmethod
    def _pre_init(cls, values: Any) -> Any:
        """Pre-processes input values to handle type and type_object fields."""
        data = cls._extract_kwargs(values)
        if not data:
            return values

            # Find type value
        type_value = None
        type_field_name = None
        for field in {cls._get_type_field(), "type"}:
            if field in data:
                type_field_name = field
                type_value = data[field]
                break

        if type_value is not None:
            # Validate type
            type_value = validate_enum_value(
                type_value, set(cls.__type_object_map__.keys())
            )

            # Handle type_object from a type-specific field
            if cls._get_type_object_field() not in data:
                type_str = str(type_value)
                if type_str in data:
                    data[cls._get_type_object_field()] = data.pop(type_str)

                    # Update type field
            data.pop(type_field_name)
            data[cls._get_type_field()] = type_value

        return values

    @classmethod
    def _check_notion_type_registration(cls, notion_type: NotionType) -> None:
        """Checks that a type is registered in the type-object map."""
        if notion_type not in cls.__type_object_map__:
            raise ValueError(f"Type '{notion_type}' is not registered")

    @classmethod
    def _convert_type_object(cls, notion_type: NotionType, type_object: Any) -> Any:
        """Converts a type object to the right class based on the notion type."""
        cls._check_notion_type_registration(notion_type)
        type_classes = cls.__type_object_map__[notion_type]

        if not isinstance(type_classes, set):
            type_classes = {type_classes}

        for type_class in type_classes:
            # Handle Literal types
            if get_origin(type_class) is Literal:
                if type_object in get_args(type_class):
                    return type_object
                continue

            # Object is already of the right type
            if type(type_object) is type_class:
                return type_object

            # Try to convert dict to object
            if isinstance(type_object, dict):
                try:
                    return type_class(**type_object)
                except TypeError:
                    continue

        raise ValueError(
            f"Failed to convert type_object: '{type_object}' for type '{notion_type}'"
        )

    @model_validator(mode="after")
    def _validate_model(self) -> TypeObjectModel:
        """Validates type and type_object consistency after initialization."""
        _type = getattr(self, self._get_type_field(), None)
        _type_object = getattr(self, self._get_type_object_field(), None)

        if _type is None and _type_object is not None:
            raise ValueError("type_object must be None when type is None")

        if _type and _type_object:
            object.__setattr__(
                self,
                self._get_type_object_field(),
                self._convert_type_object(_type, _type_object),
            )
        return self

    @model_serializer(mode="wrap")
    def serialize_model(self, nxt) -> dict:
        """Customizes serialization to transform type_object to type-specific field."""
        data: OrderedDict = super().serialize_model(nxt)
        type_field = remove_read_only_prefix(self._get_type_field())
        type_object_field = remove_read_only_prefix(self._get_type_object_field())

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


class ReadOnlyTypeObjectModel(TypeObjectModel, ABC):
    """Type object model with read-only type fields."""

    __type_field_set__ = ("read_only_type", "read_only_type_object")

    read_only_type: str | NotionType | None = Field(default=None, frozen=True)
    read_only_type_object: Any | None = Field(default=None, frozen=True)

    def __new__(cls, *args, **kwargs):
        if cls is ReadOnlyTypeObjectModel:
            raise TypeError(f"{cls.__name__} cannot be instantiated directly")
        return super().__new__(cls)

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs):
        cls._validate_type_object_map()

        super().__pydantic_init_subclass__(**kwargs)

    @property
    def type(self) -> NotionType:
        """Accessor for read_only_type."""
        return self.read_only_type

    @property
    def type_object(self) -> Any | None:
        """Accessor for read_only_type_object."""
        return self.read_only_type_object


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
