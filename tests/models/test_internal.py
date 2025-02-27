from contextlib import contextmanager
from datetime import datetime, timezone
from enum import StrEnum
from zoneinfo import ZoneInfo

import pytest
from black.trans import Literal

from pynotion.models._internal import (
    validate_timezone,
    validate_datetime,
    validate_url,
    NotionTypedModel,
    NotionBaseModel,
    register_notion_type_enum,
    register_type_data,
)


# --------------------------
#  ✅ Define Sample Types
# --------------------------
@register_notion_type_enum
class DummyType(StrEnum):
    DUMMY = "dummy"


@register_notion_type_enum
class NotionSampleType(StrEnum):
    TEXT = "text"
    DATE = "date"


@register_type_data(NotionSampleType.TEXT)
class TextData(NotionBaseModel):
    content: str


class DateData(NotionBaseModel):
    date: datetime


# Register type
register_type_data(NotionSampleType.DATE, DateData)


# --------------------------
# ✅ Utility: Reset Registry for Each Test
# --------------------------


@contextmanager
def temporary_registry():
    """
    Temporarily resets NotionTypedModel.__registry__,
    ensuring no test affects another due to the shared state.
    """
    original_registry = NotionTypedModel.__registry__.copy()  # Backup
    NotionTypedModel.__registry__.clear()  # Clear before test
    try:
        yield  # Run the test
    finally:
        NotionTypedModel.__registry__ = original_registry


# --------------------------
# ✅ Validation Function Tests
# --------------------------


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


# --------------------------
# ✅ NotionTypedModel Tests
# --------------------------
def test_register_invalid_notion_type():
    class InvalidType:
        pass

    with pytest.raises(ValueError):
        register_notion_type_enum(InvalidType)  # noqa


def test_register_notion_type_enum():
    with temporary_registry():

        class NewType(StrEnum):
            EXAMPLE = "example"

        register_notion_type_enum(NewType)
        assert NewType in NotionTypedModel.__registry__


def test_register_type_data():
    with temporary_registry():

        class ExampleData(NotionBaseModel):
            value: int

        register_notion_type_enum(NotionSampleType)
        register_type_data(NotionSampleType.TEXT, ExampleData)

        assert NotionSampleType.TEXT in NotionTypedModel.__registry__[NotionSampleType]
        assert (
            NotionTypedModel.__registry__[NotionSampleType][NotionSampleType.TEXT]
            is ExampleData
        )


@pytest.mark.parametrize("content", [TextData(content="Hello"), {"content": "Hello"}])
def test_notion_typed_model_valid(content):
    instance = NotionTypedModel(
        type="text",
        type_data=content,
    )
    assert instance.type == NotionSampleType.TEXT
    assert instance.type_data == TextData(content="Hello")


@pytest.mark.parametrize(
    "content", [DateData(date=datetime(2023, 1, 1)), {"date": "2023-01-01"}]
)
def test_notion_typed_model_valid_with_type_name(content):
    instance = NotionTypedModel(
        type="date",
        date=content,  # noqa
    )
    assert instance.type == NotionSampleType.DATE
    assert instance.type_data == DateData(date=datetime(2023, 1, 1))


@pytest.mark.parametrize("invalid_type", ["invalid", DummyType.DUMMY, 123, None])
def test_notion_typed_model_invalid_type(invalid_type):
    with temporary_registry():
        register_notion_type_enum(DummyType)
        register_type_data(DummyType.DUMMY, Literal["dummy"])

        with pytest.raises((ValueError, TypeError)):
            NotionTypedModel(type=invalid_type, type_data={"content": "Hello"})


def test_notion_typed_model_invalid_type_data():
    with pytest.raises(ValueError, match="type_data must be of type DateData"):
        NotionTypedModel(type=NotionSampleType.DATE, type_data={"content": "Invalid"})


def test_notion_typed_model_serialization():
    instance = NotionTypedModel(
        type=NotionSampleType.TEXT,
        type_data=TextData(content="Hello"),  # Use actual Pydantic model
    )
    serialized = instance.model_dump()
    assert serialized == {"type": "text", "text": {"content": "Hello"}}


# --------------------------
# ✅ Edge Cases
# --------------------------


def test_notion_typed_model_missing_type_data():
    with temporary_registry():
        with pytest.raises(
            ValueError, match="type_data must be None when the type is None"
        ):
            NotionTypedModel(type=None, type_data={"content": "Hello"})


def test_register_type_data_without_decorator():
    @register_type_data(NotionSampleType.DATE)
    class CustomDateData(NotionBaseModel):
        formatted: str

    assert NotionSampleType.DATE in NotionTypedModel.__registry__[NotionSampleType]
    assert (
        NotionTypedModel.__registry__[NotionSampleType][NotionSampleType.DATE]
        is CustomDateData
    )
