from __future__ import annotations as _annotations

import types
from datetime import datetime
from enum import StrEnum
from typing import (
    Union,
    TypeAlias,
    Any,
    TYPE_CHECKING,
    Annotated,
    Optional,
    get_args,
    Literal,
    Type,
    Iterable,
    get_type_hints,
    get_origin,
)

from pydantic import (
    BaseModel,
    model_validator,
    model_serializer,
    field_validator,
    ConfigDict,
)

NotionType: TypeAlias = StrEnum


class NotionBaseModel(BaseModel):
    """A base class for Notion-like models."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True)


def validate_enum(
    value: str | NotionType, enum_types: tuple[Type[NotionType], ...]
) -> NotionType:
    """
    Convert a string value to one of the provided StrEnum types.

    - If `value` is already an instance of one of the provided enums, return it.
    - If `value` is a string, attempt to convert it to one of the provided enums.
    - Raise a `ValueError` if the string doesn't match any enum member.
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


def validate_timezone(value: str) -> str:
    """
    Validates that the given timezone string is a valid IANA timezone.

    Args:
        value: The timezone string to validate.

    Returns:
        The input value if it is a valid IANA timezone.

    Raises:
        ValueError: If the input value is not a valid IANA timezone.
    """
    from zoneinfo import available_timezones

    if value not in available_timezones():
        raise ValueError(f"Invalid IANA timezone: {value}")
    return value


def validate_datetime(value: str | datetime) -> datetime:
    """
    Validates and converts a given value to a datetime object.

    Args:
        value: A string in ISO 8601 format or a datetime object.

    Returns:
        A datetime object representing the input value.

    Raises:
        ValueError: If the input string isn't in a valid ISO 8601 format.
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
    Validates and returns a given URL.

    Args:
        url: The URL to validate.

    Returns:
        The input URL if it's valid.

    Raises:
        ValueError: If the input URL is invalid.
    """
    if not url:
        raise ValueError("URL can't be None or empty")

    try:
        from urllib.parse import urlparse

        parsed = urlparse(url)

        if parsed.scheme not in ['http', 'https']:
            raise ValueError(
                f"Invalid URL scheme. Only http and https are allowed. Got: {parsed.scheme}"
            )

        if not parsed.netloc:
            raise ValueError("URL must contain a valid domain")

        return url

    except ValueError:
        raise


def register_notion_type_enum(cls: type[NotionType]):
    """
    Registers a `NotionType` enum class with the Notion API.

    Args:
        cls: The `NotionType` enum class to register.

    Raises:
        ValueError: If `cls` isn't a subclass of `StrEnum`.

    Returns:
        The registered class.
    """
    if not issubclass(cls, NotionType):
        raise ValueError(f"{cls.__name__} is not a subclass of StrEnum.")

    NotionTypedModel.register_notion_type_enum(cls)
    return cls


def register_type_data(main_type: NotionType, type_data_cls: Optional[type] = None):
    """
    Registers a type data class with the given Notion type.

    If `type_data_cls` is given, it registers the given type data class with the
    given Notion type.

    If `type_data_cls` isn't given, it returns a decorator that registers the
    decorated type data class with the given Notion type.

    Args:
        main_type: The Notion type to register with.
        type_data_cls: The type data class to register.

    Returns:
        If `type_data_cls` is given, the registered type data class.
        If `type_data_cls` isn't given, a decorator that registers the decorated
        type data class.
    """
    if type_data_cls:
        return NotionTypedModel.register_type_data(main_type, type_data_cls)

    def wrapper(cls: type):
        NotionTypedModel.register_type_data(main_type, cls)
        return cls

    return wrapper


class NotionTypedModel(NotionBaseModel):
    """
    A base model for handling Notion-like typed data structures.

    This class provides dynamic registration and validation for Notion type enums
    and their corresponding data classes. It ensures each instance has a valid
    `type` mapped to an appropriate registered `type_data`.

    Attributes:
        type (Optional[NotionType]):
            The Notion type associated with this instance. It must be a registered
            NotionType value.
        type_data (Any):
            The corresponding data for the given Notion type. It must match one of
            the registered data classes for the type.
        __registry__ (dict[type[NotionType], dict[NotionType, list[type]]]):
            A class-level registry that maps NotionType enums to a list of associated
            data classes. The structure is::

                {
                    NotionTypeEnum: {
                        notion_type_value: [TypeDataClass1, TypeDataClass2, ...]
                    }
                }

    Methods:
        _extract_type_hint() -> type:
            Extracts the expected NotionType enum from the class's type hint.

        _convert_to_enum(value: Union[str, NotionType]) -> Optional[NotionType]:
            Converts a given string or NotionType to a registered NotionType enum.

        _check_notion_type_registration(notion_type: NotionType) -> None:
            Ensures the given Notion type is registered.

        _convert_type_data(notion_type: NotionType, type_data: Any) -> Any:
            Converts the given `type_data` to an instance of the appropriate
            registered data class.

        register_notion_type_enum(notion_type_cls: type[NotionType]) -> None:
            Registers a Notion type enum class.

        register_type_data(notion_type: NotionType, type_data_cls: type) -> None:
            Registers a Notion type value with one or more associated data classes.

        validate_type(v: Optional[Union[str, NotionType]]) -> Optional[NotionType]:
            Validates and converts the `type` field, ensuring it corresponds
            to a registered Notion type.

        validate_model() -> NotionTypedModel:
            Ensures that the `type` and `type_data` fields are correctly associated
            and valid.

        serialize_model(nxt) -> dict:
            Custom serializer to ensure `type_data` is properly nested under
            its associated type.

        __getattr__(item: str) -> Any:
            Allows accessing `type_data` using the string representation of
            the `type` attribute.
    """

    __slots__ = ("type", "type_data")

    __registry__: dict[type[NotionType], dict[NotionType, list[type]]] = {}

    type: Optional[NotionType]
    type_data: Any

    if TYPE_CHECKING:
        type: Annotated[Union[str, NotionType, None], ...]

    def __new__(cls, *args, **kwargs):
        if cls is NotionTypedModel:
            raise TypeError(f"{cls.__name__} cannot be instantiated directly")
        return super().__new__(cls)

    def __init__(self, **data):
        """
        Initializes a NotionTypedModel instance.

        If the `type` field is provided and matches a key in `data`, the corresponding
        value is moved to `type_data`.

        Args:
            **data: Keyword arguments representing model fields.

        Raises:
            ValueError: If the provided `type` isn't registered.
        """
        type_value = data.get("type")

        if type_value and not data.get("type_data"):
            type_data = data.pop(str(type_value), None)
            if type_data is not None:
                data["type_data"] = type_data

        super().__init__(**data)

    @classmethod
    def _extract_type_hint(cls) -> type:
        type_field = get_type_hints(cls)["type"]

        if get_origin(type_field) in {Union, types.UnionType}:
            actual_type = [
                t
                for t in get_args(type_field)
                if isinstance(t, type) and issubclass(t, NotionType)
            ][0]
        else:
            actual_type = type_field

        return actual_type

    @classmethod
    def _convert_to_enum(cls, value: str | NotionType) -> NotionType | None:
        type_hint = cls._extract_type_hint()

        if isinstance(value, NotionType):
            result = value
        elif isinstance(value, str):
            if type_hint not in cls.__registry__:
                raise ValueError(f"Type '{type_hint}' is not registered")
            result = type_hint(value)
        else:
            raise ValueError(f"Invalid type: {type(value)} for {type_hint}")
        return result

    @classmethod
    def _check_notion_type_registration(cls, notion_type: NotionType):
        """
        Checks if a given Notion type enum class is registered.

        Args:
            notion_type: The Notion type enum class to check.

        Raises:
            ValueError: If the class isn't registered.
        """
        if type(notion_type) not in cls.__registry__:
            raise ValueError(f"Type '{type(notion_type).__name__}' is not registered")

    @classmethod
    def _convert_type_data(cls, notion_type: NotionType, type_data: Any) -> Any:
        """
        Retrieves the registered data type for a given Notion type.

        Args:
            notion_type: The Notion type to retrieve the data type for.
            type_data: The data to convert.

        Returns:
            The registered data type class.

        Raises:
            ValueError: If no matching data type is found.
        """
        cls._check_notion_type_registration(notion_type)

        type_classes: list[type] = cls.__registry__[type(notion_type)][notion_type]
        for type_class in type_classes:
            try:
                if (
                    hasattr(type_class, '__origin__')
                    and getattr(type_class, '__origin__') is Literal
                ):
                    if type_data not in get_args(type_class):
                        continue
                    else:
                        return type_data
                elif isinstance(type_data, type_class):
                    return type_data
                else:
                    return type_class(**type_data)
            except TypeError:
                continue

        raise ValueError(
            f"Failed to convert type_data: '{type_data}' when type is '{notion_type}'"
        )

    @classmethod
    def register_notion_type_enum(cls, notion_type_cls: type[NotionType]):
        """
        Registers a Notion type enum class.

        Args:
            notion_type_cls: The Notion type enum class to register.
        """
        if notion_type_cls not in cls.__registry__:
            cls.__registry__[notion_type_cls] = {}

    @classmethod
    def register_type_data(cls, notion_type: NotionType, type_data_cls: type):
        """
        Registers a Notion type with its associated data class.

        Args:
            notion_type: The Notion type value.
            type_data_cls: The corresponding data class.
        """
        cls._check_notion_type_registration(notion_type)

        type_classes_registry = cls.__registry__[type(notion_type)]

        prev_types = set(type_classes_registry.get(notion_type, []))
        prev_types.add(type_data_cls)

        type_classes_registry[notion_type] = list(prev_types)

    @field_validator('type', mode='before')  # noqa
    @classmethod
    def validate_type(cls, v: Optional[Union[str, NotionType]]) -> Optional[NotionType]:
        """
        Validates and converts the `type` field.

        Args:
            v: A string or NotionType value.

        Returns:
            The corresponding NotionType value if valid.

        Raises:
            ValueError: If no matching enum value is found.
        """
        enum_val = None

        if v is not None:
            try:
                enum_val = cls._convert_to_enum(v)
                if enum_val is None:
                    raise ValueError(f"No matching StrEnum found for type: {v}")

                cls._check_notion_type_registration(enum_val)
            except ValueError as e:
                raise ValueError(f"Invalid type: {v}", e)

        return enum_val

    @model_validator(mode="after")
    def validate_model(self):
        """
        Ensures the integrity of the `type` and `type_data` fields.

        Raises:
            ValueError: If `type_data` is missing or invalid for the given `type`.
        """
        if self.type is None and self.type_data is not None:
            raise ValueError("type_data must be None when the type is None.")

        if self.type and self.type_data:
            object.__setattr__(
                self, "type_data", self._convert_type_data(self.type, self.type_data)
            )

        return self

    @model_serializer(mode="wrap")
    def serialize_model(self, nxt):
        """
        Custom serialization logic to ensure `type_data` is nested correctly.

        Returns:
            A dictionary representation of the model.
        """
        data = nxt(self)
        type_data = data.pop("type_data", None)
        if type_data is not None:
            data[self.type] = type_data
        return data

    def __getattr__(self, item: str):
        """
        Overrides attribute access to return `type_data`
            when `type` is accessed as an attribute.

        If `type` is "person", then `instance.person` will return `type_data`.

        Args:
            item (str): The attribute name being accessed.

        Returns:
            The value of `type_data`
                if `item` matches `type`, otherwise default behavior.

        Raises:
            AttributeError: If the requested attribute isn't found.
        """
        if item == str(self.type):
            return self.type_data

        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{item}'"
        )

    def __dir__(self):
        base_attrs: Iterable[str] = super().__dir__()
        if self.type:
            return list(base_attrs) + [str(self.type)]
        return base_attrs
