from datetime import datetime
from uuid import UUID

import pytest
from pydantic import BaseModel, ValidationError

from pynotion.models.block import *
from pynotion.models.file import FileType, ExternalFileObject, HostedFileObject
from pynotion.models.object import NotionObjectRef
from pynotion.models.rich_text import (
    RichTextType,
    TxMentionRichText,
    Annotations,
    DateMention,
    MentionType,
    DatabaseMention,
    TxEquationRichText,
    Equation,
    TxTextRichText,
    Text,
    LinkPreviewMention,
)
from pynotion.models.types import NotionDate
from tests.models.model_test_utils import DiscriminatedModelTester, PydanticModelTester


@pytest.mark.parametrize("block_type", list(BlockType))
def test_block_type_enum(block_type):
    assert isinstance(block_type, BlockType)


@pytest.mark.parametrize(
    "invalid_data",
    [
        (TxBookmarkBlock, {"url": None, "caption": []}),
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
        (TxEmbedBlock, {"url": ""}),  # URL cannot be empty
        (
            TxFileBlock,
            {
                "caption": [],
                "name": None,
                "type": "external",
                "external": {"url": "https://companywebsite.com/files/doc.txt"},
            },
        ),  # Name is required
        (
            TxHeadingOneBlock,
            {"rich_text": [], "color": Color.DEFAULT, "is_toggleable": None},
        ),  # is_toggleable required
        (
            TxPdfBlock,
            {"caption": [], "type": "external", "type_object": None},
        ),  # type_object is required
        (
            TxTableBlock,
            {"table_width": 0, "has_column_header": True, "has_row_header": False},
        ),  # Table width must be greater than 0
        (TxTableRowBlock, {"cells": None}),  # Cells should be a list
        (TxTableContentBlock, {"color": None}),  # Color is required
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
    "annotated_clz, expected_clz, input_data",
    [
        (
            TxBlock,
            TxBookmarkBlock,
            {
                "object": "block",
                "type": "bookmark",
                "bookmark": {"url": "http://www.brewer-jones.net/"},
            },
        ),
        (
            TxBlock,
            TxBreadcrumbBlock,
            {"object": "block", "type": "breadcrumb", "breadcrumb": {}},
        ),
        (
            TxBlock,
            TxBulletListItemBlock,
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bullet_list_item": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Section week kitchen.",
                                "link": {"url": "https://www.cox-king.com/"},
                            },
                        }
                    ]
                },
            },
        ),
        (
            TxBlock,
            TxCalloutBlock,
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [
                        {
                            "annotations": {
                                "bold": True,
                                "italic": False,
                                "strikethrough": False,
                                "underline": True,
                                "code": False,
                                "color": "red_background",
                            },
                            "type": "text",
                            "text": {
                                "content": "Section week kitchen.",
                                "link": {"url": "https://www.cox-king.com/"},
                            },
                        }
                    ],
                    "color": "green_background",
                },
            },
        ),
        (
            TxBlock,
            TxChildDatabaseBlock,
            {
                "object": "block",
                "type": "child_database",
                "child_database": {"title": "Timothy Hill DDS"},
            },
        ),
        (
            TxBlock,
            TxChildPageBlock,
            {
                "object": "block",
                "type": "child_page",
                "child_page": {"title": "Melissa Dorsey"},
            },
        ),
        (
            TxBlock,
            TxCodeBlock,
            {
                "object": "block",
                "type": "code",
                "code": {
                    "caption": [
                        {
                            "type": "mention",
                            "mention": {
                                "type": "database",
                                "database": {
                                    "id": "caaeaa12-2a27-4bf4-bcb6-57e8b2b5dcd7"
                                },
                            },
                        }
                    ],
                    "rich_text": [
                        {
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": True,
                                "underline": True,
                                "code": True,
                                "color": "red_background",
                            },
                            "type": "equation",
                            "equation": {
                                "expression": "Degree you reason TV eye. Task its short beautiful. Major direction cut baby move to.\nSee whom ahead owner raise save. Left baby seat evidence."
                            },
                        }
                    ],
                    "language": "markup",
                },
            },
        ),
        (
            TxBlock,
            TxColumnBlock,
            {"object": "block", "type": "column", "column": {}},
        ),
        (
            TxBlock,
            TxColumnListBlock,
            {"object": "block", "type": "column_list", "column_list": {}},
        ),
        (
            TxBlock,
            TxDividerBlock,
            {"object": "block", "type": "divider", "divider": {}},
        ),
        (
            TxBlock,
            TxEmbedBlock,
            {
                "object": "block",
                "type": "embed",
                "embed": {"url": "https://www.ford-bryant.com/"},
            },
        ),
        (
            TxBlock,
            TxEquationBlock,
            {
                "object": "block",
                "type": "equation",
                "equation": {"expression": "AHZKFUdwexLOoEISrOLb"},
            },
        ),
        (
            TxBlock,
            TxFileBlock,
            {
                "object": "block",
                "type": "file",
                "file": {
                    "type": "external",
                    "external": {"url": "http://www.vasquez.com/"},
                    "name": "Katrina Young",
                    "caption": [
                        {
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": True,
                                "color": "red_background",
                            },
                            "type": "mention",
                            "mention": {
                                "type": "date",
                                "date": {"start": "1976-05-08T10:54:25.796193"},
                            },
                        }
                    ],
                },
            },
        ),
        (
            TxBlock,
            TxHeadingOneBlock,
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Section week kitchen.",
                                "link": {"url": "https://www.cox-king.com/"},
                            },
                        }
                    ]
                },
            },
        ),
        (
            TxBlock,
            TxHeadingTwoBlock,
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Section week kitchen.",
                                "link": {"url": "https://www.cox-king.com/"},
                            },
                        }
                    ],
                    "is_toggleable": False,
                },
            },
        ),
        (
            TxBlock,
            TxHeadingThreeBlock,
            {
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Section week kitchen.",
                                "link": {"url": "https://www.cox-king.com/"},
                            },
                        }
                    ],
                    "is_toggleable": True,
                },
            },
        ),
        (
            TxBlock,
            TxImageBlock,
            {
                "object": "block",
                "type": "image",
                "image": {
                    "type": "file",
                    "file": {
                        "url": "http://thomas.net/",
                        "expiry_time": "2015-02-01T17:05:36.823754",
                    },
                },
            },
        ),
        (
            TxBlock,
            TxNumberedListItemBlock,
            {
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Section week kitchen.",
                                "link": {"url": "https://www.cox-king.com/"},
                            },
                        }
                    ]
                },
            },
        ),
        (
            TxBlock,
            TxParagraphBlock,
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Section week kitchen.",
                                "link": {"url": "https://www.cox-king.com/"},
                            },
                        }
                    ],
                    "children": [
                        {
                            "object": "block",
                            "type": "heading_3",
                            "heading_3": {
                                "rich_text": [
                                    {
                                        "type": "text",
                                        "text": {
                                            "content": "Section week kitchen.",
                                            "link": {
                                                "url": "https://www.cox-king.com/"
                                            },
                                        },
                                    }
                                ],
                                "is_toggleable": True,
                            },
                        }
                    ],
                },
            },
        ),
        (
            TxBlock,
            TxPdfBlock,
            {
                "object": "block",
                "type": "pdf",
                "pdf": {
                    "type": "file",
                    "file": {
                        "url": "http://fernandez.org/",
                        "expiry_time": "2015-02-01T17:05:36.823754",
                    },
                    "caption": [
                        {
                            "type": "mention",
                            "mention": {
                                "type": "link_preview",
                                "link_preview": {"url": "http://gill.com/"},
                            },
                        }
                    ],
                },
            },
        ),
        (
            TxBlock,
            TxQuoteBlock,
            {
                "object": "block",
                "type": "quote",
                "quote": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Section week kitchen.",
                                "link": {"url": "https://www.cox-king.com/"},
                            },
                        }
                    ]
                },
            },
        ),
        (
            TxBlock,
            TxSyncedBlock,
            {
                "object": "block",
                "type": "synced_block",
                "synced_block": {
                    "synced_from": {"block_id": "79bdfefd-6e59-43c2-8fc8-38c208e87c42"}
                },
            },
        ),
        (
            TxBlock,
            TxTableBlock,
            {
                "object": "block",
                "type": "table",
                "table": {
                    "table_width": 6,
                    "has_column_header": False,
                    "has_row_header": False,
                },
            },
        ),
        (
            TxBlock,
            TxTableContentBlock,
            {
                "object": "block",
                "type": "table_of_contents",
                "table_of_contents": "orange",
            },
        ),
        (
            TxBlock,
            TxTableRowBlock,
            {
                "object": "block",
                "type": "table_row",
                "table_row": {
                    "rich_text": [
                        {
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": True,
                                "code": True,
                                "color": "red_background",
                            },
                            "type": "equation",
                            "equation": {
                                "expression": "Sign sea economy budget. Fly home big then clearly sure.\nState west song she speech off other. Fund last happy city measure. Plan draw benefit game source range."
                            },
                        }
                    ]
                },
            },
        ),
        (
            TxBlock,
            TxToDoBlock,
            {
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Section week kitchen.",
                                "link": {"url": "https://www.cox-king.com/"},
                            },
                        }
                    ],
                    "children": [
                        {
                            "object": "block",
                            "type": "table_of_contents",
                            "table_of_contents": "red_background",
                        }
                    ],
                },
            },
        ),
        (
            TxBlock,
            TxToggleBlock,
            {
                "object": "block",
                "type": "toggle",
                "toggle": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Section week kitchen.",
                                "link": {"url": "https://www.cox-king.com/"},
                            },
                        }
                    ]
                },
            },
        ),
        (
            TxBlock,
            TxUnsupportedBlock,
            {"object": "block", "type": "unsupported", "unsupported": {}},
        ),
        (
            TxBlock,
            TxVideoBlock,
            {
                "object": "block",
                "type": "video",
                "video": {
                    "type": "file",
                    "file": {
                        "url": "http://johns.com/",
                        "expiry_time": "2015-02-01T17:05:36.823754",
                    },
                    "caption": [
                        {
                            "type": "mention",
                            "mention": {
                                "type": "link_preview",
                                "link_preview": {"url": "http://gill.com/"},
                            },
                        }
                    ],
                },
            },
        ),
    ],
)
def test_tx_block_discriminated_model(
    annotated_clz: type, expected_clz: type, input_data: dict
):
    DiscriminatedModelTester(annotated_clz, expected_clz, **input_data).run_all_tests()


@pytest.mark.parametrize(
    "annotated_clz, expected_clz, input_data",
    [
        (
            RxBlock,
            RxBookmarkBlock,
            {
                "object": "block",
                "id": "696f62bd-f584-4137-b13c-4b10ea2c6d98",
                "created_time": "2011-12-01T09:02:40.368811",
                "last_edited_time": "2006-10-22T12:36:05.810100",
                "created_by": {
                    "object": "user",
                    "id": "3e3048dd-be9f-415e-a9b6-adc6769803d6",
                },
                "last_edited_by": {
                    "object": "user",
                    "id": "6fee47e2-f161-4dad-8788-90c571263dbe",
                },
                "archived": True,
                "has_children": False,
                "type": "bookmark",
                "bookmark": {"url": "https://www.flores.biz/"},
            },
        ),
        (
            RxBlock,
            RxBreadcrumbBlock,
            {
                "object": "block",
                "id": "dd0796c7-19cb-4e35-a70f-f6c7f6a3e47d",
                "created_time": "2011-12-01T09:02:40.368811",
                "last_edited_time": "2006-10-22T12:36:05.810100",
                "created_by": {
                    "object": "user",
                    "id": "3e3048dd-be9f-415e-a9b6-adc6769803d6",
                },
                "last_edited_by": {
                    "object": "user",
                    "id": "6fee47e2-f161-4dad-8788-90c571263dbe",
                },
                "archived": False,
                "in_trash": False,
                "type": "breadcrumb",
                "breadcrumb": {},
            },
        ),
        (
            RxBlock,
            RxBulletListItemBlock,
            {
                "object": "block",
                "id": "3d4f5aef-0c22-4282-8f4a-bcd4bc7f425b",
                "created_time": "2011-12-01T09:02:40.368811",
                "last_edited_time": "2006-10-22T12:36:05.810100",
                "created_by": {
                    "object": "user",
                    "id": "3e3048dd-be9f-415e-a9b6-adc6769803d6",
                },
                "last_edited_by": {
                    "object": "user",
                    "id": "6fee47e2-f161-4dad-8788-90c571263dbe",
                },
                "archived": False,
                "has_children": False,
                "type": "bulleted_list_item",
                "bullet_list_item": {
                    "rich_text": [
                        {
                            "annotations": {
                                "bold": False,
                                "italic": True,
                                "strikethrough": True,
                                "underline": True,
                                "code": True,
                                "color": "red_background",
                            },
                            "plain_text": "Six necessary husband production power.",
                            "href": "http://castro.com/",
                            "type": "equation",
                            "equation": {
                                "expression": "Financial them today whose approach front. Data before ability. Bar mission buy data.\nProfessional reduce for case dog gun.\nBase leave country that enter. Picture party under guy until."
                            },
                        },
                        {
                            "annotations": {
                                "bold": False,
                                "italic": True,
                                "strikethrough": True,
                                "underline": True,
                                "code": True,
                                "color": "red_background",
                            },
                            "plain_text": "Six necessary husband production power.",
                            "href": "https://www.stevens-ward.com/",
                            "type": "equation",
                            "equation": {
                                "expression": "Current interest three. Student turn challenge husband reveal do enjoy."
                            },
                        },
                    ],
                    "children": [
                        {
                            "object": "block",
                            "id": "6a3d0988-4914-49c3-ade8-3c36efa6ee52",
                            "type": "table",
                            "table": {
                                "table_width": 2,
                                "has_column_header": False,
                                "has_row_header": True,
                            },
                        }
                    ],
                    "color": "pink_background",
                },
            },
        ),
        (
            RxBlock,
            RxCalloutBlock,
            {
                "object": "block",
                "id": "4d3a1385-083b-4a7a-9b14-35ff04d63a85",
                "created_time": "2011-12-01T09:02:40.368811",
                "last_edited_time": "2006-10-22T12:36:05.810100",
                "created_by": {
                    "object": "user",
                    "id": "3e3048dd-be9f-415e-a9b6-adc6769803d6",
                },
                "last_edited_by": {
                    "object": "user",
                    "id": "6fee47e2-f161-4dad-8788-90c571263dbe",
                },
                "archived": False,
                "in_trash": False,
                "has_children": False,
                "type": "callout",
                "callout": {
                    "rich_text": [
                        {
                            "annotations": {
                                "bold": False,
                                "italic": True,
                                "strikethrough": True,
                                "underline": True,
                                "code": True,
                                "color": "red_background",
                            },
                            "plain_text": "Six necessary husband production power.",
                            "href": "https://riddle-douglas.biz/",
                            "type": "mention",
                            "mention": {
                                "type": "database",
                                "database": {
                                    "id": "caaeaa12-2a27-4bf4-bcb6-57e8b2b5dcd7"
                                },
                            },
                        },
                        {
                            "annotations": {
                                "bold": False,
                                "italic": True,
                                "strikethrough": True,
                                "underline": True,
                                "code": True,
                                "color": "red_background",
                            },
                            "plain_text": "Six necessary husband production power.",
                            "href": "https://rios.com/",
                            "type": "mention",
                            "mention": {
                                "type": "user",
                                "user": {
                                    "object": "user",
                                    "id": "a12ea4b4-b096-4a58-976b-29dfe44245f0",
                                },
                            },
                        },
                    ],
                    "icon": {
                        "type": "custom_emoji",
                        "custom_emoji": {
                            "id": "ccd3e41f-230c-4eca-9828-2d1928acebfc",
                            "name": "Anthony Myers",
                            "url": "https://dean.biz/",
                        },
                    },
                    "color": "pink",
                },
            },
        ),
        (
            RxBlock,
            RxChildDatabaseBlock,
            {
                "object": "block",
                "id": "f52c6a69-1c96-4984-88d9-a6bc639687d8",
                "created_time": "2011-12-01T09:02:40.368811",
                "last_edited_time": "2006-10-22T12:36:05.810100",
                "created_by": {
                    "object": "user",
                    "id": "3e3048dd-be9f-415e-a9b6-adc6769803d6",
                },
                "last_edited_by": {
                    "object": "user",
                    "id": "6fee47e2-f161-4dad-8788-90c571263dbe",
                },
                "type": "child_database",
                "child_database": {"title": "Nathaniel Stewart"},
            },
        ),
        (
            RxBlock,
            RxChildPageBlock,
            {
                "object": "block",
                "id": "6fd69614-39fd-4e6c-88da-67c6a642b910",
                "created_time": "2011-12-01T09:02:40.368811",
                "last_edited_time": "2006-10-22T12:36:05.810100",
                "created_by": {
                    "object": "user",
                    "id": "3e3048dd-be9f-415e-a9b6-adc6769803d6",
                },
                "last_edited_by": {
                    "object": "user",
                    "id": "6fee47e2-f161-4dad-8788-90c571263dbe",
                },
                "archived": True,
                "in_trash": False,
                "has_children": False,
                "type": "child_page",
                "child_page": {"title": "Curtis Reyes"},
            },
        ),
        (
            RxBlock,
            RxCodeBlock,
            {
                "object": "block",
                "id": "1b2d5fc9-ed59-4b81-b4c9-211923914882",
                "created_time": "2011-12-01T09:02:40.368811",
                "last_edited_time": "2006-10-22T12:36:05.810100",
                "created_by": {
                    "object": "user",
                    "id": "3e3048dd-be9f-415e-a9b6-adc6769803d6",
                },
                "last_edited_by": {
                    "object": "user",
                    "id": "6fee47e2-f161-4dad-8788-90c571263dbe",
                },
                "archived": False,
                "type": "code",
                "code": {
                    "caption": [
                        {
                            "annotations": {
                                "bold": False,
                                "italic": True,
                                "strikethrough": True,
                                "underline": True,
                                "code": True,
                                "color": "red_background",
                            },
                            "plain_text": "Six necessary husband production power.",
                            "href": "http://johnson.com/",
                            "type": "text",
                            "text": {
                                "content": "Section week kitchen.",
                                "link": {"url": "https://www.cox-king.com/"},
                            },
                        }
                    ],
                    "rich_text": [
                        {
                            "annotations": {
                                "bold": False,
                                "italic": True,
                                "strikethrough": True,
                                "underline": True,
                                "code": True,
                                "color": "red_background",
                            },
                            "plain_text": "Six necessary husband production power.",
                            "href": "http://www.adams.com/",
                            "type": "mention",
                            "mention": {
                                "type": "date",
                                "date": {"start": "1976-05-08T10:54:25.796193"},
                            },
                        },
                        {
                            "annotations": {
                                "bold": False,
                                "italic": True,
                                "strikethrough": True,
                                "underline": True,
                                "code": True,
                                "color": "red_background",
                            },
                            "plain_text": "Six necessary husband production power.",
                            "href": "https://www.mcclure.com/",
                            "type": "mention",
                            "mention": {
                                "type": "user",
                                "user": {
                                    "object": "user",
                                    "id": "a12ea4b4-b096-4a58-976b-29dfe44245f0",
                                },
                            },
                        },
                    ],
                    "language": "glsl",
                },
            },
        ),
        (
            RxBlock,
            RxColumnBlock,
            {
                "object": "block",
                "id": "928c6cf4-ee48-4447-8bae-0ec20d9f92f7",
                "created_time": "2011-12-01T09:02:40.368811",
                "last_edited_time": "2006-10-22T12:36:05.810100",
                "created_by": {
                    "object": "user",
                    "id": "3e3048dd-be9f-415e-a9b6-adc6769803d6",
                },
                "last_edited_by": {
                    "object": "user",
                    "id": "6fee47e2-f161-4dad-8788-90c571263dbe",
                },
                "in_trash": False,
                "has_children": False,
                "type": "column",
                "column": {},
            },
        ),
        (
            RxBlock,
            RxColumnListBlock,
            {
                "object": "block",
                "id": "1a1defa0-1465-4498-a3b2-58cb4127207b",
                "created_time": "2011-12-01T09:02:40.368811",
                "last_edited_time": "2006-10-22T12:36:05.810100",
                "created_by": {
                    "object": "user",
                    "id": "3e3048dd-be9f-415e-a9b6-adc6769803d6",
                },
                "last_edited_by": {
                    "object": "user",
                    "id": "6fee47e2-f161-4dad-8788-90c571263dbe",
                },
                "archived": False,
                "type": "column_list",
                "column_list": {},
            },
        ),
        (
            RxBlock,
            RxDividerBlock,
            {
                "object": "block",
                "id": "40046371-2110-4c70-a4c1-42cafcaf6b2a",
                "created_time": "2011-12-01T09:02:40.368811",
                "last_edited_time": "2006-10-22T12:36:05.810100",
                "created_by": {
                    "object": "user",
                    "id": "3e3048dd-be9f-415e-a9b6-adc6769803d6",
                },
                "last_edited_by": {
                    "object": "user",
                    "id": "6fee47e2-f161-4dad-8788-90c571263dbe",
                },
                "archived": True,
                "has_children": False,
                "type": "divider",
                "divider": {},
            },
        ),
        (
            RxBlock,
            RxEmbedBlock,
            {
                "object": "block",
                "id": "052fa6bf-e2c2-4cf7-91f8-c76211c3c05e",
                "created_time": "2011-12-01T09:02:40.368811",
                "last_edited_time": "2006-10-22T12:36:05.810100",
                "created_by": {
                    "object": "user",
                    "id": "3e3048dd-be9f-415e-a9b6-adc6769803d6",
                },
                "last_edited_by": {
                    "object": "user",
                    "id": "6fee47e2-f161-4dad-8788-90c571263dbe",
                },
                "archived": True,
                "in_trash": False,
                "has_children": False,
                "type": "embed",
                "embed": {"url": "https://stewart.com/"},
            },
        ),
        (
            RxBlock,
            RxEquationBlock,
            {
                "object": "block",
                "id": "0c7bb267-df45-4788-8068-81257cd4dd94",
                "created_time": "2011-12-01T09:02:40.368811",
                "last_edited_time": "2006-10-22T12:36:05.810100",
                "created_by": {
                    "object": "user",
                    "id": "3e3048dd-be9f-415e-a9b6-adc6769803d6",
                },
                "last_edited_by": {
                    "object": "user",
                    "id": "6fee47e2-f161-4dad-8788-90c571263dbe",
                },
                "has_children": False,
                "type": "equation",
                "equation": {"expression": "BshavfjIuyhOhQEQsuIx"},
            },
        ),
        (
            RxBlock,
            RxFileBlock,
            {
                "object": "block",
                "id": "a04dcae0-81ba-4fd5-a916-42f737d901d3",
                "created_time": "2011-12-01T09:02:40.368811",
                "last_edited_time": "2006-10-22T12:36:05.810100",
                "created_by": {
                    "object": "user",
                    "id": "3e3048dd-be9f-415e-a9b6-adc6769803d6",
                },
                "last_edited_by": {
                    "object": "user",
                    "id": "6fee47e2-f161-4dad-8788-90c571263dbe",
                },
                "in_trash": False,
                "type": "file",
                "file": {
                    "type": "external",
                    "external": {"url": "http://www.rogers.info/"},
                    "name": "Chad Campbell",
                    "caption": [
                        {
                            "annotations": {
                                "bold": False,
                                "italic": True,
                                "strikethrough": True,
                                "underline": True,
                                "code": True,
                                "color": "red_background",
                            },
                            "plain_text": "Six necessary husband production power.",
                            "href": "https://www.shaw-vega.biz/",
                            "type": "text",
                            "text": {
                                "content": "Section week kitchen.",
                                "link": {"url": "https://www.cox-king.com/"},
                            },
                        }
                    ],
                },
            },
        ),
        (
            RxBlock,
            RxHeadingOneBlock,
            {
                "object": "block",
                "id": "02379efb-183d-4987-94eb-0ddc26ba778f",
                "created_time": "2011-12-01T09:02:40.368811",
                "last_edited_time": "2006-10-22T12:36:05.810100",
                "created_by": {
                    "object": "user",
                    "id": "3e3048dd-be9f-415e-a9b6-adc6769803d6",
                },
                "last_edited_by": {
                    "object": "user",
                    "id": "6fee47e2-f161-4dad-8788-90c571263dbe",
                },
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [
                        {
                            "annotations": {
                                "bold": False,
                                "italic": True,
                                "strikethrough": True,
                                "underline": True,
                                "code": True,
                                "color": "red_background",
                            },
                            "plain_text": "Six necessary husband production power.",
                            "href": "http://www.benson-ward.com/",
                            "type": "mention",
                            "mention": {
                                "type": "database",
                                "database": {
                                    "id": "caaeaa12-2a27-4bf4-bcb6-57e8b2b5dcd7"
                                },
                            },
                        },
                        {
                            "annotations": {
                                "bold": False,
                                "italic": True,
                                "strikethrough": True,
                                "underline": True,
                                "code": True,
                                "color": "red_background",
                            },
                            "plain_text": "Six necessary husband production power.",
                            "href": "http://anderson.com/",
                            "type": "mention",
                            "mention": {
                                "type": "user",
                                "user": {
                                    "object": "user",
                                    "id": "a12ea4b4-b096-4a58-976b-29dfe44245f0",
                                },
                            },
                        },
                    ],
                    "color": "blue",
                    "is_toggleable": False,
                },
            },
        ),
        (
            RxBlock,
            RxHeadingTwoBlock,
            {
                "object": "block",
                "id": "85bc9fe3-0b6f-45d9-b980-8d998c7ae667",
                "created_time": "2011-12-01T09:02:40.368811",
                "last_edited_time": "2006-10-22T12:36:05.810100",
                "created_by": {
                    "object": "user",
                    "id": "3e3048dd-be9f-415e-a9b6-adc6769803d6",
                },
                "last_edited_by": {
                    "object": "user",
                    "id": "6fee47e2-f161-4dad-8788-90c571263dbe",
                },
                "in_trash": True,
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [
                        {
                            "annotations": {
                                "bold": False,
                                "italic": True,
                                "strikethrough": True,
                                "underline": True,
                                "code": True,
                                "color": "red_background",
                            },
                            "plain_text": "Six necessary husband production power.",
                            "href": "http://www.benson-ward.com/",
                            "type": "mention",
                            "mention": {
                                "type": "database",
                                "database": {
                                    "id": "caaeaa12-2a27-4bf4-bcb6-57e8b2b5dcd7"
                                },
                            },
                        },
                        {
                            "annotations": {
                                "bold": False,
                                "italic": True,
                                "strikethrough": True,
                                "underline": True,
                                "code": True,
                                "color": "red_background",
                            },
                            "plain_text": "Six necessary husband production power.",
                            "href": "http://anderson.com/",
                            "type": "mention",
                            "mention": {
                                "type": "user",
                                "user": {
                                    "object": "user",
                                    "id": "a12ea4b4-b096-4a58-976b-29dfe44245f0",
                                },
                            },
                        },
                    ],
                    "color": "blue",
                    "is_toggleable": False,
                },
            },
        ),
        (
            RxBlock,
            RxHeadingThreeBlock,
            {
                "object": "block",
                "id": "dae46ae1-bf50-410c-b303-683ed5b8e043",
                "created_time": "2011-12-01T09:02:40.368811",
                "last_edited_time": "2006-10-22T12:36:05.810100",
                "created_by": {
                    "object": "user",
                    "id": "3e3048dd-be9f-415e-a9b6-adc6769803d6",
                },
                "last_edited_by": {
                    "object": "user",
                    "id": "6fee47e2-f161-4dad-8788-90c571263dbe",
                },
                "in_trash": True,
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [
                        {
                            "annotations": {
                                "bold": False,
                                "italic": True,
                                "strikethrough": True,
                                "underline": True,
                                "code": True,
                                "color": "red_background",
                            },
                            "plain_text": "Six necessary husband production power.",
                            "href": "http://www.benson-ward.com/",
                            "type": "mention",
                            "mention": {
                                "type": "database",
                                "database": {
                                    "id": "caaeaa12-2a27-4bf4-bcb6-57e8b2b5dcd7"
                                },
                            },
                        },
                        {
                            "annotations": {
                                "bold": False,
                                "italic": True,
                                "strikethrough": True,
                                "underline": True,
                                "code": True,
                                "color": "red_background",
                            },
                            "plain_text": "Six necessary husband production power.",
                            "href": "http://anderson.com/",
                            "type": "mention",
                            "mention": {
                                "type": "user",
                                "user": {
                                    "object": "user",
                                    "id": "a12ea4b4-b096-4a58-976b-29dfe44245f0",
                                },
                            },
                        },
                    ],
                    "color": "blue",
                    "is_toggleable": False,
                },
            },
        ),
        (
            RxBlock,
            RxImageBlock,
            {
                "object": "block",
                "id": "1b5b0b2f-2aa3-4b63-9f72-6722b9c8b559",
                "created_time": "2011-12-01T09:02:40.368811",
                "last_edited_time": "2006-10-22T12:36:05.810100",
                "created_by": {
                    "object": "user",
                    "id": "3e3048dd-be9f-415e-a9b6-adc6769803d6",
                },
                "last_edited_by": {
                    "object": "user",
                    "id": "6fee47e2-f161-4dad-8788-90c571263dbe",
                },
                "in_trash": True,
                "has_children": True,
                "type": "image",
                "image": {
                    "type": "file",
                    "file": {
                        "url": "https://craig.info/",
                        "expiry_time": "2015-02-01T17:05:36.823754",
                    },
                },
            },
        ),
        (
            RxBlock,
            RxNumberedListItemBlock,
            {
                "object": "block",
                "id": "21011e1c-9816-4f53-bf9e-c46b26b2396e",
                "created_time": "2011-12-01T09:02:40.368811",
                "last_edited_time": "2006-10-22T12:36:05.810100",
                "created_by": {
                    "object": "user",
                    "id": "3e3048dd-be9f-415e-a9b6-adc6769803d6",
                },
                "last_edited_by": {
                    "object": "user",
                    "id": "6fee47e2-f161-4dad-8788-90c571263dbe",
                },
                "archived": True,
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": [
                        {
                            "annotations": {
                                "bold": False,
                                "italic": True,
                                "strikethrough": True,
                                "underline": True,
                                "code": True,
                                "color": "red_background",
                            },
                            "plain_text": "Six necessary husband production power.",
                            "href": "http://castro.com/",
                            "type": "equation",
                            "equation": {
                                "expression": "Financial them today whose approach front. Data before ability. Bar mission buy data.\nProfessional reduce for case dog gun.\nBase leave country that enter. Picture party under guy until."
                            },
                        },
                        {
                            "annotations": {
                                "bold": False,
                                "italic": True,
                                "strikethrough": True,
                                "underline": True,
                                "code": True,
                                "color": "red_background",
                            },
                            "plain_text": "Six necessary husband production power.",
                            "href": "https://www.stevens-ward.com/",
                            "type": "equation",
                            "equation": {
                                "expression": "Current interest three. Student turn challenge husband reveal do enjoy."
                            },
                        },
                    ],
                    "children": [
                        {
                            "object": "block",
                            "id": "48a7cfc3-3b3b-4662-8feb-3ecf10e9a081",
                            "type": "divider",
                            "divider": {},
                        }
                    ],
                    "color": "pink_background",
                },
            },
        ),
        (
            RxBlock,
            RxParagraphBlock,
            {
                "object": "block",
                "id": "1b5f3c34-1b11-4ed9-8f30-aa26da227b4a",
                "created_time": "2011-12-01T09:02:40.368811",
                "last_edited_time": "2006-10-22T12:36:05.810100",
                "created_by": {
                    "object": "user",
                    "id": "3e3048dd-be9f-415e-a9b6-adc6769803d6",
                },
                "last_edited_by": {
                    "object": "user",
                    "id": "6fee47e2-f161-4dad-8788-90c571263dbe",
                },
                "has_children": False,
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "annotations": {
                                "bold": False,
                                "italic": True,
                                "strikethrough": True,
                                "underline": True,
                                "code": True,
                                "color": "red_background",
                            },
                            "plain_text": "Six necessary husband production power.",
                            "href": "http://castro.com/",
                            "type": "equation",
                            "equation": {
                                "expression": "Financial them today whose approach front. Data before ability. Bar mission buy data.\nProfessional reduce for case dog gun.\nBase leave country that enter. Picture party under guy until."
                            },
                        },
                        {
                            "annotations": {
                                "bold": False,
                                "italic": True,
                                "strikethrough": True,
                                "underline": True,
                                "code": True,
                                "color": "red_background",
                            },
                            "plain_text": "Six necessary husband production power.",
                            "href": "https://www.stevens-ward.com/",
                            "type": "equation",
                            "equation": {
                                "expression": "Current interest three. Student turn challenge husband reveal do enjoy."
                            },
                        },
                    ],
                    "children": [
                        {
                            "object": "block",
                            "id": "5d6f8221-f2a6-41e1-9d1f-5ec32a1babed",
                            "type": "child_page",
                            "child_page": {"title": "Richard Hicks"},
                        }
                    ],
                    "color": "pink_background",
                },
            },
        ),
        (
            RxBlock,
            RxPdfBlock,
            {
                "object": "block",
                "id": "887b051f-1a14-4863-916b-1a06bc095726",
                "created_time": "2011-12-01T09:02:40.368811",
                "last_edited_time": "2006-10-22T12:36:05.810100",
                "created_by": {
                    "object": "user",
                    "id": "3e3048dd-be9f-415e-a9b6-adc6769803d6",
                },
                "last_edited_by": {
                    "object": "user",
                    "id": "6fee47e2-f161-4dad-8788-90c571263dbe",
                },
                "in_trash": False,
                "type": "pdf",
                "pdf": {
                    "type": "external",
                    "external": {"url": "https://sutton.net/"},
                    "caption": [
                        {
                            "annotations": {
                                "bold": False,
                                "italic": True,
                                "strikethrough": True,
                                "underline": True,
                                "code": True,
                                "color": "red_background",
                            },
                            "plain_text": "Six necessary husband production power.",
                            "href": "http://www.reese.net/",
                            "type": "mention",
                            "mention": {
                                "type": "link_preview",
                                "link_preview": {"url": "http://gill.com/"},
                            },
                        }
                    ],
                },
            },
        ),
        (
            RxBlock,
            RxQuoteBlock,
            {
                "object": "block",
                "id": "e007b9ae-e901-49a8-a165-ff6d54041eef",
                "created_time": "2011-12-01T09:02:40.368811",
                "last_edited_time": "2006-10-22T12:36:05.810100",
                "created_by": {
                    "object": "user",
                    "id": "3e3048dd-be9f-415e-a9b6-adc6769803d6",
                },
                "last_edited_by": {
                    "object": "user",
                    "id": "6fee47e2-f161-4dad-8788-90c571263dbe",
                },
                "archived": False,
                "in_trash": True,
                "type": "quote",
                "quote": {
                    "rich_text": [
                        {
                            "annotations": {
                                "bold": False,
                                "italic": True,
                                "strikethrough": True,
                                "underline": True,
                                "code": True,
                                "color": "red_background",
                            },
                            "plain_text": "Six necessary husband production power.",
                            "href": "http://castro.com/",
                            "type": "equation",
                            "equation": {
                                "expression": "Financial them today whose approach front. Data before ability. Bar mission buy data.\nProfessional reduce for case dog gun.\nBase leave country that enter. Picture party under guy until."
                            },
                        },
                        {
                            "annotations": {
                                "bold": False,
                                "italic": True,
                                "strikethrough": True,
                                "underline": True,
                                "code": True,
                                "color": "red_background",
                            },
                            "plain_text": "Six necessary husband production power.",
                            "href": "https://www.stevens-ward.com/",
                            "type": "equation",
                            "equation": {
                                "expression": "Current interest three. Student turn challenge husband reveal do enjoy."
                            },
                        },
                    ],
                    "children": [
                        {
                            "object": "block",
                            "id": "03e453dd-9b01-47b8-a987-82cb0ec05ad7",
                            "type": "image",
                            "image": {
                                "type": "file",
                                "file": {
                                    "url": "http://www.black.biz/",
                                    "expiry_time": "2015-02-01T17:05:36.823754",
                                },
                            },
                        }
                    ],
                    "color": "pink_background",
                },
            },
        ),
        (
            RxBlock,
            RxSyncedBlock,
            {
                "object": "block",
                "id": "5642e863-1714-406f-a6e8-91b24057388c",
                "created_time": "2011-12-01T09:02:40.368811",
                "last_edited_time": "2006-10-22T12:36:05.810100",
                "created_by": {
                    "object": "user",
                    "id": "3e3048dd-be9f-415e-a9b6-adc6769803d6",
                },
                "last_edited_by": {
                    "object": "user",
                    "id": "6fee47e2-f161-4dad-8788-90c571263dbe",
                },
                "archived": False,
                "in_trash": True,
                "type": "synced_block",
                "synced_block": {
                    "synced_from": {"block_id": "79bdfefd-6e59-43c2-8fc8-38c208e87c42"}
                },
            },
        ),
        (
            RxBlock,
            RxTableBlock,
            {
                "object": "block",
                "id": "29d7645c-aeb6-4db4-9d85-b6398c89a358",
                "created_time": "2011-12-01T09:02:40.368811",
                "last_edited_time": "2006-10-22T12:36:05.810100",
                "created_by": {
                    "object": "user",
                    "id": "3e3048dd-be9f-415e-a9b6-adc6769803d6",
                },
                "last_edited_by": {
                    "object": "user",
                    "id": "6fee47e2-f161-4dad-8788-90c571263dbe",
                },
                "type": "table",
                "table": {
                    "table_width": 1,
                    "has_column_header": True,
                    "has_row_header": False,
                },
            },
        ),
        (
            RxBlock,
            RxTableContentBlock,
            {
                "object": "block",
                "id": "63564813-8eec-4f74-8c79-1a7195b18f82",
                "created_time": "2011-12-01T09:02:40.368811",
                "last_edited_time": "2006-10-22T12:36:05.810100",
                "created_by": {
                    "object": "user",
                    "id": "3e3048dd-be9f-415e-a9b6-adc6769803d6",
                },
                "last_edited_by": {
                    "object": "user",
                    "id": "6fee47e2-f161-4dad-8788-90c571263dbe",
                },
                "archived": False,
                "type": "table_of_contents",
                "table_of_contents": "pink",
            },
        ),
        (
            RxBlock,
            RxTableRowBlock,
            {
                "object": "block",
                "id": "e9fac224-413c-4f05-b953-45fbd73f4000",
                "created_time": "2011-12-01T09:02:40.368811",
                "last_edited_time": "2006-10-22T12:36:05.810100",
                "created_by": {
                    "object": "user",
                    "id": "3e3048dd-be9f-415e-a9b6-adc6769803d6",
                },
                "last_edited_by": {
                    "object": "user",
                    "id": "6fee47e2-f161-4dad-8788-90c571263dbe",
                },
                "archived": False,
                "has_children": True,
                "type": "table_row",
                "table_row": {
                    "rich_text": [
                        {
                            "annotations": {
                                "bold": False,
                                "italic": True,
                                "strikethrough": True,
                                "underline": True,
                                "code": True,
                                "color": "red_background",
                            },
                            "plain_text": "Six necessary husband production power.",
                            "href": "https://diaz.biz/",
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
                                "bold": False,
                                "italic": True,
                                "strikethrough": True,
                                "underline": True,
                                "code": True,
                                "color": "red_background",
                            },
                            "plain_text": "Six necessary husband production power.",
                            "href": "https://www.hunter.org/",
                            "type": "equation",
                            "equation": {
                                "expression": "Meeting system appear before about alone. Everybody science across school anything animal evening save. Price into really whole wait."
                            },
                        },
                    ]
                },
            },
        ),
        (
            RxBlock,
            RxToDoBlock,
            {
                "object": "block",
                "id": "9a7e3b31-b76f-4c38-9138-81ecffd9eae6",
                "created_time": "2011-12-01T09:02:40.368811",
                "last_edited_time": "2006-10-22T12:36:05.810100",
                "created_by": {
                    "object": "user",
                    "id": "3e3048dd-be9f-415e-a9b6-adc6769803d6",
                },
                "last_edited_by": {
                    "object": "user",
                    "id": "6fee47e2-f161-4dad-8788-90c571263dbe",
                },
                "type": "to_do",
                "to_do": {
                    "rich_text": [
                        {
                            "annotations": {
                                "bold": False,
                                "italic": True,
                                "strikethrough": True,
                                "underline": True,
                                "code": True,
                                "color": "red_background",
                            },
                            "plain_text": "Six necessary husband production power.",
                            "href": "http://castro.com/",
                            "type": "equation",
                            "equation": {
                                "expression": "Financial them today whose approach front. Data before ability. Bar mission buy data.\nProfessional reduce for case dog gun.\nBase leave country that enter. Picture party under guy until."
                            },
                        },
                        {
                            "annotations": {
                                "bold": False,
                                "italic": True,
                                "strikethrough": True,
                                "underline": True,
                                "code": True,
                                "color": "red_background",
                            },
                            "plain_text": "Six necessary husband production power.",
                            "href": "https://www.stevens-ward.com/",
                            "type": "equation",
                            "equation": {
                                "expression": "Current interest three. Student turn challenge husband reveal do enjoy."
                            },
                        },
                    ],
                    "children": [
                        {
                            "object": "block",
                            "id": "9cb3c029-dcdc-48e1-843c-e1450b92c2df",
                            "type": "code",
                            "code": {
                                "caption": [
                                    {
                                        "annotations": {
                                            "bold": False,
                                            "italic": True,
                                            "strikethrough": True,
                                            "underline": True,
                                            "code": True,
                                            "color": "red_background",
                                        },
                                        "plain_text": "Six necessary husband production power.",
                                        "href": "http://johnson.com/",
                                        "type": "text",
                                        "text": {
                                            "content": "Section week kitchen.",
                                            "link": {
                                                "url": "https://www.cox-king.com/"
                                            },
                                        },
                                    }
                                ],
                                "rich_text": [
                                    {
                                        "annotations": {
                                            "bold": False,
                                            "italic": True,
                                            "strikethrough": True,
                                            "underline": True,
                                            "code": True,
                                            "color": "red_background",
                                        },
                                        "plain_text": "Six necessary husband production power.",
                                        "href": "http://www.adams.com/",
                                        "type": "mention",
                                        "mention": {
                                            "type": "date",
                                            "date": {
                                                "start": "1976-05-08T10:54:25.796193"
                                            },
                                        },
                                    },
                                    {
                                        "annotations": {
                                            "bold": False,
                                            "italic": True,
                                            "strikethrough": True,
                                            "underline": True,
                                            "code": True,
                                            "color": "red_background",
                                        },
                                        "plain_text": "Six necessary husband production power.",
                                        "href": "https://www.mcclure.com/",
                                        "type": "mention",
                                        "mention": {
                                            "type": "user",
                                            "user": {
                                                "object": "user",
                                                "id": "a12ea4b4-b096-4a58-976b-29dfe44245f0",
                                            },
                                        },
                                    },
                                ],
                                "language": "matlab",
                            },
                        }
                    ],
                    "color": "pink_background",
                    "checked": True,
                },
            },
        ),
        (
            RxBlock,
            RxToggleBlock,
            {
                "object": "block",
                "id": "d78c53fe-bb7f-42f8-94d2-7fe326b3aa59",
                "created_time": "2011-12-01T09:02:40.368811",
                "last_edited_time": "2006-10-22T12:36:05.810100",
                "created_by": {
                    "object": "user",
                    "id": "3e3048dd-be9f-415e-a9b6-adc6769803d6",
                },
                "last_edited_by": {
                    "object": "user",
                    "id": "6fee47e2-f161-4dad-8788-90c571263dbe",
                },
                "in_trash": False,
                "has_children": False,
                "type": "toggle",
                "toggle": {
                    "rich_text": [
                        {
                            "annotations": {
                                "bold": False,
                                "italic": True,
                                "strikethrough": True,
                                "underline": True,
                                "code": True,
                                "color": "red_background",
                            },
                            "plain_text": "Six necessary husband production power.",
                            "href": "http://castro.com/",
                            "type": "equation",
                            "equation": {
                                "expression": "Financial them today whose approach front. Data before ability. Bar mission buy data.\nProfessional reduce for case dog gun.\nBase leave country that enter. Picture party under guy until."
                            },
                        },
                        {
                            "annotations": {
                                "bold": False,
                                "italic": True,
                                "strikethrough": True,
                                "underline": True,
                                "code": True,
                                "color": "red_background",
                            },
                            "plain_text": "Six necessary husband production power.",
                            "href": "https://www.stevens-ward.com/",
                            "type": "equation",
                            "equation": {
                                "expression": "Current interest three. Student turn challenge husband reveal do enjoy."
                            },
                        },
                    ],
                    "children": [
                        {
                            "object": "block",
                            "id": "37fc09de-e0d4-4831-a3f9-a5f59b1fba95",
                            "type": "heading_3",
                            "heading_3": {
                                "rich_text": [
                                    {
                                        "annotations": {
                                            "bold": False,
                                            "italic": True,
                                            "strikethrough": True,
                                            "underline": True,
                                            "code": True,
                                            "color": "red_background",
                                        },
                                        "plain_text": "Six necessary husband production power.",
                                        "href": "http://www.benson-ward.com/",
                                        "type": "mention",
                                        "mention": {
                                            "type": "database",
                                            "database": {
                                                "id": "caaeaa12-2a27-4bf4-bcb6-57e8b2b5dcd7"
                                            },
                                        },
                                    },
                                    {
                                        "annotations": {
                                            "bold": False,
                                            "italic": True,
                                            "strikethrough": True,
                                            "underline": True,
                                            "code": True,
                                            "color": "red_background",
                                        },
                                        "plain_text": "Six necessary husband production power.",
                                        "href": "http://anderson.com/",
                                        "type": "mention",
                                        "mention": {
                                            "type": "user",
                                            "user": {
                                                "object": "user",
                                                "id": "a12ea4b4-b096-4a58-976b-29dfe44245f0",
                                            },
                                        },
                                    },
                                ],
                                "color": "blue",
                                "is_toggleable": False,
                            },
                        }
                    ],
                    "color": "pink_background",
                },
            },
        ),
        (
            RxBlock,
            RxUnsupportedBlock,
            {
                "object": "block",
                "id": "f7ac779b-6265-49b8-bd1b-7f325570a2e0",
                "created_time": "2011-12-01T09:02:40.368811",
                "last_edited_time": "2006-10-22T12:36:05.810100",
                "created_by": {
                    "object": "user",
                    "id": "3e3048dd-be9f-415e-a9b6-adc6769803d6",
                },
                "last_edited_by": {
                    "object": "user",
                    "id": "6fee47e2-f161-4dad-8788-90c571263dbe",
                },
                "archived": False,
                "has_children": False,
                "type": "unsupported",
                "unsupported": {},
            },
        ),
        (
            RxBlock,
            RxVideoBlock,
            {
                "object": "block",
                "id": "aca6b6ab-f5d0-4c9e-9968-1bc6036a7885",
                "created_time": "2011-12-01T09:02:40.368811",
                "last_edited_time": "2006-10-22T12:36:05.810100",
                "created_by": {
                    "object": "user",
                    "id": "3e3048dd-be9f-415e-a9b6-adc6769803d6",
                },
                "last_edited_by": {
                    "object": "user",
                    "id": "6fee47e2-f161-4dad-8788-90c571263dbe",
                },
                "archived": True,
                "type": "video",
                "video": {
                    "type": "external",
                    "external": {"url": "http://flores.net/"},
                    "caption": [
                        {
                            "annotations": {
                                "bold": False,
                                "italic": True,
                                "strikethrough": True,
                                "underline": True,
                                "code": True,
                                "color": "red_background",
                            },
                            "plain_text": "Six necessary husband production power.",
                            "href": "https://hernandez.com/",
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
                },
            },
        ),
    ],
)
def test_rx_block_discriminated_model(
    annotated_clz: type, expected_clz: type, input_data: dict
):
    DiscriminatedModelTester(annotated_clz, expected_clz, **input_data).run_all_tests()


@pytest.mark.parametrize(
    "clz, test_data",
    [
        (
            TxBookmarkBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.BOOKMARK,
                    'bookmark': TxBookmark(
                        caption=[
                            TxTextRichText(
                                annotations=None,
                                type=RichTextType.TEXT,
                                text=Text(
                                    content='Miss page set than bank democratic million.',
                                    link=NotionUrlObject(url='http://clarke.com/'),
                                ),
                            )
                        ],
                        url='https://ortiz.info/',
                    ),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.BOOKMARK,
                    'bookmark': {
                        'caption': [
                            {
                                'type': RichTextType.TEXT,
                                'text': {
                                    'content': 'Miss page set than bank democratic million.',
                                    'link': {'url': 'http://clarke.com/'},
                                },
                            }
                        ],
                        'url': 'https://ortiz.info/',
                    },
                },
                {
                    "object": "block",
                    "type": "bookmark",
                    "bookmark": {
                        "caption": [
                            {
                                "type": "text",
                                "text": {
                                    "content": "Miss page set than bank democratic million.",
                                    "link": {"url": "http://clarke.com/"},
                                },
                            }
                        ],
                        "url": "https://ortiz.info/",
                    },
                },
            ),
        ),
        (
            TxBreadcrumbBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.BREADCRUMB,
                    'breadcrumb': {},
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.BREADCRUMB,
                    'breadcrumb': {},
                },
                {"object": "block", "type": "breadcrumb", "breadcrumb": {}},
            ),
        ),
        (
            TxBulletListItemBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.BULLETED_LIST_ITEM,
                    'bullet_list_item': TxBulletListItem(
                        rich_text=[
                            TxTextRichText(
                                annotations=Annotations(
                                    bold=False,
                                    italic=False,
                                    strikethrough=True,
                                    underline=False,
                                    code=False,
                                    color=BackgroundColor.PINK_BACKGROUND,
                                ),
                                type=RichTextType.TEXT,
                                text=Text(
                                    content='Miss page set than bank democratic million.',
                                    link=NotionUrlObject(url='http://clarke.com/'),
                                ),
                            ),
                            TxMentionRichText(
                                annotations=None,
                                type=RichTextType.MENTION,
                                mention=LinkPreviewMention(
                                    type=MentionType.LINK_PREVIEW,
                                    link_preview=NotionUrlObject(
                                        url='http://barber.com/'
                                    ),
                                ),
                            ),
                        ],
                        children=None,
                        color=BackgroundColor.GRAY_BACKGROUND,
                    ),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.BULLETED_LIST_ITEM,
                    'bullet_list_item': {
                        'rich_text': [
                            {
                                'annotations': {
                                    'bold': False,
                                    'italic': False,
                                    'strikethrough': True,
                                    'underline': False,
                                    'code': False,
                                    'color': BackgroundColor.PINK_BACKGROUND,
                                },
                                'type': RichTextType.TEXT,
                                'text': {
                                    'content': 'Miss page set than bank democratic million.',
                                    'link': {'url': 'http://clarke.com/'},
                                },
                            },
                            {
                                'type': RichTextType.MENTION,
                                'mention': {
                                    'type': MentionType.LINK_PREVIEW,
                                    'link_preview': {'url': 'http://barber.com/'},
                                },
                            },
                        ],
                        'color': BackgroundColor.GRAY_BACKGROUND,
                    },
                },
                {
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bullet_list_item": {
                        "rich_text": [
                            {
                                "annotations": {
                                    "bold": False,
                                    "italic": False,
                                    "strikethrough": True,
                                    "underline": False,
                                    "code": False,
                                    "color": "pink_background",
                                },
                                "type": "text",
                                "text": {
                                    "content": "Miss page set than bank democratic million.",
                                    "link": {"url": "http://clarke.com/"},
                                },
                            },
                            {
                                "type": "mention",
                                "mention": {
                                    "type": "link_preview",
                                    "link_preview": {"url": "http://barber.com/"},
                                },
                            },
                        ],
                        "color": "gray_background",
                    },
                },
            ),
        ),
        (
            TxCalloutBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.CALLOUT,
                    'callout': TxCallout(
                        rich_text=[
                            TxTextRichText(
                                annotations=None,
                                type=RichTextType.TEXT,
                                text=Text(
                                    content='Miss page set than bank democratic million.',
                                    link=NotionUrlObject(url='http://clarke.com/'),
                                ),
                            ),
                            TxEquationRichText(
                                annotations=None,
                                type=RichTextType.EQUATION,
                                equation=Equation(
                                    expression='More area piece light develop water despite. Especially score project school listen increase one.\nChild glass discussion force. Involve put home various.'
                                ),
                            ),
                        ],
                        icon=HostedFile(
                            type=FileType.FILE,
                            file=HostedFileObject(
                                url='http://www.rivera.net/',
                                expiry_time=datetime(2008, 9, 19, 4, 19, 54, 80617),
                            ),
                        ),
                        color=None,
                    ),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.CALLOUT,
                    'callout': {
                        'rich_text': [
                            {
                                'type': RichTextType.TEXT,
                                'text': {
                                    'content': 'Miss page set than bank democratic million.',
                                    'link': {'url': 'http://clarke.com/'},
                                },
                            },
                            {
                                'type': RichTextType.EQUATION,
                                'equation': {
                                    'expression': 'More area piece light develop water despite. Especially score project school listen increase one.\nChild glass discussion force. Involve put home various.'
                                },
                            },
                        ],
                        'icon': {
                            'type': FileType.FILE,
                            'file': {
                                'url': 'http://www.rivera.net/',
                                'expiry_time': datetime(2008, 9, 19, 4, 19, 54, 80617),
                            },
                        },
                    },
                },
                {
                    "object": "block",
                    "type": "callout",
                    "callout": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": "Miss page set than bank democratic million.",
                                    "link": {"url": "http://clarke.com/"},
                                },
                            },
                            {
                                "type": "equation",
                                "equation": {
                                    "expression": "More area piece light develop water despite. Especially score project school listen increase one.\nChild glass discussion force. Involve put home various."
                                },
                            },
                        ],
                        "icon": {
                            "type": "file",
                            "file": {
                                "url": "http://www.rivera.net/",
                                "expiry_time": "2008-09-19T04:19:54.080617",
                            },
                        },
                    },
                },
            ),
        ),
        (
            TxChildDatabaseBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.CHILD_DATABASE,
                    'child_database': ChildDatabase(title='James Snyder'),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.CHILD_DATABASE,
                    'child_database': {'title': 'James Snyder'},
                },
                {
                    "object": "block",
                    "type": "child_database",
                    "child_database": {"title": "James Snyder"},
                },
            ),
        ),
        (
            TxChildPageBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.CHILD_PAGE,
                    'child_page': ChildPage(title='Raymond Thompson'),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.CHILD_PAGE,
                    'child_page': {'title': 'Raymond Thompson'},
                },
                {
                    "object": "block",
                    "type": "child_page",
                    "child_page": {"title": "Raymond Thompson"},
                },
            ),
        ),
        (
            TxCodeBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.CODE,
                    'code': TxCode(
                        caption=[
                            TxMentionRichText(
                                annotations=Annotations(
                                    bold=False,
                                    italic=True,
                                    strikethrough=False,
                                    underline=True,
                                    code=True,
                                    color=BackgroundColor.PINK_BACKGROUND,
                                ),
                                type=RichTextType.MENTION,
                                mention=DateMention(
                                    type=MentionType.DATE,
                                    date=NotionDate(
                                        start=datetime(1991, 9, 13, 4, 30, 38, 559479),
                                        end=None,
                                        time_zone=None,
                                    ),
                                ),
                            )
                        ],
                        rich_text=[
                            TxMentionRichText(
                                annotations=Annotations(
                                    bold=True,
                                    italic=True,
                                    strikethrough=False,
                                    underline=True,
                                    code=True,
                                    color=BackgroundColor.PINK_BACKGROUND,
                                ),
                                type=RichTextType.MENTION,
                                mention=DatabaseMention(
                                    type=MentionType.DATABASE,
                                    database=NotionObjectRef(
                                        id=UUID('c1fcbfc1-6149-4090-8960-f330c74d21cd')
                                    ),
                                ),
                            ),
                            TxEquationRichText(
                                annotations=Annotations(
                                    bold=False,
                                    italic=False,
                                    strikethrough=False,
                                    underline=True,
                                    code=True,
                                    color=BackgroundColor.PINK_BACKGROUND,
                                ),
                                type=RichTextType.EQUATION,
                                equation=Equation(
                                    expression='Exist economy east always. Situation professor artist several television image research. Do father door worry science. Campaign especially TV figure.'
                                ),
                            ),
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
                                    'bold': False,
                                    'italic': True,
                                    'strikethrough': False,
                                    'underline': True,
                                    'code': True,
                                    'color': BackgroundColor.PINK_BACKGROUND,
                                },
                                'type': RichTextType.MENTION,
                                'mention': {
                                    'type': MentionType.DATE,
                                    'date': {
                                        'start': datetime(
                                            1991, 9, 13, 4, 30, 38, 559479
                                        )
                                    },
                                },
                            }
                        ],
                        'rich_text': [
                            {
                                'annotations': {
                                    'bold': True,
                                    'italic': True,
                                    'strikethrough': False,
                                    'underline': True,
                                    'code': True,
                                    'color': BackgroundColor.PINK_BACKGROUND,
                                },
                                'type': RichTextType.MENTION,
                                'mention': {
                                    'type': MentionType.DATABASE,
                                    'database': {
                                        'id': UUID(
                                            'c1fcbfc1-6149-4090-8960-f330c74d21cd'
                                        )
                                    },
                                },
                            },
                            {
                                'annotations': {
                                    'bold': False,
                                    'italic': False,
                                    'strikethrough': False,
                                    'underline': True,
                                    'code': True,
                                    'color': BackgroundColor.PINK_BACKGROUND,
                                },
                                'type': RichTextType.EQUATION,
                                'equation': {
                                    'expression': 'Exist economy east always. Situation professor artist several television image research. Do father door worry science. Campaign especially TV figure.'
                                },
                            },
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
                                    "bold": False,
                                    "italic": True,
                                    "strikethrough": False,
                                    "underline": True,
                                    "code": True,
                                    "color": "pink_background",
                                },
                                "type": "mention",
                                "mention": {
                                    "type": "date",
                                    "date": {"start": "1991-09-13T04:30:38.559479"},
                                },
                            }
                        ],
                        "rich_text": [
                            {
                                "annotations": {
                                    "bold": True,
                                    "italic": True,
                                    "strikethrough": False,
                                    "underline": True,
                                    "code": True,
                                    "color": "pink_background",
                                },
                                "type": "mention",
                                "mention": {
                                    "type": "database",
                                    "database": {
                                        "id": "c1fcbfc1-6149-4090-8960-f330c74d21cd"
                                    },
                                },
                            },
                            {
                                "annotations": {
                                    "bold": False,
                                    "italic": False,
                                    "strikethrough": False,
                                    "underline": True,
                                    "code": True,
                                    "color": "pink_background",
                                },
                                "type": "equation",
                                "equation": {
                                    "expression": "Exist economy east always. Situation professor artist several television image research. Do father door worry science. Campaign especially TV figure."
                                },
                            },
                        ],
                        "language": "php",
                    },
                },
            ),
        ),
        (
            TxColumnBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
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
            TxColumnListBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
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
            TxDividerBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.DIVIDER,
                    'divider': {},
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.DIVIDER,
                    'divider': {},
                },
                {"object": "block", "type": "divider", "divider": {}},
            ),
        ),
        (
            TxEmbedBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.EMBED,
                    'embed': NotionUrlObject(url='https://www.mcdaniel-nelson.net/'),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.EMBED,
                    'embed': {'url': 'https://www.mcdaniel-nelson.net/'},
                },
                {
                    "object": "block",
                    "type": "embed",
                    "embed": {"url": "https://www.mcdaniel-nelson.net/"},
                },
            ),
        ),
        (
            TxEquationBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.EQUATION,
                    'equation': NotionEquation(expression='SBWnZKYOCXkIukujsIaQ'),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.EQUATION,
                    'equation': {'expression': 'SBWnZKYOCXkIukujsIaQ'},
                },
                {
                    "object": "block",
                    "type": "equation",
                    "equation": {"expression": "SBWnZKYOCXkIukujsIaQ"},
                },
            ),
        ),
        (
            TxFileBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.FILE,
                    'file': TxCaptionHostedFileWithName(
                        type=FileType.FILE,
                        file=HostedFileObject(
                            url='http://miranda.com/',
                            expiry_time=datetime(2008, 9, 19, 4, 19, 54, 80617),
                        ),
                        name='Martin Smith',
                        caption=[
                            TxMentionRichText(
                                annotations=Annotations(
                                    bold=False,
                                    italic=True,
                                    strikethrough=True,
                                    underline=True,
                                    code=True,
                                    color=BackgroundColor.PINK_BACKGROUND,
                                ),
                                type=RichTextType.MENTION,
                                mention=DateMention(
                                    type=MentionType.DATE,
                                    date=NotionDate(
                                        start=datetime(1991, 9, 13, 4, 30, 38, 559479),
                                        end=None,
                                        time_zone=None,
                                    ),
                                ),
                            )
                        ],
                    ),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.FILE,
                    'file': {
                        'type': FileType.FILE,
                        'file': {
                            'url': 'http://miranda.com/',
                            'expiry_time': datetime(2008, 9, 19, 4, 19, 54, 80617),
                        },
                        'name': 'Martin Smith',
                        'caption': [
                            {
                                'annotations': {
                                    'bold': False,
                                    'italic': True,
                                    'strikethrough': True,
                                    'underline': True,
                                    'code': True,
                                    'color': BackgroundColor.PINK_BACKGROUND,
                                },
                                'type': RichTextType.MENTION,
                                'mention': {
                                    'type': MentionType.DATE,
                                    'date': {
                                        'start': datetime(
                                            1991, 9, 13, 4, 30, 38, 559479
                                        )
                                    },
                                },
                            }
                        ],
                    },
                },
                {
                    "object": "block",
                    "type": "file",
                    "file": {
                        "type": "file",
                        "file": {
                            "url": "http://miranda.com/",
                            "expiry_time": "2008-09-19T04:19:54.080617",
                        },
                        "name": "Martin Smith",
                        "caption": [
                            {
                                "annotations": {
                                    "bold": False,
                                    "italic": True,
                                    "strikethrough": True,
                                    "underline": True,
                                    "code": True,
                                    "color": "pink_background",
                                },
                                "type": "mention",
                                "mention": {
                                    "type": "date",
                                    "date": {"start": "1991-09-13T04:30:38.559479"},
                                },
                            }
                        ],
                    },
                },
            ),
        ),
        (
            TxHeadingOneBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.HEADING_1,
                    'heading_1': TxHeading(
                        rich_text=[
                            TxEquationRichText(
                                annotations=None,
                                type=RichTextType.EQUATION,
                                equation=Equation(
                                    expression='Girl special policy garden.\nWho couple information rise meet who focus. Now simple vote system turn member.'
                                ),
                            )
                        ],
                        color=None,
                        is_toggleable=None,
                    ),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.HEADING_1,
                    'heading_1': {
                        'rich_text': [
                            {
                                'type': RichTextType.EQUATION,
                                'equation': {
                                    'expression': 'Girl special policy garden.\nWho couple information rise meet who focus. Now simple vote system turn member.'
                                },
                            }
                        ]
                    },
                },
                {
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [
                            {
                                "type": "equation",
                                "equation": {
                                    "expression": "Girl special policy garden.\nWho couple information rise meet who focus. Now simple vote system turn member."
                                },
                            }
                        ]
                    },
                },
            ),
        ),
        (
            TxHeadingTwoBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.HEADING_2,
                    'heading_2': TxHeading(
                        rich_text=[
                            TxEquationRichText(
                                annotations=None,
                                type=RichTextType.EQUATION,
                                equation=Equation(
                                    expression='Girl special policy garden.\nWho couple information rise meet who focus. Now simple vote system turn member.'
                                ),
                            )
                        ],
                        color=None,
                        is_toggleable=True,
                    ),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.HEADING_2,
                    'heading_2': {
                        'rich_text': [
                            {
                                'type': RichTextType.EQUATION,
                                'equation': {
                                    'expression': 'Girl special policy garden.\nWho couple information rise meet who focus. Now simple vote system turn member.'
                                },
                            }
                        ],
                        'is_toggleable': True,
                    },
                },
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [
                            {
                                "type": "equation",
                                "equation": {
                                    "expression": "Girl special policy garden.\nWho couple information rise meet who focus. Now simple vote system turn member."
                                },
                            }
                        ],
                        "is_toggleable": True,
                    },
                },
            ),
        ),
        (
            TxHeadingThreeBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.HEADING_3,
                    'heading_3': TxHeading(
                        rich_text=[
                            TxEquationRichText(
                                annotations=None,
                                type=RichTextType.EQUATION,
                                equation=Equation(
                                    expression='Girl special policy garden.\nWho couple information rise meet who focus. Now simple vote system turn member.'
                                ),
                            )
                        ],
                        color=None,
                        is_toggleable=False,
                    ),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.HEADING_3,
                    'heading_3': {
                        'rich_text': [
                            {
                                'type': RichTextType.EQUATION,
                                'equation': {
                                    'expression': 'Girl special policy garden.\nWho couple information rise meet who focus. Now simple vote system turn member.'
                                },
                            }
                        ],
                        'is_toggleable': False,
                    },
                },
                {
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [
                            {
                                "type": "equation",
                                "equation": {
                                    "expression": "Girl special policy garden.\nWho couple information rise meet who focus. Now simple vote system turn member."
                                },
                            }
                        ],
                        "is_toggleable": False,
                    },
                },
            ),
        ),
        (
            TxImageBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.IMAGE,
                    'image': ExternalFile(
                        type=FileType.EXTERNAL,
                        external=ExternalFileObject(url='https://camacho.info/'),
                    ),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.IMAGE,
                    'image': {
                        'type': FileType.EXTERNAL,
                        'external': {'url': 'https://camacho.info/'},
                    },
                },
                {
                    "object": "block",
                    "type": "image",
                    "image": {
                        "type": "external",
                        "external": {"url": "https://camacho.info/"},
                    },
                },
            ),
        ),
        (
            TxNumberedListItemBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.NUMBERED_LIST_ITEM,
                    'numbered_list_item': TxNumberedListItem(
                        rich_text=[
                            TxTextRichText(
                                annotations=Annotations(
                                    bold=False,
                                    italic=False,
                                    strikethrough=True,
                                    underline=False,
                                    code=False,
                                    color=BackgroundColor.PINK_BACKGROUND,
                                ),
                                type=RichTextType.TEXT,
                                text=Text(
                                    content='Miss page set than bank democratic million.',
                                    link=NotionUrlObject(url='http://clarke.com/'),
                                ),
                            ),
                            TxMentionRichText(
                                annotations=None,
                                type=RichTextType.MENTION,
                                mention=LinkPreviewMention(
                                    type=MentionType.LINK_PREVIEW,
                                    link_preview=NotionUrlObject(
                                        url='http://barber.com/'
                                    ),
                                ),
                            ),
                        ],
                        children=None,
                        color=BackgroundColor.GRAY_BACKGROUND,
                    ),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.NUMBERED_LIST_ITEM,
                    'numbered_list_item': {
                        'rich_text': [
                            {
                                'annotations': {
                                    'bold': False,
                                    'italic': False,
                                    'strikethrough': True,
                                    'underline': False,
                                    'code': False,
                                    'color': BackgroundColor.PINK_BACKGROUND,
                                },
                                'type': RichTextType.TEXT,
                                'text': {
                                    'content': 'Miss page set than bank democratic million.',
                                    'link': {'url': 'http://clarke.com/'},
                                },
                            },
                            {
                                'type': RichTextType.MENTION,
                                'mention': {
                                    'type': MentionType.LINK_PREVIEW,
                                    'link_preview': {'url': 'http://barber.com/'},
                                },
                            },
                        ],
                        'color': BackgroundColor.GRAY_BACKGROUND,
                    },
                },
                {
                    "object": "block",
                    "type": "numbered_list_item",
                    "numbered_list_item": {
                        "rich_text": [
                            {
                                "annotations": {
                                    "bold": False,
                                    "italic": False,
                                    "strikethrough": True,
                                    "underline": False,
                                    "code": False,
                                    "color": "pink_background",
                                },
                                "type": "text",
                                "text": {
                                    "content": "Miss page set than bank democratic million.",
                                    "link": {"url": "http://clarke.com/"},
                                },
                            },
                            {
                                "type": "mention",
                                "mention": {
                                    "type": "link_preview",
                                    "link_preview": {"url": "http://barber.com/"},
                                },
                            },
                        ],
                        "color": "gray_background",
                    },
                },
            ),
        ),
        (
            TxParagraphBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.PARAGRAPH,
                    'paragraph': TxParagraph(
                        rich_text=[
                            TxTextRichText(
                                annotations=Annotations(
                                    bold=False,
                                    italic=False,
                                    strikethrough=True,
                                    underline=False,
                                    code=False,
                                    color=BackgroundColor.PINK_BACKGROUND,
                                ),
                                type=RichTextType.TEXT,
                                text=Text(
                                    content='Miss page set than bank democratic million.',
                                    link=NotionUrlObject(url='http://clarke.com/'),
                                ),
                            ),
                            TxMentionRichText(
                                annotations=None,
                                type=RichTextType.MENTION,
                                mention=LinkPreviewMention(
                                    type=MentionType.LINK_PREVIEW,
                                    link_preview=NotionUrlObject(
                                        url='http://barber.com/'
                                    ),
                                ),
                            ),
                        ],
                        children=None,
                        color=BackgroundColor.GRAY_BACKGROUND,
                    ),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.PARAGRAPH,
                    'paragraph': {
                        'rich_text': [
                            {
                                'annotations': {
                                    'bold': False,
                                    'italic': False,
                                    'strikethrough': True,
                                    'underline': False,
                                    'code': False,
                                    'color': BackgroundColor.PINK_BACKGROUND,
                                },
                                'type': RichTextType.TEXT,
                                'text': {
                                    'content': 'Miss page set than bank democratic million.',
                                    'link': {'url': 'http://clarke.com/'},
                                },
                            },
                            {
                                'type': RichTextType.MENTION,
                                'mention': {
                                    'type': MentionType.LINK_PREVIEW,
                                    'link_preview': {'url': 'http://barber.com/'},
                                },
                            },
                        ],
                        'color': BackgroundColor.GRAY_BACKGROUND,
                    },
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "annotations": {
                                    "bold": False,
                                    "italic": False,
                                    "strikethrough": True,
                                    "underline": False,
                                    "code": False,
                                    "color": "pink_background",
                                },
                                "type": "text",
                                "text": {
                                    "content": "Miss page set than bank democratic million.",
                                    "link": {"url": "http://clarke.com/"},
                                },
                            },
                            {
                                "type": "mention",
                                "mention": {
                                    "type": "link_preview",
                                    "link_preview": {"url": "http://barber.com/"},
                                },
                            },
                        ],
                        "color": "gray_background",
                    },
                },
            ),
        ),
        (
            TxPdfBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.PDF,
                    'pdf': TxCaptionExternalFile(
                        type=FileType.EXTERNAL,
                        external=ExternalFileObject(url='https://young-escobar.net/'),
                        caption=[
                            TxTextRichText(
                                annotations=Annotations(
                                    bold=False,
                                    italic=False,
                                    strikethrough=False,
                                    underline=False,
                                    code=False,
                                    color=BackgroundColor.PINK_BACKGROUND,
                                ),
                                type=RichTextType.TEXT,
                                text=Text(
                                    content='Miss page set than bank democratic million.',
                                    link=NotionUrlObject(url='http://clarke.com/'),
                                ),
                            )
                        ],
                    ),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.PDF,
                    'pdf': {
                        'type': FileType.EXTERNAL,
                        'external': {'url': 'https://young-escobar.net/'},
                        'caption': [
                            {
                                'annotations': {
                                    'bold': False,
                                    'italic': False,
                                    'strikethrough': False,
                                    'underline': False,
                                    'code': False,
                                    'color': BackgroundColor.PINK_BACKGROUND,
                                },
                                'type': RichTextType.TEXT,
                                'text': {
                                    'content': 'Miss page set than bank democratic million.',
                                    'link': {'url': 'http://clarke.com/'},
                                },
                            }
                        ],
                    },
                },
                {
                    "object": "block",
                    "type": "pdf",
                    "pdf": {
                        "type": "external",
                        "external": {"url": "https://young-escobar.net/"},
                        "caption": [
                            {
                                "annotations": {
                                    "bold": False,
                                    "italic": False,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "pink_background",
                                },
                                "type": "text",
                                "text": {
                                    "content": "Miss page set than bank democratic million.",
                                    "link": {"url": "http://clarke.com/"},
                                },
                            }
                        ],
                    },
                },
            ),
        ),
        (
            TxQuoteBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.QUOTE,
                    'quote': TxQuote(
                        rich_text=[
                            TxTextRichText(
                                annotations=Annotations(
                                    bold=False,
                                    italic=False,
                                    strikethrough=True,
                                    underline=False,
                                    code=False,
                                    color=BackgroundColor.PINK_BACKGROUND,
                                ),
                                type=RichTextType.TEXT,
                                text=Text(
                                    content='Miss page set than bank democratic million.',
                                    link=NotionUrlObject(url='http://clarke.com/'),
                                ),
                            ),
                            TxMentionRichText(
                                annotations=None,
                                type=RichTextType.MENTION,
                                mention=LinkPreviewMention(
                                    type=MentionType.LINK_PREVIEW,
                                    link_preview=NotionUrlObject(
                                        url='http://barber.com/'
                                    ),
                                ),
                            ),
                        ],
                        children=[
                            TxFileBlock(
                                object=NotionObjectType.BLOCK,
                                type=BlockType.FILE,
                                file=TxCaptionExternalFileWithName(
                                    type=FileType.EXTERNAL,
                                    external=ExternalFileObject(
                                        url='https://www.mack-lara.info/'
                                    ),
                                    name='Denise Cantu',
                                    caption=[
                                        TxTextRichText(
                                            annotations=None,
                                            type=RichTextType.TEXT,
                                            text=Text(
                                                content='Miss page set than bank democratic million.',
                                                link=NotionUrlObject(
                                                    url='http://clarke.com/'
                                                ),
                                            ),
                                        ),
                                        TxTextRichText(
                                            annotations=Annotations(
                                                bold=True,
                                                italic=False,
                                                strikethrough=True,
                                                underline=True,
                                                code=True,
                                                color=BackgroundColor.PINK_BACKGROUND,
                                            ),
                                            type=RichTextType.TEXT,
                                            text=Text(
                                                content='Miss page set than bank democratic million.',
                                                link=NotionUrlObject(
                                                    url='http://clarke.com/'
                                                ),
                                            ),
                                        ),
                                    ],
                                ),
                            )
                        ],
                        color=BackgroundColor.GRAY_BACKGROUND,
                    ),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.QUOTE,
                    'quote': {
                        'rich_text': [
                            {
                                'annotations': {
                                    'bold': False,
                                    'italic': False,
                                    'strikethrough': True,
                                    'underline': False,
                                    'code': False,
                                    'color': BackgroundColor.PINK_BACKGROUND,
                                },
                                'type': RichTextType.TEXT,
                                'text': {
                                    'content': 'Miss page set than bank democratic million.',
                                    'link': {'url': 'http://clarke.com/'},
                                },
                            },
                            {
                                'type': RichTextType.MENTION,
                                'mention': {
                                    'type': MentionType.LINK_PREVIEW,
                                    'link_preview': {'url': 'http://barber.com/'},
                                },
                            },
                        ],
                        'children': [
                            {
                                'object': NotionObjectType.BLOCK,
                                'type': BlockType.FILE,
                                'file': {
                                    'type': FileType.EXTERNAL,
                                    'external': {'url': 'https://www.mack-lara.info/'},
                                    'name': 'Denise Cantu',
                                    'caption': [
                                        {
                                            'type': RichTextType.TEXT,
                                            'text': {
                                                'content': 'Miss page set than bank democratic million.',
                                                'link': {'url': 'http://clarke.com/'},
                                            },
                                        },
                                        {
                                            'annotations': {
                                                'bold': True,
                                                'italic': False,
                                                'strikethrough': True,
                                                'underline': True,
                                                'code': True,
                                                'color': BackgroundColor.PINK_BACKGROUND,
                                            },
                                            'type': RichTextType.TEXT,
                                            'text': {
                                                'content': 'Miss page set than bank democratic million.',
                                                'link': {'url': 'http://clarke.com/'},
                                            },
                                        },
                                    ],
                                },
                            }
                        ],
                        'color': BackgroundColor.GRAY_BACKGROUND,
                    },
                },
                {
                    "object": "block",
                    "type": "quote",
                    "quote": {
                        "rich_text": [
                            {
                                "annotations": {
                                    "bold": False,
                                    "italic": False,
                                    "strikethrough": True,
                                    "underline": False,
                                    "code": False,
                                    "color": "pink_background",
                                },
                                "type": "text",
                                "text": {
                                    "content": "Miss page set than bank democratic million.",
                                    "link": {"url": "http://clarke.com/"},
                                },
                            },
                            {
                                "type": "mention",
                                "mention": {
                                    "type": "link_preview",
                                    "link_preview": {"url": "http://barber.com/"},
                                },
                            },
                        ],
                        "children": [
                            {
                                "object": "block",
                                "type": "file",
                                "file": {
                                    "type": "external",
                                    "external": {"url": "https://www.mack-lara.info/"},
                                    "name": "Denise Cantu",
                                    "caption": [
                                        {
                                            "type": "text",
                                            "text": {
                                                "content": "Miss page set than bank democratic million.",
                                                "link": {"url": "http://clarke.com/"},
                                            },
                                        },
                                        {
                                            "annotations": {
                                                "bold": True,
                                                "italic": False,
                                                "strikethrough": True,
                                                "underline": True,
                                                "code": True,
                                                "color": "pink_background",
                                            },
                                            "type": "text",
                                            "text": {
                                                "content": "Miss page set than bank democratic million.",
                                                "link": {"url": "http://clarke.com/"},
                                            },
                                        },
                                    ],
                                },
                            }
                        ],
                        "color": "gray_background",
                    },
                },
            ),
        ),
        (
            TxSyncedBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.SYNCED_BLOCK,
                    'synced_block': TxOriginalSynced(synced_from=None, children=[]),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.SYNCED_BLOCK,
                    'synced_block': {'children': []},
                },
                {
                    "object": "block",
                    "type": "synced_block",
                    "synced_block": {"children": []},
                },
            ),
        ),
        (
            TxTableBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.TABLE,
                    'table': Table(
                        table_width=1, has_column_header=True, has_row_header=True
                    ),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.TABLE,
                    'table': {
                        'table_width': 1,
                        'has_column_header': True,
                        'has_row_header': True,
                    },
                },
                {
                    "object": "block",
                    "type": "table",
                    "table": {
                        "table_width": 1,
                        "has_column_header": True,
                        "has_row_header": True,
                    },
                },
            ),
        ),
        (
            TxTableContentBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.TABLE_OF_CONTENTS,
                    'table_of_contents': BackgroundColor.BLUE_BACKGROUND,
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.TABLE_OF_CONTENTS,
                    'table_of_contents': BackgroundColor.BLUE_BACKGROUND,
                },
                {
                    "object": "block",
                    "type": "table_of_contents",
                    "table_of_contents": "blue_background",
                },
            ),
        ),
        (
            TxTableRowBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.TABLE_ROW,
                    'table_row': TxCells(
                        rich_text=[
                            TxMentionRichText(
                                annotations=Annotations(
                                    bold=False,
                                    italic=False,
                                    strikethrough=True,
                                    underline=False,
                                    code=False,
                                    color=BackgroundColor.PINK_BACKGROUND,
                                ),
                                type=RichTextType.MENTION,
                                mention=DateMention(
                                    type=MentionType.DATE,
                                    date=NotionDate(
                                        start=datetime(1991, 9, 13, 4, 30, 38, 559479),
                                        end=None,
                                        time_zone=None,
                                    ),
                                ),
                            )
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
                                    'bold': False,
                                    'italic': False,
                                    'strikethrough': True,
                                    'underline': False,
                                    'code': False,
                                    'color': BackgroundColor.PINK_BACKGROUND,
                                },
                                'type': RichTextType.MENTION,
                                'mention': {
                                    'type': MentionType.DATE,
                                    'date': {
                                        'start': datetime(
                                            1991, 9, 13, 4, 30, 38, 559479
                                        )
                                    },
                                },
                            }
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
                                    "bold": False,
                                    "italic": False,
                                    "strikethrough": True,
                                    "underline": False,
                                    "code": False,
                                    "color": "pink_background",
                                },
                                "type": "mention",
                                "mention": {
                                    "type": "date",
                                    "date": {"start": "1991-09-13T04:30:38.559479"},
                                },
                            }
                        ]
                    },
                },
            ),
        ),
        (
            TxToDoBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.TO_DO,
                    'to_do': TxToDo(
                        rich_text=[
                            TxTextRichText(
                                annotations=Annotations(
                                    bold=False,
                                    italic=False,
                                    strikethrough=True,
                                    underline=False,
                                    code=False,
                                    color=BackgroundColor.PINK_BACKGROUND,
                                ),
                                type=RichTextType.TEXT,
                                text=Text(
                                    content='Miss page set than bank democratic million.',
                                    link=NotionUrlObject(url='http://clarke.com/'),
                                ),
                            ),
                            TxMentionRichText(
                                annotations=None,
                                type=RichTextType.MENTION,
                                mention=LinkPreviewMention(
                                    type=MentionType.LINK_PREVIEW,
                                    link_preview=NotionUrlObject(
                                        url='http://barber.com/'
                                    ),
                                ),
                            ),
                        ],
                        children=None,
                        color=BackgroundColor.GRAY_BACKGROUND,
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
                                    'bold': False,
                                    'italic': False,
                                    'strikethrough': True,
                                    'underline': False,
                                    'code': False,
                                    'color': BackgroundColor.PINK_BACKGROUND,
                                },
                                'type': RichTextType.TEXT,
                                'text': {
                                    'content': 'Miss page set than bank democratic million.',
                                    'link': {'url': 'http://clarke.com/'},
                                },
                            },
                            {
                                'type': RichTextType.MENTION,
                                'mention': {
                                    'type': MentionType.LINK_PREVIEW,
                                    'link_preview': {'url': 'http://barber.com/'},
                                },
                            },
                        ],
                        'color': BackgroundColor.GRAY_BACKGROUND,
                    },
                },
                {
                    "object": "block",
                    "type": "to_do",
                    "to_do": {
                        "rich_text": [
                            {
                                "annotations": {
                                    "bold": False,
                                    "italic": False,
                                    "strikethrough": True,
                                    "underline": False,
                                    "code": False,
                                    "color": "pink_background",
                                },
                                "type": "text",
                                "text": {
                                    "content": "Miss page set than bank democratic million.",
                                    "link": {"url": "http://clarke.com/"},
                                },
                            },
                            {
                                "type": "mention",
                                "mention": {
                                    "type": "link_preview",
                                    "link_preview": {"url": "http://barber.com/"},
                                },
                            },
                        ],
                        "color": "gray_background",
                    },
                },
            ),
        ),
        (
            TxToggleBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.TOGGLE,
                    'toggle': TxToggle(
                        rich_text=[
                            TxTextRichText(
                                annotations=Annotations(
                                    bold=False,
                                    italic=False,
                                    strikethrough=True,
                                    underline=False,
                                    code=False,
                                    color=BackgroundColor.PINK_BACKGROUND,
                                ),
                                type=RichTextType.TEXT,
                                text=Text(
                                    content='Miss page set than bank democratic million.',
                                    link=NotionUrlObject(url='http://clarke.com/'),
                                ),
                            ),
                            TxMentionRichText(
                                annotations=None,
                                type=RichTextType.MENTION,
                                mention=LinkPreviewMention(
                                    type=MentionType.LINK_PREVIEW,
                                    link_preview=NotionUrlObject(
                                        url='http://barber.com/'
                                    ),
                                ),
                            ),
                        ],
                        children=None,
                        color=BackgroundColor.GRAY_BACKGROUND,
                    ),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.TOGGLE,
                    'toggle': {
                        'rich_text': [
                            {
                                'annotations': {
                                    'bold': False,
                                    'italic': False,
                                    'strikethrough': True,
                                    'underline': False,
                                    'code': False,
                                    'color': BackgroundColor.PINK_BACKGROUND,
                                },
                                'type': RichTextType.TEXT,
                                'text': {
                                    'content': 'Miss page set than bank democratic million.',
                                    'link': {'url': 'http://clarke.com/'},
                                },
                            },
                            {
                                'type': RichTextType.MENTION,
                                'mention': {
                                    'type': MentionType.LINK_PREVIEW,
                                    'link_preview': {'url': 'http://barber.com/'},
                                },
                            },
                        ],
                        'color': BackgroundColor.GRAY_BACKGROUND,
                    },
                },
                {
                    "object": "block",
                    "type": "toggle",
                    "toggle": {
                        "rich_text": [
                            {
                                "annotations": {
                                    "bold": False,
                                    "italic": False,
                                    "strikethrough": True,
                                    "underline": False,
                                    "code": False,
                                    "color": "pink_background",
                                },
                                "type": "text",
                                "text": {
                                    "content": "Miss page set than bank democratic million.",
                                    "link": {"url": "http://clarke.com/"},
                                },
                            },
                            {
                                "type": "mention",
                                "mention": {
                                    "type": "link_preview",
                                    "link_preview": {"url": "http://barber.com/"},
                                },
                            },
                        ],
                        "color": "gray_background",
                    },
                },
            ),
        ),
        (
            TxUnsupportedBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.UNSUPPORTED,
                    'unsupported': {},
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.UNSUPPORTED,
                    'unsupported': {},
                },
                {"object": "block", "type": "unsupported", "unsupported": {}},
            ),
        ),
        (
            TxVideoBlock,
            (
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.VIDEO,
                    'video': TxCaptionExternalFile(
                        type=FileType.EXTERNAL,
                        external=ExternalFileObject(url='https://lee.com/'),
                        caption=None,
                    ),
                },
                {
                    'object': NotionObjectType.BLOCK,
                    'type': BlockType.VIDEO,
                    'video': {
                        'type': FileType.EXTERNAL,
                        'external': {'url': 'https://lee.com/'},
                    },
                },
                {
                    "object": "block",
                    "type": "video",
                    "video": {
                        "type": "external",
                        "external": {"url": "https://lee.com/"},
                    },
                },
            ),
        ),
    ],
)
def test_models_serialization(clz: type[BaseModel], test_data: tuple[dict, dict, dict]):
    PydanticModelTester(clz, test_data).run_all_tests()
