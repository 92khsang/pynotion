from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import pytest
from pydantic import ValidationError, BaseModel

from pynotion.models.types import (
    NotionDate,
    NotionUrlWrapper,
    NotionDatetime,
    NotionEquation,
)
from tests.models.model_test_utils import PydanticModelTester


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
            NotionUrlWrapper(url=test_input)
    else:
        valid_link = NotionUrlWrapper(url=test_input)
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
        ("06-03-2024", "America/New_York", None, True),
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
    "model_class, test_data",
    [
        (
            NotionUrlWrapper,
            (
                {"url": "https://notion.so"},
                {"url": "https://notion.so"},
                {"url": "https://notion.so"},
            ),
        ),
        (
            NotionEquation,
            (
                {"expression": "E = mc^2"},
                {"expression": "E = mc^2"},
                {"expression": "E = mc^2"},
            ),
        ),
        (
            NotionDate,
            (
                {
                    "start": "2024-05-17",
                    "end": "2024-05-17T15:30:00",
                    "time_zone": "America/New_York",
                },
                {
                    "start": datetime(2024, 5, 17, tzinfo=ZoneInfo("America/New_York")),
                    "end": datetime(
                        2024, 5, 17, 15, 30, tzinfo=ZoneInfo("America/New_York")
                    ),
                    "time_zone": "America/New_York",
                },
                {
                    "start": "2024-05-17T00:00:00-04:00",
                    "end": "2024-05-17T15:30:00-04:00",
                    "time_zone": "America/New_York",
                },
            ),
        ),
    ],
)
def test_pydantic_models(model_class, test_data):
    tester = PydanticModelTester(model_class, test_data)
    tester.run_all_tests()


@pytest.mark.parametrize(
    "input_data, should_raise",
    [
        # Valid cases: Datetime with timezone, string datetime without offset
        (
            {
                "start": "2024-03-17T10:00:00",
                "end": "2024-03-18T10:00:00",
                "time_zone": "America/New_York",
            },
            False,
        ),
        (
            {
                "start": datetime(2024, 3, 17, 10, 0, 0, tzinfo=timezone.utc),
                "end": datetime(2024, 3, 18, 10, 0, 0, tzinfo=timezone.utc),
            },
            False,
        ),
        # Invalid cases: start with UTC offset while time_zone is set
        (
            {
                "start": "2024-03-17T10:00:00Z",
                "time_zone": "America/New_York",
            },
            True,
        ),
        # Invalid: end with UTC offset while time_zone is set
        (
            {
                "start": "2024-03-17T10:00:00",
                "end": "2024-03-18T10:00:00Z",
                "time_zone": "America/New_York",
            },
            True,
        ),
    ],
)
def test_notion_date(input_data, should_raise):
    if should_raise:
        with pytest.raises(ValidationError):
            NotionDate(**input_data)
    else:
        notion_date = NotionDate(**input_data)
        assert notion_date.start
        if "end" in input_data:
            assert notion_date.end


@pytest.mark.parametrize(
    "url, should_raise",
    [
        ("https://valid-url.com", False),
        ("http://valid-url.com", False),
        ("ftp://invalid-url.com", True),
        ("invalid-url", True),
        ("", True),
    ],
)
def test_notion_url_object(url, should_raise):
    if should_raise:
        with pytest.raises(ValidationError):
            NotionUrlWrapper(url=url)
    else:
        notion_url = NotionUrlWrapper(url=url)
        assert notion_url.url == url


@pytest.mark.parametrize(
    "model_class, test_data",
    [
        (
            NotionDate,
            (
                {"start": "2024-03-17T10:00:00", "end": "2024-03-18T10:00:00"},
                {
                    "start": datetime(2024, 3, 17, 10, 0, 0),
                    "end": datetime(2024, 3, 18, 10, 0, 0),
                },
                {"start": "2024-03-17T10:00:00", "end": "2024-03-18T10:00:00"},
            ),
        ),
        (
            NotionUrlWrapper,
            (
                {"url": "https://example.com"},
                {"url": "https://example.com"},
                {"url": "https://example.com"},
            ),
        ),
    ],
)
def test_pydantic_models(model_class, test_data):
    tester = PydanticModelTester(model_class, test_data)
    tester.run_all_tests()
