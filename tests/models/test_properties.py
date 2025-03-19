import pytest
from pydantic import BaseModel

from pynotion.models.file import FileType, ExternalFileObject, ExternalFileWithName
from pynotion.models.object import NotionObjectType
from pynotion.models.properties import *
from pynotion.models.rich_text import (
    MentionRichText,
    Annotations,
    TemplateMention,
    RichTextType,
    MentionType,
    TemplateMentionDate,
    TemplateMentionType,
    TextRichText,
    Text,
    EquationRichText,
    Equation,
)
from pynotion.models.types import NotionUrlObject
from pynotion.models.user import (
    UserRef,
    UserType,
    BotOwnerType,
    WorkspaceBotOwner,
    Bot,
    BotUser,
    PersonUser,
    Person,
)
from tests.models.model_test_utils import DiscriminatedModelTester, PydanticModelTester


@pytest.mark.parametrize(
    "annotated_clz, expected_clz, input_data",
    [
        (
            Property,
            CheckboxProperty,
            {
                "id": "78c5c3ba-7f3d-4935-81f7-97f2e40b716b",
                "name": "Whitney Burnett",
                "type": "checkbox",
                "checkbox": {},
            },
        ),
        (
            Property,
            CreatedByProperty,
            {
                "id": "eb1fc034-b61e-40f5-b1bd-9d1f8691f8d7",
                "name": "Ronald Smith",
                "type": "created_by",
                "created_by": {},
            },
        ),
        (
            Property,
            CreatedTimeProperty,
            {
                "id": "07bce6a1-e64e-4295-9236-a696bb69ca40",
                "name": "Jeffery Moore",
                "type": "created_time",
                "created_time": {},
            },
        ),
        (
            Property,
            DateProperty,
            {
                "id": "8350cdfc-ac4c-455d-b574-9cccdc1502dc",
                "name": "Joel Kaiser",
                "type": "date",
                "date": {},
            },
        ),
        (
            Property,
            EmailProperty,
            {
                "id": "30a1d009-e0e4-4cfd-bfd2-34e7fb874cb2",
                "name": "Carmen Anderson",
                "type": "email",
                "email": {},
            },
        ),
        (
            Property,
            FilesProperty,
            {
                "id": "32136576-98ee-470e-a34a-1d79beaf8bf3",
                "name": "John Rogers",
                "type": "files",
                "files": {},
            },
        ),
        (
            Property,
            FormulaProperty,
            {
                "id": "d3d6720a-15d6-471c-9fcc-c89f80fdfdc8",
                "name": "Mary Morrison",
                "type": "formula",
                "formula": {"expression": "lTECTgvsJDNoDIscsFpb"},
            },
        ),
        (
            Property,
            LastEditedByProperty,
            {
                "id": "5872ad22-922b-48db-a6c3-a8d629bbdd09",
                "name": "Steve Jones",
                "type": "last_edited_by",
                "last_edited_by": {},
            },
        ),
        (
            Property,
            LastEditedTimeProperty,
            {
                "id": "789f8af0-d1a6-43bc-b583-f2efd2077ccb",
                "name": "Lynn Hunt",
                "type": "last_edited_time",
                "last_edited_time": {},
            },
        ),
        (
            Property,
            MultiSelectProperty,
            {
                "id": "4c6c5614-5d96-4888-aba5-c0f3c43446cd",
                "name": "Melissa Martin",
                "type": "multi_select",
                "multi_select": {
                    "options": [
                        {
                            "id": "702b5212-ff28-4172-9c0c-7878419e465e",
                            "name": "Anthony Wallace",
                            "color": "green",
                        },
                        {
                            "id": "d478259b-8b3f-4dc2-8e94-0a63fd62f4f3",
                            "name": "Brandon Willis",
                            "color": "green",
                        },
                    ]
                },
            },
        ),
        (
            Property,
            PeopleProperty,
            {
                "id": "69ca72c7-7a23-4c66-a01d-e863168929ef",
                "name": "Rachel Byrd",
                "type": "people",
                "people": {},
            },
        ),
        (
            Property,
            PhoneNumberProperty,
            {
                "id": "f56b9fa8-dea0-4421-8cc6-077b9c41363d",
                "name": "Michael Fields Jr.",
                "type": "phone_number",
                "phone_number": {},
            },
        ),
        (
            Property,
            RelationProperty,
            {
                "id": "f8ccbbb5-a9ab-4fdc-b1ca-612d094a9920",
                "name": "Aaron Hodges",
                "type": "relation",
                "relation": {
                    "database_id": "a41f56fd-58ed-4718-9782-379dc7aeedf7",
                    "dual_property": {
                        "synced_property_id": "7f113203-0e09-41c2-9658-fbbdc4d59bf0",
                        "synced_property_name": "David Wallace",
                    },
                },
            },
        ),
        (
            Property,
            RichTextProperty,
            {
                "id": "ab3e989b-7c69-4d65-9b9b-03840f92097c",
                "name": "Dawn James",
                "type": "rich_text",
                "rich_text": {},
            },
        ),
        (
            Property,
            RollupProperty,
            {
                "id": "e54f2803-f667-4c5d-aac7-0b6876b726e6",
                "name": "Paula Estes",
                "type": "rollup",
                "rollup": {
                    "relation_property_name": "Dave Clark",
                    "relation_property_id": "c5a04145-3c7d-4d25-836c-af565fb639cd",
                    "rollup_property_name": "Cindy Moody",
                    "rollup_property_id": "e4fc9273-8582-4635-a8f5-e3227ec7e8db",
                    "function": "min",
                },
            },
        ),
        (
            Property,
            SelectProperty,
            {
                "id": "529e0001-9343-45fe-be11-510b5a373bad",
                "name": "Shawn Sampson",
                "type": "select",
                "select": {
                    "options": [
                        {
                            "id": "702b5212-ff28-4172-9c0c-7878419e465e",
                            "name": "Anthony Wallace",
                            "color": "green",
                        },
                        {
                            "id": "d478259b-8b3f-4dc2-8e94-0a63fd62f4f3",
                            "name": "Brandon Willis",
                            "color": "green",
                        },
                    ]
                },
            },
        ),
        (
            Property,
            StatusProperty,
            {
                "id": "09f0c092-dbaf-4206-b2c1-4d7e5f006827",
                "name": "Alexa Williams",
                "type": "status",
                "status": {
                    "options": [
                        {
                            "id": "73b14ddc-db5f-44f3-8b4c-ba7fc2540865",
                            "name": "Kimberly Kennedy",
                        }
                    ]
                },
                "groups": [
                    {
                        "id": "d8bafbe5-6bc5-4855-973a-1540a3a750e4",
                        "name": "Lisa Salinas",
                        "option_ids": ["a90fba3c-569b-4fb3-9f35-ec9a001d3a2c"],
                    },
                    {
                        "id": "732d9958-7310-4907-87e5-8d31ebc6cc8d",
                        "name": "Evan Mays",
                        "option_ids": ["a90fba3c-569b-4fb3-9f35-ec9a001d3a2c"],
                    },
                ],
            },
        ),
        (
            Property,
            TitleProperty,
            {
                "id": "d2c2bb1c-bfe9-498b-ad22-97e9a9bc227f",
                "name": "Corey Joyce",
                "type": "title",
                "title": {},
            },
        ),
        (
            Property,
            UrlProperty,
            {
                "id": "b5042810-f17e-4f64-bdc5-c9fe08d69988",
                "name": "Ronald Hines",
                "type": "url",
                "url": {},
            },
        ),
    ],
)
def test_property_discriminated_model(
    annotated_clz: type, expected_clz: type, input_data: dict
):
    DiscriminatedModelTester(annotated_clz, expected_clz, **input_data).run_all_tests()


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
            {
                "type": "date",
                "date": {
                    "start": "1988-03-06T10:17:35",
                    "time_zone": "Asia/Aden",
                },
            },
        ),
        (
            FormulaValue,
            NumberFormulaValue,
            {"type": "number"},
        ),
        (
            FormulaValue,
            StringFormulaValue,
            {
                "type": "string",
                "string": "Throw meet per risk event. Necessary home glass meet through TV. Democrat travel never cold situation ok.\nWhile second between black. Scientist week view paper mean financial push.",
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
                        "id": "598b5a95-e196-4159-a517-77e8b2735523",
                        "type": "multi_select",
                        "multi_select": [
                            {"id": "c2ac0216-a1c2-4a26-a811-829e0ce79ebb"}
                        ],
                    }
                ],
            },
        ),
        (
            RollupValue,
            DateRollupValue,
            {
                "type": "date",
                "date": {
                    "start": "2008-02-12T07:19:36.563",
                    "time_zone": "Asia/Aden",
                },
            },
        ),
        (
            RollupValue,
            IncompleteRollupValue,
            {"type": "incomplete"},
        ),
        (
            RollupValue,
            NumberRollupValue,
            {"type": "number"},
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
            PropertyValue,
            CheckboxPropertyValue,
            {
                "id": "533593db-38fe-449c-885a-0c787d09c1d9",
                "type": "checkbox",
                "checkbox": False,
            },
        ),
        (
            PropertyValue,
            CreatedByPropertyValue,
            {
                "type": "created_by",
                "created_by": {
                    "object": "user",
                    "id": "f072e011-3b71-46e7-ad65-993fb22e2531",
                },
            },
        ),
        (
            PropertyValue,
            CreatedTimePropertyValue,
            {
                "id": "b0608713-4d27-4a39-acb0-c23075a040b6",
                "type": "created_time",
                "created_time": "2024-04-30T18:46:54.236996",
            },
        ),
        (
            PropertyValue,
            DatePropertyValue,
            {
                "id": "729a8e08-5cd7-42c0-b191-995f6df701ef",
                "type": "date",
                "date": {"start": "1997-02-09T08:06:52.874808"},
            },
        ),
        (
            PropertyValue,
            EmailPropertyValue,
            {
                "id": "4617220f-efe0-479e-ad1b-35ea587b9b96",
                "type": "email",
                "email": "wilsoncrystal@example.org",
            },
        ),
        (
            PropertyValue,
            FilesPropertyValue,
            {
                "id": "cc7b8545-3ee9-45e7-9235-c5f1b7745ee5",
                "type": "files",
                "files": [
                    {
                        "type": "external",
                        "external": {"url": "http://clark.com/"},
                        "name": "John Gamble",
                    },
                    {
                        "type": "external",
                        "external": {"url": "https://taylor-walker.com/"},
                        "name": "April Rodriguez",
                    },
                ],
            },
        ),
        (
            PropertyValue,
            FormulaPropertyValue,
            {
                "id": "32cef225-517d-462c-8c60-b06bc8e58e6c",
                "type": "formula",
                "formula": {
                    "type": "string",
                    "string": "Rest especially single girl why head. Woman ok free reality yes ever experience. That weight first why available section against.",
                },
            },
        ),
        (
            PropertyValue,
            LastEditedByPropertyValue,
            {
                "id": "a4d9699f-d586-4c3d-8785-8bea4de1fb42",
                "type": "last_edited_by",
                "last_edited_by": {
                    "object": "user",
                    "id": "006f95a1-2816-4749-94cf-6474ee60cca4",
                },
            },
        ),
        (
            PropertyValue,
            LastEditedTimePropertyValue,
            {
                "type": "last_edited_time",
                "last_edited_time": "1973-12-12T01:11:29.858900",
            },
        ),
        (
            PropertyValue,
            MultiSelectPropertyValue,
            {
                "type": "multi_select",
                "multi_select": [
                    {
                        "id": "3f04507a-6fb5-443c-8731-d0749e7fd9a3",
                        "name": "Jeffery Benson",
                        "color": "orange",
                    },
                    {
                        "id": "0f155c70-4928-4340-80e8-ab57f147c8df",
                        "name": "Casey Martinez",
                        "color": "blue",
                    },
                ],
            },
        ),
        (
            PropertyValue,
            NumberPropertyValue,
            {"id": "aabb43fd-d1d5-4952-9caf-4f1df35567c2", "type": "number"},
        ),
        (
            PropertyValue,
            PeoplePropertyValue,
            {
                "id": "e9b0ebf0-46f0-4cf7-8f16-1332bd8a6c78",
                "type": "people",
                "people": [
                    {
                        "object": "user",
                        "id": "32c55014-953c-4658-87ea-3940b52e7ab9",
                        "name": "Nicholas Marshall",
                        "avatar_url": "https://myers-lopez.info/",
                        "type": "person",
                        "person": {"email": "timmoreno@example.com"},
                    }
                ],
            },
        ),
        (
            PropertyValue,
            PhoneNumberPropertyValue,
            {
                "id": "3c05398d-89a4-4e76-ba0a-9684202c0ecb",
                "type": "phone_number",
                "phone_number": "3143832011",
            },
        ),
        (
            PropertyValue,
            RelationPropertyValue,
            {
                "type": "relation",
                "relation": [
                    "40fe151f-de7d-4bdb-848c-ea6512917f2b",
                    "e24c690d-0ce6-4968-8589-9ee1de1f33be",
                ],
            },
        ),
        (
            PropertyValue,
            RichTextPropertyValue,
            {
                "type": "rich_text",
                "rich_text": [
                    {
                        "annotations": {
                            "bold": True,
                            "strikethrough": False,
                            "code": True,
                            "color": "gray",
                        },
                        "plain_text": "Evening enjoy how ready.",
                        "href": "https://www.castillo-brown.net/",
                        "type": "equation",
                        "equation": {
                            "expression": "Perform Mrs leave recently. Size someone particularly impact medical.\nThey brother actually full. Exist decide doctor court."
                        },
                    },
                    {
                        "annotations": {
                            "bold": True,
                            "strikethrough": False,
                            "code": True,
                            "color": "gray",
                        },
                        "plain_text": "Evening enjoy how ready.",
                        "href": "https://bowers.org/",
                        "type": "text",
                        "text": {
                            "content": "Design him enough accept current sign understand.",
                            "link": {"url": "https://castro.net/"},
                        },
                    },
                ],
            },
        ),
        (
            PropertyValue,
            RollupPropertyValue,
            {"type": "rollup", "rollup": {"type": "unsupported"}},
        ),
        (
            PropertyValue,
            SelectPropertyValue,
            {"type": "select", "select": {"name": "Tyler Davis"}},
        ),
        (
            PropertyValue,
            StatusPropertyValue,
            {
                "id": "e48bad7e-a6a2-40e3-b515-509fb2fde178",
                "type": "status",
                "status": {"id": "86ee6212-8b6e-4d27-b456-d849b24818a0"},
            },
        ),
        (
            PropertyValue,
            TitlePropertyValue,
            {
                "type": "title",
                "title": [
                    {
                        "annotations": {
                            "bold": True,
                            "strikethrough": False,
                            "code": True,
                            "color": "gray",
                        },
                        "plain_text": "Evening enjoy how ready.",
                        "href": "https://may.com/",
                        "type": "text",
                        "text": {
                            "content": "Design him enough accept current sign understand.",
                            "link": {"url": "https://castro.net/"},
                        },
                    }
                ],
            },
        ),
        (
            PropertyValue,
            UrlPropertyValue,
            {"type": "url", "url": "http://miller-allen.net/"},
        ),
        (
            PropertyValue,
            UniqueIdPropertyValue,
            {"type": "unique_id", "unique_id": {"number": 5361}},
        ),
        (
            PropertyValue,
            VerificationPropertyValue,
            {
                "type": "verification",
                "verification": {
                    "state": "verified",
                    "verified_by": {
                        "object": "user",
                        "id": "274c16a9-342a-455e-8d66-0ff70e1c7ba2",
                        "name": "Rachel Singh",
                        "avatar_url": "http://www.stewart.com/",
                        "type": "bot",
                        "bot": {"owner": {"type": "user"}},
                    },
                    "date": {"start": "2011-02-06T14:12:34.103888"},
                },
            },
        ),
    ],
)
def test_property_value_discriminated_model(
    annotated_clz: type, expected_clz: type, input_data: dict
):
    DiscriminatedModelTester(annotated_clz, expected_clz, **input_data).run_all_tests()


@pytest.mark.parametrize(
    "clz, test_data",
    [
        (
            CheckboxProperty,
            (
                {
                    'id': '44424ccb-5539-4305-ab97-e2cc1d43149e',
                    'name': 'Kenneth Henderson',
                    'type': PropertyType.CHECKBOX,
                    'checkbox': {},
                },
                {
                    'id': '44424ccb-5539-4305-ab97-e2cc1d43149e',
                    'name': 'Kenneth Henderson',
                    'type': PropertyType.CHECKBOX,
                    'checkbox': {},
                },
                {
                    "id": "44424ccb-5539-4305-ab97-e2cc1d43149e",
                    "name": "Kenneth Henderson",
                    "type": "checkbox",
                    "checkbox": {},
                },
            ),
        ),
        (
            CreatedByProperty,
            (
                {
                    'id': '24525542-707c-41c9-abb7-09cfbb3cb786',
                    'name': 'Manuel Miller',
                    'type': PropertyType.CREATED_BY,
                    'created_by': {},
                },
                {
                    'id': '24525542-707c-41c9-abb7-09cfbb3cb786',
                    'name': 'Manuel Miller',
                    'type': PropertyType.CREATED_BY,
                    'created_by': {},
                },
                {
                    "id": "24525542-707c-41c9-abb7-09cfbb3cb786",
                    "name": "Manuel Miller",
                    "type": "created_by",
                    "created_by": {},
                },
            ),
        ),
        (
            CreatedTimeProperty,
            (
                {
                    'id': '65075eb7-ed40-4f28-a179-0d622c46e8c3',
                    'name': 'Anthony Ballard PhD',
                    'type': PropertyType.CREATED_TIME,
                    'created_time': {},
                },
                {
                    'id': '65075eb7-ed40-4f28-a179-0d622c46e8c3',
                    'name': 'Anthony Ballard PhD',
                    'type': PropertyType.CREATED_TIME,
                    'created_time': {},
                },
                {
                    "id": "65075eb7-ed40-4f28-a179-0d622c46e8c3",
                    "name": "Anthony Ballard PhD",
                    "type": "created_time",
                    "created_time": {},
                },
            ),
        ),
        (
            DateProperty,
            (
                {
                    'id': '46c3d45f-1297-4660-a449-eaa1933013df',
                    'name': 'Paula Morris',
                    'type': PropertyType.DATE,
                    'date': {},
                },
                {
                    'id': '46c3d45f-1297-4660-a449-eaa1933013df',
                    'name': 'Paula Morris',
                    'type': PropertyType.DATE,
                    'date': {},
                },
                {
                    "id": "46c3d45f-1297-4660-a449-eaa1933013df",
                    "name": "Paula Morris",
                    "type": "date",
                    "date": {},
                },
            ),
        ),
        (
            EmailProperty,
            (
                {
                    'id': '2570f4f1-27ac-4bc8-9fa0-21cb18675e86',
                    'name': 'Derek Gonzalez',
                    'type': PropertyType.EMAIL,
                    'email': {},
                },
                {
                    'id': '2570f4f1-27ac-4bc8-9fa0-21cb18675e86',
                    'name': 'Derek Gonzalez',
                    'type': PropertyType.EMAIL,
                    'email': {},
                },
                {
                    "id": "2570f4f1-27ac-4bc8-9fa0-21cb18675e86",
                    "name": "Derek Gonzalez",
                    "type": "email",
                    "email": {},
                },
            ),
        ),
        (
            FilesProperty,
            (
                {
                    'id': 'f2e014a7-d75d-43ee-9389-1eb5d4bb5c06',
                    'name': 'Lori Russell',
                    'type': PropertyType.FILES,
                    'files': {},
                },
                {
                    'id': 'f2e014a7-d75d-43ee-9389-1eb5d4bb5c06',
                    'name': 'Lori Russell',
                    'type': PropertyType.FILES,
                    'files': {},
                },
                {
                    "id": "f2e014a7-d75d-43ee-9389-1eb5d4bb5c06",
                    "name": "Lori Russell",
                    "type": "files",
                    "files": {},
                },
            ),
        ),
        (
            FormulaProperty,
            (
                {
                    'id': 'eda6da0c-36b0-4ab6-89ce-f0dd1a7299c6',
                    'name': 'Heather Powers',
                    'type': PropertyType.FORMULA,
                    'formula': NotionEquation(expression='zfAAVnQmcZExzjDjrjXC'),
                },
                {
                    'id': 'eda6da0c-36b0-4ab6-89ce-f0dd1a7299c6',
                    'name': 'Heather Powers',
                    'type': PropertyType.FORMULA,
                    'formula': {'expression': 'zfAAVnQmcZExzjDjrjXC'},
                },
                {
                    "id": "eda6da0c-36b0-4ab6-89ce-f0dd1a7299c6",
                    "name": "Heather Powers",
                    "type": "formula",
                    "formula": {"expression": "zfAAVnQmcZExzjDjrjXC"},
                },
            ),
        ),
        (
            LastEditedByProperty,
            (
                {
                    'id': '04f9ca50-1326-47bd-ac10-5d53917cca49',
                    'name': 'John Ewing',
                    'type': PropertyType.LAST_EDITED_BY,
                    'last_edited_by': {},
                },
                {
                    'id': '04f9ca50-1326-47bd-ac10-5d53917cca49',
                    'name': 'John Ewing',
                    'type': PropertyType.LAST_EDITED_BY,
                    'last_edited_by': {},
                },
                {
                    "id": "04f9ca50-1326-47bd-ac10-5d53917cca49",
                    "name": "John Ewing",
                    "type": "last_edited_by",
                    "last_edited_by": {},
                },
            ),
        ),
        (
            LastEditedTimeProperty,
            (
                {
                    'id': 'ca6b1949-5e14-4076-b931-f5e2f4fedc03',
                    'name': 'Terry Brown',
                    'type': PropertyType.LAST_EDITED_TIME,
                    'last_edited_time': {},
                },
                {
                    'id': 'ca6b1949-5e14-4076-b931-f5e2f4fedc03',
                    'name': 'Terry Brown',
                    'type': PropertyType.LAST_EDITED_TIME,
                    'last_edited_time': {},
                },
                {
                    "id": "ca6b1949-5e14-4076-b931-f5e2f4fedc03",
                    "name": "Terry Brown",
                    "type": "last_edited_time",
                    "last_edited_time": {},
                },
            ),
        ),
        (
            MultiSelectProperty,
            (
                {
                    'id': 'f2186273-9a33-4700-ac46-4349f89e4884',
                    'name': 'Julia Delgado',
                    'type': PropertyType.MULTI_SELECT,
                    'multi_select': SelectOptions(options=None),
                },
                {
                    'id': 'f2186273-9a33-4700-ac46-4349f89e4884',
                    'name': 'Julia Delgado',
                    'type': PropertyType.MULTI_SELECT,
                    'multi_select': {},
                },
                {
                    "id": "f2186273-9a33-4700-ac46-4349f89e4884",
                    "name": "Julia Delgado",
                    "type": "multi_select",
                    "multi_select": {},
                },
            ),
        ),
        (
            PeopleProperty,
            (
                {
                    'id': 'b127aace-e98b-46cb-af23-7d1fc98c3c77',
                    'name': 'Abigail Gonzales',
                    'type': PropertyType.PEOPLE,
                    'people': {},
                },
                {
                    'id': 'b127aace-e98b-46cb-af23-7d1fc98c3c77',
                    'name': 'Abigail Gonzales',
                    'type': PropertyType.PEOPLE,
                    'people': {},
                },
                {
                    "id": "b127aace-e98b-46cb-af23-7d1fc98c3c77",
                    "name": "Abigail Gonzales",
                    "type": "people",
                    "people": {},
                },
            ),
        ),
        (
            PhoneNumberProperty,
            (
                {
                    'id': '666f99ed-0981-4288-8e9f-0a9afa90d6b9',
                    'name': 'Joshua Phillips',
                    'type': PropertyType.PHONE_NUMBER,
                    'phone_number': {},
                },
                {
                    'id': '666f99ed-0981-4288-8e9f-0a9afa90d6b9',
                    'name': 'Joshua Phillips',
                    'type': PropertyType.PHONE_NUMBER,
                    'phone_number': {},
                },
                {
                    "id": "666f99ed-0981-4288-8e9f-0a9afa90d6b9",
                    "name": "Joshua Phillips",
                    "type": "phone_number",
                    "phone_number": {},
                },
            ),
        ),
        (
            RelationProperty,
            (
                {
                    'id': '0c2ea6a9-786d-4ba1-a288-0923b4c719c1',
                    'name': 'Robert Baker',
                    'type': PropertyType.RELATION,
                    'relation': Relation(
                        database_id=UUID('264f0b92-0b6d-4fd8-a5bd-464c407c93ba'),
                        dual_property=DualProperty(
                            synced_property_id='9ce92798-a927-4376-9b5d-c53db38ec45e',
                            synced_property_name='Luke Burns',
                        ),
                    ),
                },
                {
                    'id': '0c2ea6a9-786d-4ba1-a288-0923b4c719c1',
                    'name': 'Robert Baker',
                    'type': PropertyType.RELATION,
                    'relation': {
                        'database_id': UUID('264f0b92-0b6d-4fd8-a5bd-464c407c93ba'),
                        'dual_property': {
                            'synced_property_id': '9ce92798-a927-4376-9b5d-c53db38ec45e',
                            'synced_property_name': 'Luke Burns',
                        },
                    },
                },
                {
                    "id": "0c2ea6a9-786d-4ba1-a288-0923b4c719c1",
                    "name": "Robert Baker",
                    "type": "relation",
                    "relation": {
                        "database_id": "264f0b92-0b6d-4fd8-a5bd-464c407c93ba",
                        "dual_property": {
                            "synced_property_id": "9ce92798-a927-4376-9b5d-c53db38ec45e",
                            "synced_property_name": "Luke Burns",
                        },
                    },
                },
            ),
        ),
        (
            RichTextProperty,
            (
                {
                    'id': 'c6e5f9d7-01af-4b79-ba6e-cfd72a553967',
                    'name': 'Mrs. Linda Barrett DVM',
                    'type': PropertyType.RICH_TEXT,
                    'rich_text': {},
                },
                {
                    'id': 'c6e5f9d7-01af-4b79-ba6e-cfd72a553967',
                    'name': 'Mrs. Linda Barrett DVM',
                    'type': PropertyType.RICH_TEXT,
                    'rich_text': {},
                },
                {
                    "id": "c6e5f9d7-01af-4b79-ba6e-cfd72a553967",
                    "name": "Mrs. Linda Barrett DVM",
                    "type": "rich_text",
                    "rich_text": {},
                },
            ),
        ),
        (
            RollupProperty,
            (
                {
                    'id': '9cc7addf-3d58-4e18-8af8-b3b46d9fb5e3',
                    'name': 'Devon Francis',
                    'type': PropertyType.ROLLUP,
                    'rollup': Rollup(
                        relation_property_name='Jared Peterson',
                        relation_property_id='f4a447af-78cd-437b-b2ec-7138c95cda74',
                        rollup_property_name='Daniel Ellis',
                        rollup_property_id='9aefbbcc-a1e0-4ac6-b00b-fa761cc2ddc3',
                        function=RollupFunction.EMPTY,
                    ),
                },
                {
                    'id': '9cc7addf-3d58-4e18-8af8-b3b46d9fb5e3',
                    'name': 'Devon Francis',
                    'type': PropertyType.ROLLUP,
                    'rollup': {
                        'relation_property_name': 'Jared Peterson',
                        'relation_property_id': 'f4a447af-78cd-437b-b2ec-7138c95cda74',
                        'rollup_property_name': 'Daniel Ellis',
                        'rollup_property_id': '9aefbbcc-a1e0-4ac6-b00b-fa761cc2ddc3',
                        'function': RollupFunction.EMPTY,
                    },
                },
                {
                    "id": "9cc7addf-3d58-4e18-8af8-b3b46d9fb5e3",
                    "name": "Devon Francis",
                    "type": "rollup",
                    "rollup": {
                        "relation_property_name": "Jared Peterson",
                        "relation_property_id": "f4a447af-78cd-437b-b2ec-7138c95cda74",
                        "rollup_property_name": "Daniel Ellis",
                        "rollup_property_id": "9aefbbcc-a1e0-4ac6-b00b-fa761cc2ddc3",
                        "function": "empty",
                    },
                },
            ),
        ),
        (
            SelectProperty,
            (
                {
                    'id': 'd803bb22-cfce-4257-9da4-f5d6c383310a',
                    'name': 'Nicole Maxwell',
                    'type': PropertyType.SELECT,
                    'select': SelectOptions(options=None),
                },
                {
                    'id': 'd803bb22-cfce-4257-9da4-f5d6c383310a',
                    'name': 'Nicole Maxwell',
                    'type': PropertyType.SELECT,
                    'select': {},
                },
                {
                    "id": "d803bb22-cfce-4257-9da4-f5d6c383310a",
                    "name": "Nicole Maxwell",
                    "type": "select",
                    "select": {},
                },
            ),
        ),
        (
            StatusProperty,
            (
                {
                    'id': 'ceeda090-1c49-49c7-9099-3a3dcb566679',
                    'name': 'April Miller',
                    'type': PropertyType.STATUS,
                    'status': StatusOptions(options=None),
                    'groups': [
                        GroupOption(
                            id='3b1a0c98-2622-4bd4-b9f6-2a0d5024735b',
                            name='Steven Harris',
                            color=None,
                            option_ids=None,
                        )
                    ],
                },
                {
                    'id': 'ceeda090-1c49-49c7-9099-3a3dcb566679',
                    'name': 'April Miller',
                    'type': PropertyType.STATUS,
                    'status': {},
                    'groups': [
                        {
                            'id': '3b1a0c98-2622-4bd4-b9f6-2a0d5024735b',
                            'name': 'Steven Harris',
                        }
                    ],
                },
                {
                    "id": "ceeda090-1c49-49c7-9099-3a3dcb566679",
                    "name": "April Miller",
                    "type": "status",
                    "status": {},
                    "groups": [
                        {
                            "id": "3b1a0c98-2622-4bd4-b9f6-2a0d5024735b",
                            "name": "Steven Harris",
                        }
                    ],
                },
            ),
        ),
        (
            TitleProperty,
            (
                {
                    'id': '9ac3bb69-27f7-4ad0-bfdc-8835a2e02864',
                    'name': 'Jamie Li',
                    'type': PropertyType.TITLE,
                    'title': {},
                },
                {
                    'id': '9ac3bb69-27f7-4ad0-bfdc-8835a2e02864',
                    'name': 'Jamie Li',
                    'type': PropertyType.TITLE,
                    'title': {},
                },
                {
                    "id": "9ac3bb69-27f7-4ad0-bfdc-8835a2e02864",
                    "name": "Jamie Li",
                    "type": "title",
                    "title": {},
                },
            ),
        ),
        (
            UrlProperty,
            (
                {
                    'id': 'e1c5bb83-f3a2-4f43-aeec-8ca37c559dd3',
                    'name': 'Veronica Tran',
                    'type': PropertyType.URL,
                    'url': {},
                },
                {
                    'id': 'e1c5bb83-f3a2-4f43-aeec-8ca37c559dd3',
                    'name': 'Veronica Tran',
                    'type': PropertyType.URL,
                    'url': {},
                },
                {
                    "id": "e1c5bb83-f3a2-4f43-aeec-8ca37c559dd3",
                    "name": "Veronica Tran",
                    "type": "url",
                    "url": {},
                },
            ),
        ),
    ],
)
def test_property_models_serialization(
    clz: type[BaseModel], test_data: tuple[dict, dict, dict]
):
    PydanticModelTester(clz, test_data).run_all_tests()


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
                        start=datetime(1987, 6, 6, 11, 30, 51, 130050),
                        end=None,
                        time_zone=None,
                    ),
                },
                {
                    'type': FormulaValueType.DATE,
                    'date': {'start': datetime(1987, 6, 6, 11, 30, 51, 130050)},
                },
                {"type": "date", "date": {"start": "1987-06-06T11:30:51.130050"}},
            ),
        ),
        (
            NumberFormulaValue,
            (
                {'type': FormulaValueType.NUMBER, 'number': 75192301},
                {'type': FormulaValueType.NUMBER, 'number': 75192301},
                {"type": "number", "number": 75192301},
            ),
        ),
        (
            StringFormulaValue,
            (
                {
                    'type': FormulaValueType.STRING,
                    'string': 'Across different ball study.\nGround material law raise bag.\nMedia arm be stand official. Understand leader perhaps dream military hold she.\nYour how Democrat either. Left fight look book government.',
                },
                {
                    'type': FormulaValueType.STRING,
                    'string': 'Across different ball study.\nGround material law raise bag.\nMedia arm be stand official. Understand leader perhaps dream military hold she.\nYour how Democrat either. Left fight look book government.',
                },
                {
                    "type": "string",
                    "string": "Across different ball study.\nGround material law raise bag.\nMedia arm be stand official. Understand leader perhaps dream military hold she.\nYour how Democrat either. Left fight look book government.",
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
                        EmailPropertyValue(
                            id='81845011-5ba4-4e29-9961-1292b0df9cd0',
                            type=PropertyType.EMAIL,
                            email='williechavez@example.net',
                        )
                    ],
                },
                {
                    'type': RollupValueType.ARRAY,
                    'array': [
                        {
                            'id': '81845011-5ba4-4e29-9961-1292b0df9cd0',
                            'type': PropertyType.EMAIL,
                            'email': 'williechavez@example.net',
                        }
                    ],
                },
                {
                    "type": "array",
                    "array": [
                        {
                            "id": "81845011-5ba4-4e29-9961-1292b0df9cd0",
                            "type": "email",
                            "email": "williechavez@example.net",
                        }
                    ],
                },
            ),
        ),
        (
            DateRollupValue,
            (
                {
                    'type': RollupValueType.DATE,
                    'date': NotionDate(
                        start=datetime(2015, 2, 22, 5, 24, 59, 872080),
                        end=None,
                        time_zone=None,
                    ),
                },
                {
                    'type': RollupValueType.DATE,
                    'date': {'start': datetime(2015, 2, 22, 5, 24, 59, 872080)},
                },
                {"type": "date", "date": {"start": "2015-02-22T05:24:59.872080"}},
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
                {'type': RollupValueType.NUMBER, 'number': 1.23},
                {'type': RollupValueType.NUMBER, 'number': 1.23},
                {"type": "number", "number": 1.23},
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
            CheckboxPropertyValue,
            (
                {'id': None, 'type': PropertyType.CHECKBOX, 'checkbox': True},
                {'type': PropertyType.CHECKBOX, 'checkbox': True},
                {"type": "checkbox", "checkbox": True},
            ),
        ),
        (
            CreatedByPropertyValue,
            (
                {
                    'id': '24cbc050-1ff6-4923-b835-5a19fc4f331c',
                    'type': PropertyType.CREATED_BY,
                    'created_by': PersonUser(
                        object=NotionObjectType.USER,
                        id=UUID('fd63c32e-dbd2-4ab6-bd32-ffd4cc00465a'),
                        name='Ariana Vasquez',
                        avatar_url='https://cunningham-mathews.biz/',
                        type=UserType.PERSON,
                        person=Person(email='ygordon@example.com'),
                    ),
                },
                {
                    'id': '24cbc050-1ff6-4923-b835-5a19fc4f331c',
                    'type': PropertyType.CREATED_BY,
                    'created_by': {
                        'object': NotionObjectType.USER,
                        'id': UUID('fd63c32e-dbd2-4ab6-bd32-ffd4cc00465a'),
                        'name': 'Ariana Vasquez',
                        'avatar_url': 'https://cunningham-mathews.biz/',
                        'type': UserType.PERSON,
                        'person': {'email': 'ygordon@example.com'},
                    },
                },
                {
                    "id": "24cbc050-1ff6-4923-b835-5a19fc4f331c",
                    "type": "created_by",
                    "created_by": {
                        "object": "user",
                        "id": "fd63c32e-dbd2-4ab6-bd32-ffd4cc00465a",
                        "name": "Ariana Vasquez",
                        "avatar_url": "https://cunningham-mathews.biz/",
                        "type": "person",
                        "person": {"email": "ygordon@example.com"},
                    },
                },
            ),
        ),
        (
            CreatedTimePropertyValue,
            (
                {
                    'id': 'd140449a-31ca-4159-9b98-52a3c1db790d',
                    'type': PropertyType.CREATED_TIME,
                    'created_time': datetime(1990, 6, 26, 10, 25, 29, 241103),
                },
                {
                    'id': 'd140449a-31ca-4159-9b98-52a3c1db790d',
                    'type': PropertyType.CREATED_TIME,
                    'created_time': datetime(1990, 6, 26, 10, 25, 29, 241103),
                },
                {
                    "id": "d140449a-31ca-4159-9b98-52a3c1db790d",
                    "type": "created_time",
                    "created_time": "1990-06-26T10:25:29.241103",
                },
            ),
        ),
        (
            DatePropertyValue,
            (
                {
                    'id': None,
                    'type': PropertyType.DATE,
                    'date': NotionDate(
                        start=datetime(2003, 4, 12, 4, 39, 25, 332651),
                        end=None,
                        time_zone=None,
                    ),
                },
                {
                    'type': PropertyType.DATE,
                    'date': {'start': datetime(2003, 4, 12, 4, 39, 25, 332651)},
                },
                {"type": "date", "date": {"start": "2003-04-12T04:39:25.332651"}},
            ),
        ),
        (
            EmailPropertyValue,
            (
                {
                    'id': None,
                    'type': PropertyType.EMAIL,
                    'email': 'stephanie35@example.org',
                },
                {'type': PropertyType.EMAIL, 'email': 'stephanie35@example.org'},
                {"type": "email", "email": "stephanie35@example.org"},
            ),
        ),
        (
            FilesPropertyValue,
            (
                {
                    'id': None,
                    'type': PropertyType.FILES,
                    'files': [
                        ExternalFileWithName(
                            type=FileType.EXTERNAL,
                            external=ExternalFileObject(url='http://peterson.net/'),
                            name='Lori Peterson',
                        )
                    ],
                },
                {
                    'type': PropertyType.FILES,
                    'files': [
                        {
                            'type': FileType.EXTERNAL,
                            'external': {'url': 'http://peterson.net/'},
                            'name': 'Lori Peterson',
                        }
                    ],
                },
                {
                    "type": "files",
                    "files": [
                        {
                            "type": "external",
                            "external": {"url": "http://peterson.net/"},
                            "name": "Lori Peterson",
                        }
                    ],
                },
            ),
        ),
        (
            FormulaPropertyValue,
            (
                {
                    'id': 'b5a09928-9188-47b8-b291-053fb7cfa9b7',
                    'type': PropertyType.FORMULA,
                    'formula': BooleanFormulaValue(
                        type=FormulaValueType.BOOLEAN, boolean=False
                    ),
                },
                {
                    'id': 'b5a09928-9188-47b8-b291-053fb7cfa9b7',
                    'type': PropertyType.FORMULA,
                    'formula': {'type': FormulaValueType.BOOLEAN, 'boolean': False},
                },
                {
                    "id": "b5a09928-9188-47b8-b291-053fb7cfa9b7",
                    "type": "formula",
                    "formula": {"type": "boolean", "boolean": False},
                },
            ),
        ),
        (
            LastEditedByPropertyValue,
            (
                {
                    'id': '688dc22c-12f1-49c8-8ab7-0c944a99d86b',
                    'type': PropertyType.LAST_EDITED_BY,
                    'last_edited_by': BotUser(
                        object=NotionObjectType.USER,
                        id=UUID('9d99827c-d2b7-422d-99f4-5d6b9df02806'),
                        name='Derek Hansen',
                        avatar_url='https://www.malone-gay.com/',
                        type=UserType.BOT,
                        bot=Bot(
                            owner=WorkspaceBotOwner(
                                type=BotOwnerType.WORKSPACE, workspace=True
                            ),
                            workspace_name='Sample Workspace',
                        ),
                    ),
                },
                {
                    'id': '688dc22c-12f1-49c8-8ab7-0c944a99d86b',
                    'type': PropertyType.LAST_EDITED_BY,
                    'last_edited_by': {
                        'object': NotionObjectType.USER,
                        'id': UUID('9d99827c-d2b7-422d-99f4-5d6b9df02806'),
                        'name': 'Derek Hansen',
                        'avatar_url': 'https://www.malone-gay.com/',
                        'type': UserType.BOT,
                        'bot': {
                            'owner': {
                                'type': BotOwnerType.WORKSPACE,
                                'workspace': True,
                            },
                            'workspace_name': 'Sample Workspace',
                        },
                    },
                },
                {
                    "id": "688dc22c-12f1-49c8-8ab7-0c944a99d86b",
                    "type": "last_edited_by",
                    "last_edited_by": {
                        "object": "user",
                        "id": "9d99827c-d2b7-422d-99f4-5d6b9df02806",
                        "name": "Derek Hansen",
                        "avatar_url": "https://www.malone-gay.com/",
                        "type": "bot",
                        "bot": {
                            "owner": {"type": "workspace", "workspace": True},
                            "workspace_name": "Sample Workspace",
                        },
                    },
                },
            ),
        ),
        (
            LastEditedTimePropertyValue,
            (
                {
                    'id': '397bb2eb-053c-4333-ab68-7e43ce65771c',
                    'type': PropertyType.LAST_EDITED_TIME,
                    'last_edited_time': datetime(1976, 11, 18, 6, 43, 48, 217469),
                },
                {
                    'id': '397bb2eb-053c-4333-ab68-7e43ce65771c',
                    'type': PropertyType.LAST_EDITED_TIME,
                    'last_edited_time': datetime(1976, 11, 18, 6, 43, 48, 217469),
                },
                {
                    "id": "397bb2eb-053c-4333-ab68-7e43ce65771c",
                    "type": "last_edited_time",
                    "last_edited_time": "1976-11-18T06:43:48.217469",
                },
            ),
        ),
        (
            MultiSelectPropertyValue,
            (
                {
                    'id': None,
                    'type': PropertyType.MULTI_SELECT,
                    'multi_select': [
                        FullOptionValue(
                            id='2138475d-f976-4a7f-ab85-1b563d770e37',
                            name='Kaylee Carter',
                            color=Color.BROWN,
                        )
                    ],
                },
                {
                    'type': PropertyType.MULTI_SELECT,
                    'multi_select': [
                        {
                            'id': '2138475d-f976-4a7f-ab85-1b563d770e37',
                            'name': 'Kaylee Carter',
                            'color': Color.BROWN,
                        }
                    ],
                },
                {
                    "type": "multi_select",
                    "multi_select": [
                        {
                            "id": "2138475d-f976-4a7f-ab85-1b563d770e37",
                            "name": "Kaylee Carter",
                            "color": "brown",
                        }
                    ],
                },
            ),
        ),
        (
            NumberPropertyValue,
            (
                {
                    'id': 'c0d075d8-3f6e-40f2-9f0f-e8734a235ba6',
                    'type': PropertyType.NUMBER,
                    'number': 5994,
                },
                {
                    'id': 'c0d075d8-3f6e-40f2-9f0f-e8734a235ba6',
                    'type': PropertyType.NUMBER,
                    'number': 5994,
                },
                {
                    "id": "c0d075d8-3f6e-40f2-9f0f-e8734a235ba6",
                    "type": "number",
                    "number": 5994,
                },
            ),
        ),
        (
            PeoplePropertyValue,
            (
                {
                    'id': '13cd2792-5c03-42c2-91ac-f48a1cdb32f1',
                    'type': PropertyType.PEOPLE,
                    'people': [
                        UserRef(
                            object=NotionObjectType.USER,
                            id=UUID('93b6baf3-96eb-4e65-bfdd-09b594e0571f'),
                        )
                    ],
                },
                {
                    'id': '13cd2792-5c03-42c2-91ac-f48a1cdb32f1',
                    'type': PropertyType.PEOPLE,
                    'people': [
                        {
                            'object': NotionObjectType.USER,
                            'id': UUID('93b6baf3-96eb-4e65-bfdd-09b594e0571f'),
                        }
                    ],
                },
                {
                    "id": "13cd2792-5c03-42c2-91ac-f48a1cdb32f1",
                    "type": "people",
                    "people": [
                        {"object": "user", "id": "93b6baf3-96eb-4e65-bfdd-09b594e0571f"}
                    ],
                },
            ),
        ),
        (
            PhoneNumberPropertyValue,
            (
                {
                    'id': None,
                    'type': PropertyType.PHONE_NUMBER,
                    'phone_number': '960-460-9194',
                },
                {'type': PropertyType.PHONE_NUMBER, 'phone_number': '960-460-9194'},
                {"type": "phone_number", "phone_number": "960-460-9194"},
            ),
        ),
        (
            RelationPropertyValue,
            (
                {
                    'id': None,
                    'type': PropertyType.RELATION,
                    'relation': [
                        UUID('8dfc4ea5-1332-4e41-9965-e33631d26437'),
                        UUID('ef1afd52-74b7-4397-b126-fd5a67b387db'),
                    ],
                    'has_more': None,
                },
                {
                    'type': PropertyType.RELATION,
                    'relation': [
                        UUID('8dfc4ea5-1332-4e41-9965-e33631d26437'),
                        UUID('ef1afd52-74b7-4397-b126-fd5a67b387db'),
                    ],
                },
                {
                    "type": "relation",
                    "relation": [
                        "8dfc4ea5-1332-4e41-9965-e33631d26437",
                        "ef1afd52-74b7-4397-b126-fd5a67b387db",
                    ],
                },
            ),
        ),
        (
            RichTextPropertyValue,
            (
                {
                    'id': None,
                    'type': PropertyType.RICH_TEXT,
                    'rich_text': [
                        MentionRichText(
                            annotations=Annotations(
                                bold=None,
                                italic=None,
                                strikethrough=False,
                                underline=None,
                                code=True,
                                color=Color.DEFAULT,
                            ),
                            plain_text='Never deep court writer idea bank make.',
                            href='http://www.morris.com/',
                            type=RichTextType.MENTION,
                            mention=TemplateMention(
                                type=MentionType.TEMPLATE_MENTION,
                                template_mention=TemplateMentionDate(
                                    type=TemplateMentionType.TEMPLATE_MENTION_DATE,
                                    template_mention_date='now',
                                ),
                            ),
                        )
                    ],
                },
                {
                    'type': PropertyType.RICH_TEXT,
                    'rich_text': [
                        {
                            'annotations': {
                                'strikethrough': False,
                                'code': True,
                                'color': Color.DEFAULT,
                            },
                            'plain_text': 'Never deep court writer idea bank make.',
                            'href': 'http://www.morris.com/',
                            'type': RichTextType.MENTION,
                            'mention': {
                                'type': MentionType.TEMPLATE_MENTION,
                                'template_mention': {
                                    'type': TemplateMentionType.TEMPLATE_MENTION_DATE,
                                    'template_mention_date': 'now',
                                },
                            },
                        }
                    ],
                },
                {
                    "type": "rich_text",
                    "rich_text": [
                        {
                            "annotations": {
                                "strikethrough": False,
                                "code": True,
                                "color": "default",
                            },
                            "plain_text": "Never deep court writer idea bank make.",
                            "href": "http://www.morris.com/",
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
            ),
        ),
        (
            RollupPropertyValue,
            (
                {
                    'id': None,
                    'type': PropertyType.ROLLUP,
                    'rollup': DateRollupValue(type=RollupValueType.DATE, date=None),
                },
                {'type': PropertyType.ROLLUP, 'rollup': {'type': RollupValueType.DATE}},
                {"type": "rollup", "rollup": {"type": "date"}},
            ),
        ),
        (
            SelectPropertyValue,
            (
                {
                    'id': '2739f0bd-a1e9-4437-ad87-73acb7a2abec',
                    'type': PropertyType.SELECT,
                    'select': NameOnlyOptionValue(name='Michelle Kennedy'),
                },
                {
                    'id': '2739f0bd-a1e9-4437-ad87-73acb7a2abec',
                    'type': PropertyType.SELECT,
                    'select': {'name': 'Michelle Kennedy'},
                },
                {
                    "id": "2739f0bd-a1e9-4437-ad87-73acb7a2abec",
                    "type": "select",
                    "select": {"name": "Michelle Kennedy"},
                },
            ),
        ),
        (
            StatusPropertyValue,
            (
                {
                    'id': None,
                    'type': PropertyType.STATUS,
                    'status': IdOnlyOptionValue(
                        id='6bacdac4-9c52-4b9b-a0cc-f2084167bae2'
                    ),
                },
                {
                    'type': PropertyType.STATUS,
                    'status': {'id': '6bacdac4-9c52-4b9b-a0cc-f2084167bae2'},
                },
                {
                    "type": "status",
                    "status": {"id": "6bacdac4-9c52-4b9b-a0cc-f2084167bae2"},
                },
            ),
        ),
        (
            TitlePropertyValue,
            (
                {
                    'id': None,
                    'type': PropertyType.TITLE,
                    'title': [
                        TextRichText(
                            annotations=Annotations(
                                bold=None,
                                italic=None,
                                strikethrough=False,
                                underline=None,
                                code=True,
                                color=Color.DEFAULT,
                            ),
                            plain_text='Never deep court writer idea bank make.',
                            href='https://www.white.com/',
                            type=RichTextType.TEXT,
                            text=Text(
                                content='Head take understand move society.',
                                link=NotionUrlObject(url='http://smith.biz/'),
                            ),
                        ),
                        EquationRichText(
                            annotations=Annotations(
                                bold=None,
                                italic=None,
                                strikethrough=False,
                                underline=None,
                                code=True,
                                color=Color.DEFAULT,
                            ),
                            plain_text='Never deep court writer idea bank make.',
                            href='http://jackson.com/',
                            type=RichTextType.EQUATION,
                            equation=Equation(
                                expression='Company cover increase election. Word choice enter probably environment.\nModel environment vote test while as above. Someone maybe young while respond cell key. Mention after drug me father politics.'
                            ),
                        ),
                    ],
                },
                {
                    'type': PropertyType.TITLE,
                    'title': [
                        {
                            'annotations': {
                                'strikethrough': False,
                                'code': True,
                                'color': Color.DEFAULT,
                            },
                            'plain_text': 'Never deep court writer idea bank make.',
                            'href': 'https://www.white.com/',
                            'type': RichTextType.TEXT,
                            'text': {
                                'content': 'Head take understand move society.',
                                'link': {'url': 'http://smith.biz/'},
                            },
                        },
                        {
                            'annotations': {
                                'strikethrough': False,
                                'code': True,
                                'color': Color.DEFAULT,
                            },
                            'plain_text': 'Never deep court writer idea bank make.',
                            'href': 'http://jackson.com/',
                            'type': RichTextType.EQUATION,
                            'equation': {
                                'expression': 'Company cover increase election. Word choice enter probably environment.\nModel environment vote test while as above. Someone maybe young while respond cell key. Mention after drug me father politics.'
                            },
                        },
                    ],
                },
                {
                    "type": "title",
                    "title": [
                        {
                            "annotations": {
                                "strikethrough": False,
                                "code": True,
                                "color": "default",
                            },
                            "plain_text": "Never deep court writer idea bank make.",
                            "href": "https://www.white.com/",
                            "type": "text",
                            "text": {
                                "content": "Head take understand move society.",
                                "link": {"url": "http://smith.biz/"},
                            },
                        },
                        {
                            "annotations": {
                                "strikethrough": False,
                                "code": True,
                                "color": "default",
                            },
                            "plain_text": "Never deep court writer idea bank make.",
                            "href": "http://jackson.com/",
                            "type": "equation",
                            "equation": {
                                "expression": "Company cover increase election. Word choice enter probably environment.\nModel environment vote test while as above. Someone maybe young while respond cell key. Mention after drug me father politics."
                            },
                        },
                    ],
                },
            ),
        ),
        (
            UrlPropertyValue,
            (
                {'id': None, 'type': PropertyType.URL, 'url': 'https://www.ellis.net/'},
                {'type': PropertyType.URL, 'url': 'https://www.ellis.net/'},
                {"type": "url", "url": "https://www.ellis.net/"},
            ),
        ),
        (
            UniqueIdPropertyValue,
            (
                {
                    'id': 'e3dc3147-b5f1-43fd-b8ae-a3adfd8a9335',
                    'type': PropertyType.UNIQUE_ID,
                    'unique_id': UniqueIdValue(
                        number=8087, prefix='clapFvQjxjmzfVmuNrDi'
                    ),
                },
                {
                    'id': 'e3dc3147-b5f1-43fd-b8ae-a3adfd8a9335',
                    'type': PropertyType.UNIQUE_ID,
                    'unique_id': {'number': 8087, 'prefix': 'clapFvQjxjmzfVmuNrDi'},
                },
                {
                    "id": "e3dc3147-b5f1-43fd-b8ae-a3adfd8a9335",
                    "type": "unique_id",
                    "unique_id": {"number": 8087, "prefix": "clapFvQjxjmzfVmuNrDi"},
                },
            ),
        ),
        (
            VerificationPropertyValue,
            (
                {
                    'id': None,
                    'type': PropertyType.VERIFICATION,
                    'verification': UnverifiedValue(
                        state='unverified', verified_by=None, date=None
                    ),
                },
                {
                    'type': PropertyType.VERIFICATION,
                    'verification': {'state': 'unverified'},
                },
                {"type": "verification", "verification": {"state": "unverified"}},
            ),
        ),
    ],
)
def test_property_value_models_serialization(
    clz: type[BaseModel], test_data: tuple[dict, dict, dict]
):
    PydanticModelTester(clz, test_data).run_all_tests()
