import re

from datetime import datetime
from enum import Enum
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


def validate_enum(value: str | Enum, enum_types: tuple[type[Enum], ...]) -> Enum:
    """
    Convert a string value to one of the provided Enum types.

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
    Validates and returns a given URL.
    - Allows 'http' or 'https' URLs with a valid netloc
    - Allows relative paths (e.g., /images/foo.svg)
    """
    if not isinstance(url, str):
        raise TypeError(f"Expected str, got {type(url).__name__}")

    if not url:
        raise ValueError("URL can't be None or empty")

    from urllib.parse import urlparse

    parsed = urlparse(url)

    # Absolute URL with http/https
    if parsed.scheme in ['http', 'https']:
        if parsed.netloc:
            return url
        else:
            raise ValueError(f"URL with scheme '{parsed.scheme}' missing domain")

    # Relative path like /images/foo.svg
    if not parsed.scheme and not parsed.netloc and parsed.path.startswith('/'):
        return url

    raise ValueError(
        f"Invalid URL. Must be http/https URL or relative path starting with '/'. Got: {url}"
    )


def validate_email(email: str) -> str:
    """
    Validates if the given string is a properly formatted email address.

    Args:
        email: The email address to validate

    Returns:
        bool: True if email is valid, False otherwise

    Examples:
        >>> validate_email("user@example.com")
        True
        >>> validate_email("invalid-email")
        False
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if isinstance(email, str) and bool(re.match(pattern, email)):
        return email

    raise ValueError(f"Invalid email address: {email}")


def validate_phone(phone: str) -> str:
    """
    Validates if the given string is a properly formatted phone number.
    Accepts various formats including hyphenated numbers.

    Args:
        phone: The phone number to validate

    Returns:
        bool: True if the phone number is valid, False otherwise

    Examples:
        >>> validate_phone("+1 (555) 123-4567")
        True
        >>> validate_phone("555-123-4567")
        True
        >>> validate_phone("012-3456-7890")
        True
        >>> validate_phone("02-123-4567")
        True
        >>> validate_phone("5551234567")
        True
        >>> validate_phone("invalid-number")
        False
    """
    # First check: Common hyphenated formats with 2-3 parts
    if "-" in phone and not phone.startswith("+"):
        # Split by hyphens and check if we have valid parts
        parts = phone.split("-")

        # Valid hyphenated format should have 2-3 parts, all numeric
        if 2 <= len(parts) <= 3 and all(part.isdigit() for part in parts):
            # Check total length without hyphens is reasonable
            digits_only = "".join(parts)
            if 7 <= len(digits_only) <= 15:
                return phone

                # If not a valid hyphenated format, check using other methods

    # Strip all non-numeric characters except leading +
    cleaned_phone = re.sub(r'[^\d+]', '', phone)

    # Check if it's an international format (starts with +)
    if cleaned_phone.startswith('+'):
        # International format: +[country code][number]
        pattern = r"^\+\d{1,4}\d{6,14}$"
    else:
        # National format: typically 7-15 digits
        pattern = r"^\d{7,15}$"

    if bool(re.match(pattern, cleaned_phone)):
        return phone

    raise ValueError(f"Invalid phone number: {phone}")


def validate_empty_dict(value: dict) -> dict:
    """
    Validate a given value is an empty dict.

    >>> validate_empty_dict({})
    {}

    >>> validate_empty_dict({"a": 1})
    Traceback (most recent call last):
    ...
    ValueError: Expected an empty dict, but got {'a': 1}
    """

    if not isinstance(value, dict) or len(value) != 0:
        raise ValueError(f"Expected an empty dict, but got {value}")

    return value
