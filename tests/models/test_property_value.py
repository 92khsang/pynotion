from datetime import datetime
from uuid import UUID

import pytest
from pydantic import BaseModel

from pynotion.models import *
from tests.models.model_test_utils import DiscriminatedModelTester, PydanticModelTester


@pytest.mark.parametrize(
    "annotated_clz, expected_clz, input_data",
    [
        (
            FormulaValue,
            BooleanFormulaValue,
            {"type": "boolean", "boolean": True},
        ),
        (
            FormulaValue,
            DateFormulaValue,
            {"type": "date"},
        ),
        (
            FormulaValue,
            NumberFormulaValue,
            {"type": "number", "number": 660221758},
        ),
        (
            FormulaValue,
            StringFormulaValue,
            {
                "type": "string",
                "string": "Half prove important lawyer policy. Society relationship whom dinner. Do theory receive others any time probably.\nDebate sure relate affect city evening teach. Couple cell rest once.",
            },
        ),
    ],
)
def test_formula_discriminated_model(
    annotated_clz: type, expected_clz: type, input_data: dict
):
    DiscriminatedModelTester(annotated_clz, expected_clz, **input_data).run_all_tests()


@pytest.mark.parametrize(
    "annotated_clz, expected_clz, input_data",
    [
        (
            RollupValue,
            ArrayRollupValue,
            {
                "type": "array",
                "array": [
                    {
                        "id": "04c5305e-0e23-48e2-b08f-22d28dbb85b0",
                        "type": "multi_select",
                        "multi_select": [
                            {
                                "id": "a90f3f9a-b673-45ce-b8c9-13d0675592f3",
                                "name": "Ms. Allison Morrison",
                                "color": "red",
                            }
                        ],
                    },
                    {
                        "id": "51f80270-2470-481d-b356-00d9cc083aa7",
                        "type": "title",
                        "title": [
                            {
                                "annotations": {
                                    "bold": False,
                                    "italic": True,
                                    "strikethrough": False,
                                    "underline": False,
                                    "code": False,
                                    "color": "orange",
                                },
                                "plain_text": "Reflect wonder member history.",
                                "href": "https://griffin.com/",
                                "type": "mention",
                                "mention": {
                                    "type": "link_preview",
                                    "link_preview": {
                                        "url": "http://www.noble-jackson.net/"
                                    },
                                },
                            }
                        ],
                    },
                ],
                "function": "count",
            },
        ),
        (
            RollupValue,
            DateRollupValue,
            {"type": "date", "function": "max"},
        ),
        (
            RollupValue,
            IncompleteRollupValue,
            {"type": "incomplete", "incomplete": {}, "function": "count"},
        ),
        (
            RollupValue,
            NumberRollupValue,
            {"type": "number", "number": 901578739, "function": "count"},
        ),
        (
            RollupValue,
            UnsupportedRollupValue,
            {"type": "unsupported", "unsupported": {}, "function": "count"},
        ),
    ],
)
def test_rollup_discriminated_model(
    annotated_clz: type, expected_clz: type, input_data: dict
):
    DiscriminatedModelTester(annotated_clz, expected_clz, **input_data).run_all_tests()


@pytest.mark.parametrize(
    "annotated_clz, expected_clz, input_data",
    [
        (
            RxPropertyValue,
            RxCheckboxPropertyValue,
            {
                "id": "756e717a-4e63-4d35-bf10-38df8bc35ad5",
                "type": "checkbox",
                "checkbox": False,
            },
        ),
        (
            RxPropertyValue,
            CreatedByPropertyValue,
            {
                "id": "ad140cfe-42dd-44ac-af46-6567f0e8229b",
                "type": "created_by",
                "created_by": {
                    "object": "user",
                    "id": "af1f1a1b-0d19-4f9a-8c53-58e9aea58063",
                    "name": "James Villa",
                    "avatar_url": "http://robinson.net/",
                    "type": "bot",
                    "bot": {
                        "owner": {"type": "workspace", "workspace": True},
                        "workspace_name": "Sample Workspace",
                    },
                },
            },
        ),
        (
            RxPropertyValue,
            CreatedTimePropertyValue,
            {
                "id": "539ed431-0aa6-48c8-a19d-e170ad3328e4",
                "type": "created_time",
                "created_time": "2013-11-02T04:00:49.809823",
            },
        ),
        (
            RxPropertyValue,
            RxDatePropertyValue,
            {
                "id": "a45261b0-5d2e-4838-884a-19e422ed39fc",
                "type": "date",
                "date": {
                    "start": "2005-02-17T07:14:37.856871",
                    "time_zone": "America/Antigua",
                },
            },
        ),
        (
            RxPropertyValue,
            RxEmailPropertyValue,
            {
                "id": "1127ec64-2759-479f-ba6c-2a7acb6525b6",
                "type": "email",
                "email": "jakesanders@example.net",
            },
        ),
        (
            RxPropertyValue,
            RxFilesPropertyValue,
            {
                "id": "e76ce5f8-70a3-479c-8e22-5891022c2deb",
                "type": "files",
                "files": [
                    {
                        "type": "external",
                        "external": {"url": "https://russell.com/"},
                        "name": "Danielle Horn",
                    }
                ],
            },
        ),
        (
            RxPropertyValue,
            FormulaPropertyValue,
            {
                "id": "7c995a9e-476d-4a54-b13f-312b996bb7cc",
                "type": "formula",
                "formula": {"type": "date"},
            },
        ),
        (
            RxPropertyValue,
            LastEditedByPropertyValue,
            {
                "id": "656c708e-af39-4744-8fa2-a02503e172a6",
                "type": "last_edited_by",
                "last_edited_by": {
                    "object": "user",
                    "id": "0c70339d-e16e-4c77-b519-cb8215aa135f",
                    "name": "Eric Small",
                    "avatar_url": "https://www.carney.com/",
                    "type": "bot",
                    "bot": {
                        "owner": {"type": "workspace", "workspace": True},
                        "workspace_name": "Sample Workspace",
                    },
                },
            },
        ),
        (
            RxPropertyValue,
            LastEditedTimePropertyValue,
            {
                "id": "66b5d295-fdde-4855-a768-058dac85cab0",
                "type": "last_edited_time",
                "last_edited_time": "1986-07-12T04:44:30.133236",
            },
        ),
        (
            RxPropertyValue,
            RxMultiSelectPropertyValue,
            {
                "id": "a6581fa7-ecdc-42ea-8229-457ed251a1c9",
                "type": "multi_select",
                "multi_select": [
                    {
                        "id": "dccf03f8-052d-47de-bc6b-266b772d46cb",
                        "name": "Karen Lucas",
                        "color": "default",
                    },
                    {
                        "id": "4201574a-9b9c-42f0-b67b-69da6968f061",
                        "name": "Anne Harris",
                        "color": "yellow",
                    },
                ],
            },
        ),
        (
            RxPropertyValue,
            RxNumberPropertyValue,
            {"id": "6c63b3f5-4a25-4941-93ca-0a86a50c9813", "type": "number"},
        ),
        (
            RxPropertyValue,
            RxPeoplePropertyValue,
            {
                "id": "f14f876d-9f30-490f-8d88-8914b7a41322",
                "type": "people",
                "people": [
                    {
                        "object": "user",
                        "id": "a65ef94a-5fd0-4c04-8faa-5e73987c1106",
                        "name": "Derek Lawrence",
                        "avatar_url": "https://www.lowe.biz/",
                        "type": "bot",
                        "bot": {
                            "owner": {"type": "workspace", "workspace": True},
                            "workspace_name": "Sample Workspace",
                        },
                    },
                    {
                        "object": "user",
                        "id": "3c52411e-5d83-429b-ad60-c6a191656366",
                        "name": "Ryan Harris",
                        "avatar_url": "https://pollard.info/",
                        "type": "person",
                        "person": {"email": "johnnyallen@example.org"},
                    },
                ],
            },
        ),
        (
            RxPropertyValue,
            RxPhoneNumberPropertyValue,
            {
                "id": "f59c8da9-8318-4ba9-9652-8547c10d0c2b",
                "type": "phone_number",
                "phone_number": "976-237-0376",
            },
        ),
        (
            RxPropertyValue,
            RxRelationPropertyValue,
            {
                "id": "99f582e0-c58c-4296-8c15-0c532669cb09",
                "type": "relation",
                "relation": [
                    {"id": "f72485ad-fb1c-4075-b179-47cb43ae7fce"},
                    {"id": "49a0a5de-90f2-4467-a518-a5197135d55f"},
                ],
                "has_more": True,
            },
        ),
        (
            RxPropertyValue,
            RxRichTextPropertyValue,
            {
                "id": "f271ea5f-052d-4d30-a6c5-49ca217f6a4b",
                "type": "rich_text",
                "rich_text": [
                    {
                        "annotations": {
                            "bold": False,
                            "italic": True,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "orange",
                        },
                        "plain_text": "Reflect wonder member history.",
                        "href": "http://www.gay.com/",
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
                        "annotations": {
                            "bold": False,
                            "italic": True,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "orange",
                        },
                        "plain_text": "Reflect wonder member history.",
                        "href": "http://chapman.org/",
                        "type": "mention",
                        "mention": {
                            "type": "user",
                            "user": {
                                "object": "user",
                                "id": "19452cd3-9b76-4bb0-aa21-27ee93b46310",
                            },
                        },
                    },
                ],
            },
        ),
        (
            RxPropertyValue,
            RollupPropertyValue,
            {
                "id": "cf2014bd-2aab-43d1-8bc2-3188366084a9",
                "type": "rollup",
                "rollup": {"type": "incomplete", "function": "sum"},
            },
        ),
        (
            RxPropertyValue,
            RxSelectPropertyValue,
            {
                "id": "f2d3327c-9a84-41b9-b593-a260b79f1033",
                "type": "select",
                "select": {
                    "id": "4bdd50fb-8a2c-4688-839b-b1a4b93c979b",
                    "name": "Joanna Santana",
                    "color": "gray",
                },
            },
        ),
        (
            RxPropertyValue,
            RxStatusPropertyValue,
            {
                "id": "ca3b2686-dcd0-4a9a-a4e8-428647ff23dd",
                "type": "status",
                "status": {
                    "id": "43d18b57-0f15-4029-b64d-2738b240343f",
                    "name": "Carla Burgess",
                    "color": "purple",
                },
            },
        ),
        (
            RxPropertyValue,
            RxTitlePropertyValue,
            {
                "id": "46a00b6f-0377-4676-bb41-b7042059dace",
                "type": "title",
                "title": [
                    {
                        "annotations": {
                            "bold": False,
                            "italic": True,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "orange",
                        },
                        "plain_text": "Reflect wonder member history.",
                        "href": "https://macias-lewis.org/",
                        "type": "text",
                        "text": {
                            "content": "Reveal common east dream.",
                            "link": {"url": "https://www.garcia.com/"},
                        },
                    },
                    {
                        "annotations": {
                            "bold": False,
                            "italic": True,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "orange",
                        },
                        "plain_text": "Reflect wonder member history.",
                        "href": "http://hill-ochoa.com/",
                        "type": "equation",
                        "equation": {
                            "expression": "Rich since movie feeling may over meeting leg. Town officer woman but a candidate reflect. Whatever phone son. Go board know skill deep rather within activity."
                        },
                    },
                ],
            },
        ),
        (
            RxPropertyValue,
            RxUrlPropertyValue,
            {
                "id": "5ee79b74-3317-4c3d-8a4d-136498a186bb",
                "type": "url",
                "url": "http://www.stewart.com/",
            },
        ),
        (
            RxPropertyValue,
            UniqueIdPropertyValue,
            {
                "id": "ca9fd9ec-d109-491c-b199-dee7462f4b64",
                "type": "unique_id",
                "unique_id": {"number": 8890},
            },
        ),
        (
            RxPropertyValue,
            VerificationPropertyValue,
            {
                "id": "366b81d2-cb4e-4a02-aef1-f84fdd4b914e",
                "type": "verification",
                "verification": {
                    "state": "verified",
                    "verified_by": {
                        "object": "user",
                        "id": "7f50b3fb-e4a0-4df6-84d7-444d9015445f",
                        "name": "Andre Robertson",
                        "avatar_url": "http://www.jones.com/",
                        "type": "bot",
                        "bot": {
                            "owner": {"type": "workspace", "workspace": True},
                            "workspace_name": "Sample Workspace",
                        },
                    },
                    "date": {"start": "2008-12-14T04:12:41.296705"},
                },
            },
        ),
    ],
)
def test_rx_property_value_discriminated_model(
    annotated_clz: type, expected_clz: type, input_data: dict
):
    DiscriminatedModelTester(annotated_clz, expected_clz, **input_data).run_all_tests()


@pytest.mark.parametrize(
    "clz, test_data",
    [
        (
            BooleanFormulaValue,
            (
                {'type': FormulaValueType.BOOLEAN, 'boolean': True},
                {'type': FormulaValueType.BOOLEAN, 'boolean': True},
                {"type": "boolean", "boolean": True},
            ),
        ),
        (
            DateFormulaValue,
            (
                {
                    'type': FormulaValueType.DATE,
                    'date': NotionDate(
                        start=datetime(2010, 8, 15, 22, 43, 49),
                        end=None,
                        time_zone=None,
                    ),
                },
                {
                    'type': FormulaValueType.DATE,
                    'date': {'start': datetime(2010, 8, 15, 22, 43, 49)},
                },
                {"type": "date", "date": {"start": "2010-08-15T22:43:49"}},
            ),
        ),
        (
            NumberFormulaValue,
            (
                {'type': FormulaValueType.NUMBER, 'number': None},
                {'type': FormulaValueType.NUMBER},
                {"type": "number"},
            ),
        ),
        (
            StringFormulaValue,
            (
                {
                    'type': FormulaValueType.STRING,
                    'string': 'Run foreign might late hope top. Too wait most usually True she check. New myself public voice body.',
                },
                {
                    'type': FormulaValueType.STRING,
                    'string': 'Run foreign might late hope top. Too wait most usually True she check. New myself public voice body.',
                },
                {
                    "type": "string",
                    "string": "Run foreign might late hope top. Too wait most usually True she check. New myself public voice body.",
                },
            ),
        ),
    ],
)
def test_formula_models_serialization(
    clz: type[BaseModel], test_data: tuple[dict, dict, dict]
):
    PydanticModelTester(clz, test_data).run_all_tests()


@pytest.mark.parametrize(
    "clz, test_data",
    [
        (
            ArrayRollupValue,
            (
                {
                    'type': RollupValueType.ARRAY,
                    'array': [
                        RxTitlePropertyValue(
                            id='8dd68534-debe-4195-ae5c-5c351e5ffec0',
                            type=PropertyType.TITLE,
                            title=[
                                RxMentionRichText(
                                    annotations=Annotations(
                                        bold=False,
                                        italic=True,
                                        strikethrough=False,
                                        underline=False,
                                        code=True,
                                        color=BackgroundColor.YELLOW_BACKGROUND,
                                    ),
                                    plain_text='Where miss technology hand none hot second.',
                                    href='http://orr.net/',
                                    type=RichTextType.MENTION,
                                    mention=RxUserMention(
                                        type=MentionType.USER,
                                        user=PersonUser(
                                            object=NotionObjectType.USER,
                                            id=UUID(
                                                '75a23975-8797-43c5-80e2-a9febe61b545'
                                            ),
                                            name='Christopher Graham',
                                            avatar_url='http://hogan-smith.com/',
                                            type=UserType.PERSON,
                                            person=Person(
                                                email='andersonstanley@example.com'
                                            ),
                                        ),
                                    ),
                                ),
                                RxEquationRichText(
                                    annotations=Annotations(
                                        bold=True,
                                        italic=True,
                                        strikethrough=True,
                                        underline=False,
                                        code=False,
                                        color=BackgroundColor.YELLOW_BACKGROUND,
                                    ),
                                    plain_text='Perhaps market ask.',
                                    href='http://smith.com/',
                                    type=RichTextType.EQUATION,
                                    equation=Equation(
                                        expression='Pm possible boy fund per base require. Her edge administration particularly cultural tell. Save better tree note best.\nBoy or past one class. Board read human single.'
                                    ),
                                ),
                            ],
                        )
                    ],
                    'function': RollupFunction.UNCHECKED,
                },
                {
                    'type': RollupValueType.ARRAY,
                    'array': [
                        {
                            'id': '8dd68534-debe-4195-ae5c-5c351e5ffec0',
                            'type': PropertyType.TITLE,
                            'title': [
                                {
                                    'annotations': {
                                        'bold': False,
                                        'italic': True,
                                        'strikethrough': False,
                                        'underline': False,
                                        'code': True,
                                        'color': BackgroundColor.YELLOW_BACKGROUND,
                                    },
                                    'plain_text': 'Where miss technology hand none hot second.',
                                    'href': 'http://orr.net/',
                                    'type': RichTextType.MENTION,
                                    'mention': {
                                        'type': MentionType.USER,
                                        'user': {
                                            'object': NotionObjectType.USER,
                                            'id': UUID(
                                                '75a23975-8797-43c5-80e2-a9febe61b545'
                                            ),
                                            'name': 'Christopher Graham',
                                            'avatar_url': 'http://hogan-smith.com/',
                                            'type': UserType.PERSON,
                                            'person': {
                                                'email': 'andersonstanley@example.com'
                                            },
                                        },
                                    },
                                },
                                {
                                    'annotations': {
                                        'bold': True,
                                        'italic': True,
                                        'strikethrough': True,
                                        'underline': False,
                                        'code': False,
                                        'color': BackgroundColor.YELLOW_BACKGROUND,
                                    },
                                    'plain_text': 'Perhaps market ask.',
                                    'href': 'http://smith.com/',
                                    'type': RichTextType.EQUATION,
                                    'equation': {
                                        'expression': 'Pm possible boy fund per base require. Her edge administration particularly cultural tell. Save better tree note best.\nBoy or past one class. Board read human single.'
                                    },
                                },
                            ],
                        }
                    ],
                    'function': RollupFunction.UNCHECKED,
                },
                {
                    "type": "array",
                    "array": [
                        {
                            "id": "8dd68534-debe-4195-ae5c-5c351e5ffec0",
                            "type": "title",
                            "title": [
                                {
                                    "annotations": {
                                        "bold": False,
                                        "italic": True,
                                        "strikethrough": False,
                                        "underline": False,
                                        "code": True,
                                        "color": "yellow_background",
                                    },
                                    "plain_text": "Where miss technology hand none hot second.",
                                    "href": "http://orr.net/",
                                    "type": "mention",
                                    "mention": {
                                        "type": "user",
                                        "user": {
                                            "object": "user",
                                            "id": "75a23975-8797-43c5-80e2-a9febe61b545",
                                            "name": "Christopher Graham",
                                            "avatar_url": "http://hogan-smith.com/",
                                            "type": "person",
                                            "person": {
                                                "email": "andersonstanley@example.com"
                                            },
                                        },
                                    },
                                },
                                {
                                    "annotations": {
                                        "bold": True,
                                        "italic": True,
                                        "strikethrough": True,
                                        "underline": False,
                                        "code": False,
                                        "color": "yellow_background",
                                    },
                                    "plain_text": "Perhaps market ask.",
                                    "href": "http://smith.com/",
                                    "type": "equation",
                                    "equation": {
                                        "expression": "Pm possible boy fund per base require. Her edge administration particularly cultural tell. Save better tree note best.\nBoy or past one class. Board read human single."
                                    },
                                },
                            ],
                        }
                    ],
                    "function": "unchecked",
                },
            ),
        ),
        (
            DateRollupValue,
            (
                {
                    'type': RollupValueType.DATE,
                    'date': None,
                    'function': RollupFunction.AVERAGE,
                },
                {'type': RollupValueType.DATE, 'function': RollupFunction.AVERAGE},
                {"type": "date", "function": "average"},
            ),
        ),
        (
            IncompleteRollupValue,
            (
                {
                    'type': RollupValueType.INCOMPLETE,
                    'incomplete': {},
                    'function': RollupFunction.MAX,
                },
                {
                    'type': RollupValueType.INCOMPLETE,
                    'incomplete': {},
                    'function': RollupFunction.MAX,
                },
                {"type": "incomplete", "incomplete": {}, "function": "max"},
            ),
        ),
        (
            NumberRollupValue,
            (
                {
                    'type': RollupValueType.NUMBER,
                    'number': 73,
                    'function': RollupFunction.PERCENT_CHECKED,
                },
                {
                    'type': RollupValueType.NUMBER,
                    'number': 73,
                    'function': RollupFunction.PERCENT_CHECKED,
                },
                {"type": "number", "number": 73, "function": "percent_checked"},
            ),
        ),
        (
            UnsupportedRollupValue,
            (
                {
                    'type': RollupValueType.UNSUPPORTED,
                    'unsupported': {},
                    'function': RollupFunction.NOT_EMPTY,
                },
                {
                    'type': RollupValueType.UNSUPPORTED,
                    'unsupported': {},
                    'function': RollupFunction.NOT_EMPTY,
                },
                {"type": "unsupported", "unsupported": {}, "function": "not_empty"},
            ),
        ),
    ],
)
def test_rollup_models_serialization(
    clz: type[BaseModel], test_data: tuple[dict, dict, dict]
):
    PydanticModelTester(clz, test_data).run_all_tests()


@pytest.mark.parametrize(
    "clz, test_data",
    [
        (
            RxCheckboxPropertyValue,
            (
                {
                    'id': 'fd014775-27b6-4fa7-96aa-c1a7c188efb2',
                    'type': PropertyType.CHECKBOX,
                    'checkbox': False,
                },
                {
                    'id': 'fd014775-27b6-4fa7-96aa-c1a7c188efb2',
                    'type': PropertyType.CHECKBOX,
                    'checkbox': False,
                },
                {
                    "id": "fd014775-27b6-4fa7-96aa-c1a7c188efb2",
                    "type": "checkbox",
                    "checkbox": False,
                },
            ),
        ),
        (
            CreatedByPropertyValue,
            (
                {
                    'id': 'a565ef74-2814-49ff-9d91-e8825790d5e1',
                    'type': PropertyType.CREATED_BY,
                    'created_by': PersonUser(
                        object=NotionObjectType.USER,
                        id=UUID('e55b15e8-be24-424a-87b9-6c44ece104f0'),
                        name='Devin Morales',
                        avatar_url='http://braun.com/',
                        type=UserType.PERSON,
                        person=Person(email='owilliams@example.org'),
                    ),
                },
                {
                    'id': 'a565ef74-2814-49ff-9d91-e8825790d5e1',
                    'type': PropertyType.CREATED_BY,
                    'created_by': {
                        'object': NotionObjectType.USER,
                        'id': UUID('e55b15e8-be24-424a-87b9-6c44ece104f0'),
                        'name': 'Devin Morales',
                        'avatar_url': 'http://braun.com/',
                        'type': UserType.PERSON,
                        'person': {'email': 'owilliams@example.org'},
                    },
                },
                {
                    "id": "a565ef74-2814-49ff-9d91-e8825790d5e1",
                    "type": "created_by",
                    "created_by": {
                        "object": "user",
                        "id": "e55b15e8-be24-424a-87b9-6c44ece104f0",
                        "name": "Devin Morales",
                        "avatar_url": "http://braun.com/",
                        "type": "person",
                        "person": {"email": "owilliams@example.org"},
                    },
                },
            ),
        ),
        (
            CreatedTimePropertyValue,
            (
                {
                    'id': '285fd678-3347-4df6-99cd-a8fb052b3e97',
                    'type': PropertyType.CREATED_TIME,
                    'created_time': datetime(2002, 3, 19, 15, 44, 49, 790074),
                },
                {
                    'id': '285fd678-3347-4df6-99cd-a8fb052b3e97',
                    'type': PropertyType.CREATED_TIME,
                    'created_time': datetime(2002, 3, 19, 15, 44, 49, 790074),
                },
                {
                    "id": "285fd678-3347-4df6-99cd-a8fb052b3e97",
                    "type": "created_time",
                    "created_time": "2002-03-19T15:44:49.790074",
                },
            ),
        ),
        (
            RxDatePropertyValue,
            (
                {
                    'id': 'ec4b0171-2859-419b-9ebd-ba2407619e0d',
                    'type': PropertyType.DATE,
                    'date': NotionDate(
                        start=datetime(2004, 10, 22, 20, 31, 7),
                        end=None,
                        time_zone=None,
                    ),
                },
                {
                    'id': 'ec4b0171-2859-419b-9ebd-ba2407619e0d',
                    'type': PropertyType.DATE,
                    'date': {'start': datetime(2004, 10, 22, 20, 31, 7)},
                },
                {
                    "id": "ec4b0171-2859-419b-9ebd-ba2407619e0d",
                    "type": "date",
                    "date": {"start": "2004-10-22T20:31:07"},
                },
            ),
        ),
        (
            RxEmailPropertyValue,
            (
                {
                    'id': '2b2f55cc-b2e9-463a-835a-8947dbbcb661',
                    'type': PropertyType.EMAIL,
                    'email': 'tinawilson@example.net',
                },
                {
                    'id': '2b2f55cc-b2e9-463a-835a-8947dbbcb661',
                    'type': PropertyType.EMAIL,
                    'email': 'tinawilson@example.net',
                },
                {
                    "id": "2b2f55cc-b2e9-463a-835a-8947dbbcb661",
                    "type": "email",
                    "email": "tinawilson@example.net",
                },
            ),
        ),
        (
            RxFilesPropertyValue,
            (
                {
                    'id': 'f8d20638-0502-46b8-a204-7d5d4f9457c0',
                    'type': PropertyType.FILES,
                    'files': [
                        ExternalFileWithName(
                            type=FileType.EXTERNAL,
                            external=ExternalFileObject(
                                url='http://butler-ramsey.com/'
                            ),
                            name='Kelly Davis',
                        )
                    ],
                },
                {
                    'id': 'f8d20638-0502-46b8-a204-7d5d4f9457c0',
                    'type': PropertyType.FILES,
                    'files': [
                        {
                            'type': FileType.EXTERNAL,
                            'external': {'url': 'http://butler-ramsey.com/'},
                            'name': 'Kelly Davis',
                        }
                    ],
                },
                {
                    "id": "f8d20638-0502-46b8-a204-7d5d4f9457c0",
                    "type": "files",
                    "files": [
                        {
                            "type": "external",
                            "external": {"url": "http://butler-ramsey.com/"},
                            "name": "Kelly Davis",
                        }
                    ],
                },
            ),
        ),
        (
            FormulaPropertyValue,
            (
                {
                    'id': '1c5c2e92-aa52-4d3f-b3b7-d745dc0d5efd',
                    'type': PropertyType.FORMULA,
                    'formula': NumberFormulaValue(
                        type=FormulaValueType.NUMBER, number=None
                    ),
                },
                {
                    'id': '1c5c2e92-aa52-4d3f-b3b7-d745dc0d5efd',
                    'type': PropertyType.FORMULA,
                    'formula': {'type': FormulaValueType.NUMBER},
                },
                {
                    "id": "1c5c2e92-aa52-4d3f-b3b7-d745dc0d5efd",
                    "type": "formula",
                    "formula": {"type": "number"},
                },
            ),
        ),
        (
            LastEditedByPropertyValue,
            (
                {
                    'id': '0cf04e3e-4b1a-4ae0-bada-3b4d42b2a234',
                    'type': PropertyType.LAST_EDITED_BY,
                    'last_edited_by': UserRef(
                        object=NotionObjectType.USER,
                        id=UUID('695fa60c-f8d9-401c-aa98-627c7bd2e632'),
                    ),
                },
                {
                    'id': '0cf04e3e-4b1a-4ae0-bada-3b4d42b2a234',
                    'type': PropertyType.LAST_EDITED_BY,
                    'last_edited_by': {
                        'object': NotionObjectType.USER,
                        'id': UUID('695fa60c-f8d9-401c-aa98-627c7bd2e632'),
                    },
                },
                {
                    "id": "0cf04e3e-4b1a-4ae0-bada-3b4d42b2a234",
                    "type": "last_edited_by",
                    "last_edited_by": {
                        "object": "user",
                        "id": "695fa60c-f8d9-401c-aa98-627c7bd2e632",
                    },
                },
            ),
        ),
        (
            LastEditedTimePropertyValue,
            (
                {
                    'id': 'a26d9bdf-f827-4eeb-9f16-62c8bcb77cb2',
                    'type': PropertyType.LAST_EDITED_TIME,
                    'last_edited_time': datetime(2024, 8, 29, 12, 23, 37, 917929),
                },
                {
                    'id': 'a26d9bdf-f827-4eeb-9f16-62c8bcb77cb2',
                    'type': PropertyType.LAST_EDITED_TIME,
                    'last_edited_time': datetime(2024, 8, 29, 12, 23, 37, 917929),
                },
                {
                    "id": "a26d9bdf-f827-4eeb-9f16-62c8bcb77cb2",
                    "type": "last_edited_time",
                    "last_edited_time": "2024-08-29T12:23:37.917929",
                },
            ),
        ),
        (
            RxMultiSelectPropertyValue,
            (
                {
                    'id': '01a11a5a-7441-4652-9003-a61039fa6787',
                    'type': PropertyType.MULTI_SELECT,
                    'multi_select': [
                        RxOptionValue(
                            id='13988fbf-e372-48e7-b466-a378df8050cb',
                            name='Joshua Rodriguez',
                            color=Color.PINK,
                        ),
                        RxOptionValue(
                            id='8e1a0382-2501-42d4-80ca-fbb85f1f03b0',
                            name='Latoya Gilbert',
                            color=Color.PURPLE,
                        ),
                    ],
                },
                {
                    'id': '01a11a5a-7441-4652-9003-a61039fa6787',
                    'type': PropertyType.MULTI_SELECT,
                    'multi_select': [
                        {
                            'id': '13988fbf-e372-48e7-b466-a378df8050cb',
                            'name': 'Joshua Rodriguez',
                            'color': Color.PINK,
                        },
                        {
                            'id': '8e1a0382-2501-42d4-80ca-fbb85f1f03b0',
                            'name': 'Latoya Gilbert',
                            'color': Color.PURPLE,
                        },
                    ],
                },
                {
                    "id": "01a11a5a-7441-4652-9003-a61039fa6787",
                    "type": "multi_select",
                    "multi_select": [
                        {
                            "id": "13988fbf-e372-48e7-b466-a378df8050cb",
                            "name": "Joshua Rodriguez",
                            "color": "pink",
                        },
                        {
                            "id": "8e1a0382-2501-42d4-80ca-fbb85f1f03b0",
                            "name": "Latoya Gilbert",
                            "color": "purple",
                        },
                    ],
                },
            ),
        ),
        (
            RxNumberPropertyValue,
            (
                {
                    'id': '0fca8718-01be-4ff9-9299-d52947ea98dd',
                    'type': PropertyType.NUMBER,
                    'number': None,
                },
                {
                    'id': '0fca8718-01be-4ff9-9299-d52947ea98dd',
                    'type': PropertyType.NUMBER,
                },
                {"id": "0fca8718-01be-4ff9-9299-d52947ea98dd", "type": "number"},
            ),
        ),
        (
            RxPeoplePropertyValue,
            (
                {
                    'id': 'c23918f7-dfaf-4ff3-8440-41f89b5e4d97',
                    'type': PropertyType.PEOPLE,
                    'people': [
                        PersonUser(
                            object=NotionObjectType.USER,
                            id=UUID('c3e8be58-69f6-4937-946c-2a0e1e321dc1'),
                            name='James Craig',
                            avatar_url='http://romero.com/',
                            type=UserType.PERSON,
                            person=Person(email='owilliams@example.org'),
                        )
                    ],
                },
                {
                    'id': 'c23918f7-dfaf-4ff3-8440-41f89b5e4d97',
                    'type': PropertyType.PEOPLE,
                    'people': [
                        {
                            'object': NotionObjectType.USER,
                            'id': UUID('c3e8be58-69f6-4937-946c-2a0e1e321dc1'),
                            'name': 'James Craig',
                            'avatar_url': 'http://romero.com/',
                            'type': UserType.PERSON,
                            'person': {'email': 'owilliams@example.org'},
                        }
                    ],
                },
                {
                    "id": "c23918f7-dfaf-4ff3-8440-41f89b5e4d97",
                    "type": "people",
                    "people": [
                        {
                            "object": "user",
                            "id": "c3e8be58-69f6-4937-946c-2a0e1e321dc1",
                            "name": "James Craig",
                            "avatar_url": "http://romero.com/",
                            "type": "person",
                            "person": {"email": "owilliams@example.org"},
                        }
                    ],
                },
            ),
        ),
        (
            RxPhoneNumberPropertyValue,
            (
                {
                    'id': '00b90016-0456-4c1d-9cf8-f286ec890803',
                    'type': PropertyType.PHONE_NUMBER,
                    'phone_number': '300-264-8153',
                },
                {
                    'id': '00b90016-0456-4c1d-9cf8-f286ec890803',
                    'type': PropertyType.PHONE_NUMBER,
                    'phone_number': '300-264-8153',
                },
                {
                    "id": "00b90016-0456-4c1d-9cf8-f286ec890803",
                    "type": "phone_number",
                    "phone_number": "300-264-8153",
                },
            ),
        ),
        (
            RxRelationPropertyValue,
            (
                {
                    'id': '36c1b911-0bb0-4e65-86f3-687c47aab2b3',
                    'type': PropertyType.RELATION,
                    'relation': [
                        NotionObjectIdWrapper(
                            id=UUID('d0f23faa-35c8-41dc-985b-55091f14c36d')
                        )
                    ],
                    'has_more': True,
                },
                {
                    'id': '36c1b911-0bb0-4e65-86f3-687c47aab2b3',
                    'type': PropertyType.RELATION,
                    'relation': [{'id': UUID('d0f23faa-35c8-41dc-985b-55091f14c36d')}],
                    'has_more': True,
                },
                {
                    "id": "36c1b911-0bb0-4e65-86f3-687c47aab2b3",
                    "type": "relation",
                    "relation": [{"id": "d0f23faa-35c8-41dc-985b-55091f14c36d"}],
                    "has_more": True,
                },
            ),
        ),
        (
            RxRichTextPropertyValue,
            (
                {
                    'id': '497e2067-4eb2-4409-a673-223d210ced67',
                    'type': PropertyType.RICH_TEXT,
                    'rich_text': [
                        RxTextRichText(
                            annotations=Annotations(
                                bold=True,
                                italic=True,
                                strikethrough=True,
                                underline=True,
                                code=False,
                                color=Color.YELLOW,
                            ),
                            plain_text='Dog his environment market property.',
                            href='http://patterson.com/',
                            type=RichTextType.TEXT,
                            text=Text(
                                content='Structure dinner data notice cover.',
                                link=NotionUrlWrapper(url='http://www.pratt.com/'),
                            ),
                        )
                    ],
                },
                {
                    'id': '497e2067-4eb2-4409-a673-223d210ced67',
                    'type': PropertyType.RICH_TEXT,
                    'rich_text': [
                        {
                            'annotations': {
                                'bold': True,
                                'italic': True,
                                'strikethrough': True,
                                'underline': True,
                                'code': False,
                                'color': Color.YELLOW,
                            },
                            'plain_text': 'Dog his environment market property.',
                            'href': 'http://patterson.com/',
                            'type': RichTextType.TEXT,
                            'text': {
                                'content': 'Structure dinner data notice cover.',
                                'link': {'url': 'http://www.pratt.com/'},
                            },
                        }
                    ],
                },
                {
                    "id": "497e2067-4eb2-4409-a673-223d210ced67",
                    "type": "rich_text",
                    "rich_text": [
                        {
                            "annotations": {
                                "bold": True,
                                "italic": True,
                                "strikethrough": True,
                                "underline": True,
                                "code": False,
                                "color": "yellow",
                            },
                            "plain_text": "Dog his environment market property.",
                            "href": "http://patterson.com/",
                            "type": "text",
                            "text": {
                                "content": "Structure dinner data notice cover.",
                                "link": {"url": "http://www.pratt.com/"},
                            },
                        }
                    ],
                },
            ),
        ),
        (
            RollupPropertyValue,
            (
                {
                    'id': '5f2eb176-b7cd-4be7-ac89-65aab0941490',
                    'type': PropertyType.ROLLUP,
                    'rollup': DateRollupValue(
                        type=RollupValueType.DATE,
                        date=None,
                        function=RollupFunction.SUM,
                    ),
                },
                {
                    'id': '5f2eb176-b7cd-4be7-ac89-65aab0941490',
                    'type': PropertyType.ROLLUP,
                    'rollup': {
                        'type': RollupValueType.DATE,
                        'function': RollupFunction.SUM,
                    },
                },
                {
                    "id": "5f2eb176-b7cd-4be7-ac89-65aab0941490",
                    "type": "rollup",
                    "rollup": {"type": "date", "function": "sum"},
                },
            ),
        ),
        (
            RxSelectPropertyValue,
            (
                {
                    'id': '6048abc2-eaa4-419a-86fc-6c8e7cd8aac3',
                    'type': PropertyType.SELECT,
                    'select': RxOptionValue(
                        id='e2076828-1e57-41e1-8cf7-1dbe7295b4e1',
                        name='Marc Miller',
                        color=Color.ORANGE,
                    ),
                },
                {
                    'id': '6048abc2-eaa4-419a-86fc-6c8e7cd8aac3',
                    'type': PropertyType.SELECT,
                    'select': {
                        'id': 'e2076828-1e57-41e1-8cf7-1dbe7295b4e1',
                        'name': 'Marc Miller',
                        'color': Color.ORANGE,
                    },
                },
                {
                    "id": "6048abc2-eaa4-419a-86fc-6c8e7cd8aac3",
                    "type": "select",
                    "select": {
                        "id": "e2076828-1e57-41e1-8cf7-1dbe7295b4e1",
                        "name": "Marc Miller",
                        "color": "orange",
                    },
                },
            ),
        ),
        (
            RxStatusPropertyValue,
            (
                {
                    'id': 'af0a7854-3ca9-4809-bcda-e8d42e80e092',
                    'type': PropertyType.STATUS,
                    'status': RxOptionValue(
                        id='c98fc96e-697c-4d90-b95b-437a358d0e89',
                        name='Dr. Shannon Costa',
                        color=Color.GRAY,
                    ),
                },
                {
                    'id': 'af0a7854-3ca9-4809-bcda-e8d42e80e092',
                    'type': PropertyType.STATUS,
                    'status': {
                        'id': 'c98fc96e-697c-4d90-b95b-437a358d0e89',
                        'name': 'Dr. Shannon Costa',
                        'color': Color.GRAY,
                    },
                },
                {
                    "id": "af0a7854-3ca9-4809-bcda-e8d42e80e092",
                    "type": "status",
                    "status": {
                        "id": "c98fc96e-697c-4d90-b95b-437a358d0e89",
                        "name": "Dr. Shannon Costa",
                        "color": "gray",
                    },
                },
            ),
        ),
        (
            RxTitlePropertyValue,
            (
                {
                    'id': 'c90db3c1-812e-40a0-817a-d551bc1bf1a3',
                    'type': PropertyType.TITLE,
                    'title': [
                        RxEquationRichText(
                            annotations=Annotations(
                                bold=True,
                                italic=True,
                                strikethrough=True,
                                underline=True,
                                code=False,
                                color=Color.YELLOW,
                            ),
                            plain_text='Dog his environment market property.',
                            href='https://barber.com/',
                            type=RichTextType.EQUATION,
                            equation=Equation(
                                expression='Whom let plant green line chance board catch. Month discover state check science full. Her movie fall.\nMaybe per know soon value. Recently front ago.'
                            ),
                        )
                    ],
                },
                {
                    'id': 'c90db3c1-812e-40a0-817a-d551bc1bf1a3',
                    'type': PropertyType.TITLE,
                    'title': [
                        {
                            'annotations': {
                                'bold': True,
                                'italic': True,
                                'strikethrough': True,
                                'underline': True,
                                'code': False,
                                'color': Color.YELLOW,
                            },
                            'plain_text': 'Dog his environment market property.',
                            'href': 'https://barber.com/',
                            'type': RichTextType.EQUATION,
                            'equation': {
                                'expression': 'Whom let plant green line chance board catch. Month discover state check science full. Her movie fall.\nMaybe per know soon value. Recently front ago.'
                            },
                        }
                    ],
                },
                {
                    "id": "c90db3c1-812e-40a0-817a-d551bc1bf1a3",
                    "type": "title",
                    "title": [
                        {
                            "annotations": {
                                "bold": True,
                                "italic": True,
                                "strikethrough": True,
                                "underline": True,
                                "code": False,
                                "color": "yellow",
                            },
                            "plain_text": "Dog his environment market property.",
                            "href": "https://barber.com/",
                            "type": "equation",
                            "equation": {
                                "expression": "Whom let plant green line chance board catch. Month discover state check science full. Her movie fall.\nMaybe per know soon value. Recently front ago."
                            },
                        }
                    ],
                },
            ),
        ),
        (
            RxUrlPropertyValue,
            (
                {
                    'id': '94bc8573-2ac8-4b6e-bda0-784cd36a397d',
                    'type': PropertyType.URL,
                    'url': 'https://www.levy.com/',
                },
                {
                    'id': '94bc8573-2ac8-4b6e-bda0-784cd36a397d',
                    'type': PropertyType.URL,
                    'url': 'https://www.levy.com/',
                },
                {
                    "id": "94bc8573-2ac8-4b6e-bda0-784cd36a397d",
                    "type": "url",
                    "url": "https://www.levy.com/",
                },
            ),
        ),
        (
            UniqueIdPropertyValue,
            (
                {
                    'id': '7b0aa4a8-cb1b-437f-acf7-c109f5ee39d5',
                    'type': PropertyType.UNIQUE_ID,
                    'unique_id': UniqueIdValue(
                        number=6516, prefix='kpPUokMhOvcGfPuoibDh'
                    ),
                },
                {
                    'id': '7b0aa4a8-cb1b-437f-acf7-c109f5ee39d5',
                    'type': PropertyType.UNIQUE_ID,
                    'unique_id': {'number': 6516, 'prefix': 'kpPUokMhOvcGfPuoibDh'},
                },
                {
                    "id": "7b0aa4a8-cb1b-437f-acf7-c109f5ee39d5",
                    "type": "unique_id",
                    "unique_id": {"number": 6516, "prefix": "kpPUokMhOvcGfPuoibDh"},
                },
            ),
        ),
        (
            VerificationPropertyValue,
            (
                {
                    'id': '78754b7a-ead7-4aaa-bfc7-f329f5e9cd29',
                    'type': PropertyType.VERIFICATION,
                    'verification': UnverifiedValue(
                        state='unverified', verified_by=None, date=None
                    ),
                },
                {
                    'id': '78754b7a-ead7-4aaa-bfc7-f329f5e9cd29',
                    'type': PropertyType.VERIFICATION,
                    'verification': {'state': 'unverified'},
                },
                {
                    "id": "78754b7a-ead7-4aaa-bfc7-f329f5e9cd29",
                    "type": "verification",
                    "verification": {"state": "unverified"},
                },
            ),
        ),
    ],
)
def test_rx_property_value_models_serialization(
    clz: type[BaseModel], test_data: tuple[dict, dict, dict]
):
    PydanticModelTester(clz, test_data).run_all_tests()


@pytest.mark.parametrize(
    "clz, test_data",
    [
        (
            TxCheckboxPropertyValue,
            ({'checkbox': False}, {'checkbox': False}, {"checkbox": False}),
        ),
        (
            TxDatePropertyValue,
            (
                {
                    'date': NotionDate(
                        start=datetime(1982, 9, 21, 14, 9, 43), end=None, time_zone=None
                    )
                },
                {'date': {'start': datetime(1982, 9, 21, 14, 9, 43)}},
                {"date": {"start": "1982-09-21T14:09:43"}},
            ),
        ),
        (
            TxEmailPropertyValue,
            (
                {'email': 'abbottbrian@example.net'},
                {'email': 'abbottbrian@example.net'},
                {"email": "abbottbrian@example.net"},
            ),
        ),
        (
            TxFilesPropertyValue,
            (
                {
                    'files': [
                        ExternalFileWithName(
                            type=FileType.EXTERNAL,
                            external=ExternalFileObject(url='http://frederick.com/'),
                            name='Lauren Young',
                        ),
                        HostedFileWithName(
                            type=FileType.FILE,
                            file=HostedFileObject(
                                url='http://silva.info/',
                                expiry_time=datetime(1994, 10, 21, 2, 11, 53, 777070),
                            ),
                            name='Thomas Holmes',
                        ),
                    ]
                },
                {
                    'files': [
                        {
                            'type': FileType.EXTERNAL,
                            'external': {'url': 'http://frederick.com/'},
                            'name': 'Lauren Young',
                        },
                        {
                            'type': FileType.FILE,
                            'file': {
                                'url': 'http://silva.info/',
                                'expiry_time': datetime(
                                    1994, 10, 21, 2, 11, 53, 777070
                                ),
                            },
                            'name': 'Thomas Holmes',
                        },
                    ]
                },
                {
                    "files": [
                        {
                            "type": "external",
                            "external": {"url": "http://frederick.com/"},
                            "name": "Lauren Young",
                        },
                        {
                            "type": "file",
                            "file": {
                                "url": "http://silva.info/",
                                "expiry_time": "1994-10-21T02:11:53.777070",
                            },
                            "name": "Thomas Holmes",
                        },
                    ]
                },
            ),
        ),
        (
            TxMultiSelectPropertyValue,
            (
                {
                    'multi_select': [
                        TxOptionValue(name='Joshua Obrien'),
                        TxOptionValue(name='Allison Robertson'),
                    ]
                },
                {
                    'multi_select': [
                        {'name': 'Joshua Obrien'},
                        {'name': 'Allison Robertson'},
                    ]
                },
                {
                    "multi_select": [
                        {"name": "Joshua Obrien"},
                        {"name": "Allison Robertson"},
                    ]
                },
            ),
        ),
        (
            TxNumberPropertyValue,
            ({'number': None}, {}, {}),
        ),
        (
            TxPeoplePropertyValue,
            (
                {
                    'people': [
                        UserRef(
                            object=NotionObjectType.USER,
                            id=UUID('25216906-8a9e-48ab-a63d-92f48e1e1cfa'),
                        ),
                        BotUser(
                            object=NotionObjectType.USER,
                            id=UUID('a1625f93-3c3b-4450-9508-108b5ea00080'),
                            name='Keith Schaefer',
                            avatar_url='https://www.hernandez.com/',
                            type=UserType.BOT,
                            bot=Bot(
                                owner=WorkspaceBotOwner(
                                    type=BotOwnerType.WORKSPACE, workspace=True
                                ),
                                workspace_name='Sample Workspace',
                            ),
                        ),
                    ]
                },
                {
                    'people': [
                        {
                            'object': NotionObjectType.USER,
                            'id': UUID('25216906-8a9e-48ab-a63d-92f48e1e1cfa'),
                        },
                        {
                            'object': NotionObjectType.USER,
                            'id': UUID('a1625f93-3c3b-4450-9508-108b5ea00080'),
                        },
                    ]
                },
                {
                    "people": [
                        {
                            "object": "user",
                            "id": "25216906-8a9e-48ab-a63d-92f48e1e1cfa",
                        },
                        {
                            "object": "user",
                            "id": "a1625f93-3c3b-4450-9508-108b5ea00080",
                        },
                    ]
                },
            ),
        ),
        (
            TxPhoneNumberPropertyValue,
            (
                {'phone_number': '951-754-5310'},
                {'phone_number': '951-754-5310'},
                {"phone_number": "951-754-5310"},
            ),
        ),
        (
            TxRelationPropertyValue,
            (
                {
                    'relation': [
                        NotionObjectIdWrapper(
                            id=UUID('67237716-e823-4918-84bc-1572142296b6')
                        )
                    ]
                },
                {'relation': [{'id': UUID('67237716-e823-4918-84bc-1572142296b6')}]},
                {"relation": [{"id": "67237716-e823-4918-84bc-1572142296b6"}]},
            ),
        ),
        (
            TxRichTextPropertyValue,
            (
                {
                    'rich_text': [
                        TxMentionRichText(
                            annotations=Annotations(
                                bold=False,
                                italic=True,
                                strikethrough=True,
                                underline=True,
                                code=True,
                                color=Color.DEFAULT,
                            ),
                            type=RichTextType.MENTION,
                            mention=TemplateMention(
                                type=MentionType.TEMPLATE_MENTION,
                                template_mention=TemplateMentionDate(
                                    type=TemplateMentionType.TEMPLATE_MENTION_DATE,
                                    template_mention_date='now',
                                ),
                            ),
                        ),
                        TxMentionRichText(
                            annotations=Annotations(
                                bold=True,
                                italic=False,
                                strikethrough=False,
                                underline=True,
                                code=False,
                                color=Color.DEFAULT,
                            ),
                            type=RichTextType.MENTION,
                            mention=TxUserMention(
                                type=MentionType.USER,
                                user=UserRef(
                                    object=NotionObjectType.USER,
                                    id=UUID('a709328c-61f1-481e-8353-ed4690b084e4'),
                                ),
                            ),
                        ),
                    ]
                },
                {
                    'rich_text': [
                        {
                            'annotations': {
                                'bold': False,
                                'italic': True,
                                'strikethrough': True,
                                'underline': True,
                                'code': True,
                                'color': Color.DEFAULT,
                            },
                            'mention': {
                                'type': MentionType.TEMPLATE_MENTION,
                                'template_mention': {
                                    'type': TemplateMentionType.TEMPLATE_MENTION_DATE,
                                    'template_mention_date': 'now',
                                },
                            },
                        },
                        {
                            'annotations': {
                                'bold': True,
                                'italic': False,
                                'strikethrough': False,
                                'underline': True,
                                'code': False,
                                'color': Color.DEFAULT,
                            },
                            'mention': {
                                'type': MentionType.USER,
                                'user': {
                                    'object': NotionObjectType.USER,
                                    'id': UUID('a709328c-61f1-481e-8353-ed4690b084e4'),
                                },
                            },
                        },
                    ]
                },
                {
                    "rich_text": [
                        {
                            "annotations": {
                                "bold": False,
                                "italic": True,
                                "strikethrough": True,
                                "underline": True,
                                "code": True,
                                "color": "default",
                            },
                            "mention": {
                                "type": "template_mention",
                                "template_mention": {
                                    "type": "template_mention_date",
                                    "template_mention_date": "now",
                                },
                            },
                        },
                        {
                            "annotations": {
                                "bold": True,
                                "italic": False,
                                "strikethrough": False,
                                "underline": True,
                                "code": False,
                                "color": "default",
                            },
                            "mention": {
                                "type": "user",
                                "user": {
                                    "object": "user",
                                    "id": "a709328c-61f1-481e-8353-ed4690b084e4",
                                },
                            },
                        },
                    ]
                },
            ),
        ),
        (
            TxSelectPropertyValue,
            (
                {'select': TxOptionValue(name='David Gonzales')},
                {'select': {'name': 'David Gonzales'}},
                {"select": {"name": "David Gonzales"}},
            ),
        ),
        (
            TxStatusPropertyValue,
            (
                {'status': TxOptionValue(name='Christopher Schmidt')},
                {'status': {'name': 'Christopher Schmidt'}},
                {"status": {"name": "Christopher Schmidt"}},
            ),
        ),
        (
            TxTitlePropertyValue,
            (
                {
                    'title': [
                        TxMentionRichText(
                            annotations=Annotations(
                                bold=False,
                                italic=True,
                                strikethrough=True,
                                underline=False,
                                code=False,
                                color=Color.DEFAULT,
                            ),
                            type=RichTextType.MENTION,
                            mention=TemplateMention(
                                type=MentionType.TEMPLATE_MENTION,
                                template_mention=TemplateMentionDate(
                                    type=TemplateMentionType.TEMPLATE_MENTION_DATE,
                                    template_mention_date='now',
                                ),
                            ),
                        ),
                        TxTextRichText(
                            annotations=Annotations(
                                bold=True,
                                italic=False,
                                strikethrough=True,
                                underline=True,
                                code=False,
                                color=Color.DEFAULT,
                            ),
                            type=RichTextType.TEXT,
                            text=Text(
                                content='Sing street possible.',
                                link=NotionUrlWrapper(
                                    url='https://www.good-flynn.com/'
                                ),
                            ),
                        ),
                    ]
                },
                {
                    'title': [
                        {
                            'annotations': {
                                'bold': False,
                                'italic': True,
                                'strikethrough': True,
                                'underline': False,
                                'code': False,
                                'color': Color.DEFAULT,
                            },
                            'mention': {
                                'type': MentionType.TEMPLATE_MENTION,
                                'template_mention': {
                                    'type': TemplateMentionType.TEMPLATE_MENTION_DATE,
                                    'template_mention_date': 'now',
                                },
                            },
                        },
                        {
                            'annotations': {
                                'bold': True,
                                'italic': False,
                                'strikethrough': True,
                                'underline': True,
                                'code': False,
                                'color': Color.DEFAULT,
                            },
                            'text': {
                                'content': 'Sing street possible.',
                                'link': {'url': 'https://www.good-flynn.com/'},
                            },
                        },
                    ]
                },
                {
                    "title": [
                        {
                            "annotations": {
                                "bold": False,
                                "italic": True,
                                "strikethrough": True,
                                "underline": False,
                                "code": False,
                                "color": "default",
                            },
                            "mention": {
                                "type": "template_mention",
                                "template_mention": {
                                    "type": "template_mention_date",
                                    "template_mention_date": "now",
                                },
                            },
                        },
                        {
                            "annotations": {
                                "bold": True,
                                "italic": False,
                                "strikethrough": True,
                                "underline": True,
                                "code": False,
                                "color": "default",
                            },
                            "text": {
                                "content": "Sing street possible.",
                                "link": {"url": "https://www.good-flynn.com/"},
                            },
                        },
                    ]
                },
            ),
        ),
        (
            TxUrlPropertyValue,
            (
                {'url': 'https://www.alexander.biz/'},
                {'url': 'https://www.alexander.biz/'},
                {"url": "https://www.alexander.biz/"},
            ),
        ),
    ],
)
def test_tx_property_value_models_serialization(
    clz: type[BaseModel], test_data: tuple[dict, dict, dict]
):
    PydanticModelTester(clz, test_data).run_all_tests()
