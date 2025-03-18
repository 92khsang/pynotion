from uuid import UUID
from zoneinfo import ZoneInfo

import pytest
from pydantic import BaseModel, ValidationError

from pynotion.models.block import *
from pynotion.models.emoji import EmojiType, CustomEmoji, CustomEmojiObject
from pynotion.models.file import FileType, ExternalFileObject
from pynotion.models.object import NotionObjectRef
from pynotion.models.parent import ParentType, WorkspaceParent
from pynotion.models.rich_text import (
    TemplateMentionType,
    TemplateMentionDate,
    TemplateMention,
    MentionRichText,
    Annotations,
    RichTextType,
    MentionType,
    DateMention,
    Equation,
    EquationRichText,
    LinkPreviewMention,
    Text,
    TextRichText,
    DatabaseMention,
)
from pynotion.models.types import NotionDate
from tests.models.model_test_utils import DiscriminatedModelTester, PydanticModelTester


@pytest.mark.parametrize("block_type", list(BlockType))
def test_block_type_enum(block_type):
    assert isinstance(block_type, BlockType)


@pytest.mark.parametrize(
    "annotated_clz, expected_clz, input_data",
    [
        (
            Block,
            BookmarkBlock,
            {
                "object": "block",
                "type": "bookmark",
                "bookmark": {
                    "caption": [
                        {
                            "annotations": {"color": "orange_background"},
                            "plain_text": "ZUPXodHrFVyZkktikSMw",
                            "href": "https://manning.com/",
                            "type": "text",
                            "text": {
                                "content": "Exactly success wonder before by present.",
                                "link": {"url": "http://gardner.com/"},
                            },
                        }
                    ],
                    "url": "http://www.adams.com/",
                },
            },
        ),
        (
            Block,
            BreadcrumbBlock,
            {"object": "block", "type": "breadcrumb", "breadcrumb": {}},
        ),
        (
            Block,
            BulletListItemBlock,
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bullet_list_item": {
                    "rich_text": [
                        {
                            "annotations": {"color": "orange_background"},
                            "plain_text": "oVYWrfQcUZZdDZlIpAIB",
                            "href": "http://www.stokes.info/",
                            "type": "text",
                            "text": {
                                "content": "Exactly success wonder before by present.",
                                "link": {"url": "http://gardner.com/"},
                            },
                        }
                    ],
                    "color": "green_background",
                    "children": [
                        {
                            "object": "block",
                            "type": "child_database",
                            "child_database": {"title": "Gloria Murphy"},
                        }
                    ],
                },
            },
        ),
        (
            Block,
            CalloutBlock,
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [
                        {
                            "annotations": {"color": "orange_background"},
                            "href": "https://jensen.com/",
                            "type": "text",
                            "text": {
                                "content": "Exactly success wonder before by present.",
                                "link": {"url": "http://gardner.com/"},
                            },
                        },
                        {
                            "annotations": {"color": "orange_background"},
                            "plain_text": "CXALqfUuErIvXsspmdzB",
                            "href": "http://www.ryan.org/",
                            "type": "equation",
                            "equation": {
                                "expression": "Mrs very high long week prevent. Ok cause follow southern.\nSubject light notice sometimes night. Truth again face especially despite player. Be kitchen include serious girl performance region."
                            },
                        },
                    ],
                    "color": "purple",
                },
            },
        ),
        (
            Block,
            ChildDatabaseBlock,
            {
                "object": "block",
                "type": "child_database",
                "child_database": {"title": "Joseph Martinez"},
            },
        ),
        (
            Block,
            ChildPageBlock,
            {
                "object": "block",
                "type": "child_page",
                "child_page": {"title": "Richard Dominguez"},
            },
        ),
        (
            Block,
            CodeBlock,
            {
                "object": "block",
                "type": "code",
                "code": {
                    "caption": [],
                    "rich_text": [
                        {
                            "annotations": {"color": "orange_background"},
                            "plain_text": "yGzeqKFJHozBEQimadPl",
                            "href": "https://nelson.com/",
                            "type": "equation",
                            "equation": {
                                "expression": "Through get require none couple become. Student hard ahead raise thus morning soon.\nCatch somebody several treat. Feel pattern development history moment. Ago plan catch instead among painting."
                            },
                        }
                    ],
                    "language": "java",
                },
            },
        ),
        (Block, ColumnBlock, {"object": "block", "type": "column", "column": {}}),
        (
            Block,
            ColumnListBlock,
            {"object": "block", "type": "column_list", "column_list": {}},
        ),
        (Block, DividerBlock, {"object": "block", "type": "divider", "divider": {}}),
        (
            Block,
            EmbedBlock,
            {
                "object": "block",
                "type": "embed",
                "embed": {"url": "http://www.santiago.net/"},
            },
        ),
        (
            Block,
            EquationBlock,
            {
                "object": "block",
                "type": "equation",
                "equation": {"expression": "ZbesfMcXStsEnKQjqQcy"},
            },
        ),
        (
            Block,
            FileBlock,
            {
                "object": "block",
                "type": "file",
                "file": {
                    "type": "external",
                    "external": {"url": "https://www.ponce.org/"},
                    "caption": [
                        {
                            "annotations": {"color": "orange_background"},
                            "plain_text": "eeeGsiTSIFCevLCBkinX",
                            "href": "https://www.gomez.com/",
                            "type": "mention",
                            "mention": {
                                "type": "template_mention",
                                "template_mention": {
                                    "type": "template_mention_date",
                                    "template_mention_date": "now",
                                },
                            },
                        },
                        {
                            "annotations": {"color": "orange_background"},
                            "href": "https://www.hobbs.org/",
                            "type": "equation",
                            "equation": {
                                "expression": "Where tax high control truth subject give among. Operation tonight occur kitchen young west number moment.\nCapital blue fly century player say TV."
                            },
                        },
                    ],
                    "name": "Kenneth Martin",
                },
            },
        ),
        (
            Block,
            HeadingOneBlock,
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [
                        {
                            "annotations": {"color": "orange_background"},
                            "plain_text": "IQXBPJrSAnZZmYYTIsBk",
                            "href": "http://mccoy-schultz.com/",
                            "type": "equation",
                            "equation": {
                                "expression": "Raise president attention miss mission. Increase all forward firm these.\nIts mother town mind. Today heart smile under ten either add. Up red general in admit."
                            },
                        },
                        {
                            "annotations": {"color": "orange_background"},
                            "href": "https://www.henry.com/",
                            "type": "mention",
                            "mention": {
                                "type": "user",
                                "user": {
                                    "object": "user",
                                    "id": "dab841c9-8cac-4e63-b0fc-87bee80e552b",
                                    "name": "Emma Williams",
                                    "avatar_url": "https://www.romero.com/",
                                    "type": "bot",
                                    "bot": {
                                        "owner": {
                                            "type": "workspace",
                                            "workspace": True,
                                        },
                                        "workspace_name": "Sample Workspace",
                                    },
                                },
                            },
                        },
                    ],
                    "color": "pink",
                    "is_toggleable": False,
                },
            },
        ),
        (
            Block,
            ImageBlock,
            {
                "object": "block",
                "type": "image",
                "image": {
                    "type": "file",
                    "file": {
                        "url": "https://miller-price.net/",
                        "expiry_time": "2022-03-18T19:28:42.149062",
                    },
                },
            },
        ),
        (
            Block,
            NumberedListItemBlock,
            {
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": [
                        {
                            "annotations": {"color": "orange_background"},
                            "plain_text": "oVYWrfQcUZZdDZlIpAIB",
                            "href": "http://www.stokes.info/",
                            "type": "text",
                            "text": {
                                "content": "Exactly success wonder before by present.",
                                "link": {"url": "http://gardner.com/"},
                            },
                        }
                    ],
                    "color": "green_background",
                    "children": [{"object": "block", "type": "column", "column": {}}],
                },
            },
        ),
        (
            Block,
            ParagraphBlock,
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "annotations": {"color": "orange_background"},
                            "plain_text": "oVYWrfQcUZZdDZlIpAIB",
                            "href": "http://www.stokes.info/",
                            "type": "text",
                            "text": {
                                "content": "Exactly success wonder before by present.",
                                "link": {"url": "http://gardner.com/"},
                            },
                        }
                    ],
                    "color": "green_background",
                    "children": [
                        {
                            "object": "block",
                            "type": "equation",
                            "equation": {"expression": "NCXHDCasrnVWDaUImsth"},
                        }
                    ],
                },
            },
        ),
        (
            Block,
            PdfBlock,
            {
                "object": "block",
                "type": "pdf",
                "pdf": {
                    "type": "external",
                    "external": {"url": "http://leach.org/"},
                    "caption": [
                        {
                            "annotations": {"color": "orange_background"},
                            "plain_text": "spaZtPpKrlEZaOqamyqK",
                            "href": "https://www.david.com/",
                            "type": "text",
                            "text": {
                                "content": "Exactly success wonder before by present.",
                                "link": {"url": "http://gardner.com/"},
                            },
                        },
                        {
                            "annotations": {"color": "orange_background"},
                            "plain_text": "aClEuvtdEEGgnpWPEtRw",
                            "href": "http://www.gonzalez-cunningham.com/",
                            "type": "equation",
                            "equation": {
                                "expression": "Protect mean fear easy serve will five. Theory probably want technology provide Republican.\nEye attack form serve arrive. Mind source cup local prove."
                            },
                        },
                    ],
                },
            },
        ),
        (
            Block,
            QuoteBlock,
            {
                "object": "block",
                "type": "quote",
                "quote": {
                    "rich_text": [
                        {
                            "annotations": {"color": "orange_background"},
                            "plain_text": "oVYWrfQcUZZdDZlIpAIB",
                            "href": "http://www.stokes.info/",
                            "type": "text",
                            "text": {
                                "content": "Exactly success wonder before by present.",
                                "link": {"url": "http://gardner.com/"},
                            },
                        }
                    ],
                    "color": "green_background",
                    "children": [
                        {"object": "block", "type": "breadcrumb", "breadcrumb": {}}
                    ],
                },
            },
        ),
        (
            Block,
            SyncedBlock,
            {
                "object": "block",
                "type": "synced_block",
                "synced_block": {"children": []},
            },
        ),
        (
            Block,
            TableBlock,
            {
                "object": "block",
                "type": "table",
                "table": {
                    "table_width": 3,
                    "has_column_header": True,
                    "has_row_header": True,
                },
            },
        ),
        (
            Block,
            TableContentBlock,
            {
                "object": "block",
                "type": "table_of_contents",
                "table_of_contents": "red_background",
            },
        ),
        (
            Block,
            TableRowBlock,
            {
                "object": "block",
                "type": "table_row",
                "table_row": {
                    "rich_text": [
                        {
                            "annotations": {"color": "orange_background"},
                            "plain_text": "ZRHeklfLKMFPahVybpiN",
                            "href": "https://williams.com/",
                            "type": "mention",
                            "mention": {
                                "type": "template_mention",
                                "template_mention": {
                                    "type": "template_mention_date",
                                    "template_mention_date": "now",
                                },
                            },
                        }
                    ]
                },
            },
        ),
        (
            Block,
            ToDoBlock,
            {
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": [
                        {
                            "annotations": {"color": "orange_background"},
                            "plain_text": "oVYWrfQcUZZdDZlIpAIB",
                            "href": "http://www.stokes.info/",
                            "type": "text",
                            "text": {
                                "content": "Exactly success wonder before by present.",
                                "link": {"url": "http://gardner.com/"},
                            },
                        }
                    ],
                    "color": "green_background",
                    "children": [
                        {"object": "block", "type": "column_list", "column_list": {}}
                    ],
                },
            },
        ),
        (
            Block,
            ToggleBlock,
            {
                "object": "block",
                "type": "toggle",
                "toggle": {
                    "rich_text": [
                        {
                            "annotations": {"color": "orange_background"},
                            "plain_text": "oVYWrfQcUZZdDZlIpAIB",
                            "href": "http://www.stokes.info/",
                            "type": "text",
                            "text": {
                                "content": "Exactly success wonder before by present.",
                                "link": {"url": "http://gardner.com/"},
                            },
                        }
                    ],
                    "color": "green_background",
                    "children": [
                        {
                            "object": "block",
                            "type": "embed",
                            "embed": {"url": "http://www.thomas-barker.org/"},
                        }
                    ],
                },
            },
        ),
        (Block, UnsupportedBlock, {"object": "block", "type": "unsupported"}),
        (
            Block,
            VideoBlock,
            {
                "object": "block",
                "type": "video",
                "video": {
                    "type": "file",
                    "file": {
                        "url": "http://chan.org/",
                        "expiry_time": "2022-03-18T19:28:42.149062",
                    },
                    "caption": [
                        {
                            "annotations": {"color": "orange_background"},
                            "plain_text": "ThvcbQMCNzKftJdWjMOE",
                            "href": "https://www.dominguez.org/",
                            "type": "mention",
                            "mention": {
                                "type": "template_mention",
                                "template_mention": {
                                    "type": "template_mention_date",
                                    "template_mention_date": "now",
                                },
                            },
                        }
                    ],
                },
            },
        ),
    ],
)
def test_discriminated_model(annotated_clz: type, expected_clz: type, input_data: dict):
    DiscriminatedModelTester(annotated_clz, expected_clz, **input_data).run_all_tests()


@pytest.mark.parametrize(
    "invalid_data",
    [
        (BookmarkBlock, {"url": None, "caption": []}),
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
        # (EmbedBlock, {"url": ""}),  # URL cannot be empty
        (
            FileBlock,
            {
                "caption": [],
                "name": None,
                "type": "external",
                "external": {"url": "https://companywebsite.com/files/doc.txt"},
            },
        ),  # Name is required
        (
            HeadingOneBlock,
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
                    'object': NotionObjectType.BLOCK,
                    'id': UUID('b9b40b5b-2995-4570-b534-8de8b44505c1'),
                    'parent': WorkspaceParent(
                        type=ParentType.WORKSPACE, workspace=True
                    ),
                    'created_time': datetime(2000, 10, 23, 14, 47, 52, 738518),
                    'last_edited_time': datetime(2002, 10, 16, 19, 12, 59, 868332),
                    'created_by': UserRef(
                        object=NotionObjectType.User,
                        id=UUID('9c30bf5b-0f43-4172-ad21-2870959f6976'),
                    ),
                    'last_edited_by': UserRef(
                        object=NotionObjectType.User,
                        id=UUID('22dafb54-4a0c-4e39-9900-f6281bcd0912'),
                    ),
                    'archived': False,
                    'in_trash': False,
                    'has_children': None,
                    'type': BlockType.BOOKMARK,
                    'bookmark': Bookmark(
                        caption=[
                            MentionRichText(
                                annotations=Annotations(
                                    bold=True,
                                    italic=None,
                                    strikethrough=False,
                                    underline=False,
                                    code=False,
                                    color=Color.GREEN,
                                ),
                                plain_text='A one company hour.',
                                href='https://douglas-sanchez.com/',
                                type=RichTextType.MENTION,
                                mention=TemplateMention(
                                    type=MentionType.TEMPLATE_MENTION,
                                    template_mention=TemplateMentionDate(
                                        type=TemplateMentionType.TEMPLATE_MENTION_DATE,
                                        template_mention_date='today',
                                    ),
                                ),
                            )
                        ],
                        url='http://www.oliver.com/',
                    ),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'id': UUID('b9b40b5b-2995-4570-b534-8de8b44505c1'),
                    'parent': {'type': ParentType.WORKSPACE, 'workspace': True},
                    'created_time': datetime(2000, 10, 23, 14, 47, 52, 738518),
                    'last_edited_time': datetime(2002, 10, 16, 19, 12, 59, 868332),
                    'created_by': {
                        'object': NotionObjectType.User,
                        'id': UUID('9c30bf5b-0f43-4172-ad21-2870959f6976'),
                    },
                    'last_edited_by': {
                        'object': NotionObjectType.User,
                        'id': UUID('22dafb54-4a0c-4e39-9900-f6281bcd0912'),
                    },
                    'archived': False,
                    'in_trash': False,
                    'type': BlockType.BOOKMARK,
                    'bookmark': {
                        'caption': [
                            {
                                'annotations': {
                                    'bold': True,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': Color.GREEN,
                                },
                                'plain_text': 'A one company hour.',
                                'href': 'https://douglas-sanchez.com/',
                                'type': RichTextType.MENTION,
                                'mention': {
                                    'type': MentionType.TEMPLATE_MENTION,
                                    'template_mention': {
                                        'type': TemplateMentionType.TEMPLATE_MENTION_DATE,
                                        'template_mention_date': 'today',
                                    },
                                },
                            }
                        ],
                        'url': 'http://www.oliver.com/',
                    },
                },
                {
                    "object": "block",
                    "id": "b9b40b5b-2995-4570-b534-8de8b44505c1",
                    "parent": {"type": "workspace", "workspace": True},
                    "created_time": "2000-10-23T14:47:52.738518",
                    "last_edited_time": "2002-10-16T19:12:59.868332",
                    "created_by": {
                        "object": "user",
                        "id": "9c30bf5b-0f43-4172-ad21-2870959f6976",
                    },
                    "last_edited_by": {
                        "object": "user",
                        "id": "22dafb54-4a0c-4e39-9900-f6281bcd0912",
                    },
                    "archived": False,
                    "in_trash": False,
                    "type": "bookmark",
                    "bookmark": {
                        "caption": [
                            {
                                "annotations": {
                                    "bold": True,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "green",
                                },
                                "plain_text": "A one company hour.",
                                "href": "https://douglas-sanchez.com/",
                                "type": "mention",
                                "mention": {
                                    "type": "template_mention",
                                    "template_mention": {
                                        "type": "template_mention_date",
                                        "template_mention_date": "today",
                                    },
                                },
                            }
                        ],
                        "url": "http://www.oliver.com/",
                    },
                },
            ),
        ),
        (
            BreadcrumbBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'id': UUID('43d0de9e-641b-48a4-be4a-64ec416fc7ab'),
                    'parent': WorkspaceParent(
                        type=ParentType.WORKSPACE, workspace=True
                    ),
                    'created_time': datetime(2000, 10, 23, 14, 47, 52, 738518),
                    'last_edited_time': datetime(2002, 10, 16, 19, 12, 59, 868332),
                    'created_by': UserRef(
                        object=NotionObjectType.User,
                        id=UUID('9c30bf5b-0f43-4172-ad21-2870959f6976'),
                    ),
                    'last_edited_by': UserRef(
                        object=NotionObjectType.User,
                        id=UUID('22dafb54-4a0c-4e39-9900-f6281bcd0912'),
                    ),
                    'archived': None,
                    'in_trash': None,
                    'has_children': None,
                    'type': BlockType.BREADCRUMB,
                    'breadcrumb': {},
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'id': UUID('43d0de9e-641b-48a4-be4a-64ec416fc7ab'),
                    'parent': {'type': ParentType.WORKSPACE, 'workspace': True},
                    'created_time': datetime(2000, 10, 23, 14, 47, 52, 738518),
                    'last_edited_time': datetime(2002, 10, 16, 19, 12, 59, 868332),
                    'created_by': {
                        'object': NotionObjectType.User,
                        'id': UUID('9c30bf5b-0f43-4172-ad21-2870959f6976'),
                    },
                    'last_edited_by': {
                        'object': NotionObjectType.User,
                        'id': UUID('22dafb54-4a0c-4e39-9900-f6281bcd0912'),
                    },
                    'type': BlockType.BREADCRUMB,
                    'breadcrumb': {},
                },
                {
                    "object": "block",
                    "id": "43d0de9e-641b-48a4-be4a-64ec416fc7ab",
                    "parent": {"type": "workspace", "workspace": True},
                    "created_time": "2000-10-23T14:47:52.738518",
                    "last_edited_time": "2002-10-16T19:12:59.868332",
                    "created_by": {
                        "object": "user",
                        "id": "9c30bf5b-0f43-4172-ad21-2870959f6976",
                    },
                    "last_edited_by": {
                        "object": "user",
                        "id": "22dafb54-4a0c-4e39-9900-f6281bcd0912",
                    },
                    "type": "breadcrumb",
                    "breadcrumb": {},
                },
            ),
        ),
        (
            BulletListItemBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'id': UUID('1b6659b8-156d-4360-b2b6-d8fcb1c3949f'),
                    'parent': WorkspaceParent(
                        type=ParentType.WORKSPACE, workspace=True
                    ),
                    'created_time': datetime(2000, 10, 23, 14, 47, 52, 738518),
                    'last_edited_time': datetime(2002, 10, 16, 19, 12, 59, 868332),
                    'created_by': UserRef(
                        object=NotionObjectType.User,
                        id=UUID('9c30bf5b-0f43-4172-ad21-2870959f6976'),
                    ),
                    'last_edited_by': UserRef(
                        object=NotionObjectType.User,
                        id=UUID('22dafb54-4a0c-4e39-9900-f6281bcd0912'),
                    ),
                    'archived': None,
                    'in_trash': False,
                    'has_children': False,
                    'type': BlockType.BULLETED_LIST_ITEM,
                    'bullet_list_item': BulletListItem(
                        rich_text=[
                            TextRichText(
                                annotations=Annotations(
                                    bold=True,
                                    italic=None,
                                    strikethrough=False,
                                    underline=False,
                                    code=False,
                                    color=Color.GREEN,
                                ),
                                plain_text='A one company hour.',
                                href='http://barker.com/',
                                type=RichTextType.TEXT,
                                text=Text(
                                    content='These someone avoid.',
                                    link=NotionUrlObject(url='https://www.arnold.com/'),
                                ),
                            ),
                            TextRichText(
                                annotations=Annotations(
                                    bold=True,
                                    italic=None,
                                    strikethrough=False,
                                    underline=False,
                                    code=False,
                                    color=Color.GREEN,
                                ),
                                plain_text='A one company hour.',
                                href='http://www.hammond.com/',
                                type=RichTextType.TEXT,
                                text=Text(
                                    content='These someone avoid.',
                                    link=NotionUrlObject(url='https://www.arnold.com/'),
                                ),
                            ),
                        ],
                        color=Color.PURPLE,
                        children=[
                            TableContentBlock(
                                object=NotionObjectType.BLOCK,
                                id=None,
                                parent=None,
                                created_time=None,
                                last_edited_time=None,
                                created_by=None,
                                last_edited_by=None,
                                archived=None,
                                in_trash=None,
                                has_children=None,
                                type=BlockType.TABLE_OF_CONTENTS,
                                table_of_contents=BackgroundColor.GRAY_BACKGROUND,
                            )
                        ],
                    ),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'id': UUID('1b6659b8-156d-4360-b2b6-d8fcb1c3949f'),
                    'parent': {'type': ParentType.WORKSPACE, 'workspace': True},
                    'created_time': datetime(2000, 10, 23, 14, 47, 52, 738518),
                    'last_edited_time': datetime(2002, 10, 16, 19, 12, 59, 868332),
                    'created_by': {
                        'object': NotionObjectType.User,
                        'id': UUID('9c30bf5b-0f43-4172-ad21-2870959f6976'),
                    },
                    'last_edited_by': {
                        'object': NotionObjectType.User,
                        'id': UUID('22dafb54-4a0c-4e39-9900-f6281bcd0912'),
                    },
                    'in_trash': False,
                    'has_children': False,
                    'type': BlockType.BULLETED_LIST_ITEM,
                    'bullet_list_item': {
                        'rich_text': [
                            {
                                'annotations': {
                                    'bold': True,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': Color.GREEN,
                                },
                                'plain_text': 'A one company hour.',
                                'href': 'http://barker.com/',
                                'type': RichTextType.TEXT,
                                'text': {
                                    'content': 'These someone avoid.',
                                    'link': {'url': 'https://www.arnold.com/'},
                                },
                            },
                            {
                                'annotations': {
                                    'bold': True,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': Color.GREEN,
                                },
                                'plain_text': 'A one company hour.',
                                'href': 'http://www.hammond.com/',
                                'type': RichTextType.TEXT,
                                'text': {
                                    'content': 'These someone avoid.',
                                    'link': {'url': 'https://www.arnold.com/'},
                                },
                            },
                        ],
                        'color': Color.PURPLE,
                        'children': [
                            {
                                'object': NotionObjectType.BLOCK,
                                'type': BlockType.TABLE_OF_CONTENTS,
                                'table_of_contents': BackgroundColor.GRAY_BACKGROUND,
                            }
                        ],
                    },
                },
                {
                    "object": "block",
                    "id": "1b6659b8-156d-4360-b2b6-d8fcb1c3949f",
                    "parent": {"type": "workspace", "workspace": True},
                    "created_time": "2000-10-23T14:47:52.738518",
                    "last_edited_time": "2002-10-16T19:12:59.868332",
                    "created_by": {
                        "object": "user",
                        "id": "9c30bf5b-0f43-4172-ad21-2870959f6976",
                    },
                    "last_edited_by": {
                        "object": "user",
                        "id": "22dafb54-4a0c-4e39-9900-f6281bcd0912",
                    },
                    "in_trash": False,
                    "has_children": False,
                    "type": "bulleted_list_item",
                    "bullet_list_item": {
                        "rich_text": [
                            {
                                "annotations": {
                                    "bold": True,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "green",
                                },
                                "plain_text": "A one company hour.",
                                "href": "http://barker.com/",
                                "type": "text",
                                "text": {
                                    "content": "These someone avoid.",
                                    "link": {"url": "https://www.arnold.com/"},
                                },
                            },
                            {
                                "annotations": {
                                    "bold": True,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "green",
                                },
                                "plain_text": "A one company hour.",
                                "href": "http://www.hammond.com/",
                                "type": "text",
                                "text": {
                                    "content": "These someone avoid.",
                                    "link": {"url": "https://www.arnold.com/"},
                                },
                            },
                        ],
                        "color": "purple",
                        "children": [
                            {
                                "object": "block",
                                "type": "table_of_contents",
                                "table_of_contents": "gray_background",
                            }
                        ],
                    },
                },
            ),
        ),
        (
            CalloutBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'id': UUID('0d54876e-ffa4-48b3-af80-4d8ca34d2af8'),
                    'parent': WorkspaceParent(
                        type=ParentType.WORKSPACE, workspace=True
                    ),
                    'created_time': datetime(2000, 10, 23, 14, 47, 52, 738518),
                    'last_edited_time': datetime(2002, 10, 16, 19, 12, 59, 868332),
                    'created_by': UserRef(
                        object=NotionObjectType.User,
                        id=UUID('9c30bf5b-0f43-4172-ad21-2870959f6976'),
                    ),
                    'last_edited_by': UserRef(
                        object=NotionObjectType.User,
                        id=UUID('22dafb54-4a0c-4e39-9900-f6281bcd0912'),
                    ),
                    'archived': False,
                    'in_trash': None,
                    'has_children': None,
                    'type': BlockType.CALLOUT,
                    'callout': Callout(
                        rich_text=[
                            MentionRichText(
                                annotations=Annotations(
                                    bold=True,
                                    italic=None,
                                    strikethrough=False,
                                    underline=False,
                                    code=False,
                                    color=Color.GREEN,
                                ),
                                plain_text='A one company hour.',
                                href='https://stevenson.com/',
                                type=RichTextType.MENTION,
                                mention=TemplateMention(
                                    type=MentionType.TEMPLATE_MENTION,
                                    template_mention=TemplateMentionDate(
                                        type=TemplateMentionType.TEMPLATE_MENTION_DATE,
                                        template_mention_date='today',
                                    ),
                                ),
                            ),
                            MentionRichText(
                                annotations=Annotations(
                                    bold=True,
                                    italic=None,
                                    strikethrough=False,
                                    underline=False,
                                    code=False,
                                    color=Color.GREEN,
                                ),
                                plain_text='A one company hour.',
                                href='https://www.roberson.com/',
                                type=RichTextType.MENTION,
                                mention=LinkPreviewMention(
                                    type=MentionType.LINK_PREVIEW,
                                    link_preview=NotionUrlObject(
                                        url='https://chavez.org/'
                                    ),
                                ),
                            ),
                        ],
                        icon=CustomEmoji(
                            type=EmojiType.CUSTOM_EMOJI,
                            custom_emoji=CustomEmojiObject(
                                id=UUID('e8d36775-ee3c-4ecf-845d-a40d549f8720'),
                                name='Crystal White',
                                url='http://www.goodman.com/',
                            ),
                        ),
                        color=BackgroundColor.ORANGE_BACKGROUND,
                    ),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'id': UUID('0d54876e-ffa4-48b3-af80-4d8ca34d2af8'),
                    'parent': {'type': ParentType.WORKSPACE, 'workspace': True},
                    'created_time': datetime(2000, 10, 23, 14, 47, 52, 738518),
                    'last_edited_time': datetime(2002, 10, 16, 19, 12, 59, 868332),
                    'created_by': {
                        'object': NotionObjectType.User,
                        'id': UUID('9c30bf5b-0f43-4172-ad21-2870959f6976'),
                    },
                    'last_edited_by': {
                        'object': NotionObjectType.User,
                        'id': UUID('22dafb54-4a0c-4e39-9900-f6281bcd0912'),
                    },
                    'archived': False,
                    'type': BlockType.CALLOUT,
                    'callout': {
                        'rich_text': [
                            {
                                'annotations': {
                                    'bold': True,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': Color.GREEN,
                                },
                                'plain_text': 'A one company hour.',
                                'href': 'https://stevenson.com/',
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
                                'annotations': {
                                    'bold': True,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': Color.GREEN,
                                },
                                'plain_text': 'A one company hour.',
                                'href': 'https://www.roberson.com/',
                                'type': RichTextType.MENTION,
                                'mention': {
                                    'type': MentionType.LINK_PREVIEW,
                                    'link_preview': {'url': 'https://chavez.org/'},
                                },
                            },
                        ],
                        'icon': {
                            'type': EmojiType.CUSTOM_EMOJI,
                            'custom_emoji': {
                                'id': UUID('e8d36775-ee3c-4ecf-845d-a40d549f8720'),
                                'name': 'Crystal White',
                                'url': 'http://www.goodman.com/',
                            },
                        },
                        'color': BackgroundColor.ORANGE_BACKGROUND,
                    },
                },
                {
                    "object": "block",
                    "id": "0d54876e-ffa4-48b3-af80-4d8ca34d2af8",
                    "parent": {"type": "workspace", "workspace": True},
                    "created_time": "2000-10-23T14:47:52.738518",
                    "last_edited_time": "2002-10-16T19:12:59.868332",
                    "created_by": {
                        "object": "user",
                        "id": "9c30bf5b-0f43-4172-ad21-2870959f6976",
                    },
                    "last_edited_by": {
                        "object": "user",
                        "id": "22dafb54-4a0c-4e39-9900-f6281bcd0912",
                    },
                    "archived": False,
                    "type": "callout",
                    "callout": {
                        "rich_text": [
                            {
                                "annotations": {
                                    "bold": True,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "green",
                                },
                                "plain_text": "A one company hour.",
                                "href": "https://stevenson.com/",
                                "type": "mention",
                                "mention": {
                                    "type": "template_mention",
                                    "template_mention": {
                                        "type": "template_mention_date",
                                        "template_mention_date": "today",
                                    },
                                },
                            },
                            {
                                "annotations": {
                                    "bold": True,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "green",
                                },
                                "plain_text": "A one company hour.",
                                "href": "https://www.roberson.com/",
                                "type": "mention",
                                "mention": {
                                    "type": "link_preview",
                                    "link_preview": {"url": "https://chavez.org/"},
                                },
                            },
                        ],
                        "icon": {
                            "type": "custom_emoji",
                            "custom_emoji": {
                                "id": "e8d36775-ee3c-4ecf-845d-a40d549f8720",
                                "name": "Crystal White",
                                "url": "http://www.goodman.com/",
                            },
                        },
                        "color": "orange_background",
                    },
                },
            ),
        ),
        (
            ChildDatabaseBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'id': None,
                    'parent': None,
                    'created_time': None,
                    'last_edited_time': None,
                    'created_by': None,
                    'last_edited_by': None,
                    'archived': None,
                    'in_trash': None,
                    'has_children': None,
                    'type': BlockType.CHILD_DATABASE,
                    'child_database': ChildDatabase(title='Linda Willis'),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.CHILD_DATABASE,
                    'child_database': {'title': 'Linda Willis'},
                },
                {
                    "object": "block",
                    "type": "child_database",
                    "child_database": {"title": "Linda Willis"},
                },
            ),
        ),
        (
            ChildPageBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'id': None,
                    'parent': None,
                    'created_time': None,
                    'last_edited_time': None,
                    'created_by': None,
                    'last_edited_by': None,
                    'archived': None,
                    'in_trash': None,
                    'has_children': None,
                    'type': BlockType.CHILD_PAGE,
                    'child_page': ChildPage(title='Natasha Coleman'),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.CHILD_PAGE,
                    'child_page': {'title': 'Natasha Coleman'},
                },
                {
                    "object": "block",
                    "type": "child_page",
                    "child_page": {"title": "Natasha Coleman"},
                },
            ),
        ),
        (
            CodeBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'id': None,
                    'parent': None,
                    'created_time': None,
                    'last_edited_time': None,
                    'created_by': None,
                    'last_edited_by': None,
                    'archived': None,
                    'in_trash': None,
                    'has_children': None,
                    'type': BlockType.CODE,
                    'code': Code(
                        caption=[
                            EquationRichText(
                                annotations=Annotations(
                                    bold=True,
                                    italic=None,
                                    strikethrough=False,
                                    underline=False,
                                    code=False,
                                    color=Color.GREEN,
                                ),
                                plain_text='A one company hour.',
                                href='https://tran.com/',
                                type=RichTextType.EQUATION,
                                equation=Equation(
                                    expression='History television seem partner local measure change. Medical well understand floor song may mention.'
                                ),
                            )
                        ],
                        rich_text=[
                            MentionRichText(
                                annotations=Annotations(
                                    bold=True,
                                    italic=None,
                                    strikethrough=False,
                                    underline=False,
                                    code=False,
                                    color=Color.GREEN,
                                ),
                                plain_text='A one company hour.',
                                href='http://www.reed-young.com/',
                                type=RichTextType.MENTION,
                                mention=DateMention(
                                    type=MentionType.DATE,
                                    date=NotionDate(
                                        start=datetime(
                                            1997,
                                            10,
                                            29,
                                            6,
                                            34,
                                            4,
                                            949878,
                                            tzinfo=ZoneInfo(key='Africa/Asmera'),
                                        ),
                                        end=datetime(
                                            2005,
                                            1,
                                            2,
                                            12,
                                            15,
                                            42,
                                            844224,
                                            tzinfo=ZoneInfo(key='Africa/Asmera'),
                                        ),
                                        time_zone='Africa/Asmera',
                                    ),
                                ),
                            )
                        ],
                        language=ProgrammingLanguage.PHP,
                    ),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.CODE,
                    'code': {
                        'caption': [
                            {
                                'annotations': {
                                    'bold': True,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': Color.GREEN,
                                },
                                'plain_text': 'A one company hour.',
                                'href': 'https://tran.com/',
                                'type': RichTextType.EQUATION,
                                'equation': {
                                    'expression': 'History television seem partner local measure change. Medical well understand floor song may mention.'
                                },
                            }
                        ],
                        'rich_text': [
                            {
                                'annotations': {
                                    'bold': True,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': Color.GREEN,
                                },
                                'plain_text': 'A one company hour.',
                                'href': 'http://www.reed-young.com/',
                                'type': RichTextType.MENTION,
                                'mention': {
                                    'type': MentionType.DATE,
                                    'date': {
                                        'start': datetime(
                                            1997,
                                            10,
                                            29,
                                            6,
                                            34,
                                            4,
                                            949878,
                                            tzinfo=ZoneInfo(key='Africa/Asmera'),
                                        ),
                                        'end': datetime(
                                            2005,
                                            1,
                                            2,
                                            12,
                                            15,
                                            42,
                                            844224,
                                            tzinfo=ZoneInfo(key='Africa/Asmera'),
                                        ),
                                        'time_zone': 'Africa/Asmera',
                                    },
                                },
                            }
                        ],
                        'language': ProgrammingLanguage.PHP,
                    },
                },
                {
                    "object": "block",
                    "type": "code",
                    "code": {
                        "caption": [
                            {
                                "annotations": {
                                    "bold": True,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "green",
                                },
                                "plain_text": "A one company hour.",
                                "href": "https://tran.com/",
                                "type": "equation",
                                "equation": {
                                    "expression": "History television seem partner local measure change. Medical well understand floor song may mention."
                                },
                            }
                        ],
                        "rich_text": [
                            {
                                "annotations": {
                                    "bold": True,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "green",
                                },
                                "plain_text": "A one company hour.",
                                "href": "http://www.reed-young.com/",
                                "type": "mention",
                                "mention": {
                                    "type": "date",
                                    "date": {
                                        "start": "1997-10-29T06:34:04.949878+03:00",
                                        "end": "2005-01-02T12:15:42.844224+03:00",
                                        "time_zone": "Africa/Asmera",
                                    },
                                },
                            }
                        ],
                        "language": "php",
                    },
                },
            ),
        ),
        (
            ColumnBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'id': None,
                    'parent': None,
                    'created_time': None,
                    'last_edited_time': None,
                    'created_by': None,
                    'last_edited_by': None,
                    'archived': None,
                    'in_trash': None,
                    'has_children': None,
                    'type': BlockType.COLUMN,
                    'column': {},
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.COLUMN,
                    'column': {},
                },
                {"object": "block", "type": "column", "column": {}},
            ),
        ),
        (
            ColumnListBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'id': None,
                    'parent': None,
                    'created_time': None,
                    'last_edited_time': None,
                    'created_by': None,
                    'last_edited_by': None,
                    'archived': None,
                    'in_trash': None,
                    'has_children': None,
                    'type': BlockType.COLUMN_LIST,
                    'column_list': {},
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.COLUMN_LIST,
                    'column_list': {},
                },
                {"object": "block", "type": "column_list", "column_list": {}},
            ),
        ),
        (
            DividerBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'id': UUID('17ad000c-9f1b-400d-af52-e652357733a9'),
                    'parent': WorkspaceParent(
                        type=ParentType.WORKSPACE, workspace=True
                    ),
                    'created_time': datetime(2000, 10, 23, 14, 47, 52, 738518),
                    'last_edited_time': datetime(2002, 10, 16, 19, 12, 59, 868332),
                    'created_by': UserRef(
                        object=NotionObjectType.User,
                        id=UUID('9c30bf5b-0f43-4172-ad21-2870959f6976'),
                    ),
                    'last_edited_by': UserRef(
                        object=NotionObjectType.User,
                        id=UUID('22dafb54-4a0c-4e39-9900-f6281bcd0912'),
                    ),
                    'archived': None,
                    'in_trash': None,
                    'has_children': False,
                    'type': BlockType.DIVIDER,
                    'divider': {},
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'id': UUID('17ad000c-9f1b-400d-af52-e652357733a9'),
                    'parent': {'type': ParentType.WORKSPACE, 'workspace': True},
                    'created_time': datetime(2000, 10, 23, 14, 47, 52, 738518),
                    'last_edited_time': datetime(2002, 10, 16, 19, 12, 59, 868332),
                    'created_by': {
                        'object': NotionObjectType.User,
                        'id': UUID('9c30bf5b-0f43-4172-ad21-2870959f6976'),
                    },
                    'last_edited_by': {
                        'object': NotionObjectType.User,
                        'id': UUID('22dafb54-4a0c-4e39-9900-f6281bcd0912'),
                    },
                    'has_children': False,
                    'type': BlockType.DIVIDER,
                    'divider': {},
                },
                {
                    "object": "block",
                    "id": "17ad000c-9f1b-400d-af52-e652357733a9",
                    "parent": {"type": "workspace", "workspace": True},
                    "created_time": "2000-10-23T14:47:52.738518",
                    "last_edited_time": "2002-10-16T19:12:59.868332",
                    "created_by": {
                        "object": "user",
                        "id": "9c30bf5b-0f43-4172-ad21-2870959f6976",
                    },
                    "last_edited_by": {
                        "object": "user",
                        "id": "22dafb54-4a0c-4e39-9900-f6281bcd0912",
                    },
                    "has_children": False,
                    "type": "divider",
                    "divider": {},
                },
            ),
        ),
        (
            EmbedBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'id': None,
                    'parent': None,
                    'created_time': None,
                    'last_edited_time': None,
                    'created_by': None,
                    'last_edited_by': None,
                    'archived': None,
                    'in_trash': None,
                    'has_children': None,
                    'type': BlockType.EMBED,
                    'embed': NotionUrlObject(url='https://www.ruiz.com/'),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.EMBED,
                    'embed': {'url': 'https://www.ruiz.com/'},
                },
                {
                    "object": "block",
                    "type": "embed",
                    "embed": {"url": "https://www.ruiz.com/"},
                },
            ),
        ),
        (
            EquationBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'id': None,
                    'parent': None,
                    'created_time': None,
                    'last_edited_time': None,
                    'created_by': None,
                    'last_edited_by': None,
                    'archived': None,
                    'in_trash': None,
                    'has_children': None,
                    'type': BlockType.EQUATION,
                    'equation': NotionEquation(expression='oPcXhAkayitnjlbcharN'),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.EQUATION,
                    'equation': {'expression': 'oPcXhAkayitnjlbcharN'},
                },
                {
                    "object": "block",
                    "type": "equation",
                    "equation": {"expression": "oPcXhAkayitnjlbcharN"},
                },
            ),
        ),
        (
            FileBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'id': None,
                    'parent': None,
                    'created_time': None,
                    'last_edited_time': None,
                    'created_by': None,
                    'last_edited_by': None,
                    'archived': None,
                    'in_trash': None,
                    'has_children': None,
                    'type': BlockType.FILE,
                    'file': CaptionExternalFileWithName(
                        type=FileType.EXTERNAL,
                        external=ExternalFileObject(url='https://tyler.com/'),
                        caption=[
                            EquationRichText(
                                annotations=Annotations(
                                    bold=True,
                                    italic=None,
                                    strikethrough=False,
                                    underline=False,
                                    code=False,
                                    color=Color.GREEN,
                                ),
                                plain_text='A one company hour.',
                                href='http://www.green.biz/',
                                type=RichTextType.EQUATION,
                                equation=Equation(
                                    expression='Job audience stop remain discussion rock. Life grow simply increase focus structure tree.\nAgree agent old piece gun. Simple management various. Record get production because.'
                                ),
                            ),
                            EquationRichText(
                                annotations=Annotations(
                                    bold=True,
                                    italic=None,
                                    strikethrough=False,
                                    underline=False,
                                    code=False,
                                    color=Color.GREEN,
                                ),
                                plain_text='A one company hour.',
                                href='https://www.burgess.biz/',
                                type=RichTextType.EQUATION,
                                equation=Equation(
                                    expression='Senior direction show under stage among perform. Left best market note kind. Prepare wear final back edge result rate between.\nCheck character high party pattern. Ten wait before time.'
                                ),
                            ),
                        ],
                        name='Mark Miller',
                    ),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.FILE,
                    'file': {
                        'type': FileType.EXTERNAL,
                        'external': {'url': 'https://tyler.com/'},
                        'caption': [
                            {
                                'annotations': {
                                    'bold': True,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': Color.GREEN,
                                },
                                'plain_text': 'A one company hour.',
                                'href': 'http://www.green.biz/',
                                'type': RichTextType.EQUATION,
                                'equation': {
                                    'expression': 'Job audience stop remain discussion rock. Life grow simply increase focus structure tree.\nAgree agent old piece gun. Simple management various. Record get production because.'
                                },
                            },
                            {
                                'annotations': {
                                    'bold': True,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': Color.GREEN,
                                },
                                'plain_text': 'A one company hour.',
                                'href': 'https://www.burgess.biz/',
                                'type': RichTextType.EQUATION,
                                'equation': {
                                    'expression': 'Senior direction show under stage among perform. Left best market note kind. Prepare wear final back edge result rate between.\nCheck character high party pattern. Ten wait before time.'
                                },
                            },
                        ],
                        'name': 'Mark Miller',
                    },
                },
                {
                    "object": "block",
                    "type": "file",
                    "file": {
                        "type": "external",
                        "external": {"url": "https://tyler.com/"},
                        "caption": [
                            {
                                "annotations": {
                                    "bold": True,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "green",
                                },
                                "plain_text": "A one company hour.",
                                "href": "http://www.green.biz/",
                                "type": "equation",
                                "equation": {
                                    "expression": "Job audience stop remain discussion rock. Life grow simply increase focus structure tree.\nAgree agent old piece gun. Simple management various. Record get production because."
                                },
                            },
                            {
                                "annotations": {
                                    "bold": True,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "green",
                                },
                                "plain_text": "A one company hour.",
                                "href": "https://www.burgess.biz/",
                                "type": "equation",
                                "equation": {
                                    "expression": "Senior direction show under stage among perform. Left best market note kind. Prepare wear final back edge result rate between.\nCheck character high party pattern. Ten wait before time."
                                },
                            },
                        ],
                        "name": "Mark Miller",
                    },
                },
            ),
        ),
        (
            HeadingOneBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'id': UUID('0cbc8611-9f84-4c95-ab7a-3f7a50f42cfe'),
                    'parent': WorkspaceParent(
                        type=ParentType.WORKSPACE, workspace=True
                    ),
                    'created_time': datetime(2000, 10, 23, 14, 47, 52, 738518),
                    'last_edited_time': datetime(2002, 10, 16, 19, 12, 59, 868332),
                    'created_by': UserRef(
                        object=NotionObjectType.User,
                        id=UUID('9c30bf5b-0f43-4172-ad21-2870959f6976'),
                    ),
                    'last_edited_by': UserRef(
                        object=NotionObjectType.User,
                        id=UUID('22dafb54-4a0c-4e39-9900-f6281bcd0912'),
                    ),
                    'archived': None,
                    'in_trash': None,
                    'has_children': True,
                    'type': BlockType.HEADING_1,
                    'heading_1': Heading(
                        rich_text=[
                            MentionRichText(
                                annotations=Annotations(
                                    bold=True,
                                    italic=None,
                                    strikethrough=False,
                                    underline=False,
                                    code=False,
                                    color=Color.GREEN,
                                ),
                                plain_text='A one company hour.',
                                href='http://white.com/',
                                type=RichTextType.MENTION,
                                mention=DateMention(
                                    type=MentionType.DATE,
                                    date=NotionDate(
                                        start=datetime(
                                            1997,
                                            10,
                                            29,
                                            6,
                                            34,
                                            4,
                                            949878,
                                            tzinfo=ZoneInfo(key='Africa/Asmera'),
                                        ),
                                        end=datetime(
                                            2005,
                                            1,
                                            2,
                                            12,
                                            15,
                                            42,
                                            844224,
                                            tzinfo=ZoneInfo(key='Africa/Asmera'),
                                        ),
                                        time_zone='Africa/Asmera',
                                    ),
                                ),
                            ),
                            TextRichText(
                                annotations=Annotations(
                                    bold=True,
                                    italic=None,
                                    strikethrough=False,
                                    underline=False,
                                    code=False,
                                    color=Color.GREEN,
                                ),
                                plain_text='A one company hour.',
                                href='https://www.woodward.com/',
                                type=RichTextType.TEXT,
                                text=Text(
                                    content='These someone avoid.',
                                    link=NotionUrlObject(url='https://www.arnold.com/'),
                                ),
                            ),
                        ],
                        color=BackgroundColor.BROWN_BACKGROUND,
                        is_toggleable=False,
                    ),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'id': UUID('0cbc8611-9f84-4c95-ab7a-3f7a50f42cfe'),
                    'parent': {'type': ParentType.WORKSPACE, 'workspace': True},
                    'created_time': datetime(2000, 10, 23, 14, 47, 52, 738518),
                    'last_edited_time': datetime(2002, 10, 16, 19, 12, 59, 868332),
                    'created_by': {
                        'object': NotionObjectType.User,
                        'id': UUID('9c30bf5b-0f43-4172-ad21-2870959f6976'),
                    },
                    'last_edited_by': {
                        'object': NotionObjectType.User,
                        'id': UUID('22dafb54-4a0c-4e39-9900-f6281bcd0912'),
                    },
                    'has_children': True,
                    'type': BlockType.HEADING_1,
                    'heading_1': {
                        'rich_text': [
                            {
                                'annotations': {
                                    'bold': True,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': Color.GREEN,
                                },
                                'plain_text': 'A one company hour.',
                                'href': 'http://white.com/',
                                'type': RichTextType.MENTION,
                                'mention': {
                                    'type': MentionType.DATE,
                                    'date': {
                                        'start': datetime(
                                            1997,
                                            10,
                                            29,
                                            6,
                                            34,
                                            4,
                                            949878,
                                            tzinfo=ZoneInfo(key='Africa/Asmera'),
                                        ),
                                        'end': datetime(
                                            2005,
                                            1,
                                            2,
                                            12,
                                            15,
                                            42,
                                            844224,
                                            tzinfo=ZoneInfo(key='Africa/Asmera'),
                                        ),
                                        'time_zone': 'Africa/Asmera',
                                    },
                                },
                            },
                            {
                                'annotations': {
                                    'bold': True,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': Color.GREEN,
                                },
                                'plain_text': 'A one company hour.',
                                'href': 'https://www.woodward.com/',
                                'type': RichTextType.TEXT,
                                'text': {
                                    'content': 'These someone avoid.',
                                    'link': {'url': 'https://www.arnold.com/'},
                                },
                            },
                        ],
                        'color': BackgroundColor.BROWN_BACKGROUND,
                        'is_toggleable': False,
                    },
                },
                {
                    "object": "block",
                    "id": "0cbc8611-9f84-4c95-ab7a-3f7a50f42cfe",
                    "parent": {"type": "workspace", "workspace": True},
                    "created_time": "2000-10-23T14:47:52.738518",
                    "last_edited_time": "2002-10-16T19:12:59.868332",
                    "created_by": {
                        "object": "user",
                        "id": "9c30bf5b-0f43-4172-ad21-2870959f6976",
                    },
                    "last_edited_by": {
                        "object": "user",
                        "id": "22dafb54-4a0c-4e39-9900-f6281bcd0912",
                    },
                    "has_children": True,
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [
                            {
                                "annotations": {
                                    "bold": True,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "green",
                                },
                                "plain_text": "A one company hour.",
                                "href": "http://white.com/",
                                "type": "mention",
                                "mention": {
                                    "type": "date",
                                    "date": {
                                        "start": "1997-10-29T06:34:04.949878+03:00",
                                        "end": "2005-01-02T12:15:42.844224+03:00",
                                        "time_zone": "Africa/Asmera",
                                    },
                                },
                            },
                            {
                                "annotations": {
                                    "bold": True,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "green",
                                },
                                "plain_text": "A one company hour.",
                                "href": "https://www.woodward.com/",
                                "type": "text",
                                "text": {
                                    "content": "These someone avoid.",
                                    "link": {"url": "https://www.arnold.com/"},
                                },
                            },
                        ],
                        "color": "brown_background",
                        "is_toggleable": False,
                    },
                },
            ),
        ),
        (
            HeadingTwoBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'id': UUID('91dfcceb-b7a2-48da-bbb3-4f8db4bbed63'),
                    'parent': WorkspaceParent(
                        type=ParentType.WORKSPACE, workspace=True
                    ),
                    'created_time': datetime(2000, 10, 23, 14, 47, 52, 738518),
                    'last_edited_time': datetime(2002, 10, 16, 19, 12, 59, 868332),
                    'created_by': UserRef(
                        object=NotionObjectType.User,
                        id=UUID('9c30bf5b-0f43-4172-ad21-2870959f6976'),
                    ),
                    'last_edited_by': UserRef(
                        object=NotionObjectType.User,
                        id=UUID('22dafb54-4a0c-4e39-9900-f6281bcd0912'),
                    ),
                    'archived': None,
                    'in_trash': None,
                    'has_children': False,
                    'type': BlockType.HEADING_2,
                    'heading_2': Heading(
                        rich_text=[
                            MentionRichText(
                                annotations=Annotations(
                                    bold=True,
                                    italic=None,
                                    strikethrough=False,
                                    underline=False,
                                    code=False,
                                    color=Color.GREEN,
                                ),
                                plain_text='A one company hour.',
                                href='http://white.com/',
                                type=RichTextType.MENTION,
                                mention=DateMention(
                                    type=MentionType.DATE,
                                    date=NotionDate(
                                        start=datetime(
                                            1997,
                                            10,
                                            29,
                                            6,
                                            34,
                                            4,
                                            949878,
                                            tzinfo=ZoneInfo(key='Africa/Asmera'),
                                        ),
                                        end=datetime(
                                            2005,
                                            1,
                                            2,
                                            12,
                                            15,
                                            42,
                                            844224,
                                            tzinfo=ZoneInfo(key='Africa/Asmera'),
                                        ),
                                        time_zone='Africa/Asmera',
                                    ),
                                ),
                            ),
                            TextRichText(
                                annotations=Annotations(
                                    bold=True,
                                    italic=None,
                                    strikethrough=False,
                                    underline=False,
                                    code=False,
                                    color=Color.GREEN,
                                ),
                                plain_text='A one company hour.',
                                href='https://www.woodward.com/',
                                type=RichTextType.TEXT,
                                text=Text(
                                    content='These someone avoid.',
                                    link=NotionUrlObject(url='https://www.arnold.com/'),
                                ),
                            ),
                        ],
                        color=BackgroundColor.BROWN_BACKGROUND,
                        is_toggleable=False,
                    ),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'id': UUID('91dfcceb-b7a2-48da-bbb3-4f8db4bbed63'),
                    'parent': {'type': ParentType.WORKSPACE, 'workspace': True},
                    'created_time': datetime(2000, 10, 23, 14, 47, 52, 738518),
                    'last_edited_time': datetime(2002, 10, 16, 19, 12, 59, 868332),
                    'created_by': {
                        'object': NotionObjectType.User,
                        'id': UUID('9c30bf5b-0f43-4172-ad21-2870959f6976'),
                    },
                    'last_edited_by': {
                        'object': NotionObjectType.User,
                        'id': UUID('22dafb54-4a0c-4e39-9900-f6281bcd0912'),
                    },
                    'has_children': False,
                    'type': BlockType.HEADING_2,
                    'heading_2': {
                        'rich_text': [
                            {
                                'annotations': {
                                    'bold': True,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': Color.GREEN,
                                },
                                'plain_text': 'A one company hour.',
                                'href': 'http://white.com/',
                                'type': RichTextType.MENTION,
                                'mention': {
                                    'type': MentionType.DATE,
                                    'date': {
                                        'start': datetime(
                                            1997,
                                            10,
                                            29,
                                            6,
                                            34,
                                            4,
                                            949878,
                                            tzinfo=ZoneInfo(key='Africa/Asmera'),
                                        ),
                                        'end': datetime(
                                            2005,
                                            1,
                                            2,
                                            12,
                                            15,
                                            42,
                                            844224,
                                            tzinfo=ZoneInfo(key='Africa/Asmera'),
                                        ),
                                        'time_zone': 'Africa/Asmera',
                                    },
                                },
                            },
                            {
                                'annotations': {
                                    'bold': True,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': Color.GREEN,
                                },
                                'plain_text': 'A one company hour.',
                                'href': 'https://www.woodward.com/',
                                'type': RichTextType.TEXT,
                                'text': {
                                    'content': 'These someone avoid.',
                                    'link': {'url': 'https://www.arnold.com/'},
                                },
                            },
                        ],
                        'color': BackgroundColor.BROWN_BACKGROUND,
                        'is_toggleable': False,
                    },
                },
                {
                    "object": "block",
                    "id": "91dfcceb-b7a2-48da-bbb3-4f8db4bbed63",
                    "parent": {"type": "workspace", "workspace": True},
                    "created_time": "2000-10-23T14:47:52.738518",
                    "last_edited_time": "2002-10-16T19:12:59.868332",
                    "created_by": {
                        "object": "user",
                        "id": "9c30bf5b-0f43-4172-ad21-2870959f6976",
                    },
                    "last_edited_by": {
                        "object": "user",
                        "id": "22dafb54-4a0c-4e39-9900-f6281bcd0912",
                    },
                    "has_children": False,
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [
                            {
                                "annotations": {
                                    "bold": True,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "green",
                                },
                                "plain_text": "A one company hour.",
                                "href": "http://white.com/",
                                "type": "mention",
                                "mention": {
                                    "type": "date",
                                    "date": {
                                        "start": "1997-10-29T06:34:04.949878+03:00",
                                        "end": "2005-01-02T12:15:42.844224+03:00",
                                        "time_zone": "Africa/Asmera",
                                    },
                                },
                            },
                            {
                                "annotations": {
                                    "bold": True,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "green",
                                },
                                "plain_text": "A one company hour.",
                                "href": "https://www.woodward.com/",
                                "type": "text",
                                "text": {
                                    "content": "These someone avoid.",
                                    "link": {"url": "https://www.arnold.com/"},
                                },
                            },
                        ],
                        "color": "brown_background",
                        "is_toggleable": False,
                    },
                },
            ),
        ),
        (
            HeadingThreeBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'id': UUID('90fa06ea-6322-40ed-8a2c-26cbfc56b232'),
                    'parent': WorkspaceParent(
                        type=ParentType.WORKSPACE, workspace=True
                    ),
                    'created_time': datetime(2000, 10, 23, 14, 47, 52, 738518),
                    'last_edited_time': datetime(2002, 10, 16, 19, 12, 59, 868332),
                    'created_by': UserRef(
                        object=NotionObjectType.User,
                        id=UUID('9c30bf5b-0f43-4172-ad21-2870959f6976'),
                    ),
                    'last_edited_by': UserRef(
                        object=NotionObjectType.User,
                        id=UUID('22dafb54-4a0c-4e39-9900-f6281bcd0912'),
                    ),
                    'archived': True,
                    'in_trash': False,
                    'has_children': None,
                    'type': BlockType.HEADING_3,
                    'heading_3': Heading(
                        rich_text=[
                            MentionRichText(
                                annotations=Annotations(
                                    bold=True,
                                    italic=None,
                                    strikethrough=False,
                                    underline=False,
                                    code=False,
                                    color=Color.GREEN,
                                ),
                                plain_text='A one company hour.',
                                href='http://white.com/',
                                type=RichTextType.MENTION,
                                mention=DateMention(
                                    type=MentionType.DATE,
                                    date=NotionDate(
                                        start=datetime(
                                            1997,
                                            10,
                                            29,
                                            6,
                                            34,
                                            4,
                                            949878,
                                            tzinfo=ZoneInfo(key='Africa/Asmera'),
                                        ),
                                        end=datetime(
                                            2005,
                                            1,
                                            2,
                                            12,
                                            15,
                                            42,
                                            844224,
                                            tzinfo=ZoneInfo(key='Africa/Asmera'),
                                        ),
                                        time_zone='Africa/Asmera',
                                    ),
                                ),
                            ),
                            TextRichText(
                                annotations=Annotations(
                                    bold=True,
                                    italic=None,
                                    strikethrough=False,
                                    underline=False,
                                    code=False,
                                    color=Color.GREEN,
                                ),
                                plain_text='A one company hour.',
                                href='https://www.woodward.com/',
                                type=RichTextType.TEXT,
                                text=Text(
                                    content='These someone avoid.',
                                    link=NotionUrlObject(url='https://www.arnold.com/'),
                                ),
                            ),
                        ],
                        color=BackgroundColor.BROWN_BACKGROUND,
                        is_toggleable=True,
                    ),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'id': UUID('90fa06ea-6322-40ed-8a2c-26cbfc56b232'),
                    'parent': {'type': ParentType.WORKSPACE, 'workspace': True},
                    'created_time': datetime(2000, 10, 23, 14, 47, 52, 738518),
                    'last_edited_time': datetime(2002, 10, 16, 19, 12, 59, 868332),
                    'created_by': {
                        'object': NotionObjectType.User,
                        'id': UUID('9c30bf5b-0f43-4172-ad21-2870959f6976'),
                    },
                    'last_edited_by': {
                        'object': NotionObjectType.User,
                        'id': UUID('22dafb54-4a0c-4e39-9900-f6281bcd0912'),
                    },
                    'archived': True,
                    'in_trash': False,
                    'type': BlockType.HEADING_3,
                    'heading_3': {
                        'rich_text': [
                            {
                                'annotations': {
                                    'bold': True,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': Color.GREEN,
                                },
                                'plain_text': 'A one company hour.',
                                'href': 'http://white.com/',
                                'type': RichTextType.MENTION,
                                'mention': {
                                    'type': MentionType.DATE,
                                    'date': {
                                        'start': datetime(
                                            1997,
                                            10,
                                            29,
                                            6,
                                            34,
                                            4,
                                            949878,
                                            tzinfo=ZoneInfo(key='Africa/Asmera'),
                                        ),
                                        'end': datetime(
                                            2005,
                                            1,
                                            2,
                                            12,
                                            15,
                                            42,
                                            844224,
                                            tzinfo=ZoneInfo(key='Africa/Asmera'),
                                        ),
                                        'time_zone': 'Africa/Asmera',
                                    },
                                },
                            },
                            {
                                'annotations': {
                                    'bold': True,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': Color.GREEN,
                                },
                                'plain_text': 'A one company hour.',
                                'href': 'https://www.woodward.com/',
                                'type': RichTextType.TEXT,
                                'text': {
                                    'content': 'These someone avoid.',
                                    'link': {'url': 'https://www.arnold.com/'},
                                },
                            },
                        ],
                        'color': BackgroundColor.BROWN_BACKGROUND,
                        'is_toggleable': True,
                    },
                },
                {
                    "object": "block",
                    "id": "90fa06ea-6322-40ed-8a2c-26cbfc56b232",
                    "parent": {"type": "workspace", "workspace": True},
                    "created_time": "2000-10-23T14:47:52.738518",
                    "last_edited_time": "2002-10-16T19:12:59.868332",
                    "created_by": {
                        "object": "user",
                        "id": "9c30bf5b-0f43-4172-ad21-2870959f6976",
                    },
                    "last_edited_by": {
                        "object": "user",
                        "id": "22dafb54-4a0c-4e39-9900-f6281bcd0912",
                    },
                    "archived": True,
                    "in_trash": False,
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [
                            {
                                "annotations": {
                                    "bold": True,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "green",
                                },
                                "plain_text": "A one company hour.",
                                "href": "http://white.com/",
                                "type": "mention",
                                "mention": {
                                    "type": "date",
                                    "date": {
                                        "start": "1997-10-29T06:34:04.949878+03:00",
                                        "end": "2005-01-02T12:15:42.844224+03:00",
                                        "time_zone": "Africa/Asmera",
                                    },
                                },
                            },
                            {
                                "annotations": {
                                    "bold": True,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "green",
                                },
                                "plain_text": "A one company hour.",
                                "href": "https://www.woodward.com/",
                                "type": "text",
                                "text": {
                                    "content": "These someone avoid.",
                                    "link": {"url": "https://www.arnold.com/"},
                                },
                            },
                        ],
                        "color": "brown_background",
                        "is_toggleable": True,
                    },
                },
            ),
        ),
        (
            ImageBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'id': UUID('3cc2a298-822e-4c49-9e0f-1b6da7a2a31d'),
                    'parent': WorkspaceParent(
                        type=ParentType.WORKSPACE, workspace=True
                    ),
                    'created_time': datetime(2000, 10, 23, 14, 47, 52, 738518),
                    'last_edited_time': datetime(2002, 10, 16, 19, 12, 59, 868332),
                    'created_by': UserRef(
                        object=NotionObjectType.User,
                        id=UUID('9c30bf5b-0f43-4172-ad21-2870959f6976'),
                    ),
                    'last_edited_by': UserRef(
                        object=NotionObjectType.User,
                        id=UUID('22dafb54-4a0c-4e39-9900-f6281bcd0912'),
                    ),
                    'archived': True,
                    'in_trash': None,
                    'has_children': True,
                    'type': BlockType.IMAGE,
                    'image': ExternalFile(
                        type=FileType.EXTERNAL,
                        external=ExternalFileObject(url='http://rodriguez-juarez.com/'),
                    ),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'id': UUID('3cc2a298-822e-4c49-9e0f-1b6da7a2a31d'),
                    'parent': {'type': ParentType.WORKSPACE, 'workspace': True},
                    'created_time': datetime(2000, 10, 23, 14, 47, 52, 738518),
                    'last_edited_time': datetime(2002, 10, 16, 19, 12, 59, 868332),
                    'created_by': {
                        'object': NotionObjectType.User,
                        'id': UUID('9c30bf5b-0f43-4172-ad21-2870959f6976'),
                    },
                    'last_edited_by': {
                        'object': NotionObjectType.User,
                        'id': UUID('22dafb54-4a0c-4e39-9900-f6281bcd0912'),
                    },
                    'archived': True,
                    'has_children': True,
                    'type': BlockType.IMAGE,
                    'image': {
                        'type': FileType.EXTERNAL,
                        'external': {'url': 'http://rodriguez-juarez.com/'},
                    },
                },
                {
                    "object": "block",
                    "id": "3cc2a298-822e-4c49-9e0f-1b6da7a2a31d",
                    "parent": {"type": "workspace", "workspace": True},
                    "created_time": "2000-10-23T14:47:52.738518",
                    "last_edited_time": "2002-10-16T19:12:59.868332",
                    "created_by": {
                        "object": "user",
                        "id": "9c30bf5b-0f43-4172-ad21-2870959f6976",
                    },
                    "last_edited_by": {
                        "object": "user",
                        "id": "22dafb54-4a0c-4e39-9900-f6281bcd0912",
                    },
                    "archived": True,
                    "has_children": True,
                    "type": "image",
                    "image": {
                        "type": "external",
                        "external": {"url": "http://rodriguez-juarez.com/"},
                    },
                },
            ),
        ),
        (
            NumberedListItemBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'id': None,
                    'parent': None,
                    'created_time': None,
                    'last_edited_time': None,
                    'created_by': None,
                    'last_edited_by': None,
                    'archived': None,
                    'in_trash': None,
                    'has_children': None,
                    'type': BlockType.NUMBERED_LIST_ITEM,
                    'numbered_list_item': NumberedListItem(
                        rich_text=[
                            TextRichText(
                                annotations=Annotations(
                                    bold=True,
                                    italic=None,
                                    strikethrough=False,
                                    underline=False,
                                    code=False,
                                    color=Color.GREEN,
                                ),
                                plain_text='A one company hour.',
                                href='http://barker.com/',
                                type=RichTextType.TEXT,
                                text=Text(
                                    content='These someone avoid.',
                                    link=NotionUrlObject(url='https://www.arnold.com/'),
                                ),
                            ),
                            TextRichText(
                                annotations=Annotations(
                                    bold=True,
                                    italic=None,
                                    strikethrough=False,
                                    underline=False,
                                    code=False,
                                    color=Color.GREEN,
                                ),
                                plain_text='A one company hour.',
                                href='http://www.hammond.com/',
                                type=RichTextType.TEXT,
                                text=Text(
                                    content='These someone avoid.',
                                    link=NotionUrlObject(url='https://www.arnold.com/'),
                                ),
                            ),
                        ],
                        color=Color.PURPLE,
                        children=[
                            HeadingTwoBlock(
                                object=NotionObjectType.BLOCK,
                                id=None,
                                parent=None,
                                created_time=None,
                                last_edited_time=None,
                                created_by=None,
                                last_edited_by=None,
                                archived=None,
                                in_trash=None,
                                has_children=None,
                                type=BlockType.HEADING_2,
                                heading_2=Heading(
                                    rich_text=[
                                        MentionRichText(
                                            annotations=Annotations(
                                                bold=True,
                                                italic=None,
                                                strikethrough=False,
                                                underline=False,
                                                code=False,
                                                color=Color.GREEN,
                                            ),
                                            plain_text='A one company hour.',
                                            href='http://white.com/',
                                            type=RichTextType.MENTION,
                                            mention=DateMention(
                                                type=MentionType.DATE,
                                                date=NotionDate(
                                                    start=datetime(
                                                        1997,
                                                        10,
                                                        29,
                                                        6,
                                                        34,
                                                        4,
                                                        949878,
                                                        tzinfo=ZoneInfo(
                                                            key='Africa/Asmera'
                                                        ),
                                                    ),
                                                    end=datetime(
                                                        2005,
                                                        1,
                                                        2,
                                                        12,
                                                        15,
                                                        42,
                                                        844224,
                                                        tzinfo=ZoneInfo(
                                                            key='Africa/Asmera'
                                                        ),
                                                    ),
                                                    time_zone='Africa/Asmera',
                                                ),
                                            ),
                                        ),
                                        TextRichText(
                                            annotations=Annotations(
                                                bold=True,
                                                italic=None,
                                                strikethrough=False,
                                                underline=False,
                                                code=False,
                                                color=Color.GREEN,
                                            ),
                                            plain_text='A one company hour.',
                                            href='https://www.woodward.com/',
                                            type=RichTextType.TEXT,
                                            text=Text(
                                                content='These someone avoid.',
                                                link=NotionUrlObject(
                                                    url='https://www.arnold.com/'
                                                ),
                                            ),
                                        ),
                                    ],
                                    color=BackgroundColor.BROWN_BACKGROUND,
                                    is_toggleable=False,
                                ),
                            )
                        ],
                    ),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.NUMBERED_LIST_ITEM,
                    'numbered_list_item': {
                        'rich_text': [
                            {
                                'annotations': {
                                    'bold': True,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': Color.GREEN,
                                },
                                'plain_text': 'A one company hour.',
                                'href': 'http://barker.com/',
                                'type': RichTextType.TEXT,
                                'text': {
                                    'content': 'These someone avoid.',
                                    'link': {'url': 'https://www.arnold.com/'},
                                },
                            },
                            {
                                'annotations': {
                                    'bold': True,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': Color.GREEN,
                                },
                                'plain_text': 'A one company hour.',
                                'href': 'http://www.hammond.com/',
                                'type': RichTextType.TEXT,
                                'text': {
                                    'content': 'These someone avoid.',
                                    'link': {'url': 'https://www.arnold.com/'},
                                },
                            },
                        ],
                        'color': Color.PURPLE,
                        'children': [
                            {
                                'object': NotionObjectType.BLOCK,
                                'type': BlockType.HEADING_2,
                                'heading_2': {
                                    'rich_text': [
                                        {
                                            'annotations': {
                                                'bold': True,
                                                'strikethrough': False,
                                                'underline': False,
                                                'code': False,
                                                'color': Color.GREEN,
                                            },
                                            'plain_text': 'A one company hour.',
                                            'href': 'http://white.com/',
                                            'type': RichTextType.MENTION,
                                            'mention': {
                                                'type': MentionType.DATE,
                                                'date': {
                                                    'start': datetime(
                                                        1997,
                                                        10,
                                                        29,
                                                        6,
                                                        34,
                                                        4,
                                                        949878,
                                                        tzinfo=ZoneInfo(
                                                            key='Africa/Asmera'
                                                        ),
                                                    ),
                                                    'end': datetime(
                                                        2005,
                                                        1,
                                                        2,
                                                        12,
                                                        15,
                                                        42,
                                                        844224,
                                                        tzinfo=ZoneInfo(
                                                            key='Africa/Asmera'
                                                        ),
                                                    ),
                                                    'time_zone': 'Africa/Asmera',
                                                },
                                            },
                                        },
                                        {
                                            'annotations': {
                                                'bold': True,
                                                'strikethrough': False,
                                                'underline': False,
                                                'code': False,
                                                'color': Color.GREEN,
                                            },
                                            'plain_text': 'A one company hour.',
                                            'href': 'https://www.woodward.com/',
                                            'type': RichTextType.TEXT,
                                            'text': {
                                                'content': 'These someone avoid.',
                                                'link': {
                                                    'url': 'https://www.arnold.com/'
                                                },
                                            },
                                        },
                                    ],
                                    'color': BackgroundColor.BROWN_BACKGROUND,
                                    'is_toggleable': False,
                                },
                            }
                        ],
                    },
                },
                {
                    "object": "block",
                    "type": "numbered_list_item",
                    "numbered_list_item": {
                        "rich_text": [
                            {
                                "annotations": {
                                    "bold": True,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "green",
                                },
                                "plain_text": "A one company hour.",
                                "href": "http://barker.com/",
                                "type": "text",
                                "text": {
                                    "content": "These someone avoid.",
                                    "link": {"url": "https://www.arnold.com/"},
                                },
                            },
                            {
                                "annotations": {
                                    "bold": True,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "green",
                                },
                                "plain_text": "A one company hour.",
                                "href": "http://www.hammond.com/",
                                "type": "text",
                                "text": {
                                    "content": "These someone avoid.",
                                    "link": {"url": "https://www.arnold.com/"},
                                },
                            },
                        ],
                        "color": "purple",
                        "children": [
                            {
                                "object": "block",
                                "type": "heading_2",
                                "heading_2": {
                                    "rich_text": [
                                        {
                                            "annotations": {
                                                "bold": True,
                                                "strikethrough": False,
                                                "underline": False,
                                                "code": False,
                                                "color": "green",
                                            },
                                            "plain_text": "A one company hour.",
                                            "href": "http://white.com/",
                                            "type": "mention",
                                            "mention": {
                                                "type": "date",
                                                "date": {
                                                    "start": "1997-10-29T06:34:04.949878+03:00",
                                                    "end": "2005-01-02T12:15:42.844224+03:00",
                                                    "time_zone": "Africa/Asmera",
                                                },
                                            },
                                        },
                                        {
                                            "annotations": {
                                                "bold": True,
                                                "strikethrough": False,
                                                "underline": False,
                                                "code": False,
                                                "color": "green",
                                            },
                                            "plain_text": "A one company hour.",
                                            "href": "https://www.woodward.com/",
                                            "type": "text",
                                            "text": {
                                                "content": "These someone avoid.",
                                                "link": {
                                                    "url": "https://www.arnold.com/"
                                                },
                                            },
                                        },
                                    ],
                                    "color": "brown_background",
                                    "is_toggleable": False,
                                },
                            }
                        ],
                    },
                },
            ),
        ),
        (
            ParagraphBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'id': UUID('12f87753-6a01-4d05-b07f-539257c64938'),
                    'parent': WorkspaceParent(
                        type=ParentType.WORKSPACE, workspace=True
                    ),
                    'created_time': datetime(2000, 10, 23, 14, 47, 52, 738518),
                    'last_edited_time': datetime(2002, 10, 16, 19, 12, 59, 868332),
                    'created_by': UserRef(
                        object=NotionObjectType.User,
                        id=UUID('9c30bf5b-0f43-4172-ad21-2870959f6976'),
                    ),
                    'last_edited_by': UserRef(
                        object=NotionObjectType.User,
                        id=UUID('22dafb54-4a0c-4e39-9900-f6281bcd0912'),
                    ),
                    'archived': True,
                    'in_trash': True,
                    'has_children': None,
                    'type': BlockType.PARAGRAPH,
                    'paragraph': Paragraph(
                        rich_text=[
                            TextRichText(
                                annotations=Annotations(
                                    bold=True,
                                    italic=None,
                                    strikethrough=False,
                                    underline=False,
                                    code=False,
                                    color=Color.GREEN,
                                ),
                                plain_text='A one company hour.',
                                href='http://barker.com/',
                                type=RichTextType.TEXT,
                                text=Text(
                                    content='These someone avoid.',
                                    link=NotionUrlObject(url='https://www.arnold.com/'),
                                ),
                            ),
                            TextRichText(
                                annotations=Annotations(
                                    bold=True,
                                    italic=None,
                                    strikethrough=False,
                                    underline=False,
                                    code=False,
                                    color=Color.GREEN,
                                ),
                                plain_text='A one company hour.',
                                href='http://www.hammond.com/',
                                type=RichTextType.TEXT,
                                text=Text(
                                    content='These someone avoid.',
                                    link=NotionUrlObject(url='https://www.arnold.com/'),
                                ),
                            ),
                        ],
                        color=Color.PURPLE,
                        children=[
                            DividerBlock(
                                object=NotionObjectType.BLOCK,
                                id=None,
                                parent=None,
                                created_time=None,
                                last_edited_time=None,
                                created_by=None,
                                last_edited_by=None,
                                archived=None,
                                in_trash=None,
                                has_children=None,
                                type=BlockType.DIVIDER,
                                divider={},
                            )
                        ],
                    ),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'id': UUID('12f87753-6a01-4d05-b07f-539257c64938'),
                    'parent': {'type': ParentType.WORKSPACE, 'workspace': True},
                    'created_time': datetime(2000, 10, 23, 14, 47, 52, 738518),
                    'last_edited_time': datetime(2002, 10, 16, 19, 12, 59, 868332),
                    'created_by': {
                        'object': NotionObjectType.User,
                        'id': UUID('9c30bf5b-0f43-4172-ad21-2870959f6976'),
                    },
                    'last_edited_by': {
                        'object': NotionObjectType.User,
                        'id': UUID('22dafb54-4a0c-4e39-9900-f6281bcd0912'),
                    },
                    'archived': True,
                    'in_trash': True,
                    'type': BlockType.PARAGRAPH,
                    'paragraph': {
                        'rich_text': [
                            {
                                'annotations': {
                                    'bold': True,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': Color.GREEN,
                                },
                                'plain_text': 'A one company hour.',
                                'href': 'http://barker.com/',
                                'type': RichTextType.TEXT,
                                'text': {
                                    'content': 'These someone avoid.',
                                    'link': {'url': 'https://www.arnold.com/'},
                                },
                            },
                            {
                                'annotations': {
                                    'bold': True,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': Color.GREEN,
                                },
                                'plain_text': 'A one company hour.',
                                'href': 'http://www.hammond.com/',
                                'type': RichTextType.TEXT,
                                'text': {
                                    'content': 'These someone avoid.',
                                    'link': {'url': 'https://www.arnold.com/'},
                                },
                            },
                        ],
                        'color': Color.PURPLE,
                        'children': [
                            {
                                'object': NotionObjectType.BLOCK,
                                'type': BlockType.DIVIDER,
                                'divider': {},
                            }
                        ],
                    },
                },
                {
                    "object": "block",
                    "id": "12f87753-6a01-4d05-b07f-539257c64938",
                    "parent": {"type": "workspace", "workspace": True},
                    "created_time": "2000-10-23T14:47:52.738518",
                    "last_edited_time": "2002-10-16T19:12:59.868332",
                    "created_by": {
                        "object": "user",
                        "id": "9c30bf5b-0f43-4172-ad21-2870959f6976",
                    },
                    "last_edited_by": {
                        "object": "user",
                        "id": "22dafb54-4a0c-4e39-9900-f6281bcd0912",
                    },
                    "archived": True,
                    "in_trash": True,
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "annotations": {
                                    "bold": True,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "green",
                                },
                                "plain_text": "A one company hour.",
                                "href": "http://barker.com/",
                                "type": "text",
                                "text": {
                                    "content": "These someone avoid.",
                                    "link": {"url": "https://www.arnold.com/"},
                                },
                            },
                            {
                                "annotations": {
                                    "bold": True,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "green",
                                },
                                "plain_text": "A one company hour.",
                                "href": "http://www.hammond.com/",
                                "type": "text",
                                "text": {
                                    "content": "These someone avoid.",
                                    "link": {"url": "https://www.arnold.com/"},
                                },
                            },
                        ],
                        "color": "purple",
                        "children": [
                            {"object": "block", "type": "divider", "divider": {}}
                        ],
                    },
                },
            ),
        ),
        (
            PdfBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'id': None,
                    'parent': None,
                    'created_time': None,
                    'last_edited_time': None,
                    'created_by': None,
                    'last_edited_by': None,
                    'archived': None,
                    'in_trash': None,
                    'has_children': None,
                    'type': BlockType.PDF,
                    'pdf': CaptionExternalFile(
                        type=FileType.EXTERNAL,
                        external=ExternalFileObject(url='https://neal.org/'),
                        caption=[
                            TextRichText(
                                annotations=Annotations(
                                    bold=True,
                                    italic=None,
                                    strikethrough=False,
                                    underline=False,
                                    code=False,
                                    color=Color.GREEN,
                                ),
                                plain_text='A one company hour.',
                                href='https://sanchez.com/',
                                type=RichTextType.TEXT,
                                text=Text(
                                    content='These someone avoid.',
                                    link=NotionUrlObject(url='https://www.arnold.com/'),
                                ),
                            ),
                            MentionRichText(
                                annotations=Annotations(
                                    bold=True,
                                    italic=None,
                                    strikethrough=False,
                                    underline=False,
                                    code=False,
                                    color=Color.GREEN,
                                ),
                                plain_text='A one company hour.',
                                href='https://wright.com/',
                                type=RichTextType.MENTION,
                                mention=DatabaseMention(
                                    type=MentionType.DATABASE,
                                    database=NotionObjectRef(
                                        id=UUID('7e5fd597-ae50-4594-8d94-8f909b448e86')
                                    ),
                                ),
                            ),
                        ],
                    ),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.PDF,
                    'pdf': {
                        'type': FileType.EXTERNAL,
                        'external': {'url': 'https://neal.org/'},
                        'caption': [
                            {
                                'annotations': {
                                    'bold': True,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': Color.GREEN,
                                },
                                'plain_text': 'A one company hour.',
                                'href': 'https://sanchez.com/',
                                'type': RichTextType.TEXT,
                                'text': {
                                    'content': 'These someone avoid.',
                                    'link': {'url': 'https://www.arnold.com/'},
                                },
                            },
                            {
                                'annotations': {
                                    'bold': True,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': Color.GREEN,
                                },
                                'plain_text': 'A one company hour.',
                                'href': 'https://wright.com/',
                                'type': RichTextType.MENTION,
                                'mention': {
                                    'type': MentionType.DATABASE,
                                    'database': {
                                        'id': UUID(
                                            '7e5fd597-ae50-4594-8d94-8f909b448e86'
                                        )
                                    },
                                },
                            },
                        ],
                    },
                },
                {
                    "object": "block",
                    "type": "pdf",
                    "pdf": {
                        "type": "external",
                        "external": {"url": "https://neal.org/"},
                        "caption": [
                            {
                                "annotations": {
                                    "bold": True,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "green",
                                },
                                "plain_text": "A one company hour.",
                                "href": "https://sanchez.com/",
                                "type": "text",
                                "text": {
                                    "content": "These someone avoid.",
                                    "link": {"url": "https://www.arnold.com/"},
                                },
                            },
                            {
                                "annotations": {
                                    "bold": True,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "green",
                                },
                                "plain_text": "A one company hour.",
                                "href": "https://wright.com/",
                                "type": "mention",
                                "mention": {
                                    "type": "database",
                                    "database": {
                                        "id": "7e5fd597-ae50-4594-8d94-8f909b448e86"
                                    },
                                },
                            },
                        ],
                    },
                },
            ),
        ),
        (
            QuoteBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'id': None,
                    'parent': None,
                    'created_time': None,
                    'last_edited_time': None,
                    'created_by': None,
                    'last_edited_by': None,
                    'archived': None,
                    'in_trash': None,
                    'has_children': None,
                    'type': BlockType.QUOTE,
                    'quote': Quote(
                        rich_text=[
                            TextRichText(
                                annotations=Annotations(
                                    bold=True,
                                    italic=None,
                                    strikethrough=False,
                                    underline=False,
                                    code=False,
                                    color=Color.GREEN,
                                ),
                                plain_text='A one company hour.',
                                href='http://barker.com/',
                                type=RichTextType.TEXT,
                                text=Text(
                                    content='These someone avoid.',
                                    link=NotionUrlObject(url='https://www.arnold.com/'),
                                ),
                            ),
                            TextRichText(
                                annotations=Annotations(
                                    bold=True,
                                    italic=None,
                                    strikethrough=False,
                                    underline=False,
                                    code=False,
                                    color=Color.GREEN,
                                ),
                                plain_text='A one company hour.',
                                href='http://www.hammond.com/',
                                type=RichTextType.TEXT,
                                text=Text(
                                    content='These someone avoid.',
                                    link=NotionUrlObject(url='https://www.arnold.com/'),
                                ),
                            ),
                        ],
                        color=Color.PURPLE,
                        children=[
                            BreadcrumbBlock(
                                object=NotionObjectType.BLOCK,
                                id=None,
                                parent=None,
                                created_time=None,
                                last_edited_time=None,
                                created_by=None,
                                last_edited_by=None,
                                archived=None,
                                in_trash=None,
                                has_children=None,
                                type=BlockType.BREADCRUMB,
                                breadcrumb={},
                            )
                        ],
                    ),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.QUOTE,
                    'quote': {
                        'rich_text': [
                            {
                                'annotations': {
                                    'bold': True,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': Color.GREEN,
                                },
                                'plain_text': 'A one company hour.',
                                'href': 'http://barker.com/',
                                'type': RichTextType.TEXT,
                                'text': {
                                    'content': 'These someone avoid.',
                                    'link': {'url': 'https://www.arnold.com/'},
                                },
                            },
                            {
                                'annotations': {
                                    'bold': True,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': Color.GREEN,
                                },
                                'plain_text': 'A one company hour.',
                                'href': 'http://www.hammond.com/',
                                'type': RichTextType.TEXT,
                                'text': {
                                    'content': 'These someone avoid.',
                                    'link': {'url': 'https://www.arnold.com/'},
                                },
                            },
                        ],
                        'color': Color.PURPLE,
                        'children': [
                            {
                                'object': NotionObjectType.BLOCK,
                                'type': BlockType.BREADCRUMB,
                                'breadcrumb': {},
                            }
                        ],
                    },
                },
                {
                    "object": "block",
                    "type": "quote",
                    "quote": {
                        "rich_text": [
                            {
                                "annotations": {
                                    "bold": True,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "green",
                                },
                                "plain_text": "A one company hour.",
                                "href": "http://barker.com/",
                                "type": "text",
                                "text": {
                                    "content": "These someone avoid.",
                                    "link": {"url": "https://www.arnold.com/"},
                                },
                            },
                            {
                                "annotations": {
                                    "bold": True,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "green",
                                },
                                "plain_text": "A one company hour.",
                                "href": "http://www.hammond.com/",
                                "type": "text",
                                "text": {
                                    "content": "These someone avoid.",
                                    "link": {"url": "https://www.arnold.com/"},
                                },
                            },
                        ],
                        "color": "purple",
                        "children": [
                            {"object": "block", "type": "breadcrumb", "breadcrumb": {}}
                        ],
                    },
                },
            ),
        ),
        (
            SyncedBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'id': None,
                    'parent': None,
                    'created_time': None,
                    'last_edited_time': None,
                    'created_by': None,
                    'last_edited_by': None,
                    'archived': None,
                    'in_trash': None,
                    'has_children': None,
                    'type': BlockType.SYNCED_BLOCK,
                    'synced_block': DuplicateSynced(
                        synced_from=SyncedFrom(
                            block_id=UUID('5d1cafdf-4f6e-427f-a222-66ee6037a882')
                        ),
                        children=None,
                    ),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.SYNCED_BLOCK,
                    'synced_block': {
                        'synced_from': {
                            'block_id': UUID('5d1cafdf-4f6e-427f-a222-66ee6037a882')
                        }
                    },
                },
                {
                    "object": "block",
                    "type": "synced_block",
                    "synced_block": {
                        "synced_from": {
                            "block_id": "5d1cafdf-4f6e-427f-a222-66ee6037a882"
                        }
                    },
                },
            ),
        ),
        (
            TableBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'id': UUID('8d6c1452-7a20-46d6-98d4-f18d6cd71aad'),
                    'parent': WorkspaceParent(
                        type=ParentType.WORKSPACE, workspace=True
                    ),
                    'created_time': datetime(2000, 10, 23, 14, 47, 52, 738518),
                    'last_edited_time': datetime(2002, 10, 16, 19, 12, 59, 868332),
                    'created_by': UserRef(
                        object=NotionObjectType.User,
                        id=UUID('9c30bf5b-0f43-4172-ad21-2870959f6976'),
                    ),
                    'last_edited_by': UserRef(
                        object=NotionObjectType.User,
                        id=UUID('22dafb54-4a0c-4e39-9900-f6281bcd0912'),
                    ),
                    'archived': None,
                    'in_trash': True,
                    'has_children': True,
                    'type': BlockType.TABLE,
                    'table': Table(
                        table_width=5, has_column_header=True, has_row_header=False
                    ),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'id': UUID('8d6c1452-7a20-46d6-98d4-f18d6cd71aad'),
                    'parent': {'type': ParentType.WORKSPACE, 'workspace': True},
                    'created_time': datetime(2000, 10, 23, 14, 47, 52, 738518),
                    'last_edited_time': datetime(2002, 10, 16, 19, 12, 59, 868332),
                    'created_by': {
                        'object': NotionObjectType.User,
                        'id': UUID('9c30bf5b-0f43-4172-ad21-2870959f6976'),
                    },
                    'last_edited_by': {
                        'object': NotionObjectType.User,
                        'id': UUID('22dafb54-4a0c-4e39-9900-f6281bcd0912'),
                    },
                    'in_trash': True,
                    'has_children': True,
                    'type': BlockType.TABLE,
                    'table': {
                        'table_width': 5,
                        'has_column_header': True,
                        'has_row_header': False,
                    },
                },
                {
                    "object": "block",
                    "id": "8d6c1452-7a20-46d6-98d4-f18d6cd71aad",
                    "parent": {"type": "workspace", "workspace": True},
                    "created_time": "2000-10-23T14:47:52.738518",
                    "last_edited_time": "2002-10-16T19:12:59.868332",
                    "created_by": {
                        "object": "user",
                        "id": "9c30bf5b-0f43-4172-ad21-2870959f6976",
                    },
                    "last_edited_by": {
                        "object": "user",
                        "id": "22dafb54-4a0c-4e39-9900-f6281bcd0912",
                    },
                    "in_trash": True,
                    "has_children": True,
                    "type": "table",
                    "table": {
                        "table_width": 5,
                        "has_column_header": True,
                        "has_row_header": False,
                    },
                },
            ),
        ),
        (
            TableContentBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'id': None,
                    'parent': None,
                    'created_time': None,
                    'last_edited_time': None,
                    'created_by': None,
                    'last_edited_by': None,
                    'archived': None,
                    'in_trash': None,
                    'has_children': None,
                    'type': BlockType.TABLE_OF_CONTENTS,
                    'table_of_contents': Color.RED,
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.TABLE_OF_CONTENTS,
                    'table_of_contents': Color.RED,
                },
                {
                    "object": "block",
                    "type": "table_of_contents",
                    "table_of_contents": "red",
                },
            ),
        ),
        (
            TableRowBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'id': None,
                    'parent': None,
                    'created_time': None,
                    'last_edited_time': None,
                    'created_by': None,
                    'last_edited_by': None,
                    'archived': None,
                    'in_trash': None,
                    'has_children': None,
                    'type': BlockType.TABLE_ROW,
                    'table_row': Cells(
                        rich_text=[
                            TextRichText(
                                annotations=Annotations(
                                    bold=True,
                                    italic=None,
                                    strikethrough=False,
                                    underline=False,
                                    code=False,
                                    color=Color.GREEN,
                                ),
                                plain_text='A one company hour.',
                                href='http://www.johns.com/',
                                type=RichTextType.TEXT,
                                text=Text(
                                    content='These someone avoid.',
                                    link=NotionUrlObject(url='https://www.arnold.com/'),
                                ),
                            ),
                            TextRichText(
                                annotations=Annotations(
                                    bold=True,
                                    italic=None,
                                    strikethrough=False,
                                    underline=False,
                                    code=False,
                                    color=Color.GREEN,
                                ),
                                plain_text='A one company hour.',
                                href='http://hunt.net/',
                                type=RichTextType.TEXT,
                                text=Text(
                                    content='These someone avoid.',
                                    link=NotionUrlObject(url='https://www.arnold.com/'),
                                ),
                            ),
                        ]
                    ),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.TABLE_ROW,
                    'table_row': {
                        'rich_text': [
                            {
                                'annotations': {
                                    'bold': True,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': Color.GREEN,
                                },
                                'plain_text': 'A one company hour.',
                                'href': 'http://www.johns.com/',
                                'type': RichTextType.TEXT,
                                'text': {
                                    'content': 'These someone avoid.',
                                    'link': {'url': 'https://www.arnold.com/'},
                                },
                            },
                            {
                                'annotations': {
                                    'bold': True,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': Color.GREEN,
                                },
                                'plain_text': 'A one company hour.',
                                'href': 'http://hunt.net/',
                                'type': RichTextType.TEXT,
                                'text': {
                                    'content': 'These someone avoid.',
                                    'link': {'url': 'https://www.arnold.com/'},
                                },
                            },
                        ]
                    },
                },
                {
                    "object": "block",
                    "type": "table_row",
                    "table_row": {
                        "rich_text": [
                            {
                                "annotations": {
                                    "bold": True,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "green",
                                },
                                "plain_text": "A one company hour.",
                                "href": "http://www.johns.com/",
                                "type": "text",
                                "text": {
                                    "content": "These someone avoid.",
                                    "link": {"url": "https://www.arnold.com/"},
                                },
                            },
                            {
                                "annotations": {
                                    "bold": True,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "green",
                                },
                                "plain_text": "A one company hour.",
                                "href": "http://hunt.net/",
                                "type": "text",
                                "text": {
                                    "content": "These someone avoid.",
                                    "link": {"url": "https://www.arnold.com/"},
                                },
                            },
                        ]
                    },
                },
            ),
        ),
        (
            ToDoBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'id': None,
                    'parent': None,
                    'created_time': None,
                    'last_edited_time': None,
                    'created_by': None,
                    'last_edited_by': None,
                    'archived': None,
                    'in_trash': None,
                    'has_children': None,
                    'type': BlockType.TO_DO,
                    'to_do': ToDo(
                        rich_text=[
                            TextRichText(
                                annotations=Annotations(
                                    bold=True,
                                    italic=None,
                                    strikethrough=False,
                                    underline=False,
                                    code=False,
                                    color=Color.GREEN,
                                ),
                                plain_text='A one company hour.',
                                href='http://barker.com/',
                                type=RichTextType.TEXT,
                                text=Text(
                                    content='These someone avoid.',
                                    link=NotionUrlObject(url='https://www.arnold.com/'),
                                ),
                            ),
                            TextRichText(
                                annotations=Annotations(
                                    bold=True,
                                    italic=None,
                                    strikethrough=False,
                                    underline=False,
                                    code=False,
                                    color=Color.GREEN,
                                ),
                                plain_text='A one company hour.',
                                href='http://www.hammond.com/',
                                type=RichTextType.TEXT,
                                text=Text(
                                    content='These someone avoid.',
                                    link=NotionUrlObject(url='https://www.arnold.com/'),
                                ),
                            ),
                        ],
                        color=Color.PURPLE,
                        children=[
                            ChildDatabaseBlock(
                                object=NotionObjectType.BLOCK,
                                id=None,
                                parent=None,
                                created_time=None,
                                last_edited_time=None,
                                created_by=None,
                                last_edited_by=None,
                                archived=None,
                                in_trash=None,
                                has_children=None,
                                type=BlockType.CHILD_DATABASE,
                                child_database=ChildDatabase(
                                    title='James Anderson Jr.'
                                ),
                            )
                        ],
                        checked=None,
                    ),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.TO_DO,
                    'to_do': {
                        'rich_text': [
                            {
                                'annotations': {
                                    'bold': True,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': Color.GREEN,
                                },
                                'plain_text': 'A one company hour.',
                                'href': 'http://barker.com/',
                                'type': RichTextType.TEXT,
                                'text': {
                                    'content': 'These someone avoid.',
                                    'link': {'url': 'https://www.arnold.com/'},
                                },
                            },
                            {
                                'annotations': {
                                    'bold': True,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': Color.GREEN,
                                },
                                'plain_text': 'A one company hour.',
                                'href': 'http://www.hammond.com/',
                                'type': RichTextType.TEXT,
                                'text': {
                                    'content': 'These someone avoid.',
                                    'link': {'url': 'https://www.arnold.com/'},
                                },
                            },
                        ],
                        'color': Color.PURPLE,
                        'children': [
                            {
                                'object': NotionObjectType.BLOCK,
                                'type': BlockType.CHILD_DATABASE,
                                'child_database': {'title': 'James Anderson Jr.'},
                            }
                        ],
                    },
                },
                {
                    "object": "block",
                    "type": "to_do",
                    "to_do": {
                        "rich_text": [
                            {
                                "annotations": {
                                    "bold": True,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "green",
                                },
                                "plain_text": "A one company hour.",
                                "href": "http://barker.com/",
                                "type": "text",
                                "text": {
                                    "content": "These someone avoid.",
                                    "link": {"url": "https://www.arnold.com/"},
                                },
                            },
                            {
                                "annotations": {
                                    "bold": True,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "green",
                                },
                                "plain_text": "A one company hour.",
                                "href": "http://www.hammond.com/",
                                "type": "text",
                                "text": {
                                    "content": "These someone avoid.",
                                    "link": {"url": "https://www.arnold.com/"},
                                },
                            },
                        ],
                        "color": "purple",
                        "children": [
                            {
                                "object": "block",
                                "type": "child_database",
                                "child_database": {"title": "James Anderson Jr."},
                            }
                        ],
                    },
                },
            ),
        ),
        (
            ToggleBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'id': UUID('65ffe5c6-f67b-4ce4-8aa6-d296a1dbd216'),
                    'parent': WorkspaceParent(
                        type=ParentType.WORKSPACE, workspace=True
                    ),
                    'created_time': datetime(2000, 10, 23, 14, 47, 52, 738518),
                    'last_edited_time': datetime(2002, 10, 16, 19, 12, 59, 868332),
                    'created_by': UserRef(
                        object=NotionObjectType.User,
                        id=UUID('9c30bf5b-0f43-4172-ad21-2870959f6976'),
                    ),
                    'last_edited_by': UserRef(
                        object=NotionObjectType.User,
                        id=UUID('22dafb54-4a0c-4e39-9900-f6281bcd0912'),
                    ),
                    'archived': None,
                    'in_trash': True,
                    'has_children': None,
                    'type': BlockType.TOGGLE,
                    'toggle': Toggle(
                        rich_text=[
                            TextRichText(
                                annotations=Annotations(
                                    bold=True,
                                    italic=None,
                                    strikethrough=False,
                                    underline=False,
                                    code=False,
                                    color=Color.GREEN,
                                ),
                                plain_text='A one company hour.',
                                href='http://barker.com/',
                                type=RichTextType.TEXT,
                                text=Text(
                                    content='These someone avoid.',
                                    link=NotionUrlObject(url='https://www.arnold.com/'),
                                ),
                            ),
                            TextRichText(
                                annotations=Annotations(
                                    bold=True,
                                    italic=None,
                                    strikethrough=False,
                                    underline=False,
                                    code=False,
                                    color=Color.GREEN,
                                ),
                                plain_text='A one company hour.',
                                href='http://www.hammond.com/',
                                type=RichTextType.TEXT,
                                text=Text(
                                    content='These someone avoid.',
                                    link=NotionUrlObject(url='https://www.arnold.com/'),
                                ),
                            ),
                        ],
                        color=Color.PURPLE,
                        children=[
                            EmbedBlock(
                                object=NotionObjectType.BLOCK,
                                id=None,
                                parent=None,
                                created_time=None,
                                last_edited_time=None,
                                created_by=None,
                                last_edited_by=None,
                                archived=None,
                                in_trash=None,
                                has_children=None,
                                type=BlockType.EMBED,
                                embed=NotionUrlObject(url='http://www.ramsey.com/'),
                            )
                        ],
                    ),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'id': UUID('65ffe5c6-f67b-4ce4-8aa6-d296a1dbd216'),
                    'parent': {'type': ParentType.WORKSPACE, 'workspace': True},
                    'created_time': datetime(2000, 10, 23, 14, 47, 52, 738518),
                    'last_edited_time': datetime(2002, 10, 16, 19, 12, 59, 868332),
                    'created_by': {
                        'object': NotionObjectType.User,
                        'id': UUID('9c30bf5b-0f43-4172-ad21-2870959f6976'),
                    },
                    'last_edited_by': {
                        'object': NotionObjectType.User,
                        'id': UUID('22dafb54-4a0c-4e39-9900-f6281bcd0912'),
                    },
                    'in_trash': True,
                    'type': BlockType.TOGGLE,
                    'toggle': {
                        'rich_text': [
                            {
                                'annotations': {
                                    'bold': True,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': Color.GREEN,
                                },
                                'plain_text': 'A one company hour.',
                                'href': 'http://barker.com/',
                                'type': RichTextType.TEXT,
                                'text': {
                                    'content': 'These someone avoid.',
                                    'link': {'url': 'https://www.arnold.com/'},
                                },
                            },
                            {
                                'annotations': {
                                    'bold': True,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': Color.GREEN,
                                },
                                'plain_text': 'A one company hour.',
                                'href': 'http://www.hammond.com/',
                                'type': RichTextType.TEXT,
                                'text': {
                                    'content': 'These someone avoid.',
                                    'link': {'url': 'https://www.arnold.com/'},
                                },
                            },
                        ],
                        'color': Color.PURPLE,
                        'children': [
                            {
                                'object': NotionObjectType.BLOCK,
                                'type': BlockType.EMBED,
                                'embed': {'url': 'http://www.ramsey.com/'},
                            }
                        ],
                    },
                },
                {
                    "object": "block",
                    "id": "65ffe5c6-f67b-4ce4-8aa6-d296a1dbd216",
                    "parent": {"type": "workspace", "workspace": True},
                    "created_time": "2000-10-23T14:47:52.738518",
                    "last_edited_time": "2002-10-16T19:12:59.868332",
                    "created_by": {
                        "object": "user",
                        "id": "9c30bf5b-0f43-4172-ad21-2870959f6976",
                    },
                    "last_edited_by": {
                        "object": "user",
                        "id": "22dafb54-4a0c-4e39-9900-f6281bcd0912",
                    },
                    "in_trash": True,
                    "type": "toggle",
                    "toggle": {
                        "rich_text": [
                            {
                                "annotations": {
                                    "bold": True,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "green",
                                },
                                "plain_text": "A one company hour.",
                                "href": "http://barker.com/",
                                "type": "text",
                                "text": {
                                    "content": "These someone avoid.",
                                    "link": {"url": "https://www.arnold.com/"},
                                },
                            },
                            {
                                "annotations": {
                                    "bold": True,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "green",
                                },
                                "plain_text": "A one company hour.",
                                "href": "http://www.hammond.com/",
                                "type": "text",
                                "text": {
                                    "content": "These someone avoid.",
                                    "link": {"url": "https://www.arnold.com/"},
                                },
                            },
                        ],
                        "color": "purple",
                        "children": [
                            {
                                "object": "block",
                                "type": "embed",
                                "embed": {"url": "http://www.ramsey.com/"},
                            }
                        ],
                    },
                },
            ),
        ),
        (
            UnsupportedBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'id': None,
                    'parent': None,
                    'created_time': None,
                    'last_edited_time': None,
                    'created_by': None,
                    'last_edited_by': None,
                    'archived': None,
                    'in_trash': None,
                    'has_children': None,
                    'type': BlockType.UNSUPPORTED,
                },
                {'object': NotionObjectType.BLOCK, 'type': BlockType.UNSUPPORTED},
                {"object": "block", "type": "unsupported"},
            ),
        ),
        (
            VideoBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'id': UUID('2c70ab98-7343-41a6-9f50-236b57028679'),
                    'parent': WorkspaceParent(
                        type=ParentType.WORKSPACE, workspace=True
                    ),
                    'created_time': datetime(2000, 10, 23, 14, 47, 52, 738518),
                    'last_edited_time': datetime(2002, 10, 16, 19, 12, 59, 868332),
                    'created_by': UserRef(
                        object=NotionObjectType.User,
                        id=UUID('9c30bf5b-0f43-4172-ad21-2870959f6976'),
                    ),
                    'last_edited_by': UserRef(
                        object=NotionObjectType.User,
                        id=UUID('22dafb54-4a0c-4e39-9900-f6281bcd0912'),
                    ),
                    'archived': True,
                    'in_trash': True,
                    'has_children': None,
                    'type': BlockType.VIDEO,
                    'video': CaptionExternalFile(
                        type=FileType.EXTERNAL,
                        external=ExternalFileObject(url='http://parker.com/'),
                        caption=[
                            MentionRichText(
                                annotations=Annotations(
                                    bold=True,
                                    italic=None,
                                    strikethrough=False,
                                    underline=False,
                                    code=False,
                                    color=Color.GREEN,
                                ),
                                plain_text='A one company hour.',
                                href='https://clark.com/',
                                type=RichTextType.MENTION,
                                mention=DateMention(
                                    type=MentionType.DATE,
                                    date=NotionDate(
                                        start=datetime(
                                            1997,
                                            10,
                                            29,
                                            6,
                                            34,
                                            4,
                                            949878,
                                            tzinfo=ZoneInfo(key='Africa/Asmera'),
                                        ),
                                        end=datetime(
                                            2005,
                                            1,
                                            2,
                                            12,
                                            15,
                                            42,
                                            844224,
                                            tzinfo=ZoneInfo(key='Africa/Asmera'),
                                        ),
                                        time_zone='Africa/Asmera',
                                    ),
                                ),
                            )
                        ],
                    ),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'id': UUID('2c70ab98-7343-41a6-9f50-236b57028679'),
                    'parent': {'type': ParentType.WORKSPACE, 'workspace': True},
                    'created_time': datetime(2000, 10, 23, 14, 47, 52, 738518),
                    'last_edited_time': datetime(2002, 10, 16, 19, 12, 59, 868332),
                    'created_by': {
                        'object': NotionObjectType.User,
                        'id': UUID('9c30bf5b-0f43-4172-ad21-2870959f6976'),
                    },
                    'last_edited_by': {
                        'object': NotionObjectType.User,
                        'id': UUID('22dafb54-4a0c-4e39-9900-f6281bcd0912'),
                    },
                    'archived': True,
                    'in_trash': True,
                    'type': BlockType.VIDEO,
                    'video': {
                        'type': FileType.EXTERNAL,
                        'external': {'url': 'http://parker.com/'},
                        'caption': [
                            {
                                'annotations': {
                                    'bold': True,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': Color.GREEN,
                                },
                                'plain_text': 'A one company hour.',
                                'href': 'https://clark.com/',
                                'type': RichTextType.MENTION,
                                'mention': {
                                    'type': MentionType.DATE,
                                    'date': {
                                        'start': datetime(
                                            1997,
                                            10,
                                            29,
                                            6,
                                            34,
                                            4,
                                            949878,
                                            tzinfo=ZoneInfo(key='Africa/Asmera'),
                                        ),
                                        'end': datetime(
                                            2005,
                                            1,
                                            2,
                                            12,
                                            15,
                                            42,
                                            844224,
                                            tzinfo=ZoneInfo(key='Africa/Asmera'),
                                        ),
                                        'time_zone': 'Africa/Asmera',
                                    },
                                },
                            }
                        ],
                    },
                },
                {
                    "object": "block",
                    "id": "2c70ab98-7343-41a6-9f50-236b57028679",
                    "parent": {"type": "workspace", "workspace": True},
                    "created_time": "2000-10-23T14:47:52.738518",
                    "last_edited_time": "2002-10-16T19:12:59.868332",
                    "created_by": {
                        "object": "user",
                        "id": "9c30bf5b-0f43-4172-ad21-2870959f6976",
                    },
                    "last_edited_by": {
                        "object": "user",
                        "id": "22dafb54-4a0c-4e39-9900-f6281bcd0912",
                    },
                    "archived": True,
                    "in_trash": True,
                    "type": "video",
                    "video": {
                        "type": "external",
                        "external": {"url": "http://parker.com/"},
                        "caption": [
                            {
                                "annotations": {
                                    "bold": True,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "green",
                                },
                                "plain_text": "A one company hour.",
                                "href": "https://clark.com/",
                                "type": "mention",
                                "mention": {
                                    "type": "date",
                                    "date": {
                                        "start": "1997-10-29T06:34:04.949878+03:00",
                                        "end": "2005-01-02T12:15:42.844224+03:00",
                                        "time_zone": "Africa/Asmera",
                                    },
                                },
                            }
                        ],
                    },
                },
            ),
        ),
    ],
)
def test_models_serialization(clz: type[BaseModel], test_data: tuple[dict, dict, dict]):
    PydanticModelTester(clz, test_data).run_all_tests()
