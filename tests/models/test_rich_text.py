from uuid import UUID

import pytest
from pydantic import ValidationError

from pynotion.models.rich_text import *
from pynotion.models.user import UserRef
from tests.models.model_test_utils import (
    DiscriminatedModelTester,
    PydanticModelTester,
)


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
    assert sample_annotations.italic is None
    assert sample_annotations.color == "red"

    with pytest.raises(ValueError):
        Annotations(color="invalid_color")


@pytest.mark.parametrize(
    "content, link",
    [
        ("Hello, Notion!", NotionUrlObject(url="https://notion.so")),
        ("Hello", None),
    ],
)
def test_text_model(content, link):
    """Test Text model instantiation and serialization."""
    sample_text = Text(content=content, link=link)
    assert sample_text.content == content
    if link:
        assert sample_text.link == link
    else:
        assert sample_text.link is None


def test_invalid_text_model():
    with pytest.raises(ValidationError):
        Text(content="Hello", link=NotionUrlObject(url="invalid_url"))

    with pytest.raises(ValidationError):
        Text(content=None)


@pytest.mark.parametrize(
    "annotated_clz, expected_clz, input_data",
    [
        (
            Mention,
            DatabaseMention,
            {
                "type": "database",
                "database": {
                    "id": "a7db80bd-b3e3-4394-b134-a21b05412c7c",
                },
            },
        ),
        (
            Mention,
            DateMention,
            {
                "type": "date",
                "date": {
                    "start": "2022-01-01",
                    "end": "2022-12-31",
                },
            },
        ),
        (
            Mention,
            LinkPreviewMention,
            {
                "type": "link_preview",
                "link_preview": {
                    "url": "https://notion.so",
                },
            },
        ),
        (
            Mention,
            PageMention,
            {
                "type": "page",
                "page": {
                    "id": "a7db80bd-b3e3-4394-b134-a21b05412c7c",
                },
            },
        ),
        (
            Mention,
            TemplateMention,
            {
                "type": "template_mention",
                "template_mention": {
                    "type": "template_mention_date",
                    "template_mention_date": "today",
                },
            },
        ),
        (
            RichText,
            TextRichText,
            {
                "type": "text",
                "text": {"content": "Test Text", "link": {"url": "https://notion.so"}},
                "annotations": {"bold": True, "color": "gray_background"},
                "plain_text": "Test Text",
                "href": "https://notion.so",
            },
        ),
        (
            RichText,
            EquationRichText,
            {
                "type": "equation",
                "equation": {"expression": "a = b + c"},
                "annotations": {"italic": True, "color": "gray"},
            },
        ),
        (
            RichText,
            MentionRichText,
            {
                "type": "mention",
                "mention": {
                    "type": "user",
                    "user": {
                        "object": "user",
                        "id": "a7db80bd-b3e3-4394-b134-a21b05412c7c",
                    },
                },
                "annotations": {"bold": True, "color": "gray_background"},
                "plain_text": "Test User",
                "href": "https://notion.so",
            },
        ),
    ],
    ids=[
        "mention_database",
        "mention_date",
        "mention_link_preview",
        "mention_page",
        "mention_template_mention",
        "rich_text_text",
        "rich_text_equation",
        "rich_text_mention_user",
    ],
)
def test_discriminated_model(annotated_clz: type, expected_clz: type, input_data: dict):
    """Test valid User model instantiation with the type 'person' or 'bot'."""
    DiscriminatedModelTester(annotated_clz, expected_clz, **input_data).run_all_tests()


@pytest.mark.parametrize(
    "clz, invalid_data, expected_error",
    [
        (
            TextRichText,
            {"type": "text", "text": {"invalid_field": "value"}},
            "2 validation errors for",
        ),
        (
            MentionRichText,
            {"type": "mention", "mention": {"type": "invalid_type"}},
            "1 validation error for",
        ),
    ],
)
def test_rich_text_validation_errors(clz, invalid_data, expected_error):
    """Test invalid data should raise ValidationError."""
    with pytest.raises(ValidationError, match=expected_error):
        clz.model_validate(invalid_data)


@pytest.mark.parametrize(
    "clz, test_data",
    [
        (
            TextRichText,
            (
                {
                    "type": RichTextType.TEXT,
                    "text": Text(
                        content="Test Text",
                        link=NotionUrlObject(url="https://notion.so"),
                    ),
                    "annotations": Annotations(bold=True),
                    "plain_text": "Test Text",
                    "href": "https://notion.so",
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
            EquationRichText,
            (
                {
                    "type": RichTextType.EQUATION,
                    "equation": Equation(expression="E = mc^2"),
                    "annotations": Annotations(bold=True, italic=True, color=Color.RED),
                    "plain_text": "E = mc^2",
                    "href": None,
                },
                {
                    "type": RichTextType.EQUATION,
                    "equation": {
                        "expression": "E = mc^2",
                    },
                    "annotations": {
                        "bold": True,
                        "italic": True,
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
            MentionRichText,
            (
                {
                    "type": RichTextType.MENTION,
                    "mention": UserMention(
                        type=MentionType.USER,
                        user=UserRef(
                            object="user", id="a7db80bd-b3e3-4394-b134-a21b05412c7c"
                        ),
                    ),
                    "annotations": Annotations(
                        bold=True,
                        italic=False,
                        strikethrough=True,
                        underline=False,
                        code=True,
                        color=BackgroundColor.RED_BACKGROUND,
                    ),
                    "plain_text": "Test User",
                    "href": None,
                },
                {
                    "type": RichTextType.MENTION,
                    "mention": {
                        "type": MentionType.USER,
                        "user": {
                            "object": "user",
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
                            "object": "user",
                            "id": "a7db80bd-b3e3-4394-b134-a21b05412c7c",
                        },
                    },
                    "annotations": {
                        "bold": True,
                        "italic": False,
                        "strikethrough": True,
                        "underline": False,
                        "code": True,
                        "color": BackgroundColor.RED_BACKGROUND.value,
                    },
                    "plain_text": "Test User",
                },
            ),
        ),
        (
            MentionRichText,
            (
                {
                    "type": RichTextType.MENTION,
                    "mention": TemplateMention(
                        type=MentionType.TEMPLATE_MENTION,
                        template_mention=TemplateMentionDate(
                            type=TemplateMentionType.TEMPLATE_MENTION_DATE,
                            template_mention_date="now",
                        ),
                    ),
                    "annotations": Annotations(
                        italic=True, underline=True, color=Color.YELLOW
                    ),
                    "plain_text": "now",
                    "href": None,
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
                        "italic": True,
                        "underline": True,
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
            MentionRichText,
            (
                {
                    "type": RichTextType.MENTION,
                    "mention": TemplateMention(
                        type=MentionType.TEMPLATE_MENTION,
                        template_mention=TemplateMentionUser(),
                    ),
                    "annotations": Annotations(
                        strikethrough=True, code=True, color=Color.PURPLE
                    ),
                    "plain_text": "now",
                    "href": None,
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
                        "strikethrough": True,
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
def test_models_serialization(
    clz: type[BaseNotionModel], test_data: tuple[dict, dict, dict]
):
    PydanticModelTester(clz, test_data).run_all_tests()
