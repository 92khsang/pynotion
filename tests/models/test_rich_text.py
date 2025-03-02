import uuid

import pytest
from pydantic import ValidationError, BaseModel

from pynotion.models.rich_text import (
    RichTextType,
    MentionType,
    TemplateMentionType,
    Annotations,
    Text,
    MentionDatabase,
    MentionUser,
    MentionPage,
    MentionLinkPreview,
    MentionDate,
    MentionDateTemplate,
    MentionUserTemplate,
    MentionObjectId,
    TemplateMentionDate,
    TemplateMentionUser,
    RichText,
)
from pynotion.models.types import (
    NotionEquation,
    NotionLink,
    NotionDate,
    Color,
)
from pynotion.models.user import User
from tests.models.model_test_utils import PydanticModelTester


# ------------------ FIXTURES ------------------ #
@pytest.fixture(scope="module")
def sample_uuid():
    return str(uuid.uuid4())


# ------------------ ENUM TESTS ------------------ #
@pytest.mark.parametrize(
    "enum_class, value, expected",
    [
        (RichTextType, RichTextType.TEXT, "text"),
        (RichTextType, RichTextType.EQUATION, "equation"),
        (RichTextType, RichTextType.MENTION, "mention"),
        (MentionType, MentionType.USER, "user"),
        (MentionType, MentionType.PAGE, "page"),
        (
            TemplateMentionType,
            TemplateMentionType.TEMPLATE_MENTION_DATE,
            "template_mention_date",
        ),
        (
            TemplateMentionType,
            TemplateMentionType.TEMPLATE_MENTION_USER,
            "template_mention_user",
        ),
    ],
)
def test_enum_values(enum_class, value, expected):
    """Test enum values for correctness."""
    assert value.value == expected


# ------------------ MODEL TESTS ------------------ #
def test_annotations():
    """Test Annotations model instantiation."""
    sample_annotations = Annotations(bold=True, color="red")
    assert sample_annotations.bold is True
    assert sample_annotations.italic is False
    assert sample_annotations.color == "red"

    with pytest.raises(ValueError):
        Annotations(color="invalid_color")


@pytest.mark.parametrize(
    "content, link_url",
    [
        ("Hello, Notion!", "https://notion.so"),
        ("Hello", None),
    ],
)
def test_text_model(content, link_url):
    """Test Text model instantiation and serialization."""
    sample_text = Text(content=content, link=link_url)
    assert sample_text.content == content
    if link_url:
        assert sample_text.link.url == link_url
    else:
        assert sample_text.link is None


def test_invalid_text_model():
    with pytest.raises(ValidationError):
        Text(content="Hello", link="invalid_url")

    with pytest.raises(ValidationError):
        Text(content=None)


@pytest.mark.parametrize(
    "mention_class, type_value, type_data, type_asdict",
    [
        (
            MentionDatabase,
            MentionType.DATABASE,
            MentionObjectId(id="d7db80bd-b3e3-4394-b134-a21b05412c7c"),
            {
                "type": "database",
                "database": {"id": "d7db80bd-b3e3-4394-b134-a21b05412c7c"},
            },
        ),
        (
            MentionDate,
            MentionType.DATE,
            NotionDate(start="2022-01-01", end="2022-01-31"),
            {"type": "date", "date": {"start": "2022-01-01", "end": "2022-01-31"}},
        ),
        (
            MentionLinkPreview,
            MentionType.LINK_PREVIEW,
            NotionLink(url="https://notion.so"),
            {"type": "link_preview", "link_preview": {"url": "https://notion.so"}},
        ),
        (
            MentionPage,
            MentionType.PAGE,
            MentionObjectId(id="a7db80bd-b3e3-4394-b134-a21b05412c7c"),
            {
                "type": "page",
                "page": {"id": "a7db80bd-b3e3-4394-b134-a21b05412c7c"},
            },
        ),
        (
            MentionDateTemplate,
            MentionType.TEMPLATE_MENTION,
            TemplateMentionDate(type_data="today"),
            {
                "type": "template_mention",
                "template_mention": {
                    "type": "template_mention_date",
                    "type_data": "today",
                },
            },
        ),
        (
            MentionUserTemplate,
            MentionType.TEMPLATE_MENTION,
            TemplateMentionUser(),
            {
                "type": "template_mention",
                "template_mention": {
                    "type": "template_mention_user",
                    "type_data": "me",
                },
            },
        ),
        (
            MentionUser,
            MentionType.USER,
            User(id="a7db80bd-b3e3-4394-b134-a21b05412c7c"),
            {
                "type": "user",
                "user": {
                    "object": "user",
                    "id": "a7db80bd-b3e3-4394-b134-a21b05412c7c",
                },
            },
        ),
    ],
)
def test_mentions(mention_class, type_value, type_data, type_asdict):
    """Test Mention-based models."""
    mention_data = mention_class(type_data=type_data)
    assert mention_data.type == type_value
    assert mention_data.type_data == type_data
    assert getattr(mention_data, type_value) == type_data
    assert eval(f"mention_data.{type_value}") == type_data
    assert mention_data == mention_class.model_validate(type_asdict)


@pytest.mark.parametrize(
    "type_data",
    [
        MentionObjectId(id="d7db80bd-b3e3-4394-b134-a21b05412c7c"),
        NotionDate(start="2022-01-01", end="2022-01-31"),
        NotionLink(url="https://notion.so"),
        TemplateMentionDate(type_data="today"),
        TemplateMentionUser(),
        User(id="a7db80bd-b3e3-4394-b134-a21b05412c7c"),
    ],
)
def test_invalid_mentions(type_data):
    """Test invalid Mention-based models."""
    mention_classes: list[tuple[type, type]] = [
        (MentionDatabase, MentionObjectId),
        (MentionDate, NotionDate),
        (MentionLinkPreview, NotionLink),
        (MentionPage, MentionObjectId),
        (MentionDateTemplate, TemplateMentionDate),
        (MentionUser, User),
    ]

    for mention_class, mention_data_class in mention_classes:
        if mention_data_class != type(type_data):
            with pytest.raises((ValueError, TypeError)):
                mention_class(type_data=type_data)


# ------------------ RICH TEXT TESTS ------------------ #
@pytest.mark.parametrize(
    "rich_text_type, annotations, plain_text, href, type_data",
    [
        (
            RichTextType.TEXT,
            Annotations(),
            "Test Text",
            "https://notion.so",
            Text(content="Test Text", link="https://notion.so"),
        ),
        (
            RichTextType.EQUATION,
            Annotations(),
            "E = mc^2",
            None,
            NotionEquation(expression="E = mc^2"),
        ),
        (
            RichTextType.MENTION,
            Annotations(),
            "Test User",
            None,
            MentionUser(type_data=User(id="a7db80bd-b3e3-4394-b134-a21b05412c7c")),
        ),
        (
            RichTextType.MENTION,
            Annotations(),
            "Test Page",
            None,
            MentionPage(
                type_data=MentionObjectId(id="d7db80bd-b3e3-4394-b134-a21b05412c7c")
            ),
        ),
        (
            RichTextType.MENTION,
            Annotations(),
            "Test Database",
            None,
            MentionDatabase(
                type_data=MentionObjectId(id="d7db80bd-b3e3-4394-b134-a21b05412c7c")
            ),
        ),
        (
            RichTextType.MENTION,
            Annotations(),
            "Test Date",
            None,
            MentionDate(type_data=NotionDate(start="2022-01-01", end="2022-01-31")),
        ),
        (
            RichTextType.MENTION,
            Annotations(),
            "Test Link Preview",
            None,
            MentionLinkPreview(type_data=NotionLink(url="https://notion.so")),
        ),
        (
            RichTextType.MENTION,
            Annotations(),
            "Test Template",
            None,
            MentionDateTemplate(type_data=TemplateMentionDate(type_data="today")),
        ),
    ],
    ids=[
        "rich_text_text",
        "rich_text_equation",
        "rich_text_mention_user",
        "rich_text_mention_page",
        "rich_text_mention_database",
        "rich_text_mention_date",
        "rich_text_mention_link_preview",
        "rich_text_mention_date_template",
    ],
)
def test_rich_text(rich_text_type, annotations, plain_text, href, type_data):
    """Test RichText model with a text type."""
    rich_text = RichText(
        type=rich_text_type,
        type_data=type_data,
        annotations=annotations,
        plain_text=plain_text,
        href=href,
    )

    assert rich_text.type == rich_text_type
    assert rich_text.type_data == type_data
    assert rich_text.annotations == annotations
    assert rich_text.plain_text == plain_text
    assert rich_text.href == href


# ------------------ VALIDATION TESTS ------------------ #
@pytest.mark.parametrize(
    "invalid_data",
    [
        {"type": "text", "type_data": {"invalid_field": "value"}},
        {"type": "mention", "type_data": {"type": "invalid_type"}},
    ],
)
def test_rich_text_validation_errors(invalid_data):
    """Test invalid data should raise ValidationError."""
    with pytest.raises(ValidationError):
        RichText.model_validate(invalid_data)


# ------------------ SERIALIZATION TESTS ------------------ #
@pytest.mark.parametrize(
    "clz, test_data",
    [
        (
            RichText,
            [
                (
                    RichText(
                        type=RichTextType.TEXT,
                        type_data=Text(content="Test Text", link="https://notion.so"),
                        annotations=Annotations(),
                        plain_text="Test Text",
                        href="https://notion.so",
                    ),
                    {
                        "type": "text",
                        "text": {
                            "content": "Test Text",
                            "link": "https://notion.so",
                        },
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default",
                        },
                        "plain_text": "Test Text",
                        "href": "https://notion.so",
                    },
                ),
            ],
        ),
        (
            RichText,
            [
                (
                    RichText(
                        type=RichTextType.EQUATION,
                        type_data=NotionEquation(expression="E = mc^2"),
                        annotations=Annotations(),
                        plain_text="E = mc^2",
                        href=None,
                    ),
                    {
                        "type": "equation",
                        "equation": {
                            "expression": "E = mc^2",
                        },
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default",
                        },
                        "plain_text": "E = mc^2",
                        "href": None,
                    },
                ),
            ],
        ),
        (
            RichText,
            [
                (
                    RichText(
                        type=RichTextType.MENTION,
                        type_data=MentionUser(
                            type_data=User(id="a7db80bd-b3e3-4394-b134-a21b05412c7c")
                        ),
                        annotations=Annotations(
                            bold=False,
                            italic=True,
                            strikethrough=False,
                            underline=True,
                            code=False,
                            color=Color.BLUE,
                        ),
                        plain_text="Test User",
                        href=None,
                    ),
                    {
                        "type": "mention",
                        "mention": {
                            "type": "user",
                            "user": {
                                "object": "user",
                                "id": "a7db80bd-b3e3-4394-b134-a21b05412c7c",
                            },
                        },
                        "annotations": {
                            "bold": False,
                            "italic": True,
                            "strikethrough": False,
                            "underline": True,
                            "code": False,
                            "color": "blue",
                        },
                        "plain_text": "Test User",
                    },
                ),
            ],
        ),
        (
            RichText,
            [
                (
                    RichText(
                        type=RichTextType.MENTION,
                        type_data=MentionDateTemplate(
                            type_data=TemplateMentionDate(type_data="now")
                        ),
                        annotations=Annotations(),
                        plain_text="now",
                        href=None,
                    ),
                    {
                        "type": "mention",
                        "mention": {
                            "type": "template_mention",
                            "template_mention": {
                                "type": "template_mention_date",
                                "template_mention_date": "now",
                            },
                        },
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default",
                        },
                        "plain_text": "now",
                    },
                )
            ],
        ),
        (
            RichText,
            [
                (
                    RichText(
                        type=RichTextType.MENTION,
                        type_data=MentionUserTemplate(),
                        annotations=Annotations(),
                        plain_text="now",
                        href=None,
                    ),
                    {
                        "type": "mention",
                        "mention": {
                            "type": "template_mention",
                            "template_mention": {
                                "type": "template_mention_user",
                                "template_mention_user": "me",
                            },
                        },
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default",
                        },
                        "plain_text": "now",
                    },
                )
            ],
        ),
    ],
    ids=[
        "RichTextText",
        "RichTextEquation",
        "RichTextMentionUser",
        "RichTextMentionTemplateDate",
        "RichTextMentionTemplateUser",
    ],
)
def test_models_serialization(clz: type, test_data: list[tuple[BaseModel, dict, ...]]):
    PydanticModelTester(clz, test_data).run_all_tests()
