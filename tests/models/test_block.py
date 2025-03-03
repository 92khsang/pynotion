from uuid import uuid4

import pytest
from pydantic import ValidationError

from pynotion.models.block import (
    BlockType,
    BookmarkBlock,
    TextBaseBlock,
    CalloutBlock,
    ChildObjectBlock,
    RichText,
    Color,
    NotionEmoji,
    CodeBlock,
    ProgrammingLanguage,
    EmbedBlock,
    FileBlock,
    HeadingBlock,
    PdfBlock,
    TableBlock,
    TableRowBlock,
    TableContentBlock,
    ToDoBlock,
    SyncedFrom,
    SyncedBlock,
)
from pynotion.models.rich_text import Text, RichTextType
from pynotion.models.types import EmojiType, NotionLink, BackgroundColor
from tests.models.model_test_utils import PydanticModelTester


@pytest.mark.parametrize("block_type", list(BlockType))
def test_block_type_enum(block_type):
    assert isinstance(block_type, BlockType)


@pytest.mark.parametrize(
    "model_class, kwargs",
    [
        (
            BookmarkBlock,
            {
                "url": "https://example.com",
                "caption": [
                    RichText(
                        type=RichTextType.TEXT,
                        type_data=Text(content="Bookmark Caption"),
                    )
                ],
            },
        ),
        (
            TextBaseBlock,
            {
                "rich_text": [
                    RichText(
                        type=RichTextType.TEXT,
                        type_data=Text(content="TextBase Text"),
                    )
                ],
                "color": Color.BLUE,
                "children": [],
            },
        ),
        (
            CalloutBlock,
            {
                "rich_text": [
                    RichText(
                        type=RichTextType.TEXT,
                        type_data=Text(content="Callout Text"),
                    )
                ],
                "icon": NotionEmoji(type=EmojiType.EMOJI, type_data="🔥"),
                "color": Color.PINK,
            },
        ),
        (ChildObjectBlock, {"title": "Database Title"}),
        (
            CodeBlock,
            {
                "caption": [
                    RichText(
                        type=RichTextType.TEXT,
                        type_data=Text(content="Code Caption"),
                    )
                ],
                "rich_text": [
                    RichText(
                        type=RichTextType.TEXT,
                        type_data=Text(content="print('Hello')"),
                    )
                ],
                "language": ProgrammingLanguage.PYTHON,
            },
        ),
        (EmbedBlock, {"url": "https://example.com/embed"}),
        (
            FileBlock,
            {
                "caption": [],
                "name": "doc.txt",
                "type": "external",
                "external": NotionLink(url="https://companywebsite.com/files/doc.txt"),
            },
        ),
        (
            HeadingBlock,
            {
                "rich_text": [
                    RichText(
                        type=RichTextType.TEXT,
                        type_data=Text(content="Heading Text"),
                    )
                ],
                "color": Color.DEFAULT,
                "is_toggleable": True,
            },
        ),
        (
            PdfBlock,
            {
                "caption": [
                    RichText(
                        type=RichTextType.TEXT,
                        type_data=Text(content="PDF Caption"),
                    )
                ],
                "type": "external",
                "type_data": NotionLink(url="https://companywebsite.com/files/doc.pdf"),
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
                    RichText(
                        type=RichTextType.TEXT,
                        type_data=Text(content="Cell Text"),
                    )
                ],
            },
        ),
        (TableContentBlock, {"color": BackgroundColor.GRAY_BACKGROUND}),
        (
            ToDoBlock,
            {
                "rich_text": [
                    RichText(
                        type=RichTextType.TEXT,
                        type_data=Text(content="To Do Text"),
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
        (BookmarkBlock, {"url": None, "caption": []}),  # URL should not be None
        (
            BookmarkBlock,
            {"url": "https://example.com", "caption": "Invalid Type"},
        ),  # Caption should be a list
        (
            TextBaseBlock,
            {"rich_text": None, "color": Color.BLUE, "children": []},
        ),  # rich_text should be a list
        (
            CalloutBlock,
            {"rich_text": [], "icon": None, "color": Color.PINK},
        ),  # Icon is required
        (
            CodeBlock,
            {"caption": [], "rich_text": [], "language": None},
        ),  # Language is required
        (EmbedBlock, {"url": ""}),  # URL cannot be empty
        (
            FileBlock,
            {
                "caption": [],
                "name": None,
                "type": "external",
                "external": NotionLink(url="https://companywebsite.com/files/doc.txt"),
            },
        ),  # Name is required
        (
            HeadingBlock,
            {"rich_text": [], "color": Color.DEFAULT, "is_toggleable": None},
        ),  # is_toggleable required
        (
            PdfBlock,
            {"caption": [], "type": "external", "type_data": None},
        ),  # type_data is required
        (
            TableBlock,
            {"table_width": 0, "has_column_header": True, "has_row_header": False},
        ),  # Table width must be greater than 0
        (TableRowBlock, {"cells": None}),  # Cells should be a list
        (TableContentBlock, {"color": None}),  # Color is required
        (
            ToDoBlock,
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
            BookmarkBlock,
            [
                (
                    BookmarkBlock(
                        url="https://example.com",
                        caption=[
                            RichText(
                                type=RichTextType.TEXT,
                                type_data=Text(content="Bookmark Caption"),
                            )
                        ],
                    ),
                    {
                        "url": "https://example.com",
                        "caption": [
                            {
                                "type": "text",
                                "text": {"content": "Bookmark Caption"},
                            }
                        ],
                    },
                ),
            ],
        ),
        (
            CalloutBlock,
            [
                (
                    CalloutBlock(
                        rich_text=[
                            RichText(
                                type=RichTextType.TEXT,
                                type_data=Text(content="Callout Text"),
                            )
                        ],
                        icon=NotionEmoji(type=EmojiType.EMOJI, type_data="🔥"),
                        color=Color.PINK,
                    ),
                    {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": "Callout Text"},
                            }
                        ],
                        "icon": {"type": "emoji", "emoji": "🔥"},
                        "color": "pink",
                    },
                ),
            ],
        ),
        (
            CodeBlock,
            [
                (
                    CodeBlock(
                        caption=[
                            RichText(
                                type=RichTextType.TEXT,
                                type_data=Text(content="Code Caption"),
                            )
                        ],
                        rich_text=[
                            RichText(
                                type=RichTextType.TEXT,
                                type_data=Text(content="print('Hello')"),
                            )
                        ],
                        language=ProgrammingLanguage.PYTHON,
                    ),
                    {
                        "caption": [
                            {
                                "type": "text",
                                "text": {"content": "Code Caption"},
                            }
                        ],
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": "print('Hello')"},
                            }
                        ],
                        "language": "python",
                    },
                ),
            ],
        ),
        (
            TableBlock,
            [
                (
                    TableBlock(
                        table_width=3, has_column_header=True, has_row_header=False
                    ),
                    {
                        "table_width": 3,
                        "has_column_header": True,
                        "has_row_header": False,
                    },
                ),
            ],
        ),
        (
            ToDoBlock,
            [
                (
                    ToDoBlock(
                        rich_text=[
                            RichText(
                                type=RichTextType.TEXT,
                                type_data=Text(content="ToDo Text"),
                            )
                        ],
                        checked=True,
                    ),
                    {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": "ToDo Text"},
                            }
                        ],
                        "checked": True,
                    },
                ),
            ],
        ),
    ],
    ids=[
        "BookmarkBlockSerialization",
        "CalloutBlockSerialization",
        "CodeBlockSerialization",
        "TableBlockSerialization",
        "ToDoBlockSerialization",
    ],
)
def test_models_serialization(clz: type, test_data: list[tuple]):
    PydanticModelTester(clz, test_data).run_all_tests()
