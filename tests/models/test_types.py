from datetime import datetime, timezone
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo

import pytest
from pydantic import ValidationError, BaseModel, UUID4

from pynotion.models.types import (
    NotionObjectId,
    NotionDatetime,
    NotionEmail,
    NotionUrl,
    Color,
    BackgroundColor,
    NotionLink,
    NotionEquation,
    NotionDate,
    NotionHostedFile,
    ParentType,
    NotionParent,
    FileType,
    NotionFile,
    EmojiType,
    CustomEmoji,
    NotionEmoji,
    NotionUserRef,
    NotionExternalFile,
    TxNotionObject,
    RxNotionObject,
)
from tests.models.model_test_utils import PydanticModelTester


# --- Test Type Aliases ---
@pytest.mark.parametrize(
    "test_input",
    [str(uuid4()), uuid4().hex],
)
def test_object_id(test_input):
    class ObjectIdModel(BaseModel):
        object_id: NotionObjectId

    assert ObjectIdModel(object_id=test_input).object_id == UUID4(test_input)


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


# --- Test NotionHostedFile ---
@pytest.mark.parametrize(
    "url, expiry_time, should_raise",
    [
        ("https://valid-url.com/file.png", "2024-05-17T15:30:00Z", False),
        (
            "https://valid-url.com/file.png",
            datetime(2024, 5, 17, 15, 30, tzinfo=timezone.utc),
            False,
        ),
        ("invalid-url", "2024-05-17T15:30:00Z", True),  # Invalid URL
        (
            "https://valid-url.com/file.png",
            "invalid-datetime",
            True,
        ),  # Invalid datetime
    ],
)
def test_notion_hosted_file(url, expiry_time, should_raise):
    if should_raise:
        with pytest.raises(ValidationError):
            NotionHostedFile(url=url, expiry_time=expiry_time)
    else:
        notion_file = NotionHostedFile(url=url, expiry_time=expiry_time)
        assert notion_file.url == url
        assert (
            notion_file.expiry_time == expiry_time
            if isinstance(expiry_time, datetime)
            else datetime.fromisoformat(expiry_time)
        )


@pytest.mark.parametrize(
    "parent_type, type_object, should_raise",
    [
        (ParentType.DATABASE_ID, uuid4(), False),
        (ParentType.PAGE_ID, uuid4(), False),
        (ParentType.BLOCK_ID, uuid4(), False),
        (ParentType.WORKSPACE, True, False),
        (ParentType.WORKSPACE, False, False),
        (ParentType.WORKSPACE, uuid4(), True),  # Invalid: should be bool
        (ParentType.PAGE_ID, "invalid-id", True),  # Invalid UUID
    ],
)
def test_notion_parent(parent_type, type_object, should_raise):
    if should_raise:
        with pytest.raises(ValidationError):
            NotionParent(type=parent_type, type_object=type_object)
    else:
        parent = NotionParent(type=parent_type, type_object=type_object)
        assert parent.type == parent_type
        assert parent.type_object == type_object


@pytest.mark.parametrize(
    "file_type, type_object, should_raise",
    [
        (
            FileType.FILE,
            NotionHostedFile(
                url="https://valid-url.com", expiry_time="2024-05-17T15:30:00Z"
            ),
            False,
        ),
        (FileType.EXTERNAL, NotionExternalFile(url="https://external.com"), False),
        (
            FileType.FILE,
            NotionExternalFile(url="https://external.com"),
            True,
        ),  # Wrong type_object for FILE
        (
            FileType.EXTERNAL,
            NotionHostedFile(
                url="https://valid-url.com", expiry_time="2024-05-17T15:30:00Z"
            ),
            True,
        ),  # Wrong type_object for EXTERNAL
        (
            "invalid-type",
            NotionExternalFile(url="https://valid-url.com"),
            True,
        ),  # Invalid file type
    ],
)
def test_notion_file(file_type, type_object, should_raise):
    if should_raise:
        with pytest.raises(ValueError):
            NotionFile(type=file_type, type_object=type_object)
    else:
        notion_file = NotionFile(type=file_type, type_object=type_object)
        assert notion_file.type == file_type
        assert (
            notion_file.expiry_time == datetime.fromisoformat(type_object)
            if isinstance(type_object, str)
            else type_object
        )


@pytest.mark.parametrize(
    "emoji_type, type_object, should_raise",
    [
        (EmojiType.EMOJI, "🔥", False),
        (
            EmojiType.CUSTOM_EMOJI,
            CustomEmoji(id=uuid4(), name="custom", url="https://valid-url.com"),
            False,
        ),
        (
            EmojiType.EMOJI,
            CustomEmoji(id=uuid4(), name="custom", url="https://valid-url.com"),
            True,
        ),  # Invalid type_object
        (EmojiType.CUSTOM_EMOJI, "🔥", True),  # Invalid type_object
    ],
)
def test_notion_emoji(emoji_type, type_object, should_raise):
    if should_raise:
        with pytest.raises(ValidationError):
            NotionEmoji(type=emoji_type, type_object=type_object)
    else:
        notion_emoji = NotionEmoji(type=emoji_type, type_object=type_object)
        assert notion_emoji.type == emoji_type
        assert notion_emoji.type_object == type_object


def test_notion_user_ref():
    with pytest.raises(ValueError, match="Input should be \'user\'"):
        NotionUserRef(object="page")

    valid_user_ref = NotionUserRef(object="user", id=uuid4())

    assert valid_user_ref.object == "user"


def test_frozen_object():
    with pytest.raises(ValidationError, match="Field is frozen"):
        emoji_object = NotionEmoji(type=EmojiType.EMOJI, type_object="🔥")
        emoji_object.__setattr__("type", EmojiType.CUSTOM_EMOJI)


@pytest.mark.parametrize(
    "input_dict, expected_dict, should_raise",
    [
        (
            {
                "object": "block",
                "parent": {
                    "type": "page_id",
                    "page_id": "59833787-2cf9-4fdf-8782-e53db20768a5",
                },
            },
            {
                "object": "block",
                "parent": NotionParent(
                    type=ParentType.PAGE_ID,
                    type_object=UUID("59833787-2cf9-4fdf-8782-e53db20768a5"),
                ),
            },
            False,
        ),
        (
            {
                "object": "database",
                "parent": {
                    "type": "workspace",
                    "workspace": True,
                },
            },
            {
                "object": "database",
                "parent": NotionParent(
                    type=ParentType.WORKSPACE,
                    type_object=True,
                ),
            },
            False,
        ),
        (
            {
                "object": "user",
                "id": "ee5f0f84-409a-440f-983a-a5315961c6e4",
            },
            None,
            True,
        ),
    ],
)
def test_notion_object_req(input_dict, expected_dict, should_raise):
    class TxNotionObjectImpl(TxNotionObject):
        parent: NotionParent

    if should_raise:
        with pytest.raises(ValueError):
            TxNotionObjectImpl(**input_dict)
    else:
        notion_obj = TxNotionObjectImpl(**input_dict)
        for key, value in expected_dict.items():
            assert getattr(notion_obj, key) == value


@pytest.mark.parametrize(
    "input_dict, expected_dict, should_raise",
    [
        (
            {
                "object": "block",
                "id": "c02fc1d3-db8b-45c5-a222-27595b15aea7",
                "parent": {
                    "type": "page_id",
                    "page_id": "59833787-2cf9-4fdf-8782-e53db20768a5",
                },
                "created_time": "2022-03-01T19:05:00.000Z",
                "last_edited_time": "2022-07-06T19:41:00.000Z",
                "created_by": {
                    "object": "user",
                    "id": "ee5f0f84-409a-440f-983a-a5315961c6e4",
                },
                "last_edited_by": {
                    "object": "user",
                    "id": "ee5f0f84-409a-440f-983a-a5315961c6e4",
                },
                "archived": False,
                "in_trash": False,
            },
            {
                "object": "block",
                "id": UUID("c02fc1d3-db8b-45c5-a222-27595b15aea7"),
                "parent": NotionParent(
                    type=ParentType.PAGE_ID,
                    type_object=UUID("59833787-2cf9-4fdf-8782-e53db20768a5"),
                ),
                "created_time": datetime(2022, 3, 1, 19, 5, tzinfo=timezone.utc),
                "last_edited_time": datetime(2022, 7, 6, 19, 41, tzinfo=timezone.utc),
                "created_by": NotionUserRef(
                    object="user", id=UUID("ee5f0f84-409a-440f-983a-a5315961c6e4")
                ),
                "last_edited_by": NotionUserRef(
                    object="user", id=UUID("ee5f0f84-409a-440f-983a-a5315961c6e4")
                ),
                "archived": False,
                "in_trash": False,
            },
            False,
        ),
        (
            {
                "object": "database",
                "id": "ee5f0f84-409a-440f-983a-a53151c6e4",
            },
            None,
            True,
        ),
        (
            {
                "object": "user",
                "id": "ee5f0f84-409a-440f-983a-a5315961c6e4",
            },
            None,
            True,
        ),
    ],
)
def test_notion_object_res(input_dict, expected_dict, should_raise):
    class RxNotionObjectImpl(RxNotionObject):
        pass

    if should_raise:
        with pytest.raises(ValueError):
            RxNotionObjectImpl(**input_dict)
    else:
        notion_obj = RxNotionObjectImpl(**input_dict)
        for key, value in expected_dict.items():
            assert getattr(notion_obj, key) == value


def test_create_abstract_class():
    for clz in [TxNotionObject, RxNotionObject]:
        with pytest.raises(TypeError, match="Cannot instantiate abstract class"):
            clz()


@pytest.mark.parametrize(
    "model_class, test_data",
    [
        (
            NotionLink,
            (
                {"url": "https://notion.so"},
                {"url": "https://notion.so"},
                {"url": "https://notion.so"},
            ),
        ),
        (
            NotionHostedFile,
            (
                {
                    "url": "https://notion.so",
                    "expiry_time": "2024-05-17T15:30:00Z",
                },
                {
                    "url": "https://notion.so",
                    "expiry_time": datetime(2024, 5, 17, 15, 30, tzinfo=timezone.utc),
                },
                {
                    "url": "https://notion.so",
                    "expiry_time": "2024-05-17T15:30:00Z",
                },
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
        (
            NotionParent,
            (
                {
                    "type": "page_id",
                    "page_id": "f4de14e1-0cff-4497-835f-29d6d04d62c1",
                },
                {
                    "type": ParentType.PAGE_ID,
                    "page_id": UUID("f4de14e1-0cff-4497-835f-29d6d04d62c1"),
                },
                {"type": "page_id", "page_id": "f4de14e1-0cff-4497-835f-29d6d04d62c1"},
            ),
        ),
        (
            NotionFile,
            (
                {
                    "type": FileType.EXTERNAL,
                    "type_object": {"url": "https://example.com"},
                },
                {
                    "type": "external",
                    "external": {"url": "https://example.com"},
                },
                {
                    "type": "external",
                    "external": {"url": "https://example.com"},
                },
            ),
        ),
        (
            NotionEmoji,
            (
                {
                    "type": "custom_emoji",
                    "custom_emoji": {
                        "id": "f4de14e1-0cff-4497-835f-29d6d04d62c1",
                        "name": "smile",
                        "url": "https://example.com/emoji.png",
                    },
                },
                {
                    "type": EmojiType.CUSTOM_EMOJI,
                    "custom_emoji": {
                        "id": UUID("f4de14e1-0cff-4497-835f-29d6d04d62c1"),
                        "name": "smile",
                        "url": "https://example.com/emoji.png",
                    },
                },
                {
                    "type": "custom_emoji",
                    "custom_emoji": {
                        "id": "f4de14e1-0cff-4497-835f-29d6d04d62c1",
                        "name": "smile",
                        "url": "https://example.com/emoji.png",
                    },
                },
            ),
        ),
    ],
)
def test_pydantic_models(model_class, test_data):
    tester = PydanticModelTester(model_class, test_data)
    tester.run_all_tests()
