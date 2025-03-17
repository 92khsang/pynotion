from datetime import datetime, timezone
from enum import Enum
from uuid import UUID
from zoneinfo import ZoneInfo

import pytest

from pynotion.models._internal import (
    validate_timezone,
    validate_datetime,
    validate_url,
    BaseNotionModel,
    validate_enum,
    validate_uuid4,
    validate_phone,
    validate_email,
)


# --------------------------
#  ✅ Define Sample Types
# --------------------------
class DummyType(str, Enum):
    DUMMY = "dummy"


class NotionSampleType(str, Enum):
    TEXT = "text"
    DATE = "date"


class TextData(BaseNotionModel):
    content: str


class DateData(BaseNotionModel):
    date: datetime


@pytest.mark.parametrize(
    "tz",
    ["UTC", "America/New_York", "Asia/Seoul", "Europe/London"],
)
def test_validate_timezone_valid(tz):
    assert validate_timezone(tz) == tz


@pytest.mark.parametrize("tz", ["Fake/Timezone", "", "Not_A_Zone"])
def test_validate_timezone_invalid(tz):
    with pytest.raises(ValueError, match="Invalid IANA timezone"):
        validate_timezone(tz)


@pytest.mark.parametrize(
    "input_value, expected",
    [
        (
            datetime(2023, 1, 1, 12, 0, tzinfo=timezone.utc),
            datetime(2023, 1, 1, 12, 0, tzinfo=timezone.utc),
        ),
        ("2023-01-01T12:00:00Z", datetime(2023, 1, 1, 12, 0, tzinfo=timezone.utc)),
        (
            "2024-06-15T08:30:00+09:00",
            datetime(2024, 6, 15, 8, 30, tzinfo=ZoneInfo("Asia/Seoul")),
        ),
        ("2024-06-15", datetime(2024, 6, 15)),
    ],
)
def test_validate_datetime_valid(input_value, expected):
    assert validate_datetime(input_value) == expected


@pytest.mark.parametrize("invalid_value", ["invalid-date", 12345, None])
def test_validate_datetime_invalid(invalid_value):
    with pytest.raises(
        (ValueError, TypeError),  # noqa
        match="Datetime value cannot be None|Invalid ISO 8601 format|Expected str or datetime",
    ):
        validate_datetime(invalid_value)


@pytest.mark.parametrize(
    "url",
    ["https://example.com", "http://valid-url.org", "https://sub.domain.com/path"],
)
def test_validate_url_valid(url):
    assert validate_url(url) == url


@pytest.mark.parametrize(
    "invalid_url",
    ["", "ftp://example.com", "not-a-url", "https://"],
)
def test_validate_url_invalid(invalid_url):
    with pytest.raises(ValueError):
        validate_url(invalid_url)


@pytest.mark.parametrize(
    "value, expected",
    [
        ("dummy", DummyType.DUMMY),
        ("text", NotionSampleType.TEXT),
        ("date", NotionSampleType.DATE),
        (DummyType.DUMMY, DummyType.DUMMY),
        (NotionSampleType.TEXT, NotionSampleType.TEXT),
    ],
)
def test_validate_enum_valid(value, expected):
    """Test that valid values return correct enum instances."""
    assert validate_enum(value, (DummyType, NotionSampleType)) == expected


@pytest.mark.parametrize(
    "invalid_value",
    ["invalid", "notion", "DATE_WRONG", "123", "", None, 42, []],
)
def test_validate_enum_invalid(invalid_value):
    """Test that invalid values raise ValueError."""
    with pytest.raises(ValueError, match="Invalid value"):
        validate_enum(invalid_value, (DummyType, NotionSampleType))


def test_validate_enum_empty_enum_list():
    """Test that an empty enum list raises ValueError."""
    with pytest.raises(ValueError, match="Invalid value"):
        validate_enum("dummy", ())


@pytest.mark.parametrize(
    "value, expected_hex",
    [
        (
            UUID("12345678-1234-5678-1234-567812345678"),
            "12345678123456781234567812345678",
        ),
        ("12345678-1234-5678-1234-567812345678", "12345678123456781234567812345678"),
        (b"\x12\x34\x56\x78" * 4, "12345678123456781234567812345678"),
        (
            int("12345678123456781234567812345678", 16),
            "12345678123456781234567812345678",
        ),
    ],
)
def test_validate_uuid4_valid(value, expected_hex):
    """Ensures validate_uuid4 handles all supported input types."""
    result = validate_uuid4(value)
    assert isinstance(result, UUID)
    assert result.hex == expected_hex


def test_validate_uuid4_invalid_type():
    """
    Ensures validate_uuid4 raises ValueError for unsupported types.
    """
    with pytest.raises(ValueError, match="Cannot convert <class 'list'> to UUID4"):
        validate_uuid4([])


def test_no_instances():
    class TestModel(BaseNotionModel):
        __no_instance__ = True

    with pytest.raises(TypeError, match="Cannot instantiate non-instance class"):
        TestModel()


def test_invalid_email():
    with pytest.raises(ValueError, match="Invalid email address"):
        validate_email("invalid-email")


def test_invalid_phone():
    with pytest.raises(ValueError, match="Invalid phone number"):
        validate_phone("invalid-phone")


@pytest.mark.parametrize(
    "phone, expected",
    [
        ("+1 (555) 123-4567", "+1 (555) 123-4567"),
        ("555-123-4567", "555-123-4567"),
        ("012-3456-7890", "012-3456-7890"),
        ("02-123-4567", "02-123-4567"),
        ("5551234567", "5551234567"),
        ("+44 20 7946 0958", "+44 20 7946 0958"),
        ("+91-9876543210", "+91-9876543210"),
    ],
)
def test_validate_phone_valid(phone, expected):
    assert validate_phone(phone) == expected
