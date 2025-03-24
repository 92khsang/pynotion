from datetime import datetime
from uuid import UUID

import pytest
from pydantic import BaseModel

from pynotion.models.file import (
    ExternalFileWithName,
    FileType,
    ExternalFileObject,
    HostedFileWithName,
    HostedFileObject,
)
from pynotion.models.object import NotionObjectType
from pynotion.models.properties.property_value import *
from pynotion.models.rich_text import *
from pynotion.models.user import (
    BotUser,
    UserType,
    Bot,
    WorkspaceBotOwner,
    BotOwnerType,
    PersonUser,
    Person,
)
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
            },
        ),
        (
            RollupValue,
            DateRollupValue,
            {"type": "date"},
        ),
        (
            RollupValue,
            IncompleteRollupValue,
            {"type": "incomplete", "incomplete": {}},
        ),
        (
            RollupValue,
            NumberRollupValue,
            {"type": "number", "number": 901578739},
        ),
        (
            RollupValue,
            UnsupportedRollupValue,
            {"type": "unsupported", "unsupported": {}},
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
                "id": "ef160da7-abc9-4b3a-89b8-db95365dadb6",
                "type": "relation",
                "relation": ["cfddaddc-5848-4974-a5f6-78d68ed32b78"],
                "has_more": False,
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
                "rollup": {"type": "incomplete"},
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
    "annotated_clz, expected_clz, input_data",
    [
        (
            TxPropertyValue,
            TxCheckboxPropertyValue,
            {"checkbox": False},
        ),
        (
            TxPropertyValue,
            TxDatePropertyValue,
            {"date": {"start": "1975-10-03T22:40:52"}},
        ),
        (
            TxPropertyValue,
            TxEmailPropertyValue,
            {"email": "alexgriffith@example.com"},
        ),
        (
            TxPropertyValue,
            TxFilesPropertyValue,
            {
                "files": [
                    {
                        "type": "file",
                        "file": {
                            "url": "http://murphy.com/",
                            "expiry_time": "1981-01-21T13:19:06.159888",
                        },
                        "name": "Dana Parker",
                    }
                ]
            },
        ),
        (
            TxPropertyValue,
            TxMultiSelectPropertyValue,
            {"multi_select": [{"name": "Melissa Allen"}]},
        ),
        (
            TxPropertyValue,
            TxNumberPropertyValue,
            {"number": 44336787},
        ),
        (
            TxPropertyValue,
            TxPeoplePropertyValue,
            {
                "people": [
                    {"object": "user", "id": "6c2dbd5b-ae3f-4351-bbac-ff4b4d07a7d7"}
                ]
            },
        ),
        (
            TxPropertyValue,
            TxPhoneNumberPropertyValue,
            {"phone_number": "(997)545-1663"},
        ),
        (
            TxPropertyValue,
            TxRelationPropertyValue,
            {
                "relation": [
                    "6288cb51-cd17-4499-9f78-062b49fcb11f",
                    "08a7f08f-0940-4ead-ae34-ba7d290a39f0",
                ]
            },
        ),
        (
            TxPropertyValue,
            TxSelectPropertyValue,
            {"select": {"name": "Kelly Palmer"}},
        ),
        (
            TxPropertyValue,
            TxStatusPropertyValue,
            {"status": {"name": "Brenda Smith"}},
        ),
        (
            TxPropertyValue,
            TxUrlPropertyValue,
            {"url": "https://www.holder-thomas.com/"},
        ),
    ],
)
def test_tx_property_value_discriminated_model(
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
                        RxPeoplePropertyValue(
                            id='a9974da7-7a88-49d5-a368-9a3737c2dfce',
                            type=PropertyType.PEOPLE,
                            people=[
                                BotUser(
                                    object=NotionObjectType.USER,
                                    id=UUID('1cf52fc2-9bfe-4628-91e1-6aea031c46dc'),
                                    name='Kevin Wagner',
                                    avatar_url='https://oconnor.net/',
                                    type=UserType.BOT,
                                    bot=Bot(
                                        owner=WorkspaceBotOwner(
                                            type=BotOwnerType.WORKSPACE, workspace=True
                                        ),
                                        workspace_name='Sample Workspace',
                                    ),
                                ),
                                BotUser(
                                    object=NotionObjectType.USER,
                                    id=UUID('f224fb5a-5b55-496a-84e0-fe4b34c00c4e'),
                                    name='Steven Mckee',
                                    avatar_url='http://montgomery.com/',
                                    type=UserType.BOT,
                                    bot=Bot(
                                        owner=WorkspaceBotOwner(
                                            type=BotOwnerType.WORKSPACE, workspace=True
                                        ),
                                        workspace_name='Sample Workspace',
                                    ),
                                ),
                            ],
                        )
                    ],
                },
                {
                    'type': RollupValueType.ARRAY,
                    'array': [
                        {
                            'id': 'a9974da7-7a88-49d5-a368-9a3737c2dfce',
                            'type': PropertyType.PEOPLE,
                            'people': [
                                {
                                    'object': NotionObjectType.USER,
                                    'id': UUID('1cf52fc2-9bfe-4628-91e1-6aea031c46dc'),
                                    'name': 'Kevin Wagner',
                                    'avatar_url': 'https://oconnor.net/',
                                    'type': UserType.BOT,
                                    'bot': {
                                        'owner': {
                                            'type': BotOwnerType.WORKSPACE,
                                            'workspace': True,
                                        },
                                        'workspace_name': 'Sample Workspace',
                                    },
                                },
                                {
                                    'object': NotionObjectType.USER,
                                    'id': UUID('f224fb5a-5b55-496a-84e0-fe4b34c00c4e'),
                                    'name': 'Steven Mckee',
                                    'avatar_url': 'http://montgomery.com/',
                                    'type': UserType.BOT,
                                    'bot': {
                                        'owner': {
                                            'type': BotOwnerType.WORKSPACE,
                                            'workspace': True,
                                        },
                                        'workspace_name': 'Sample Workspace',
                                    },
                                },
                            ],
                        }
                    ],
                },
                {
                    "type": "array",
                    "array": [
                        {
                            "id": "a9974da7-7a88-49d5-a368-9a3737c2dfce",
                            "type": "people",
                            "people": [
                                {
                                    "object": "user",
                                    "id": "1cf52fc2-9bfe-4628-91e1-6aea031c46dc",
                                    "name": "Kevin Wagner",
                                    "avatar_url": "https://oconnor.net/",
                                    "type": "bot",
                                    "bot": {
                                        "owner": {
                                            "type": "workspace",
                                            "workspace": True,
                                        },
                                        "workspace_name": "Sample Workspace",
                                    },
                                },
                                {
                                    "object": "user",
                                    "id": "f224fb5a-5b55-496a-84e0-fe4b34c00c4e",
                                    "name": "Steven Mckee",
                                    "avatar_url": "http://montgomery.com/",
                                    "type": "bot",
                                    "bot": {
                                        "owner": {
                                            "type": "workspace",
                                            "workspace": True,
                                        },
                                        "workspace_name": "Sample Workspace",
                                    },
                                },
                            ],
                        }
                    ],
                },
            ),
        ),
        (
            DateRollupValue,
            (
                {'type': RollupValueType.DATE, 'date': None},
                {'type': RollupValueType.DATE},
                {"type": "date"},
            ),
        ),
        (
            IncompleteRollupValue,
            (
                {'type': RollupValueType.INCOMPLETE, 'incomplete': {}},
                {'type': RollupValueType.INCOMPLETE, 'incomplete': {}},
                {"type": "incomplete", "incomplete": {}},
            ),
        ),
        (
            NumberRollupValue,
            (
                {'type': RollupValueType.NUMBER, 'number': 73591},
                {'type': RollupValueType.NUMBER, 'number': 73591},
                {"type": "number", "number": 73591},
            ),
        ),
        (
            UnsupportedRollupValue,
            (
                {'type': RollupValueType.UNSUPPORTED, 'unsupported': {}},
                {'type': RollupValueType.UNSUPPORTED, 'unsupported': {}},
                {"type": "unsupported", "unsupported": {}},
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
                    'relation': [UUID('d0f23faa-35c8-41dc-985b-55091f14c36d')],
                    'has_more': True,
                },
                {
                    'id': '36c1b911-0bb0-4e65-86f3-687c47aab2b3',
                    'type': PropertyType.RELATION,
                    'relation': [UUID('d0f23faa-35c8-41dc-985b-55091f14c36d')],
                    'has_more': True,
                },
                {
                    "id": "36c1b911-0bb0-4e65-86f3-687c47aab2b3",
                    "type": "relation",
                    "relation": ["d0f23faa-35c8-41dc-985b-55091f14c36d"],
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
                                link=NotionUrlObject(url='http://www.pratt.com/'),
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
                    'rollup': DateRollupValue(type=RollupValueType.DATE, date=None),
                },
                {
                    'id': '5f2eb176-b7cd-4be7-ac89-65aab0941490',
                    'type': PropertyType.ROLLUP,
                    'rollup': {'type': RollupValueType.DATE},
                },
                {
                    "id": "5f2eb176-b7cd-4be7-ac89-65aab0941490",
                    "type": "rollup",
                    "rollup": {"type": "date"},
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
            ({'checkbox': True}, {'checkbox': True}, {"checkbox": True}),
        ),
        (
            TxDatePropertyValue,
            (
                {
                    'date': NotionDate(
                        start=datetime(1988, 8, 6, 6, 30, 44), end=None, time_zone=None
                    )
                },
                {'date': {'start': datetime(1988, 8, 6, 6, 30, 44)}},
                {"date": {"start": "1988-08-06T06:30:44"}},
            ),
        ),
        (
            TxEmailPropertyValue,
            (
                {'email': 'jesusevans@example.net'},
                {'email': 'jesusevans@example.net'},
                {"email": "jesusevans@example.net"},
            ),
        ),
        (
            TxFilesPropertyValue,
            (
                {
                    'files': [
                        HostedFileWithName(
                            type=FileType.FILE,
                            file=HostedFileObject(
                                url='https://www.hunt.org/',
                                expiry_time=datetime(2018, 4, 21, 8, 8, 37, 21627),
                            ),
                            name='Gregory Short',
                        ),
                        ExternalFileWithName(
                            type=FileType.EXTERNAL,
                            external=ExternalFileObject(
                                url='http://www.thomas-smith.com/'
                            ),
                            name='Sarah Smith',
                        ),
                    ]
                },
                {
                    'files': [
                        {
                            'type': FileType.FILE,
                            'file': {
                                'url': 'https://www.hunt.org/',
                                'expiry_time': datetime(2018, 4, 21, 8, 8, 37, 21627),
                            },
                            'name': 'Gregory Short',
                        },
                        {
                            'type': FileType.EXTERNAL,
                            'external': {'url': 'http://www.thomas-smith.com/'},
                            'name': 'Sarah Smith',
                        },
                    ]
                },
                {
                    "files": [
                        {
                            "type": "file",
                            "file": {
                                "url": "https://www.hunt.org/",
                                "expiry_time": "2018-04-21T08:08:37.021627",
                            },
                            "name": "Gregory Short",
                        },
                        {
                            "type": "external",
                            "external": {"url": "http://www.thomas-smith.com/"},
                            "name": "Sarah Smith",
                        },
                    ]
                },
            ),
        ),
        (
            TxMultiSelectPropertyValue,
            (
                {'multi_select': [TxOptionValue(name='Taylor Woodard')]},
                {'multi_select': [{'name': 'Taylor Woodard'}]},
                {"multi_select": [{"name": "Taylor Woodard"}]},
            ),
        ),
        (
            TxNumberPropertyValue,
            ({'number': 214540}, {'number': 214540}, {"number": 214540}),
        ),
        (
            TxPeoplePropertyValue,
            (
                {
                    'people': [
                        UserRef(
                            object=NotionObjectType.USER,
                            id=UUID('00e6bfd6-a3c1-4495-86da-7cb32f3d52a2'),
                        ),
                        BotUser(
                            object=NotionObjectType.USER,
                            id=UUID('79aeca41-0dce-4263-aeb0-54920e251cca'),
                            name='Jennifer Oliver',
                            avatar_url='https://page.net/',
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
                            'id': UUID('00e6bfd6-a3c1-4495-86da-7cb32f3d52a2'),
                        },
                        {
                            'object': NotionObjectType.USER,
                            'id': UUID('79aeca41-0dce-4263-aeb0-54920e251cca'),
                        },
                    ]
                },
                {
                    "people": [
                        {
                            "object": "user",
                            "id": "00e6bfd6-a3c1-4495-86da-7cb32f3d52a2",
                        },
                        {
                            "object": "user",
                            "id": "79aeca41-0dce-4263-aeb0-54920e251cca",
                        },
                    ]
                },
            ),
        ),
        (
            TxPhoneNumberPropertyValue,
            (
                {'phone_number': '5554586668'},
                {'phone_number': '5554586668'},
                {"phone_number": "5554586668"},
            ),
        ),
        (
            TxRelationPropertyValue,
            (
                {
                    'relation': [
                        UUID('a13b2f23-9f51-4774-aa0d-baba3c17efbe'),
                        UUID('f7ea4ab1-0244-409d-8631-5772cd52c2fb'),
                    ]
                },
                {
                    'relation': [
                        UUID('a13b2f23-9f51-4774-aa0d-baba3c17efbe'),
                        UUID('f7ea4ab1-0244-409d-8631-5772cd52c2fb'),
                    ]
                },
                {
                    "relation": [
                        "a13b2f23-9f51-4774-aa0d-baba3c17efbe",
                        "f7ea4ab1-0244-409d-8631-5772cd52c2fb",
                    ]
                },
            ),
        ),
        (
            TxRichTextPropertyValue,
            (
                {
                    'rich_text': [
                        TxEquationRichText(
                            annotations=Annotations(
                                bold=True,
                                italic=False,
                                strikethrough=False,
                                underline=True,
                                code=False,
                                color=Color.YELLOW,
                            ),
                            type=RichTextType.EQUATION,
                            equation=Equation(
                                expression='Best boy carry assume firm of according. Friend bad western push if treatment. Citizen always trial. Expert receive discover itself yes.'
                            ),
                        ),
                        TxMentionRichText(
                            annotations=Annotations(
                                bold=True,
                                italic=False,
                                strikethrough=False,
                                underline=False,
                                code=True,
                                color=Color.YELLOW,
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
                    ]
                },
                {
                    'rich_text': [
                        {
                            'annotations': {
                                'bold': True,
                                'italic': False,
                                'strikethrough': False,
                                'underline': True,
                                'code': False,
                                'color': Color.YELLOW,
                            },
                            'equation': {
                                'expression': 'Best boy carry assume firm of according. Friend bad western push if treatment. Citizen always trial. Expert receive discover itself yes.'
                            },
                        },
                        {
                            'annotations': {
                                'bold': True,
                                'italic': False,
                                'strikethrough': False,
                                'underline': False,
                                'code': True,
                                'color': Color.YELLOW,
                            },
                            'mention': {
                                'type': MentionType.TEMPLATE_MENTION,
                                'template_mention': {
                                    'type': TemplateMentionType.TEMPLATE_MENTION_DATE,
                                    'template_mention_date': 'now',
                                },
                            },
                        },
                    ]
                },
                {
                    "rich_text": [
                        {
                            "annotations": {
                                "bold": True,
                                "italic": False,
                                "strikethrough": False,
                                "underline": True,
                                "code": False,
                                "color": "yellow",
                            },
                            "equation": {
                                "expression": "Best boy carry assume firm of according. Friend bad western push if treatment. Citizen always trial. Expert receive discover itself yes."
                            },
                        },
                        {
                            "annotations": {
                                "bold": True,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": True,
                                "color": "yellow",
                            },
                            "mention": {
                                "type": "template_mention",
                                "template_mention": {
                                    "type": "template_mention_date",
                                    "template_mention_date": "now",
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
                {'select': TxOptionValue(name='Jennifer Williams')},
                {'select': {'name': 'Jennifer Williams'}},
                {"select": {"name": "Jennifer Williams"}},
            ),
        ),
        (
            TxStatusPropertyValue,
            (
                {'status': TxOptionValue(name='Kimberly Potts')},
                {'status': {'name': 'Kimberly Potts'}},
                {"status": {"name": "Kimberly Potts"}},
            ),
        ),
        (
            TxTitlePropertyValue,
            (
                {
                    'title': [
                        TxMentionRichText(
                            annotations=Annotations(
                                bold=True,
                                italic=True,
                                strikethrough=True,
                                underline=True,
                                code=True,
                                color=Color.YELLOW,
                            ),
                            type=RichTextType.MENTION,
                            mention=DateMention(
                                type=MentionType.DATE,
                                date=NotionDate(
                                    start=datetime(2006, 10, 14, 13, 22, 32),
                                    end=None,
                                    time_zone=None,
                                ),
                            ),
                        ),
                        TxEquationRichText(
                            annotations=Annotations(
                                bold=False,
                                italic=False,
                                strikethrough=False,
                                underline=False,
                                code=True,
                                color=Color.YELLOW,
                            ),
                            type=RichTextType.EQUATION,
                            equation=Equation(
                                expression='Provide seven TV citizen ahead. Traditional carry bit central way.\nWill moment keep opportunity open employee control another. Attorney baby school form church.'
                            ),
                        ),
                    ]
                },
                {
                    'title': [
                        {
                            'annotations': {
                                'bold': True,
                                'italic': True,
                                'strikethrough': True,
                                'underline': True,
                                'code': True,
                                'color': Color.YELLOW,
                            },
                            'mention': {
                                'type': MentionType.DATE,
                                'date': {
                                    'start': datetime(2006, 10, 14, 13, 22, 32),
                                    'end': None,
                                    'time_zone': None,
                                },
                            },
                        },
                        {
                            'annotations': {
                                'bold': False,
                                'italic': False,
                                'strikethrough': False,
                                'underline': False,
                                'code': True,
                                'color': Color.YELLOW,
                            },
                            'equation': {
                                'expression': 'Provide seven TV citizen ahead. Traditional carry bit central way.\nWill moment keep opportunity open employee control another. Attorney baby school form church.'
                            },
                        },
                    ]
                },
                {
                    "title": [
                        {
                            "annotations": {
                                "bold": True,
                                "italic": True,
                                "strikethrough": True,
                                "underline": True,
                                "code": True,
                                "color": "yellow",
                            },
                            "mention": {
                                "type": "date",
                                "date": {
                                    "start": "2006-10-14T13:22:32",
                                    "end": None,
                                    "time_zone": None,
                                },
                            },
                        },
                        {
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": True,
                                "color": "yellow",
                            },
                            "equation": {
                                "expression": "Provide seven TV citizen ahead. Traditional carry bit central way.\nWill moment keep opportunity open employee control another. Attorney baby school form church."
                            },
                        },
                    ]
                },
            ),
        ),
        (
            TxUrlPropertyValue,
            (
                {'url': 'https://bradford.info/'},
                {'url': 'https://bradford.info/'},
                {"url": "https://bradford.info/"},
            ),
        ),
    ],
)
def test_tx_property_value_models_serialization(
    clz: type[BaseModel], test_data: tuple[dict, dict, dict]
):
    PydanticModelTester(clz, test_data).run_all_tests()
