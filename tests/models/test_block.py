import uuid
from uuid import uuid4

import pytest
from pydantic import ValidationError, BaseModel

from pynotion.models.block import (
    BlockType,
    BookmarkBlock,
    CalloutBlock,
    RichText,
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
    ParagraphBlock,
    ChildDatabaseBlock,
    QuoteBlock,
    DividerBlock,
    Block,
)
from pynotion.models.rich_text import Text, RichTextType, Annotations
from pynotion.models.types import (
    Color,
    EmojiType,
    NotionLink,
    BackgroundColor,
    NotionExternalFile,
    ObjectType,
)
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
                        type_object=Text(content="Bookmark Caption"),
                    )
                ],
            },
        ),
        (
            ParagraphBlock,
            {
                "rich_text": [
                    RichText(
                        type=RichTextType.TEXT,
                        type_object=Text(content="TextBase Text"),
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
                        type_object=Text(content="Callout Text"),
                    )
                ],
                "icon": NotionEmoji(type=EmojiType.EMOJI, type_object="🔥"),
                "color": Color.PINK,
            },
        ),
        (ChildDatabaseBlock, {"title": "Database Title"}),
        (
            CodeBlock,
            {
                "caption": [
                    RichText(
                        type=RichTextType.TEXT,
                        type_object=Text(content="Code Caption"),
                    )
                ],
                "rich_text": [
                    RichText(
                        type=RichTextType.TEXT,
                        type_object=Text(content="print('Hello')"),
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
                "external": NotionExternalFile(
                    url="https://companywebsite.com/files/doc.txt"
                ),
            },
        ),
        (
            HeadingBlock,
            {
                "rich_text": [
                    RichText(
                        type=RichTextType.TEXT,
                        type_object=Text(content="Heading Text"),
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
                    RichText(
                        type=RichTextType.TEXT,
                        type_object=Text(content="Cell Text"),
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
        (BookmarkBlock, {"url": None, "caption": []}),  # URL should not be None
        (
            BookmarkBlock,
            {"url": "https://example.com", "caption": "Invalid Type"},
        ),  # Caption should be a list
        (
            QuoteBlock,
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
            {"caption": [], "type": "external", "type_object": None},
        ),  # type_object is required
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
            (
                {
                    "url": "https://example.com",
                    "caption": [
                        RichText(
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
            CalloutBlock,
            (
                {
                    "rich_text": [
                        RichText(
                            type=RichTextType.TEXT,
                            type_object=Text(content="Callout Text"),
                        )
                    ],
                    "icon": NotionEmoji(type=EmojiType.EMOJI, type_object="🔥"),
                    "color": Color.PINK,
                },
                {
                    "rich_text": [
                        {
                            "type": RichTextType.TEXT,
                            "text": {"content": "Callout Text"},
                            "annotations": Annotations().model_dump(),
                        }
                    ],
                    "icon": {"type": EmojiType.EMOJI, "emoji": "🔥"},
                    "color": Color.PINK,
                },
                {
                    "rich_text": [
                        {
                            "type": RichTextType.TEXT.value,
                            "text": {"content": "Callout Text"},
                        }
                    ],
                    "icon": {"type": EmojiType.EMOJI.value, "emoji": "🔥"},
                    "color": Color.PINK.value,
                },
            ),
        ),
        (
            CodeBlock,
            (
                {
                    "caption": [
                        RichText(
                            type=RichTextType.TEXT,
                            type_object=Text(content="Code Caption"),
                        )
                    ],
                    "rich_text": [
                        RichText(
                            type=RichTextType.TEXT,
                            type_object=Text(content="print('Hello')"),
                        )
                    ],
                    "language": ProgrammingLanguage.PYTHON,
                },
                {
                    "caption": [
                        {
                            "type": RichTextType.TEXT,
                            "text": {"content": "Code Caption"},
                            "annotations": Annotations().model_dump(),
                        }
                    ],
                    "rich_text": [
                        {
                            "type": RichTextType.TEXT,
                            "text": {"content": "print('Hello')"},
                            "annotations": Annotations().model_dump(),
                        }
                    ],
                    "language": ProgrammingLanguage.PYTHON,
                },
                {
                    "caption": [
                        {
                            "type": RichTextType.TEXT.value,
                            "text": {"content": "Code Caption"},
                        }
                    ],
                    "rich_text": [
                        {
                            "type": RichTextType.TEXT.value,
                            "text": {"content": "print('Hello')"},
                        }
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
            ToDoBlock,
            (
                {
                    "rich_text": [
                        RichText(
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
            Block,
            (
                {
                    "type": BlockType.PARAGRAPH,
                    "type_object": ParagraphBlock(rich_text=[]),
                    "has_children": False,
                },
                {
                    "object": ObjectType.BLOCK,
                    "type": BlockType.PARAGRAPH,
                    "paragraph": {
                        "rich_text": [],
                        "color": Color.DEFAULT,
                        "children": [],
                    },
                    "has_children": False,
                },
                {
                    "object": ObjectType.BLOCK.value,
                    "type": BlockType.PARAGRAPH.value,
                    "paragraph": {},
                    "has_children": False,
                },
            ),
        ),
        (
            Block,
            (
                {
                    "type": BlockType.CODE,
                    "type_object": CodeBlock(
                        caption=[
                            RichText(
                                type=RichTextType.TEXT,
                                type_object=Text(content="Code Caption"),
                            )
                        ],
                        rich_text=[
                            RichText(
                                type=RichTextType.TEXT,
                                type_object=Text(content="print('Hello')"),
                            )
                        ],
                        language=ProgrammingLanguage.PYTHON,
                    ),
                    "has_children": False,
                },
                {
                    "object": ObjectType.BLOCK,
                    "type": BlockType.CODE,
                    "code": {
                        "caption": [
                            {
                                "type": RichTextType.TEXT,
                                "text": {"content": "Code Caption"},
                                "annotations": Annotations().model_dump(),
                            }
                        ],
                        "rich_text": [
                            {
                                "type": RichTextType.TEXT,
                                "text": {"content": "print('Hello')"},
                                "annotations": Annotations().model_dump(),
                            }
                        ],
                        "language": ProgrammingLanguage.PYTHON,
                    },
                    "has_children": False,
                },
                {
                    "object": ObjectType.BLOCK.value,
                    "type": BlockType.CODE.value,
                    "code": {
                        "caption": [
                            {
                                "type": RichTextType.TEXT.value,
                                "text": {"content": "Code Caption"},
                            }
                        ],
                        "rich_text": [
                            {
                                "type": RichTextType.TEXT.value,
                                "text": {"content": "print('Hello')"},
                            }
                        ],
                        "language": ProgrammingLanguage.PYTHON.value,
                    },
                    "has_children": False,
                },
            ),
        ),
        (
            Block,
            (
                {
                    "type": BlockType.DIVIDER,
                    "type_object": {},
                },
                {
                    "object": ObjectType.BLOCK,
                    "type": BlockType.DIVIDER,
                    "divider": {},
                },
                {
                    "object": ObjectType.BLOCK.value,
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
