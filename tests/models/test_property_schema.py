from uuid import UUID

import pytest
from pydantic import BaseModel

from pynotion.models.properties.property_schema import *
from pynotion.models.rich_text import *
from tests.models.model_test_utils import DiscriminatedModelTester, PydanticModelTester


@pytest.mark.parametrize(
    "annotated_clz, expected_clz, input_data",
    [
        (
            RxPropertySchema,
            RxCheckboxPropertySchema,
            {
                "id": "00f8b116-129d-464a-90b1-bf366895c807",
                "name": "Jennifer Scott",
                "type": "checkbox",
                "checkbox": {},
            },
        ),
        (
            RxPropertySchema,
            RxCreatedByPropertySchema,
            {
                "id": "b255ecd1-8613-4cbe-a59d-f54026161089",
                "name": "Mary Collins",
                "type": "created_by",
                "created_by": {},
            },
        ),
        (
            RxPropertySchema,
            RxCreatedTimePropertySchema,
            {
                "id": "9258d317-319a-455a-be4d-410515a74abb",
                "name": "Gregory Mills",
                "type": "created_time",
                "created_time": {},
            },
        ),
        (
            RxPropertySchema,
            RxDatePropertySchema,
            {
                "id": "e384cdea-08ab-4069-86e1-bcbf50a69d15",
                "name": "Andrew Jones",
                "type": "date",
                "date": {},
            },
        ),
        (
            RxPropertySchema,
            RxEmailPropertySchema,
            {
                "id": "47095820-9ee8-475f-a52d-2600a54e2ab0",
                "name": "Melinda Lewis",
                "type": "email",
                "email": {},
            },
        ),
        (
            RxPropertySchema,
            RxFilesPropertySchema,
            {
                "id": "d94ac29a-3c9a-4275-9562-4be646ac21a5",
                "name": "Jared Baldwin",
                "type": "files",
                "files": {},
            },
        ),
        (
            RxPropertySchema,
            RxFormulaPropertySchema,
            {
                "id": "64d01177-21b6-4b56-9081-66d1b0d3cc0e",
                "name": "Daisy Torres",
                "type": "formula",
                "formula": {"expression": "yNNAhzyidWzaBWEDtIte"},
            },
        ),
        (
            RxPropertySchema,
            RxLastEditedByPropertySchema,
            {
                "id": "f35e4bd5-8efa-4552-8fca-b64bf47627be",
                "name": "Debbie Ferrell",
                "type": "last_edited_by",
                "last_edited_by": {},
            },
        ),
        (
            RxPropertySchema,
            RxLastEditedTimePropertySchema,
            {
                "id": "baef7d3e-e049-4222-817d-c21b69249120",
                "name": "Juan Lopez",
                "type": "last_edited_time",
                "last_edited_time": {},
            },
        ),
        (
            RxPropertySchema,
            RxMultiSelectPropertySchema,
            {
                "id": "7a9ca922-a2a1-4d78-a590-9b25c4f0d0f4",
                "name": "Andrew Williams",
                "type": "multi_select",
                "multi_select": {
                    "options": [
                        {
                            "id": "f1e8608a-77f2-40b3-861a-6753c87aab21",
                            "name": "Jake Garcia",
                            "color": "yellow",
                        }
                    ]
                },
            },
        ),
        (
            RxPropertySchema,
            RxNumberPropertySchema,
            {
                "id": "4c69752e-ffa3-46bf-9cbc-6dfa61b56e74",
                "name": "Andrew Reyes",
                "type": "number",
                "number": {"format": "uruguayan_peso"},
            },
        ),
        (
            RxPropertySchema,
            RxPeoplePropertySchema,
            {
                "id": "de58137e-cb92-4b83-90d4-a7a3b0b6c3e1",
                "name": "Steven Robinson",
                "type": "people",
                "people": {},
            },
        ),
        (
            RxPropertySchema,
            RxPhoneNumberPropertySchema,
            {
                "id": "fed3aa8e-c187-4b31-83a2-333b40a98c18",
                "name": "Kenneth Brown",
                "type": "phone_number",
                "phone_number": {},
            },
        ),
        (
            RxPropertySchema,
            RxRelationPropertySchema,
            {
                "id": "00136949-c579-4139-a59c-5c316b29f1b7",
                "name": "Steven Gonzalez",
                "type": "relation",
                "relation": {
                    "database_id": "ad618acb-88bb-4e89-a00a-80835858907c",
                    "dual_property": {},
                },
            },
        ),
        (
            RxPropertySchema,
            RxRichTextPropertySchema,
            {
                "id": "52e86395-e52c-41ac-916c-8dfac1fa901d",
                "name": "Zachary Adams",
                "type": "rich_text",
                "rich_text": {},
            },
        ),
        (
            RxPropertySchema,
            RxRollupPropertySchema,
            {
                "id": "6b86bd4e-9cf0-4aac-b99c-0a51eaf95fbb",
                "name": "Jean Greer",
                "type": "rollup",
                "rollup": {
                    "relation_property_id": "79f7b396-cb8d-43d9-a5ed-90fe86256ab7",
                    "rollup_property_id": "6ba870a1-fa8a-4fe7-81c1-404cf3ab3bdf",
                    "relation_property_name": "Kaitlyn Johnson",
                    "rollup_property_name": "Meredith Castro",
                    "function": "count_values",
                },
            },
        ),
        (
            RxPropertySchema,
            RxSelectPropertySchema,
            {
                "id": "883c3574-6c76-4cf8-bef4-d0bc0ae532d6",
                "name": "Trevor Serrano",
                "type": "select",
                "select": {
                    "options": [
                        {
                            "id": "f1e8608a-77f2-40b3-861a-6753c87aab21",
                            "name": "Jake Garcia",
                            "color": "yellow",
                        }
                    ]
                },
            },
        ),
        (
            RxPropertySchema,
            RxTitlePropertySchema,
            {
                "id": "cc358a81-d604-4c0b-9fd9-ca50256913f7",
                "name": "Lacey Ryan DDS",
                "type": "title",
                "title": {},
            },
        ),
        (
            RxPropertySchema,
            RxUrlPropertySchema,
            {
                "id": "53d6ac87-a7ef-4f0a-a451-3609187b3ce9",
                "name": "Joan Lutz",
                "type": "url",
                "url": {},
            },
        ),
    ],
)
def test_rx_property_schema_discriminated_model(
    annotated_clz: type, expected_clz: type, input_data: dict
):
    DiscriminatedModelTester(annotated_clz, expected_clz, **input_data).run_all_tests()


@pytest.mark.parametrize(
    "clz, test_data",
    [
        (
            RxCheckboxPropertySchema,
            (
                {
                    'id': 'd5b0494c-e936-4304-9e9e-80b137143096',
                    'name': 'Michael Nelson',
                    'type': PropertyType.CHECKBOX,
                    'checkbox': {},
                },
                {
                    'id': 'd5b0494c-e936-4304-9e9e-80b137143096',
                    'name': 'Michael Nelson',
                    'type': PropertyType.CHECKBOX,
                    'checkbox': {},
                },
                {
                    "id": "d5b0494c-e936-4304-9e9e-80b137143096",
                    "name": "Michael Nelson",
                    "type": "checkbox",
                    "checkbox": {},
                },
            ),
        ),
        (
            RxCreatedByPropertySchema,
            (
                {
                    'id': 'b6d26b98-70ea-4c6d-8876-c43c368b8a27',
                    'name': 'Megan Williams',
                    'type': PropertyType.CREATED_BY,
                    'created_by': {},
                },
                {
                    'id': 'b6d26b98-70ea-4c6d-8876-c43c368b8a27',
                    'name': 'Megan Williams',
                    'type': PropertyType.CREATED_BY,
                    'created_by': {},
                },
                {
                    "id": "b6d26b98-70ea-4c6d-8876-c43c368b8a27",
                    "name": "Megan Williams",
                    "type": "created_by",
                    "created_by": {},
                },
            ),
        ),
        (
            RxCreatedTimePropertySchema,
            (
                {
                    'id': 'f8b03f21-e0d3-45b6-a971-ddd5bdd7f4cd',
                    'name': 'Karen Simmons',
                    'type': PropertyType.CREATED_TIME,
                    'created_time': {},
                },
                {
                    'id': 'f8b03f21-e0d3-45b6-a971-ddd5bdd7f4cd',
                    'name': 'Karen Simmons',
                    'type': PropertyType.CREATED_TIME,
                    'created_time': {},
                },
                {
                    "id": "f8b03f21-e0d3-45b6-a971-ddd5bdd7f4cd",
                    "name": "Karen Simmons",
                    "type": "created_time",
                    "created_time": {},
                },
            ),
        ),
        (
            RxDatePropertySchema,
            (
                {
                    'id': '41ec58ae-5f6b-447b-b169-0a227007c39d',
                    'name': 'Sarah Madden',
                    'type': PropertyType.DATE,
                    'date': {},
                },
                {
                    'id': '41ec58ae-5f6b-447b-b169-0a227007c39d',
                    'name': 'Sarah Madden',
                    'type': PropertyType.DATE,
                    'date': {},
                },
                {
                    "id": "41ec58ae-5f6b-447b-b169-0a227007c39d",
                    "name": "Sarah Madden",
                    "type": "date",
                    "date": {},
                },
            ),
        ),
        (
            RxEmailPropertySchema,
            (
                {
                    'id': '482dfea4-a29b-40e1-ae72-ec25c725a305',
                    'name': 'Gloria Bentley',
                    'type': PropertyType.EMAIL,
                    'email': {},
                },
                {
                    'id': '482dfea4-a29b-40e1-ae72-ec25c725a305',
                    'name': 'Gloria Bentley',
                    'type': PropertyType.EMAIL,
                    'email': {},
                },
                {
                    "id": "482dfea4-a29b-40e1-ae72-ec25c725a305",
                    "name": "Gloria Bentley",
                    "type": "email",
                    "email": {},
                },
            ),
        ),
        (
            RxFilesPropertySchema,
            (
                {
                    'id': '7ecac2df-d02a-4b09-a391-830f8865ec82',
                    'name': 'Joseph Rojas',
                    'type': PropertyType.FILES,
                    'files': {},
                },
                {
                    'id': '7ecac2df-d02a-4b09-a391-830f8865ec82',
                    'name': 'Joseph Rojas',
                    'type': PropertyType.FILES,
                    'files': {},
                },
                {
                    "id": "7ecac2df-d02a-4b09-a391-830f8865ec82",
                    "name": "Joseph Rojas",
                    "type": "files",
                    "files": {},
                },
            ),
        ),
        (
            RxFormulaPropertySchema,
            (
                {
                    'id': '26004f3b-a345-47da-a736-d52ed24b284d',
                    'name': 'Mark Nicholson',
                    'type': PropertyType.FORMULA,
                    'formula': NotionEquation(expression='IgDkpAFCnzPtwfPQYpsU'),
                },
                {
                    'id': '26004f3b-a345-47da-a736-d52ed24b284d',
                    'name': 'Mark Nicholson',
                    'type': PropertyType.FORMULA,
                    'formula': {'expression': 'IgDkpAFCnzPtwfPQYpsU'},
                },
                {
                    "id": "26004f3b-a345-47da-a736-d52ed24b284d",
                    "name": "Mark Nicholson",
                    "type": "formula",
                    "formula": {"expression": "IgDkpAFCnzPtwfPQYpsU"},
                },
            ),
        ),
        (
            RxLastEditedByPropertySchema,
            (
                {
                    'id': 'dd9e06b4-ceca-4d3c-91b0-5592dc0589e4',
                    'name': 'Maria Allen',
                    'type': PropertyType.LAST_EDITED_BY,
                    'last_edited_by': {},
                },
                {
                    'id': 'dd9e06b4-ceca-4d3c-91b0-5592dc0589e4',
                    'name': 'Maria Allen',
                    'type': PropertyType.LAST_EDITED_BY,
                    'last_edited_by': {},
                },
                {
                    "id": "dd9e06b4-ceca-4d3c-91b0-5592dc0589e4",
                    "name": "Maria Allen",
                    "type": "last_edited_by",
                    "last_edited_by": {},
                },
            ),
        ),
        (
            RxLastEditedTimePropertySchema,
            (
                {
                    'id': '3a3e9661-ab9b-4c33-b767-4d45b9249153',
                    'name': 'Dwayne Mendez',
                    'type': PropertyType.LAST_EDITED_TIME,
                    'last_edited_time': {},
                },
                {
                    'id': '3a3e9661-ab9b-4c33-b767-4d45b9249153',
                    'name': 'Dwayne Mendez',
                    'type': PropertyType.LAST_EDITED_TIME,
                    'last_edited_time': {},
                },
                {
                    "id": "3a3e9661-ab9b-4c33-b767-4d45b9249153",
                    "name": "Dwayne Mendez",
                    "type": "last_edited_time",
                    "last_edited_time": {},
                },
            ),
        ),
        (
            RxMultiSelectPropertySchema,
            (
                {
                    'id': '108e1c1b-52c8-4314-9e37-76a7db2db69e',
                    'name': 'Mary Jordan',
                    'type': PropertyType.MULTI_SELECT,
                    'multi_select': RxSelectOptionsSchema(
                        options=[
                            RxBaseOptionSchema(
                                id='f1e8608a-77f2-40b3-861a-6753c87aab21',
                                name='Jake Garcia',
                                color=Color.YELLOW,
                            )
                        ]
                    ),
                },
                {
                    'id': '108e1c1b-52c8-4314-9e37-76a7db2db69e',
                    'name': 'Mary Jordan',
                    'type': PropertyType.MULTI_SELECT,
                    'multi_select': {
                        'options': [
                            {
                                'id': 'f1e8608a-77f2-40b3-861a-6753c87aab21',
                                'name': 'Jake Garcia',
                                'color': Color.YELLOW,
                            }
                        ]
                    },
                },
                {
                    "id": "108e1c1b-52c8-4314-9e37-76a7db2db69e",
                    "name": "Mary Jordan",
                    "type": "multi_select",
                    "multi_select": {
                        "options": [
                            {
                                "id": "f1e8608a-77f2-40b3-861a-6753c87aab21",
                                "name": "Jake Garcia",
                                "color": "yellow",
                            }
                        ]
                    },
                },
            ),
        ),
        (
            RxNumberPropertySchema,
            (
                {
                    'id': '0536b4e0-6aff-4947-9c10-9c73cfac2e66',
                    'name': 'Casey Kennedy',
                    'type': PropertyType.NUMBER,
                    'number': NumberSchema(format=NumberFormat.BAHT),
                },
                {
                    'id': '0536b4e0-6aff-4947-9c10-9c73cfac2e66',
                    'name': 'Casey Kennedy',
                    'type': PropertyType.NUMBER,
                    'number': {'format': NumberFormat.BAHT},
                },
                {
                    "id": "0536b4e0-6aff-4947-9c10-9c73cfac2e66",
                    "name": "Casey Kennedy",
                    "type": "number",
                    "number": {"format": "baht"},
                },
            ),
        ),
        (
            RxPeoplePropertySchema,
            (
                {
                    'id': '5180b2dc-da64-4aea-b67b-f9a4eccd78f0',
                    'name': 'Kevin Moss',
                    'type': PropertyType.PEOPLE,
                    'people': {},
                },
                {
                    'id': '5180b2dc-da64-4aea-b67b-f9a4eccd78f0',
                    'name': 'Kevin Moss',
                    'type': PropertyType.PEOPLE,
                    'people': {},
                },
                {
                    "id": "5180b2dc-da64-4aea-b67b-f9a4eccd78f0",
                    "name": "Kevin Moss",
                    "type": "people",
                    "people": {},
                },
            ),
        ),
        (
            RxPhoneNumberPropertySchema,
            (
                {
                    'id': 'b5dee75d-cde3-46b9-893e-b132c3263387',
                    'name': 'Lauren Bautista',
                    'type': PropertyType.PHONE_NUMBER,
                    'phone_number': {},
                },
                {
                    'id': 'b5dee75d-cde3-46b9-893e-b132c3263387',
                    'name': 'Lauren Bautista',
                    'type': PropertyType.PHONE_NUMBER,
                    'phone_number': {},
                },
                {
                    "id": "b5dee75d-cde3-46b9-893e-b132c3263387",
                    "name": "Lauren Bautista",
                    "type": "phone_number",
                    "phone_number": {},
                },
            ),
        ),
        (
            RxRelationPropertySchema,
            (
                {
                    'id': '44277101-f35e-4123-90f1-bc8122046a02',
                    'name': 'Anne Chavez',
                    'type': PropertyType.RELATION,
                    'relation': DualRelationSchema(
                        database_id=UUID('a722d1f6-a61a-4832-b1d3-304956ae48a3'),
                        dual_property={},
                    ),
                },
                {
                    'id': '44277101-f35e-4123-90f1-bc8122046a02',
                    'name': 'Anne Chavez',
                    'type': PropertyType.RELATION,
                    'relation': {
                        'database_id': UUID('a722d1f6-a61a-4832-b1d3-304956ae48a3'),
                        'dual_property': {},
                    },
                },
                {
                    "id": "44277101-f35e-4123-90f1-bc8122046a02",
                    "name": "Anne Chavez",
                    "type": "relation",
                    "relation": {
                        "database_id": "a722d1f6-a61a-4832-b1d3-304956ae48a3",
                        "dual_property": {},
                    },
                },
            ),
        ),
        (
            RxRichTextPropertySchema,
            (
                {
                    'id': '6806842c-fd86-4304-a5f0-d8daeda3e6cb',
                    'name': 'Jordan Mcbride',
                    'type': PropertyType.RICH_TEXT,
                    'rich_text': {},
                },
                {
                    'id': '6806842c-fd86-4304-a5f0-d8daeda3e6cb',
                    'name': 'Jordan Mcbride',
                    'type': PropertyType.RICH_TEXT,
                    'rich_text': {},
                },
                {
                    "id": "6806842c-fd86-4304-a5f0-d8daeda3e6cb",
                    "name": "Jordan Mcbride",
                    "type": "rich_text",
                    "rich_text": {},
                },
            ),
        ),
        (
            RxRollupPropertySchema,
            (
                {
                    'id': 'e1795266-4410-43b9-a3af-46aceb8257ef',
                    'name': 'James Yu',
                    'type': PropertyType.ROLLUP,
                    'rollup': RxRollupSchema(
                        relation_property_id='e7fe9d1f-462d-4daf-96c0-71915d0c56b1',
                        rollup_property_id='70f79e9c-b80a-4242-b61a-a11f95f06d87',
                        relation_property_name='Jordan Rhodes',
                        rollup_property_name='Amy Howard',
                        function=RollupFunction.SHOW_ORIGINAL,
                    ),
                },
                {
                    'id': 'e1795266-4410-43b9-a3af-46aceb8257ef',
                    'name': 'James Yu',
                    'type': PropertyType.ROLLUP,
                    'rollup': {
                        'relation_property_id': 'e7fe9d1f-462d-4daf-96c0-71915d0c56b1',
                        'rollup_property_id': '70f79e9c-b80a-4242-b61a-a11f95f06d87',
                        'relation_property_name': 'Jordan Rhodes',
                        'rollup_property_name': 'Amy Howard',
                        'function': RollupFunction.SHOW_ORIGINAL,
                    },
                },
                {
                    "id": "e1795266-4410-43b9-a3af-46aceb8257ef",
                    "name": "James Yu",
                    "type": "rollup",
                    "rollup": {
                        "relation_property_id": "e7fe9d1f-462d-4daf-96c0-71915d0c56b1",
                        "rollup_property_id": "70f79e9c-b80a-4242-b61a-a11f95f06d87",
                        "relation_property_name": "Jordan Rhodes",
                        "rollup_property_name": "Amy Howard",
                        "function": "show_original",
                    },
                },
            ),
        ),
        (
            RxSelectPropertySchema,
            (
                {
                    'id': '5ea88a73-0e94-4efa-a95a-ff052ac9c2a8',
                    'name': 'Sara Powell',
                    'type': PropertyType.SELECT,
                    'select': RxSelectOptionsSchema(
                        options=[
                            RxBaseOptionSchema(
                                id='f1e8608a-77f2-40b3-861a-6753c87aab21',
                                name='Jake Garcia',
                                color=Color.YELLOW,
                            )
                        ]
                    ),
                },
                {
                    'id': '5ea88a73-0e94-4efa-a95a-ff052ac9c2a8',
                    'name': 'Sara Powell',
                    'type': PropertyType.SELECT,
                    'select': {
                        'options': [
                            {
                                'id': 'f1e8608a-77f2-40b3-861a-6753c87aab21',
                                'name': 'Jake Garcia',
                                'color': Color.YELLOW,
                            }
                        ]
                    },
                },
                {
                    "id": "5ea88a73-0e94-4efa-a95a-ff052ac9c2a8",
                    "name": "Sara Powell",
                    "type": "select",
                    "select": {
                        "options": [
                            {
                                "id": "f1e8608a-77f2-40b3-861a-6753c87aab21",
                                "name": "Jake Garcia",
                                "color": "yellow",
                            }
                        ]
                    },
                },
            ),
        ),
        (
            RxTitlePropertySchema,
            (
                {
                    'id': '4a934a0e-ba7c-40b2-84f2-42ad4e175862',
                    'name': 'Jill Mason',
                    'type': PropertyType.TITLE,
                    'title': {},
                },
                {
                    'id': '4a934a0e-ba7c-40b2-84f2-42ad4e175862',
                    'name': 'Jill Mason',
                    'type': PropertyType.TITLE,
                    'title': {},
                },
                {
                    "id": "4a934a0e-ba7c-40b2-84f2-42ad4e175862",
                    "name": "Jill Mason",
                    "type": "title",
                    "title": {},
                },
            ),
        ),
        (
            RxUrlPropertySchema,
            (
                {
                    'id': '6e91e1e5-1f37-4bc6-9f8d-abbaac629000',
                    'name': 'Mr. Matthew Jones',
                    'type': PropertyType.URL,
                    'url': {},
                },
                {
                    'id': '6e91e1e5-1f37-4bc6-9f8d-abbaac629000',
                    'name': 'Mr. Matthew Jones',
                    'type': PropertyType.URL,
                    'url': {},
                },
                {
                    "id": "6e91e1e5-1f37-4bc6-9f8d-abbaac629000",
                    "name": "Mr. Matthew Jones",
                    "type": "url",
                    "url": {},
                },
            ),
        ),
    ],
)
def test_rx_property_schema_models_serialization(
    clz: type[BaseModel], test_data: tuple[dict, dict, dict]
):
    PydanticModelTester(clz, test_data).run_all_tests()


@pytest.mark.parametrize(
    "annotated_clz, expected_clz, input_data",
    [
        (
            TxPropertySchema,
            TxCheckboxPropertySchema,
            {"checkbox": {}},
        ),
        (
            TxPropertySchema,
            TxCreatedByPropertySchema,
            {"created_by": {}},
        ),
        (
            TxPropertySchema,
            TxCreatedTimePropertySchema,
            {"created_time": {}},
        ),
        (
            TxPropertySchema,
            TxDatePropertySchema,
            {"date": {}},
        ),
        (
            TxPropertySchema,
            TxEmailPropertySchema,
            {"email": {}},
        ),
        (
            TxPropertySchema,
            TxFilesPropertySchema,
            {"files": {}},
        ),
        (
            TxPropertySchema,
            TxFormulaPropertySchema,
            {"formula": {"expression": "qrYXDTvTFoIHjopNkIuL"}},
        ),
        (
            TxPropertySchema,
            TxLastEditedByPropertySchema,
            {"last_edited_by": {}},
        ),
        (
            TxPropertySchema,
            TxLastEditedTimePropertySchema,
            {"last_edited_time": {}},
        ),
        (
            TxPropertySchema,
            TxMultiSelectPropertySchema,
            {
                "multi_select": {
                    "options": [{"name": "Michael Collins", "color": "pink"}]
                }
            },
        ),
        (
            TxPropertySchema,
            TxNumberPropertySchema,
            {"number": {"format": "new_zealand_dollar"}},
        ),
        (
            TxPropertySchema,
            TxPeoplePropertySchema,
            {"people": {}},
        ),
        (
            TxPropertySchema,
            TxPhoneNumberPropertySchema,
            {"phone_number": {}},
        ),
        (
            TxPropertySchema,
            TxRelationPropertySchema,
            {
                "relation": {
                    "database_id": "47c20530-e732-4a30-829e-f00f512b4bd0",
                    "single_property": {},
                }
            },
        ),
        (
            TxPropertySchema,
            TxRichTextPropertySchema,
            {"rich_text": {}},
        ),
        (
            TxPropertySchema,
            TxRollupPropertySchema,
            {
                "rollup": {
                    "relation_property_name": "Craig Perkins",
                    "rollup_property_name": "David Smith",
                    "function": "show_unique",
                }
            },
        ),
        (
            TxPropertySchema,
            TxSelectPropertySchema,
            {"select": {"options": [{"name": "Michael Collins", "color": "pink"}]}},
        ),
        (
            TxPropertySchema,
            TxTitlePropertySchema,
            {"title": {}},
        ),
        (
            TxPropertySchema,
            TxUrlPropertySchema,
            {"url": {}},
        ),
    ],
)
def test_tx_property_schema_discriminated_model(
    annotated_clz: type, expected_clz: type, input_data: dict
):
    DiscriminatedModelTester(annotated_clz, expected_clz, **input_data).run_all_tests()


@pytest.mark.parametrize(
    "clz, test_data",
    [
        (
            TxCheckboxPropertySchema,
            ({'checkbox': {}}, {'checkbox': {}}, {"checkbox": {}}),
        ),
        (
            TxCreatedByPropertySchema,
            ({'created_by': {}}, {'created_by': {}}, {"created_by": {}}),
        ),
        (
            TxCreatedTimePropertySchema,
            ({'created_time': {}}, {'created_time': {}}, {"created_time": {}}),
        ),
        (
            TxDatePropertySchema,
            ({'date': {}}, {'date': {}}, {"date": {}}),
        ),
        (
            TxEmailPropertySchema,
            ({'email': {}}, {'email': {}}, {"email": {}}),
        ),
        (
            TxFilesPropertySchema,
            ({'files': {}}, {'files': {}}, {"files": {}}),
        ),
        (
            TxFormulaPropertySchema,
            (
                {'formula': NotionEquation(expression='GOiShXcLdCSStyOrcXlv')},
                {'formula': {'expression': 'GOiShXcLdCSStyOrcXlv'}},
                {"formula": {"expression": "GOiShXcLdCSStyOrcXlv"}},
            ),
        ),
        (
            TxLastEditedByPropertySchema,
            ({'last_edited_by': {}}, {'last_edited_by': {}}, {"last_edited_by": {}}),
        ),
        (
            TxLastEditedTimePropertySchema,
            (
                {'last_edited_time': {}},
                {'last_edited_time': {}},
                {"last_edited_time": {}},
            ),
        ),
        (
            TxMultiSelectPropertySchema,
            (
                {
                    'multi_select': TxSelectOptionsSchema(
                        options=[
                            TxBaseOptionSchema(name='Michael Collins', color=Color.PINK)
                        ]
                    )
                },
                {
                    'multi_select': {
                        'options': [{'name': 'Michael Collins', 'color': Color.PINK}]
                    }
                },
                {
                    "multi_select": {
                        "options": [{"name": "Michael Collins", "color": "pink"}]
                    }
                },
            ),
        ),
        (
            TxNumberPropertySchema,
            (
                {'number': NumberSchema(format=NumberFormat.NEW_ZEALAND_DOLLAR)},
                {'number': {'format': NumberFormat.NEW_ZEALAND_DOLLAR}},
                {"number": {"format": "new_zealand_dollar"}},
            ),
        ),
        (
            TxPeoplePropertySchema,
            ({'people': {}}, {'people': {}}, {"people": {}}),
        ),
        (
            TxPhoneNumberPropertySchema,
            ({'phone_number': {}}, {'phone_number': {}}, {"phone_number": {}}),
        ),
        (
            TxRelationPropertySchema,
            (
                {
                    'relation': DualRelationSchema(
                        database_id=UUID('770eeb8f-b434-4a1e-a020-a61792246ade'),
                        dual_property={},
                    )
                },
                {
                    'relation': {
                        'database_id': UUID('770eeb8f-b434-4a1e-a020-a61792246ade'),
                        'dual_property': {},
                    }
                },
                {
                    "relation": {
                        "database_id": "770eeb8f-b434-4a1e-a020-a61792246ade",
                        "dual_property": {},
                    }
                },
            ),
        ),
        (
            TxRichTextPropertySchema,
            ({'rich_text': {}}, {'rich_text': {}}, {"rich_text": {}}),
        ),
        (
            TxRollupPropertySchema,
            (
                {
                    'rollup': TxRollupSchema(
                        relation_property_name='Jennifer Diaz',
                        rollup_property_name='David Reyes',
                        function=RollupFunction.MEDIAN,
                    )
                },
                {
                    'rollup': {
                        'relation_property_name': 'Jennifer Diaz',
                        'rollup_property_name': 'David Reyes',
                        'function': RollupFunction.MEDIAN,
                    }
                },
                {
                    "rollup": {
                        "relation_property_name": "Jennifer Diaz",
                        "rollup_property_name": "David Reyes",
                        "function": "median",
                    }
                },
            ),
        ),
        (
            TxSelectPropertySchema,
            (
                {
                    'select': TxSelectOptionsSchema(
                        options=[
                            TxBaseOptionSchema(name='Michael Collins', color=Color.PINK)
                        ]
                    )
                },
                {
                    'select': {
                        'options': [{'name': 'Michael Collins', 'color': Color.PINK}]
                    }
                },
                {"select": {"options": [{"name": "Michael Collins", "color": "pink"}]}},
            ),
        ),
        (
            TxTitlePropertySchema,
            ({'title': {}}, {'title': {}}, {"title": {}}),
        ),
        (
            TxUrlPropertySchema,
            ({'url': {}}, {'url': {}}, {"url": {}}),
        ),
    ],
)
def test_tx_property_schema_models_serialization(
    clz: type[BaseModel], test_data: tuple[dict, dict, dict]
):
    PydanticModelTester(clz, test_data).run_all_tests()
