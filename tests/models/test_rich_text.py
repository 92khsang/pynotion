from uuid import UUID

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
    TemplateMentionDate,
    TemplateMentionUser,
    RichText,
)
from pynotion.models.types import (
    NotionEquation,
    NotionLink,
    NotionDate,
    Color,
    NotionUserRef,
    NotionObjectRef,
    BackgroundColor,
    ObjectType,
)
from tests.models.model_test_utils import PydanticModelTester


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
    "mention_class, type_value, type_object, type_asdict",
    [
        (
            MentionDatabase,
            MentionType.DATABASE,
            NotionObjectRef(id="d7db80bd-b3e3-4394-b134-a21b05412c7c"),
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
            NotionObjectRef(id="a7db80bd-b3e3-4394-b134-a21b05412c7c"),
            {
                "type": "page",
                "page": {"id": "a7db80bd-b3e3-4394-b134-a21b05412c7c"},
            },
        ),
        (
            MentionDateTemplate,
            MentionType.TEMPLATE_MENTION,
            TemplateMentionDate(type_object="today"),
            {
                "type": "template_mention",
                "template_mention": {
                    "type": "template_mention_date",
                    "type_object": "today",
                },
            },
        ),
        (
            MentionUserTemplate,
            MentionType.TEMPLATE_MENTION,
            TemplateMentionUser(type_object="me"),
            {
                "type": "template_mention",
                "template_mention": {
                    "type": "template_mention_user",
                    "type_object": "me",
                },
            },
        ),
        (
            MentionUser,
            MentionType.USER,
            NotionUserRef(id="a7db80bd-b3e3-4394-b134-a21b05412c7c"),
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
def test_mentions(mention_class, type_value, type_object, type_asdict):
    """Test Mention-based models."""
    mention_data = mention_class(type_object=type_object)
    assert mention_data.type == type_value
    assert mention_data.type_object == type_object
    assert getattr(mention_data, type_value) == type_object
    assert eval(f"mention_data.{type_value}") == type_object
    assert mention_data == mention_class.model_validate(type_asdict)


@pytest.mark.parametrize(
    "type_object",
    [
        NotionObjectRef(id="d7db80bd-b3e3-4394-b134-a21b05412c7c"),
        NotionDate(start="2022-01-01", end="2022-01-31"),
        NotionLink(url="https://notion.so"),
        TemplateMentionDate(type_object="today"),
        TemplateMentionUser(type_object="me"),
        NotionUserRef(id="a7db80bd-b3e3-4394-b134-a21b05412c7c"),
    ],
)
def test_invalid_mentions(type_object):
    """Test invalid Mention-based models."""
    mention_classes: list[tuple[type, type]] = [
        (MentionDatabase, NotionObjectRef),
        (MentionDate, NotionDate),
        (MentionLinkPreview, NotionLink),
        (MentionPage, NotionObjectRef),
        (MentionDateTemplate, TemplateMentionDate),
        (MentionUser, NotionUserRef),
    ]

    for mention_class, mention_data_class in mention_classes:
        if mention_data_class != type(type_object):
            with pytest.raises((ValueError, TypeError)):
                mention_class(type_object=type_object)


# ------------------ RICH TEXT TESTS ------------------ #
@pytest.mark.parametrize(
    "rich_text_type, annotations, plain_text, href, type_object",
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
            MentionUser(
                type_object=NotionUserRef(id="a7db80bd-b3e3-4394-b134-a21b05412c7c")
            ),
        ),
        (
            RichTextType.MENTION,
            Annotations(),
            "Test Page",
            None,
            MentionPage(
                type_object=NotionObjectRef(id="d7db80bd-b3e3-4394-b134-a21b05412c7c")
            ),
        ),
        (
            RichTextType.MENTION,
            Annotations(),
            "Test Database",
            None,
            MentionDatabase(
                type_object=NotionObjectRef(id="d7db80bd-b3e3-4394-b134-a21b05412c7c")
            ),
        ),
        (
            RichTextType.MENTION,
            Annotations(),
            "Test Date",
            None,
            MentionDate(type_object=NotionDate(start="2022-01-01", end="2022-01-31")),
        ),
        (
            RichTextType.MENTION,
            Annotations(),
            "Test Link Preview",
            None,
            MentionLinkPreview(type_object=NotionLink(url="https://notion.so")),
        ),
        (
            RichTextType.MENTION,
            Annotations(),
            "Test Template",
            None,
            MentionDateTemplate(type_object=TemplateMentionDate(type_object="today")),
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
def test_rich_text(rich_text_type, annotations, plain_text, href, type_object):
    """Test RichText model with a text type."""
    rich_text = RichText(
        type=rich_text_type,
        type_object=type_object,
        annotations=annotations,
        plain_text=plain_text,
        href=href,
    )

    assert rich_text.type == rich_text_type
    assert rich_text.type_object == type_object
    assert rich_text.annotations == annotations
    assert rich_text.plain_text == plain_text
    assert rich_text.href == href


# ------------------ VALIDATION TESTS ------------------ #
@pytest.mark.parametrize(
    "invalid_data",
    [
        {"type": "text", "type_object": {"invalid_field": "value"}},
        {"type": "mention", "type_object": {"type": "invalid_type"}},
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
            (
                {
                    "type": RichTextType.TEXT,
                    "type_object": Text(content="Test Text", link="https://notion.so"),
                    "annotations": Annotations(bold=True),
                    "read_only_plain_text": "Test Text",
                    "read_only_href": "https://notion.so",
                },
                {
                    "type": RichTextType.TEXT,
                    "text": {
                        "content": "Test Text",
                        "link": {
                            "url": "https://notion.so",
                        },
                    },
                    "annotations": {
                        "bold": True,
                        "italic": False,
                        "strikethrough": False,
                        "underline": False,
                        "code": False,
                        "color": Color.DEFAULT,
                    },
                    "plain_text": "Test Text",
                    "href": "https://notion.so",
                },
                {
                    "type": "text",
                    "text": {
                        "content": "Test Text",
                        "link": {"url": "https://notion.so"},
                    },
                    "annotations": {"bold": True},
                    "plain_text": "Test Text",
                    "href": "https://notion.so",
                },
            ),
        ),
        (
            RichText,
            (
                {
                    "type": RichTextType.EQUATION,
                    "type_object": NotionEquation(expression="E = mc^2"),
                    "annotations": Annotations(bold=True, italic=True, color=Color.RED),
                    "read_only_plain_text": "E = mc^2",
                    "read_only_href": None,
                },
                {
                    "type": RichTextType.EQUATION,
                    "equation": {
                        "expression": "E = mc^2",
                    },
                    "annotations": {
                        "bold": True,
                        "italic": True,
                        "strikethrough": False,
                        "underline": False,
                        "code": False,
                        "color": Color.RED,
                    },
                    "plain_text": "E = mc^2",
                },
                {
                    "type": "equation",
                    "equation": {
                        "expression": "E = mc^2",
                    },
                    "annotations": {
                        "bold": True,
                        "italic": True,
                        "color": "red",
                    },
                    "plain_text": "E = mc^2",
                },
            ),
        ),
        (
            RichText,
            (
                {
                    "type": RichTextType.MENTION,
                    "type_object": MentionUser(
                        type_object=NotionUserRef(
                            id="a7db80bd-b3e3-4394-b134-a21b05412c7c"
                        )
                    ),
                    "annotations": Annotations(
                        bold=True,
                        italic=False,
                        strikethrough=True,
                        underline=False,
                        code=True,
                        color=BackgroundColor.RED_BACKGROUND,
                    ),
                    "read_only_plain_text": "Test User",
                },
                {
                    "type": RichTextType.MENTION,
                    "mention": {
                        "type": MentionType.USER,
                        "user": {
                            "object": ObjectType.USER,
                            "id": UUID("a7db80bd-b3e3-4394-b134-a21b05412c7c"),
                        },
                    },
                    "annotations": {
                        "bold": True,
                        "italic": False,
                        "strikethrough": True,
                        "underline": False,
                        "code": True,
                        "color": BackgroundColor.RED_BACKGROUND,
                    },
                    "plain_text": "Test User",
                },
                {
                    "type": "mention",
                    "mention": {
                        "type": MentionType.USER.value,
                        "user": {
                            "object": ObjectType.USER.value,
                            "id": "a7db80bd-b3e3-4394-b134-a21b05412c7c",
                        },
                    },
                    "annotations": {
                        "bold": True,
                        "strikethrough": True,
                        "code": True,
                        "color": BackgroundColor.RED_BACKGROUND.value,
                    },
                    "plain_text": "Test User",
                },
            ),
        ),
        (
            RichText,
            (
                {
                    "type": RichTextType.MENTION,
                    "type_object": MentionDateTemplate(
                        type_object=TemplateMentionDate(type_object="now")
                    ),
                    "annotations": Annotations(
                        italic=True, underline=True, color=Color.YELLOW
                    ),
                    "read_only_plain_text": "now",
                    "read_only_href": None,
                },
                {
                    "type": RichTextType.MENTION,
                    "mention": {
                        "type": MentionType.TEMPLATE_MENTION,
                        "template_mention": {
                            "type": TemplateMentionType.TEMPLATE_MENTION_DATE,
                            "template_mention_date": "now",
                        },
                    },
                    "annotations": {
                        "bold": False,
                        "italic": True,
                        "strikethrough": False,
                        "underline": True,
                        "code": False,
                        "color": Color.YELLOW,
                    },
                    "plain_text": "now",
                },
                {
                    "type": RichTextType.MENTION.value,
                    "mention": {
                        "type": MentionType.TEMPLATE_MENTION.value,
                        "template_mention": {
                            "type": TemplateMentionType.TEMPLATE_MENTION_DATE.value,
                            "template_mention_date": "now",
                        },
                    },
                    "annotations": {
                        "italic": True,
                        "underline": True,
                        "color": Color.YELLOW.value,
                    },
                    "plain_text": "now",
                },
            ),
        ),
        (
            RichText,
            (
                {
                    "type": RichTextType.MENTION,
                    "type_object": MentionUserTemplate(
                        type_object=TemplateMentionUser(type_object="me")
                    ),
                    "annotations": Annotations(
                        strikethrough=True, code=True, color=Color.PURPLE
                    ),
                    "read_only_plain_text": "now",
                    "read_only_href": None,
                },
                {
                    "type": RichTextType.MENTION,
                    "mention": {
                        "type": MentionType.TEMPLATE_MENTION,
                        "template_mention": {
                            "type": TemplateMentionType.TEMPLATE_MENTION_USER,
                            "template_mention_user": "me",
                        },
                    },
                    "annotations": {
                        "bold": False,
                        "italic": False,
                        "strikethrough": True,
                        "underline": False,
                        "code": True,
                        "color": Color.PURPLE,
                    },
                    "plain_text": "now",
                },
                {
                    "type": RichTextType.MENTION.value,
                    "mention": {
                        "type": MentionType.TEMPLATE_MENTION.value,
                        "template_mention": {
                            "type": TemplateMentionType.TEMPLATE_MENTION_USER.value,
                            "template_mention_user": "me",
                        },
                    },
                    "annotations": {
                        "strikethrough": True,
                        "code": True,
                        "color": Color.PURPLE.value,
                    },
                    "plain_text": "now",
                },
            ),
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
def test_models_serialization(clz: type[BaseModel], test_data: tuple[dict, dict, dict]):
    PydanticModelTester(clz, test_data).run_all_tests()
