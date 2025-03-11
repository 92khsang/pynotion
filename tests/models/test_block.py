import uuid
from datetime import datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError, BaseModel

from pynotion.models.block import (
    BlockType,
    ProgrammingLanguage,
    EmbedBlock,
    TableBlock,
    TableRowBlock,
    TableContentBlock,
    SyncedFrom,
    SyncedBlock,
    ChildDatabaseBlock,
    DividerBlock,
    TxBookmarkBlock,
    TxParagraphBlock,
    TxCalloutBlock,
    TxCodeBlock,
    TxFileBlock,
    TxHeadingBlock,
    TxPdfBlock,
    TxToDoBlock,
    TxQuoteBlock,
    RxCalloutBlock,
    RxCodeBlock,
    TxBlock,
    TxNumberedListItemBlock,
    RxBlock,
    RxHeadingBlock,
)
from pynotion.models.rich_text import (
    Text,
    RichTextType,
    Annotations,
    TxRichText,
    RxRichText,
    MentionUser,
    MentionType,
    Mention,
    MentionTemplate,
    TemplateMentionType,
)
from pynotion.models.types import (
    Color,
    EmojiType,
    BackgroundColor,
    NotionEmoji,
    NotionExternalFile,
    NotionLink,
    NotionParent,
    ParentType,
    NotionUserRef,
)
from tests.models.model_test_utils import PydanticModelTester


@pytest.mark.parametrize("block_type", list(BlockType))
def test_block_type_enum(block_type):
    assert isinstance(block_type, BlockType)


@pytest.mark.parametrize(
    "model_class, kwargs",
    [
        (
            TxBookmarkBlock,
            {
                "url": "https://example.com",
                "caption": [
                    TxRichText(
                        type=RichTextType.TEXT,
                        type_object=Text(content="Bookmark Caption"),
                    )
                ],
            },
        ),
        (
            TxParagraphBlock,
            {
                "rich_text": [
                    TxRichText(
                        type=RichTextType.TEXT,
                        type_object=Text(content="TextBase Text"),
                    )
                ],
                "color": Color.BLUE,
                "children": [],
            },
        ),
        (
            TxCalloutBlock,
            {
                "rich_text": [
                    TxRichText(
                        type=RichTextType.TEXT,
                        type_object=Text(content="Callout Text"),
                    )
                ],
                "icon": NotionEmoji(type=EmojiType.EMOJI, type_object="🔥"),
                "color": Color.PINK,
            },
        ),
        (ChildDatabaseBlock, {"title": "Database Title"}),
        (
            TxCodeBlock,
            {
                "caption": [
                    TxRichText(
                        type=RichTextType.TEXT,
                        type_object=Text(content="Code Caption"),
                    )
                ],
                "rich_text": [
                    TxRichText(
                        type=RichTextType.TEXT,
                        type_object=Text(content="print('Hello')"),
                    )
                ],
                "language": ProgrammingLanguage.PYTHON,
            },
        ),
        (EmbedBlock, {"url": "https://example.com/embed"}),
        (
            TxFileBlock,
            {
                "caption": [],
                "name": "doc.txt",
                "type": "external",
                "external": NotionExternalFile(
                    url="https://companywebsite.com/files/doc.txt"
                ),
            },
        ),
        (
            TxHeadingBlock,
            {
                "rich_text": [
                    TxRichText(
                        type=RichTextType.TEXT,
                        type_object=Text(content="Heading Text"),
                    )
                ],
                "color": Color.DEFAULT,
                "is_toggleable": True,
            },
        ),
        (
            TxPdfBlock,
            {
                "caption": [
                    TxRichText(
                        type=RichTextType.TEXT,
                        type_object=Text(content="PDF Caption"),
                    )
                ],
                "type": "external",
                "type_object": NotionExternalFile(
                    url="https://companywebsite.com/files/doc.pdf"
                ),
            },
        ),
        (
            TableBlock,
            {"table_width": 3, "has_column_header": True, "has_row_header": False},
        ),
        (
            TableRowBlock,
            {
                "cells": [
                    TxRichText(
                        type=RichTextType.TEXT,
                        type_object=Text(content="Cell Text"),
                    )
                ],
            },
        ),
        (TableContentBlock, {"color": BackgroundColor.GRAY_BACKGROUND}),
        (
            TxToDoBlock,
            {
                "rich_text": [
                    TxRichText(
                        type=RichTextType.TEXT,
                        type_object=Text(content="To Do Text"),
                    )
                ],
                "checked": True,
            },
        ),
    ],
)
def test_block_model_creation(model_class, kwargs):
    block = model_class(**kwargs)
    for key, value in kwargs.items():
        assert getattr(block, key) == value


@pytest.mark.parametrize(
    "synced_from, children, should_raise",
    [
        (None, [], False),
        (SyncedFrom(block_id=uuid4()), None, False),
        (None, None, True),
        (SyncedFrom(block_id=uuid4()), [], True),
    ],
)
def test_synced_block_validation(synced_from, children, should_raise):
    if should_raise:
        with pytest.raises(ValidationError):
            SyncedBlock(synced_from=synced_from, children=children)
    else:
        block = SyncedBlock(synced_from=synced_from, children=children)
        assert block.synced_from == synced_from
        assert block.children == children


@pytest.mark.parametrize(
    "invalid_data",
    [
        (TxBookmarkBlock, {"url": None, "caption": []}),  # URL should not be None
        (
            TxBookmarkBlock,
            {"url": "https://example.com", "caption": "Invalid Type"},
        ),  # Caption should be a list
        (
            TxQuoteBlock,
            {"rich_text": None, "color": Color.BLUE, "children": []},
        ),  # rich_text should be a list
        (
            TxCalloutBlock,
            {"rich_text": [], "icon": None, "color": Color.PINK},
        ),  # Icon is required
        (
            TxCodeBlock,
            {"caption": [], "rich_text": [], "language": None},
        ),  # Language is required
        (EmbedBlock, {"url": ""}),  # URL cannot be empty
        (
            TxFileBlock,
            {
                "caption": [],
                "name": None,
                "type": "external",
                "external": NotionLink(url="https://companywebsite.com/files/doc.txt"),
            },
        ),  # Name is required
        (
            TxHeadingBlock,
            {"rich_text": [], "color": Color.DEFAULT, "is_toggleable": None},
        ),  # is_toggleable required
        (
            TxPdfBlock,
            {"caption": [], "type": "external", "type_object": None},
        ),  # type_object is required
        (
            TableBlock,
            {"table_width": 0, "has_column_header": True, "has_row_header": False},
        ),  # Table width must be greater than 0
        (TableRowBlock, {"cells": None}),  # Cells should be a list
        (TableContentBlock, {"color": None}),  # Color is required
        (
            TxToDoBlock,
            {"rich_text": [], "checked": "Invalid Type"},
        ),  # Checked should be a boolean
    ],
)
def test_invalid_block_model_creation(invalid_data):
    model_class, kwargs = invalid_data
    with pytest.raises(ValidationError):
        model_class(**kwargs)


@pytest.mark.parametrize(
    "clz, test_data",
    [
        (
            TxBookmarkBlock,
            (
                {
                    "url": "https://example.com",
                    "caption": [
                        TxRichText(
                            type=RichTextType.TEXT,
                            type_object=Text(content="Bookmark Caption"),
                        )
                    ],
                },
                {
                    "url": "https://example.com",
                    "caption": [
                        {
                            "type": RichTextType.TEXT,
                            "text": {"content": "Bookmark Caption"},
                            "annotations": Annotations().model_dump(),
                        }
                    ],
                },
                {
                    "url": "https://example.com",
                    "caption": [
                        {
                            "type": RichTextType.TEXT.value,
                            "text": {"content": "Bookmark Caption"},
                        }
                    ],
                },
            ),
        ),
        (
            RxCalloutBlock,
            (
                {
                    "rich_text": [
                        RxRichText(
                            type=RichTextType.TEXT,
                            type_object=Text(
                                content="Callout Text",
                                link=NotionLink(url="https://example.com"),
                            ),
                            plain_text="Callout Text",
                            annotations=Annotations(
                                bold=True, color=BackgroundColor.GRAY_BACKGROUND
                            ),
                            href="https://example.com",
                        )
                    ],
                    "icon": NotionEmoji(type=EmojiType.EMOJI, type_object="🔥"),
                    "color": Color.PINK,
                },
                {
                    "rich_text": [
                        {
                            "type": RichTextType.TEXT,
                            "text": {
                                "content": "Callout Text",
                                "link": {"url": "https://example.com"},
                            },
                            "annotations": Annotations(
                                bold=True, color=BackgroundColor.GRAY_BACKGROUND
                            ).model_dump(),
                            "plain_text": "Callout Text",
                            "href": "https://example.com",
                        }
                    ],
                    "icon": {"type": EmojiType.EMOJI, "emoji": "🔥"},
                    "color": Color.PINK,
                },
                {
                    "rich_text": [
                        {
                            "type": RichTextType.TEXT.value,
                            "text": {
                                "content": "Callout Text",
                                "link": {"url": "https://example.com"},
                            },
                            "annotations": {
                                "bold": True,
                                "color": BackgroundColor.GRAY_BACKGROUND.value,
                            },
                            "plain_text": "Callout Text",
                            "href": "https://example.com",
                        }
                    ],
                    "icon": {"type": EmojiType.EMOJI.value, "emoji": "🔥"},
                    "color": Color.PINK.value,
                },
            ),
        ),
        (
            RxCodeBlock,
            (
                {
                    "caption": [
                        RxRichText(
                            type=RichTextType.MENTION,
                            type_object=Mention(
                                type=MentionType.USER,
                                type_object=MentionUser(
                                    object="user",
                                    id="a7db80bd-b3e3-4394-b134-a21b05412c7c",
                                ),
                            ),
                            annotations=Annotations(strikethrough=True, code=True),
                            plain_text=None,
                            href=None,
                        )
                    ],
                    "rich_text": [
                        RxRichText(
                            type=RichTextType.MENTION,
                            type_object=Mention(
                                type=MentionType.TEMPLATE_MENTION,
                                type_object=MentionTemplate(
                                    type=TemplateMentionType.TEMPLATE_MENTION_DATE,
                                    type_object="today",
                                ),
                            ),
                            annotations=Annotations(
                                underline=True, color=BackgroundColor.RED_BACKGROUND
                            ),
                            plain_text=None,
                            href=None,
                        )
                    ],
                    "language": ProgrammingLanguage.PYTHON,
                },
                {
                    "caption": [
                        {
                            "type": RichTextType.MENTION,
                            "mention": {
                                "type": MentionType.USER,
                                "user": {
                                    "id": uuid.UUID(
                                        "a7db80bd-b3e3-4394-b134-a21b05412c7c"
                                    ),
                                    "object": "user",
                                },
                            },
                            "annotations": Annotations(
                                strikethrough=True, code=True
                            ).model_dump(),
                        },
                    ],
                    "rich_text": [
                        {
                            "type": RichTextType.MENTION,
                            "mention": {
                                "type": MentionType.TEMPLATE_MENTION,
                                "template_mention": {
                                    "type": TemplateMentionType.TEMPLATE_MENTION_DATE,
                                    "template_mention_date": "today",
                                },
                            },
                            "annotations": Annotations(
                                underline=True, color=BackgroundColor.RED_BACKGROUND
                            ).model_dump(),
                        },
                    ],
                    "language": ProgrammingLanguage.PYTHON,
                },
                {
                    "caption": [
                        {
                            "type": RichTextType.MENTION.value,
                            "mention": {
                                "type": MentionType.USER.value,
                                "user": {
                                    "id": "a7db80bd-b3e3-4394-b134-a21b05412c7c",
                                    "object": "user",
                                },
                            },
                            "annotations": {
                                "strikethrough": True,
                                "code": True,
                            },
                        },
                    ],
                    "rich_text": [
                        {
                            "type": RichTextType.MENTION.value,
                            "mention": {
                                "type": MentionType.TEMPLATE_MENTION.value,
                                "template_mention": {
                                    "type": TemplateMentionType.TEMPLATE_MENTION_DATE.value,
                                    "template_mention_date": "today",
                                },
                            },
                            "annotations": {
                                "underline": True,
                                "color": BackgroundColor.RED_BACKGROUND.value,
                            },
                        },
                    ],
                    "language": ProgrammingLanguage.PYTHON.value,
                },
            ),
        ),
        (
            TableBlock,
            (
                {
                    "table_width": 3,
                    "has_column_header": True,
                    "has_row_header": False,
                },
                {
                    "table_width": 3,
                    "has_column_header": True,
                    "has_row_header": False,
                },
                {
                    "table_width": 3,
                    "has_column_header": True,
                    "has_row_header": False,
                },
            ),
        ),
        (
            TxToDoBlock,
            (
                {
                    "rich_text": [
                        TxRichText(
                            type=RichTextType.TEXT,
                            type_object=Text(content="ToDo Text"),
                        )
                    ],
                    "checked": True,
                },
                {
                    "rich_text": [
                        {
                            "type": RichTextType.TEXT,
                            "text": {"content": "ToDo Text"},
                            "annotations": Annotations().model_dump(),
                        }
                    ],
                    "color": Color.DEFAULT,
                    "children": [],
                    "checked": True,
                },
                {
                    "rich_text": [
                        {
                            "type": RichTextType.TEXT.value,
                            "text": {"content": "ToDo Text"},
                        }
                    ],
                    "checked": True,
                },
            ),
        ),
        (
            SyncedBlock,
            (
                {
                    "synced_from": SyncedFrom(
                        block_id="12345678-1234-1234-1234-123456789012"
                    ),
                },
                {
                    "synced_from": {
                        "block_id": uuid.UUID("12345678-1234-1234-1234-123456789012")
                    },
                },
                {
                    "synced_from": {"block_id": "12345678-1234-1234-1234-123456789012"},
                },
            ),
        ),
        (
            DividerBlock,
            (
                {},
                {},
                {},
            ),
        ),
        (
            TxBlock,
            (
                {
                    "object": "block",
                    "type": BlockType.NUMBERED_LIST_ITEM,
                    "numbered_list_item": TxNumberedListItemBlock(
                        rich_text=[
                            TxRichText(
                                type=RichTextType.TEXT,
                                type_object=Text(content="Numbered List Text"),
                            )
                        ],
                        children=[
                            TxBlock(
                                object="block",
                                type=BlockType.PARAGRAPH,
                                type_object=TxParagraphBlock(
                                    rich_text=[
                                        TxRichText(
                                            type=RichTextType.TEXT,
                                            type_object=Text(content="Paragraph Text"),
                                        )
                                    ]
                                ),
                            )
                        ],
                    ),
                },
                {
                    "object": "block",
                    "type": BlockType.NUMBERED_LIST_ITEM,
                    "numbered_list_item": {
                        "rich_text": [
                            {
                                "type": RichTextType.TEXT,
                                "text": {"content": "Numbered List Text"},
                                "annotations": Annotations().model_dump(),
                            }
                        ],
                        "color": Color.DEFAULT,
                        "children": [
                            {
                                "object": "block",
                                "type": BlockType.PARAGRAPH,
                                "paragraph": {
                                    "rich_text": [
                                        {
                                            "type": RichTextType.TEXT,
                                            "text": {"content": "Paragraph Text"},
                                            "annotations": Annotations().model_dump(),
                                        }
                                    ],
                                    "color": Color.DEFAULT,
                                    "children": [],
                                },
                            }
                        ],
                    },
                },
                {
                    "object": "block",
                    "type": BlockType.NUMBERED_LIST_ITEM.value,
                    "numbered_list_item": {
                        "rich_text": [
                            {
                                "type": RichTextType.TEXT.value,
                                "text": {"content": "Numbered List Text"},
                            }
                        ],
                        "children": [
                            {
                                "object": "block",
                                "type": BlockType.PARAGRAPH.value,
                                "paragraph": {
                                    "rich_text": [
                                        {
                                            "type": RichTextType.TEXT.value,
                                            "text": {"content": "Paragraph Text"},
                                        }
                                    ]
                                },
                            }
                        ],
                    },
                },
            ),
        ),
        (
            RxBlock,
            (
                {
                    "object": "block",
                    "id": "c02fc1d3-db8b-45c5-a222-27595b15aea7",
                    "parent": NotionParent(
                        type=ParentType.PAGE_ID,
                        type_object="59833787-2cf9-4fdf-8782-e53db20768a5",
                    ),
                    "created_time": "2022-03-01T19:05:00.000Z",
                    "last_edited_time": "2022-03-01T19:05:00.000Z",
                    "created_by": NotionUserRef(
                        object="user",
                        id="ee5f0f84-409a-440f-983a-a5315961c6e4",
                    ),
                    "last_edited_by": NotionUserRef(
                        object="user",
                        id="ee5f0f84-409a-440f-983a-a5315961c6e4",
                    ),
                    "archived": False,
                    "type": BlockType.HEADING_2,
                    "heading_2": RxHeadingBlock(
                        rich_text=[
                            RxRichText(
                                type=RichTextType.TEXT,
                                type_object=Text(content="Lacinato kale"),
                                plain_text="Lacinato kale",
                                annotations=Annotations(),
                                href=None,
                            )
                        ],
                        is_toggleable=False,
                    ),
                    "has_children": False,
                },
                {
                    "object": "block",
                    "type": BlockType.HEADING_2,
                    "heading_2": {
                        "rich_text": [
                            {
                                "type": RichTextType.TEXT,
                                "text": {"content": "Lacinato kale"},
                                "annotations": Annotations().model_dump(),
                                "plain_text": "Lacinato kale",
                            },
                        ],
                        "color": Color.DEFAULT,
                        "is_toggleable": False,
                    },
                    "parent": {
                        "type": ParentType.PAGE_ID,
                        "page_id": uuid.UUID("59833787-2cf9-4fdf-8782-e53db20768a5"),
                    },
                    "id": uuid.UUID("c02fc1d3-db8b-45c5-a222-27595b15aea7"),
                    "created_time": datetime.fromisoformat("2022-03-01T19:05:00.000Z"),
                    "last_edited_time": datetime.fromisoformat(
                        "2022-03-01T19:05:00.000Z"
                    ),
                    "created_by": {
                        "id": uuid.UUID("ee5f0f84-409a-440f-983a-a5315961c6e4"),
                        "object": "user",
                    },
                    "last_edited_by": {
                        "id": uuid.UUID("ee5f0f84-409a-440f-983a-a5315961c6e4"),
                        "object": "user",
                    },
                    "archived": False,
                    "in_trash": False,
                    "has_children": False,
                },
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": "Lacinato kale"},
                                "annotations": {},
                                "plain_text": "Lacinato kale",
                            }
                        ],
                        "is_toggleable": False,
                    },
                    "parent": {
                        "type": "page_id",
                        "page_id": "59833787-2cf9-4fdf-8782-e53db20768a5",
                    },
                    "id": "c02fc1d3-db8b-45c5-a222-27595b15aea7",
                    "created_time": "2022-03-01T19:05:00Z",
                    "last_edited_time": "2022-03-01T19:05:00Z",
                    "created_by": {
                        "object": "user",
                        "id": "ee5f0f84-409a-440f-983a-a5315961c6e4",
                    },
                    "last_edited_by": {
                        "object": "user",
                        "id": "ee5f0f84-409a-440f-983a-a5315961c6e4",
                    },
                    "archived": False,
                    "has_children": False,
                },
            ),
        ),
        (
            TxBlock,
            (
                {
                    "object": "block",
                    "type": BlockType.DIVIDER,
                    "type_object": {},
                },
                {
                    "object": "block",
                    "type": BlockType.DIVIDER,
                    "divider": {},
                },
                {
                    "object": "block",
                    "type": BlockType.DIVIDER.value,
                    "divider": {},
                },
            ),
        ),
    ],
    ids=[
        "BookmarkBlockSerialization",
        "CalloutBlockSerialization",
        "CodeBlockSerialization",
        "TableBlockSerialization",
        "ToDoBlockSerialization",
        "SyncedBlockSerialization",
        "DividerBlockSerialization",
        "ParagraphBlockSerialization",
        "CodeBlockSerialization",
        "DividerBlockSerialization",
    ],
)
def test_models_serialization(clz: type[BaseModel], test_data: tuple[dict, dict, dict]):
    PydanticModelTester(clz, test_data).run_all_tests()
