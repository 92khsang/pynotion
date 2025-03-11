from datetime import datetime
from enum import StrEnum
from uuid import UUID


def validate_uuid4(value: UUID | str | bytes | int) -> UUID:
    """
    Converts various types to a UUID4-compatible value.
    """
    if isinstance(value, UUID):
        return value
    if isinstance(value, str):
        return UUID(value)
    if isinstance(value, bytes):
        return UUID(UUID(bytes=value).hex)
    if isinstance(value, int):
        return UUID(UUID(int=value).hex)
    raise ValueError(f"Cannot convert {type(value)} to UUID4")


def validate_enum(
    value: str | StrEnum, enum_types: tuple[type[StrEnum], ...]
) -> StrEnum:
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
    actual_val: str | StrEnum, expected_values: set[StrEnum]
) -> StrEnum:
    """
    Validates that 'actual_val' matches one of the StrEnums in 'expected_values'.
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
