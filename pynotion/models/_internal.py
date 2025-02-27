from __future__ import annotations as _annotations

from datetime import datetime
from enum import StrEnum
from typing import (
    Union,
    TypeAlias,
    Any,
    TYPE_CHECKING,
    Annotated,
    Optional,
    overload,
    get_args,
    Literal,
)

from pydantic import (
    BaseModel,
    model_validator,
    model_serializer,
    field_validator,
)

NotionType: TypeAlias = StrEnum


class NotionBaseModel(BaseModel):
    """A base class for Notion-like models."""

    class Config:
        extra = "forbid"


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


@overload
def register_type_data(notion_type: NotionType, type_data_cls: type): ...


@overload
def register_type_data(notion_type: NotionType): ...


def register_type_data(notion_type: NotionType, type_data_cls: Optional[type] = None):
    """
    Registers a type data class with the given Notion type.

    If `type_data_cls` is given, it registers the given type data class with the
    given Notion type.

    If `type_data_cls` isn't given, it returns a decorator that registers the
    decorated type data class with the given Notion type.

    Args:
        notion_type: The Notion type to register with.
        type_data_cls: The type data class to register.

    Returns:
        If `type_data_cls` is given, the registered type data class.
        If `type_data_cls` isn't given, a decorator that registers the decorated
        type data class.
    """
    if type_data_cls:
        return NotionTypedModel.register_type_data(notion_type, type_data_cls)

    def wrapper(cls: type):
        NotionTypedModel.register_type_data(notion_type, cls)
        return cls

    return wrapper


class NotionTypedModel(NotionBaseModel):
    """
    A base model for handling Notion-like typed data structures.

    This class supports dynamic registration and validation of Notion type enums and their
    corresponding data classes. It ensures that each instance has a valid `type` associated
    with a registered `type_data`.

    Attributes
        __slots__ (tuple):
            Defines `("type", "type_data")` to limit memory usage and prevent
            accidental attribute assignment.
        __registry__ (dict):
            A class-level registry that maps NotionType enums to their associated
            data classes. Structure:
            ```python
            {
                NotionTypeEnum: {"enum_value": TypeDataClass}
            }
            ```
        type (Optional[StrEnum]):
            The Notion type associated with this instance. Must be a registered `StrEnum` value.
        type_data (Any):
            The corresponding data for the given Notion type. Must match the registered
            data type for the given `type`.

    Methods
        _check_notion_type_registration(notion_type_cls):
            Ensures that the given Notion type enum class is registered.

        _get_registered_data_type(notion_type):
            Retrieves the registered data type for a given Notion type.

        register_notion_type_enum(notion_type_cls):
            Registers a Notion type enum class.

        register_type_data(notion_type, type_data_cls):
            Registers a specific Notion type with an associated data class.

        validate_type(v):
            Validates the `type` field to ensure it corresponds to a registered Notion type.

        validate_model():
            Ensures that the `type` and `type_data` fields are correctly associated and valid.

        serialize_model(nxt):
            Custom serializer to ensure `type_data` is properly nested under its associated `type`.
    """

    __slots__ = ("type", "type_data")

    __registry__: dict[type[NotionType], dict[str, type]] = {}

    type: Optional[StrEnum]
    type_data: Any

    if TYPE_CHECKING:
        type: Annotated[Union[str, NotionType, None], ...]

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

        if (
            type_value
            and not data.get("type_data")
            and (type_data := data.pop(str(type_value)))
        ):
            data["type_data"] = type_data

        super().__init__(**data)

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
    def _get_registered_data_type(cls, notion_type: NotionType) -> type:
        """
        Retrieves the registered data type for a given Notion type.

        Args:
            notion_type: The Notion type to look up.

        Returns:
            The registered data type class.

        Raises:
            ValueError: If the type isn't registered.
        """
        cls._check_notion_type_registration(notion_type)

        return cls.__registry__[type(notion_type)][notion_type]

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

        cls.__registry__[type(notion_type)][notion_type] = type_data_cls

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
                if isinstance(v, NotionType):
                    enum_val = v
                elif isinstance(v, str):
                    for enum_cls in cls.__registry__.keys():
                        try:
                            enum_val = enum_cls(v)
                            break
                        except ValueError:
                            continue
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
            data_type = self._get_registered_data_type(self.type)
            if hasattr(data_type, '__origin__') and data_type.__origin__ is Literal:
                if self.type_data not in get_args(data_type):
                    raise ValueError(
                        f"type_data must be one of {get_args(data_type)} when type is {self.type}"
                    )
            elif not isinstance(self.type_data, data_type):
                try:
                    self.type_data = data_type(**self.type_data)
                except Exception as e:
                    raise ValueError(
                        f"type_data must be of type {data_type.__name__} when type is {self.type}",
                        e,
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
