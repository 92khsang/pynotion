from uuid import UUID

import pytest
from pydantic import ValidationError

from pynotion.models.object import NotionObjectType
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
    assert sample_annotations.italic is False
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
    "clz, invalid_data, expected_error",
    [
        (
            TxTextRichText,
            {"type": "text", "text": {"invalid_field": "value"}},
            "2 validation errors for",
        ),
        (
            TxMentionRichText,
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
    "annotated_clz, expected_clz, input_data",
    [
        (
            TxRichText,
            TxTextRichText,
            {
                "type": "text",
                "text": {
                    "content": "Food discussion table place capital.",
                    "link": {"url": "http://booth-cooper.com/"},
                },
            },
        ),
        (
            TxRichText,
            TxEquationRichText,
            {
                "annotations": {
                    "bold": True,
                    "italic": False,
                    "strikethrough": False,
                    "underline": False,
                    "code": True,
                    "color": "brown",
                },
                "type": "equation",
                "equation": {
                    "expression": "Organization series protect paper figure though want cost. Item computer TV forward option next leader. Area attorney everyone although.\nMillion product treat save forward bank. Whether age open leg."
                },
            },
        ),
        (
            TxRichText,
            TxMentionRichText,
            {
                "annotations": {
                    "bold": True,
                    "italic": False,
                    "strikethrough": True,
                    "underline": True,
                    "code": True,
                    "color": "brown",
                },
                "type": "mention",
                "mention": {
                    "type": "database",
                    "database": {"id": "1bf3dcc5-be6b-441c-91c6-b3c0730edb63"},
                },
            },
        ),
    ],
)
def test_tx_rich_text_discriminated_model(
    annotated_clz: type, expected_clz: type, input_data: dict
):
    """Test valid User model instantiation with the type 'person' or 'bot'."""
    DiscriminatedModelTester(annotated_clz, expected_clz, **input_data).run_all_tests()


@pytest.mark.parametrize(
    "annotated_clz, expected_clz, input_data",
    [
        (
            RxRichText,
            RxTextRichText,
            {
                "annotations": {
                    "bold": True,
                    "italic": False,
                    "strikethrough": True,
                    "underline": True,
                    "code": False,
                    "color": "red",
                },
                "plain_text": "Little be environment. Our finally arrive.",
                "href": "http://www.johnson.info/",
                "type": "text",
                "text": {
                    "content": "Require already available significant through.",
                    "link": {"url": "http://hayes.net/"},
                },
            },
        ),
        (
            RxRichText,
            RxEquationRichText,
            {
                "annotations": {
                    "bold": True,
                    "italic": False,
                    "strikethrough": True,
                    "underline": True,
                    "code": False,
                    "color": "red",
                },
                "plain_text": "Little be environment. Our finally arrive.",
                "href": "https://taylor-hansen.com/",
                "type": "equation",
                "equation": {
                    "expression": "Factor language chair blood play he. Near together between protect.\nTwo stock serve never government life onto. Really think appear interview before spend."
                },
            },
        ),
        (
            RxRichText,
            RxMentionRichText,
            {
                "annotations": {
                    "bold": True,
                    "italic": False,
                    "strikethrough": True,
                    "underline": True,
                    "code": False,
                    "color": "red",
                },
                "plain_text": "Little be environment. Our finally arrive.",
                "href": "http://murphy.biz/",
                "type": "mention",
                "mention": {
                    "type": "database",
                    "database": {"id": "133d621d-f0b0-4996-bb4e-8a536ea802e3"},
                },
            },
        ),
    ],
)
def test_rx_rich_text_discriminated_model(
    annotated_clz: type, expected_clz: type, input_data: dict
):
    """Test valid User model instantiation with the type 'person' or 'bot'."""
    DiscriminatedModelTester(annotated_clz, expected_clz, **input_data).run_all_tests()


@pytest.mark.parametrize(
    "clz, test_data",
    [
        (
            TxTextRichText,
            (
                {
                    'annotations': Annotations(
                        bold=False,
                        italic=False,
                        strikethrough=False,
                        underline=False,
                        code=False,
                        color=Color.YELLOW,
                    ),
                    'type': RichTextType.TEXT,
                    'text': Text(
                        content='My factor page rate exist put.',
                        link=NotionUrlObject(url='http://www.armstrong.com/'),
                    ),
                },
                {
                    'annotations': {
                        'bold': False,
                        'italic': False,
                        'strikethrough': False,
                        'underline': False,
                        'code': False,
                        'color': Color.YELLOW,
                    },
                    'type': RichTextType.TEXT,
                    'text': {
                        'content': 'My factor page rate exist put.',
                        'link': {'url': 'http://www.armstrong.com/'},
                    },
                },
                {
                    "annotations": {
                        "bold": False,
                        "italic": False,
                        "strikethrough": False,
                        "underline": False,
                        "code": False,
                        "color": "yellow",
                    },
                    "type": "text",
                    "text": {
                        "content": "My factor page rate exist put.",
                        "link": {"url": "http://www.armstrong.com/"},
                    },
                },
            ),
        ),
        (
            TxEquationRichText,
            (
                {
                    'annotations': None,
                    'type': RichTextType.EQUATION,
                    'equation': Equation(
                        expression='Very among late husband question prove either main. Be by person seven science he.\nBeat someone central kind usually. Respond much despite reach half watch party example.'
                    ),
                },
                {
                    'type': RichTextType.EQUATION,
                    'equation': {
                        'expression': 'Very among late husband question prove either main. Be by person seven science he.\nBeat someone central kind usually. Respond much despite reach half watch party example.'
                    },
                },
                {
                    "type": "equation",
                    "equation": {
                        "expression": "Very among late husband question prove either main. Be by person seven science he.\nBeat someone central kind usually. Respond much despite reach half watch party example."
                    },
                },
            ),
        ),
        (
            TxMentionRichText,
            (
                {
                    'annotations': Annotations(
                        bold=True,
                        italic=True,
                        strikethrough=False,
                        underline=False,
                        code=True,
                        color=Color.YELLOW,
                    ),
                    'type': RichTextType.MENTION,
                    'mention': TemplateMention(
                        type=MentionType.TEMPLATE_MENTION,
                        template_mention=TemplateMentionDate(
                            type=TemplateMentionType.TEMPLATE_MENTION_DATE,
                            template_mention_date='today',
                        ),
                    ),
                },
                {
                    'annotations': {
                        'bold': True,
                        'italic': True,
                        'strikethrough': False,
                        'underline': False,
                        'code': True,
                        'color': Color.YELLOW,
                    },
                    'type': RichTextType.MENTION,
                    'mention': {
                        'type': MentionType.TEMPLATE_MENTION,
                        'template_mention': {
                            'type': TemplateMentionType.TEMPLATE_MENTION_DATE,
                            'template_mention_date': 'today',
                        },
                    },
                },
                {
                    "annotations": {
                        "bold": True,
                        "italic": True,
                        "strikethrough": False,
                        "underline": False,
                        "code": True,
                        "color": "yellow",
                    },
                    "type": "mention",
                    "mention": {
                        "type": "template_mention",
                        "template_mention": {
                            "type": "template_mention_date",
                            "template_mention_date": "today",
                        },
                    },
                },
            ),
        ),
    ],
)
def test_tx_rich_models_serialization(
    clz: type[BaseNotionModel], test_data: tuple[dict, dict, dict]
):
    PydanticModelTester(clz, test_data).run_all_tests()


@pytest.mark.parametrize(
    "clz, test_data",
    [
        (
            RxTextRichText,
            (
                {
                    'annotations': Annotations(
                        bold=False,
                        italic=True,
                        strikethrough=False,
                        underline=True,
                        code=True,
                        color=Color.GRAY,
                    ),
                    'plain_text': 'Mind hot wait event.',
                    'href': 'https://hartman-villegas.com/',
                    'type': RichTextType.TEXT,
                    'text': Text(
                        content='Positive yeah how. Actually account challenge.',
                        link=NotionUrlObject(url='https://mcdaniel-robinson.com/'),
                    ),
                },
                {
                    'annotations': {
                        'bold': False,
                        'italic': True,
                        'strikethrough': False,
                        'underline': True,
                        'code': True,
                        'color': Color.GRAY,
                    },
                    'plain_text': 'Mind hot wait event.',
                    'href': 'https://hartman-villegas.com/',
                    'type': RichTextType.TEXT,
                    'text': {
                        'content': 'Positive yeah how. Actually account challenge.',
                        'link': {'url': 'https://mcdaniel-robinson.com/'},
                    },
                },
                {
                    "annotations": {
                        "bold": False,
                        "italic": True,
                        "strikethrough": False,
                        "underline": True,
                        "code": True,
                        "color": "gray",
                    },
                    "plain_text": "Mind hot wait event.",
                    "href": "https://hartman-villegas.com/",
                    "type": "text",
                    "text": {
                        "content": "Positive yeah how. Actually account challenge.",
                        "link": {"url": "https://mcdaniel-robinson.com/"},
                    },
                },
            ),
        ),
        (
            RxEquationRichText,
            (
                {
                    'annotations': Annotations(
                        bold=False,
                        italic=True,
                        strikethrough=False,
                        underline=True,
                        code=True,
                        color=Color.GRAY,
                    ),
                    'plain_text': 'Mind hot wait event.',
                    'href': 'https://kelley-harris.com/',
                    'type': RichTextType.EQUATION,
                    'equation': Equation(
                        expression='Other federal main star near actually receive theory. Buy project wear play.\nClose role Mr both fact. List class statement trial. Traditional compare and always month later else cell.'
                    ),
                },
                {
                    'annotations': {
                        'bold': False,
                        'italic': True,
                        'strikethrough': False,
                        'underline': True,
                        'code': True,
                        'color': Color.GRAY,
                    },
                    'plain_text': 'Mind hot wait event.',
                    'href': 'https://kelley-harris.com/',
                    'type': RichTextType.EQUATION,
                    'equation': {
                        'expression': 'Other federal main star near actually receive theory. Buy project wear play.\nClose role Mr both fact. List class statement trial. Traditional compare and always month later else cell.'
                    },
                },
                {
                    "annotations": {
                        "bold": False,
                        "italic": True,
                        "strikethrough": False,
                        "underline": True,
                        "code": True,
                        "color": "gray",
                    },
                    "plain_text": "Mind hot wait event.",
                    "href": "https://kelley-harris.com/",
                    "type": "equation",
                    "equation": {
                        "expression": "Other federal main star near actually receive theory. Buy project wear play.\nClose role Mr both fact. List class statement trial. Traditional compare and always month later else cell."
                    },
                },
            ),
        ),
        (
            RxMentionRichText,
            (
                {
                    'annotations': Annotations(
                        bold=False,
                        italic=True,
                        strikethrough=False,
                        underline=True,
                        code=True,
                        color=Color.GRAY,
                    ),
                    'plain_text': 'Mind hot wait event.',
                    'href': 'http://anderson.net/',
                    'type': RichTextType.MENTION,
                    'mention': RxUserMention(
                        type=MentionType.USER,
                        user=UserRef(
                            object=NotionObjectType.USER,
                            id=UUID('6a774092-f7b9-478e-a675-d8c67427b4cc'),
                        ),
                    ),
                },
                {
                    'annotations': {
                        'bold': False,
                        'italic': True,
                        'strikethrough': False,
                        'underline': True,
                        'code': True,
                        'color': Color.GRAY,
                    },
                    'plain_text': 'Mind hot wait event.',
                    'href': 'http://anderson.net/',
                    'type': RichTextType.MENTION,
                    'mention': {
                        'type': MentionType.USER,
                        'user': {
                            'object': NotionObjectType.USER,
                            'id': UUID('6a774092-f7b9-478e-a675-d8c67427b4cc'),
                        },
                    },
                },
                {
                    "annotations": {
                        "bold": False,
                        "italic": True,
                        "strikethrough": False,
                        "underline": True,
                        "code": True,
                        "color": "gray",
                    },
                    "plain_text": "Mind hot wait event.",
                    "href": "http://anderson.net/",
                    "type": "mention",
                    "mention": {
                        "type": "user",
                        "user": {
                            "object": "user",
                            "id": "6a774092-f7b9-478e-a675-d8c67427b4cc",
                        },
                    },
                },
            ),
        ),
    ],
)
def test_rx_rich_models_serialization(
    clz: type[BaseNotionModel], test_data: tuple[dict, dict, dict]
):
    PydanticModelTester(clz, test_data).run_all_tests()
