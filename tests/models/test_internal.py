from datetime import datetime, timezone
from enum import StrEnum
from typing import Annotated, Any
from uuid import UUID
from zoneinfo import ZoneInfo

import pytest
from pydantic import BeforeValidator, ValidationError, Field, PrivateAttr

from pynotion.models._internal import (
    validate_timezone,
    validate_datetime,
    validate_url,
    TypeObjectModel,
    BaseNotionModel,
    validate_enum,
    validate_uuid4,
    NotionType,
    remove_read_only_prefix,
    ReadOnlyTypeObjectModel,
    FixedTypeObjectModel,
)


# --------------------------
#  ✅ Define Sample Types
# --------------------------
class DummyType(StrEnum):
    DUMMY = "dummy"


class NotionSampleType(StrEnum):
    TEXT = "text"
    DATE = "date"


class TextData(BaseNotionModel):
    content: str


class DateData(BaseNotionModel):
    date: datetime


class TypedModel(TypeObjectModel):
    __type_object_map__ = {
        NotionSampleType.TEXT: TextData,
        NotionSampleType.DATE: DateData,
    }

    type: Annotated[
        str,
        NotionSampleType,
        BeforeValidator(lambda v: validate_enum(v, (NotionSampleType,))),
    ]

    type_object: DateData | TextData | None


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


def test_create_type_object_subclass():
    class ExampleData(BaseNotionModel):
        value: int

    class TempTypeModel(TypeObjectModel):
        __type_object_map__ = {
            NotionSampleType.TEXT: ExampleData,
        }

        type: Annotated[
            str,
            NotionSampleType,
            BeforeValidator(lambda v: validate_enum(v, (NotionSampleType,))),
        ]

        type_object: ExampleData | None

    assert ExampleData is TempTypeModel.__type_object_map__[NotionSampleType.TEXT]

    with pytest.raises(
        ValueError, match="TypeObjectModel is registered with multiple Notion types: "
    ):

        class MultipleTypeSubclass(TypeObjectModel):  # noqa
            __type_object_map__ = {
                NotionSampleType.TEXT: TextData,
                DummyType.DUMMY: str,
            }

    with pytest.raises(
        ValueError,
        match="TypeObjectModel is missing fields: \'type\'",
    ):

        class NoTypeSubclass(TypeObjectModel):  # noqa
            type_object: Any

    with pytest.raises(
        ValueError,
        match="TypeObjectModel is missing fields: \'type_object\'",
    ):

        class NoTypeObjectSubclass(TypeObjectModel):  # noqa
            type: Any


@pytest.mark.parametrize(
    "type_name, content, expected_object",
    [
        ("text", TextData(content="Hello"), TextData(content="Hello")),
        ("text", {"content": "Hello"}, TextData(content="Hello")),
        (
            "date",
            DateData(date=datetime(2023, 1, 1)),
            DateData(date=datetime(2023, 1, 1)),
        ),
        ("date", {"date": "2023-01-01"}, DateData(date=datetime(2023, 1, 1))),
    ],
)
def test_typed_model_creation(type_name, content, expected_object):
    instance = TypedModel(type=type_name, type_object=content)

    expected_type = (
        NotionSampleType.TEXT if type_name == "text" else NotionSampleType.DATE
    )

    assert instance.type == expected_type
    assert instance.type_object == expected_object


@pytest.mark.parametrize(
    "type_name, content",
    [
        ("text", {"content": datetime(2023, 1, 1)}),
        ("date", {"date": "Hello"}),
        ("text", {"date": "2023-01-01"}),
        ("date", {"content": "Hello"}),
    ],
)
def test_invalid_type_object(type_name, content):
    with pytest.raises(ValidationError):
        TypedModel(type=type_name, type_object=content)


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


def test_notion_typed_model_getattr():
    """Test that accessing type as an attribute returns type_object."""
    instance = TypedModel(
        type=NotionSampleType.TEXT,
        type_object=TextData(content="Hello"),
    )

    assert instance.type_object == TextData(content="Hello")

    assert instance.text == TextData(
        content="Hello"
    )  # instance.text should return type_object

    with pytest.raises(AttributeError, match="object has no attribute 'invalid'"):
        instance.invalid


def test_unregistered_type_raises():
    """
    Ensures that '_check_notion_type_registration' raises a ValueError
    when an unregistered type is used.
    """

    class FakeEnum(StrEnum):
        FAKE = "fake_enum"

    class NoMappingModel(TypeObjectModel):
        __type_object_map__ = {}  # no types registered
        type: str
        type_object: Any

    with pytest.raises(ValueError, match="Invalid value 'fake_enum'"):
        NoMappingModel(type=FakeEnum.FAKE, type_object={})


def test_remove_read_only_prefix_function():
    """
    Ensures remove_read_only_prefix handles both prefixed and non-prefixed strings.
    """
    assert remove_read_only_prefix("read_only_field_name") == "field_name"
    assert remove_read_only_prefix("normal_field") == "normal_field"


def test_remove_read_only_prefix_on_data_dict():
    """
    Exercises BaseNotionModel._remove_read_only_prefix(data: dict) by
    providing a dict with and without read_only_ prefix keys.
    """

    class TempModel(BaseNotionModel):
        pass

    data = {
        "read_only_oldKey": "some_value",
        "regularKey": 123,
    }
    result = TempModel._remove_read_only_prefix(data)
    # 'read_only_oldKey' should be renamed to 'oldKey'
    assert "oldKey" in result
    assert "read_only_oldKey" not in result
    assert result["oldKey"] == "some_value"
    assert result["regularKey"] == 123


def test_base_notion_model_serialize_model_wrap():
    """
    Tests the coverage of BaseNotionModel.serialize_model ensuring it calls
    _remove_read_only_prefix at the end and handles private_attrs + declared fields.
    """

    class SampleModel(BaseNotionModel):
        __serializable_private_attrs__ = {"_private_value": "alias_private"}

        _private_value: str
        read_only_something: str
        normal_field: int

        def __init__(self, **data):
            super().__init__(**data)
            object.__setattr__(self, "_private_value", "hello")

    instance = SampleModel(read_only_something="read-only", normal_field=42)
    serialized = instance.model_dump()

    # private attr should appear under aliased key
    assert "alias_private" in serialized
    assert serialized["alias_private"] == "hello"

    # the read_only_ prefix on read_only_something should be removed
    assert "something" in serialized
    assert "read_only_something" not in serialized
    assert serialized["something"] == "read-only"


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


def test_extract_kwargs_with_dict():
    """
    Exercises the (type(values) is dict) branch in _extract_kwargs.
    """

    class TestExtractModel(TypeObjectModel):
        __type_object_map__ = {}
        type: str = "test"
        type_object: str = None

        @staticmethod
        def _extract_kwargs(values):
            return super(TestExtractModel, TestExtractModel)._extract_kwargs(values)

    data = {"type": "some_type"}
    result = TestExtractModel._extract_kwargs(data)
    assert result == data


def test_extract_kwargs_with_other():
    """
    Exercises the return None path in _extract_kwargs (values is neither dict nor ArgsKwargs).
    """

    class TestExtractModel(TypeObjectModel):
        __type_object_map__ = {}
        type: str = "test"
        type_object: str = None

        @staticmethod
        def _extract_kwargs(values):
            return super(TestExtractModel, TestExtractModel)._extract_kwargs(values)

    class RandomClass:
        pass

    random_input = RandomClass()
    result = TestExtractModel._extract_kwargs(random_input)
    assert result is None


def test_pre_init_with_nested_type_dict():
    """
    Covers the block in _pre_init where:
      if cls._get_type_object_field() not in data:
          if data.get(str(type_value), None):
              data[cls._get_type_object_field()] = data.pop(str(type_value))
    """

    class SubTypeModel(TypeObjectModel):
        __type_field_set__ = ("type", "type_object")
        __type_object_map__ = {"my_nested_data": dict}
        type: str
        type_object: dict | None

    # The "my_nested_data" key matches str(type=="my_nested_data"), forcing data to be moved
    input_data = {"type": "my_nested_data", "my_nested_data": {"some": "info"}}
    instance = SubTypeModel(**input_data)
    assert instance.type == "my_nested_data"
    assert instance.type_object == {"some": "info"}


def test_convert_type_object_literal():
    """
    Exercises the branch where get_origin(type_class) is Literal but the value
    is not in get_args(type_class), causing the for-loop to continue.
    """
    from typing import Literal

    class MyLiteralEnum(NotionType):
        LITERAL_TEST = "literal_test"

    # A literal that won't match
    LiteralClass = Literal["allowed_value"]

    class LiteralTypeModel(TypeObjectModel):
        __type_object_map__ = {MyLiteralEnum.LITERAL_TEST: LiteralClass}
        type: MyLiteralEnum
        type_object: LiteralClass

    valid_instance = LiteralTypeModel(type="literal_test", type_object="allowed_value")
    assert valid_instance.type_object == "allowed_value"
    assert valid_instance.type == "literal_test"

    # 'disallowed_value' not in ("allowed_value"), so it gets skipped and fails
    with pytest.raises(ValidationError, match="Input should be 'allowed_value"):
        LiteralTypeModel(type="literal_test", type_object="disallowed_value")


def test_serialize_model_no_type_object():
    """
    Exercises the block in TypeObjectModel.serialize_model() where
    type_object_field is not in data, ensuring it simply returns data unchanged.
    """

    class MyEnum(NotionType):
        FOO = "foo"

    class SimpleTypeModel(TypeObjectModel):
        __type_object_map__ = {MyEnum.FOO: None}
        type: MyEnum
        type_object: None

    model = SimpleTypeModel(type="foo", type_object=None)
    serialized = model.model_dump(exclude_none=True)
    # Should not have added "foo" key or anything else for 'type_object'
    assert "foo" not in serialized
    assert "type_object" not in serialized
    assert serialized["type"] == "foo"


def test_read_only_type_object_model():
    """
    Covers read_only_type and read_only_type_object properties in ReadOnlyTypeObjectModel.
    """

    class MyEnum(NotionType):
        BAR = "bar"

    class ReadOnlyTestModel(ReadOnlyTypeObjectModel):
        __type_object_map__ = {MyEnum.BAR: dict}

        read_only_type: MyEnum | None = Field(default=None, frozen=True)
        read_only_type_object: Any | None = Field(default=None, frozen=True)

    instance = ReadOnlyTestModel(
        read_only_type=MyEnum.BAR, read_only_type_object={"x": 1}
    )

    assert instance.type == "bar"
    assert instance.type_object == {"x": 1}


def test_fixed_type_object_model():
    """
    Covers fixed_type and fixed_type_object properties in FixedTypeObjectModel.
    """

    class MyEnum(NotionType):
        BAR = "bar"

    class FixedTestModel(FixedTypeObjectModel):
        __type_object_map__ = {MyEnum.BAR: dict}

        _type: MyEnum = PrivateAttr(default=MyEnum.BAR)
        type_object: dict[str, Any]

    instance = FixedTestModel(type_object={"x": 1})

    assert instance.type == "bar"
    assert instance.type_object == {"x": 1}
    assert instance.bar == {"x": 1}

    with pytest.raises(AttributeError, match="object has no attribute 'invalid'"):
        instance.invalid
