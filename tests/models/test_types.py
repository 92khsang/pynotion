from datetime import datetime, timezone
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo

import pytest
from pydantic import ValidationError, BaseModel

from pynotion.models.types import (
    ObjectId,
    NotionDatetime,
    NotionEmail,
    NotionUrl,
    ObjectType,
    Color,
    BackgroundColor,
    NotionLink,
    NotionEquation,
    NotionDate,
)
from tests.models.model_test_utils import PydanticModelTester


# --- Test Type Aliases ---
@pytest.mark.parametrize(
    "test_input",
    [str(uuid4()), uuid4().hex],
)
def test_object_id(test_input):
    assert ObjectId(test_input) == UUID(test_input)


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (datetime(2023, 5, 17, 15, 30), datetime(2023, 5, 17, 15, 30)),
        ("2023-05-17T15:30:00Z", datetime(2023, 5, 17, 15, 30, tzinfo=timezone.utc)),
    ],
)
def test_notion_datetime_valid(test_input, expected):
    class TestModel(BaseModel):
        notion_date: NotionDatetime

    notion_date = TestModel(notion_date=test_input).notion_date
    assert notion_date == expected


@pytest.mark.parametrize(
    "invalid_input",
    ["invalid-datetime", 123, None, "2023-13-45T99:99:99Z"],
)
def test_notion_datetime_invalid(invalid_input):
    class TestModel(BaseModel):
        notion_date: NotionDatetime

    with pytest.raises((ValueError, TypeError)):
        _ = TestModel(notion_date=invalid_input).notion_date


@pytest.mark.parametrize(
    "test_input",
    ["user@example.com", "test.email+alias@gmail.com"],
)
def test_notion_email_valid(test_input):
    class TestModel(BaseModel):
        notion_email: NotionEmail

    assert TestModel(notion_email=test_input).notion_email == test_input


@pytest.mark.parametrize(
    "invalid_input",
    ["invalid-email", "user@com", "@no-local.com", "plainaddress"],
)
def test_notion_email_invalid(invalid_input):
    class TestModel(BaseModel):
        notion_email: NotionEmail

    with pytest.raises(ValidationError):
        _ = TestModel(notion_email=invalid_input).notion_email


@pytest.mark.parametrize(
    "test_input",
    ["https://www.example.com", "http://localhost:8000"],
)
def test_notion_url_valid(test_input):
    class TestModel(BaseModel):
        notion_url: NotionUrl

    assert TestModel(notion_url=test_input).notion_url == test_input


@pytest.mark.parametrize(
    "invalid_input",
    ["not-a-valid-url", "ftp://invalid.com", "www.google.com"],  # Missing scheme
)
def test_notion_url_invalid(invalid_input):
    class TestModel(BaseModel):
        notion_url: NotionUrl

    with pytest.raises(ValidationError):
        _ = TestModel(notion_url=invalid_input).notion_url


# --- Test Enums ---
@pytest.mark.parametrize(
    "enum_class, member, expected",
    [
        (ObjectType, "BLOCK", "block"),
        (ObjectType, "USER", "user"),
        (Color, "BLUE", "blue"),
        (Color, "RED", "red"),
        (BackgroundColor, "BLUE_BACKGROUND", "blue_background"),
        (BackgroundColor, "RED_BACKGROUND", "red_background"),
    ],
)
def test_enum_values(enum_class, member, expected):
    assert getattr(enum_class, member) == expected


# --- Test Pydantic Models ---
@pytest.mark.parametrize(
    "test_input, should_raise",
    [
        ("https://notion.so", False),
        ("invalid-url", True),
    ],
)
def test_notion_link(test_input, should_raise):
    if should_raise:
        with pytest.raises(ValidationError):
            NotionLink(url=test_input)
    else:
        valid_link = NotionLink(url=test_input)
        assert valid_link.url == test_input


@pytest.mark.parametrize(
    "expression",
    ["E = mc^2", "a^2 + b^2 = c^2"],
)
def test_notion_equation(expression):
    equation = NotionEquation(expression=expression)
    assert equation.expression == expression


@pytest.mark.parametrize(
    "start, time_zone, expected_start, should_raise",
    [
        # ✅ Valid formats
        ("2023-05-17", None, datetime(2023, 5, 17), False),
        (
            "2023-05-17",
            "America/New_York",
            datetime(2023, 5, 17, tzinfo=ZoneInfo("America/New_York")),
            False,
        ),
        (
            "2023-05-17T15:30:00.123456Z",
            None,
            datetime(2023, 5, 17, 15, 30, 0, 123456, tzinfo=timezone.utc),
            False,
        ),
        # ❌ Invalid formats
        ("2023/05/17", None, None, True),
        (12345, None, None, True),
        ("2023-05-17T15:30:00+00:00", "America/New_York", None, True),
        ("2023-05-17T15:30:00.123456", "Invalid Timezone", None, True),
        (datetime(2023, 5, 17, tzinfo=timezone.utc), "America/New_York", None, True),
    ],
)
def test_notion_date(
    start: str,
    time_zone: str,
    expected_start: datetime,
    should_raise: bool,
):
    if should_raise:
        with pytest.raises((ValidationError, ValueError)):
            NotionDate(start=start, time_zone=time_zone)
    else:
        notion_date = NotionDate(start=start, time_zone=time_zone)
        assert notion_date.start == expected_start
        assert notion_date.time_zone == time_zone


@pytest.mark.parametrize(
    "clz,test_data",
    [
        (
            NotionDate,
            [
                (NotionDate(start=datetime(2023, 5, 17)), {"start": "2023-05-17"}),
                (
                    NotionDate(
                        start=datetime(
                            2023, 5, 17, tzinfo=ZoneInfo("America/New_York")
                        ),
                        end=datetime(2023, 5, 18, tzinfo=ZoneInfo("America/New_York")),
                        time_zone="America/New_York",
                    ),
                    {
                        "start": "2023-05-17",
                        "end": "2023-05-18",
                        "time_zone": "America/New_York",
                    },
                ),
            ],
        ),
        (
            NotionEquation,
            [(NotionEquation(expression="E = mc^2"), {"expression": "E = mc^2"})],
        ),
    ],
    ids=["NotionDate", "NotionEquation"],
)
def test_models_serialization(clz: type, test_data: list[tuple[BaseModel, dict, ...]]):
    PydanticModelTester(clz, test_data).run_all_tests()
