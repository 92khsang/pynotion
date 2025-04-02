from uuid import UUID

import pytest
from pydantic import BaseModel

from pynotion.models import *
from tests.models.model_test_utils import DiscriminatedModelTester, PydanticModelTester


@pytest.mark.parametrize(
    "annotated_clz, expected_clz, input_data",
    [
        (
            Property,
            CheckboxProperty,
            {
                "id": "0c54a698-4dee-4fa2-bb67-b87f6ebdd203",
                "name": "Casey Chavez",
                "type": "checkbox",
                "checkbox": {},
            },
        ),
        (
            Property,
            CreatedByProperty,
            {
                "id": "cb8133ac-45fa-4d84-a758-aec3a420ea06",
                "name": "Bryan Williams",
                "type": "created_by",
                "created_by": {},
            },
        ),
        (
            Property,
            CreatedTimeProperty,
            {
                "id": "9e1332ce-a10c-4ff9-bfea-72163212f646",
                "name": "Laura Higgins",
                "type": "created_time",
                "created_time": {},
            },
        ),
        (
            Property,
            DateProperty,
            {
                "id": "f08b94c5-9815-4d9e-b134-aa0d95bde8e4",
                "name": "Tracy Reyes",
                "type": "date",
                "date": {},
            },
        ),
        (
            Property,
            EmailProperty,
            {
                "id": "10dd014b-d970-4af5-93b2-16f4b5145e6a",
                "name": "Christian Wallace",
                "type": "email",
                "email": {},
            },
        ),
        (
            Property,
            FilesProperty,
            {
                "id": "76fad98a-c9e0-4896-90a8-cfd019dca482",
                "name": "Lisa Lewis",
                "type": "files",
                "files": {},
            },
        ),
        (
            Property,
            FormulaProperty,
            {
                "id": "7bc73e86-898b-400a-9db9-cc36e9536f20",
                "name": "Kelly Miller",
                "type": "formula",
                "formula": {"expression": "PYWnWJwrEOWuLkEqsQZt"},
            },
        ),
        (
            Property,
            LastEditedByProperty,
            {
                "id": "80f22bb4-dfbd-4c82-bfdd-ec11d7f67111",
                "name": "Bradley Brock",
                "type": "last_edited_by",
                "last_edited_by": {},
            },
        ),
        (
            Property,
            LastEditedTimeProperty,
            {
                "id": "c73cadef-02d7-48d4-a4c1-d068cf788238",
                "name": "Robert Buchanan",
                "type": "last_edited_time",
                "last_edited_time": {},
            },
        ),
        (
            Property,
            MultiSelectProperty,
            {
                "id": "81d12707-8258-4d07-9078-ac5eb08b9c8e",
                "name": "Angela Nielsen DDS",
                "type": "multi_select",
                "multi_select": {
                    "options": [
                        {
                            "id": "be1ba75b-e9c6-48fe-8124-1ad682c19883",
                            "name": "Steven Harvey",
                            "color": "yellow",
                        },
                        {
                            "id": "d36596d7-16a9-4b4b-aa1d-1a87fb480ebf",
                            "name": "Robert Thomas",
                            "color": "yellow",
                        },
                    ]
                },
            },
        ),
        (
            Property,
            PeopleProperty,
            {
                "id": "534423ef-1855-4da8-98a6-32dc0f29d958",
                "name": "Katherine Gill",
                "type": "people",
                "people": {},
            },
        ),
        (
            Property,
            PhoneNumberProperty,
            {
                "id": "5520c0d4-1845-44de-ac5a-bc087e59fc19",
                "name": "Veronica Valdez",
                "type": "phone_number",
                "phone_number": {},
            },
        ),
        (
            Property,
            RelationProperty,
            {
                "id": "59a5c8fa-171c-4741-ac82-f4b705783a70",
                "name": "Andrea Crosby",
                "type": "relation",
                "relation": {
                    "database_id": "a3ff7b89-b871-4000-8fd8-0d10c638049e",
                    "dual_property": {
                        "synced_property_id": "JpPfilfNdRldmYZqtcIL",
                        "synced_property_name": "olgUEBzQNJXNTolmQwIg",
                    },
                },
            },
        ),
        (
            Property,
            RichTextProperty,
            {
                "id": "812f27f5-8808-452d-a160-f478e4e9f1f7",
                "name": "Priscilla Hanson",
                "type": "rich_text",
                "rich_text": {},
            },
        ),
        (
            Property,
            RollupProperty,
            {
                "id": "9eff3992-5e61-4cc3-8d4c-b96b54f2c09b",
                "name": "Gary Austin",
                "type": "rollup",
                "rollup": {
                    "relation_property_id": "ce32341c-4f95-4d83-905c-f91a2479080e",
                    "rollup_property_id": "8cffa6b7-29cc-4cb5-a7ae-9033b03721af",
                    "relation_property_name": "Brooke Coffey",
                    "rollup_property_name": "Sandra Nelson",
                    "function": "count",
                },
            },
        ),
        (
            Property,
            SelectProperty,
            {
                "id": "5ff23549-94a7-4c38-bb65-6a3d9517dda7",
                "name": "Jeffrey Gonzalez",
                "type": "select",
                "select": {
                    "options": [
                        {
                            "id": "be1ba75b-e9c6-48fe-8124-1ad682c19883",
                            "name": "Steven Harvey",
                            "color": "yellow",
                        },
                        {
                            "id": "d36596d7-16a9-4b4b-aa1d-1a87fb480ebf",
                            "name": "Robert Thomas",
                            "color": "yellow",
                        },
                    ]
                },
            },
        ),
        (
            Property,
            StatusProperty,
            {
                "id": "8f8fd636-04de-4196-91fc-21c37522fa9b",
                "name": "Christina Henderson",
                "type": "status",
                "status": {
                    "options": [
                        {
                            "id": "007a7315-f15e-4369-a2d2-b30b47acfe76",
                            "name": "Emma Kent",
                            "color": "yellow",
                        },
                        {
                            "id": "04a94bff-d91a-4a1b-ab32-ef96ad7fc7bd",
                            "name": "Natalie Yang",
                            "color": "yellow",
                        },
                    ]
                },
                "groups": [{"option_ids": ["441ca561-a349-485b-af44-2d8a34b64bd5"]}],
            },
        ),
        (
            Property,
            TitleProperty,
            {
                "id": "6d8f0b9c-e198-4224-8f66-45b3f50f72fc",
                "name": "Gregory Beck",
                "type": "title",
                "title": {},
            },
        ),
        (
            Property,
            UrlProperty,
            {
                "id": "9d626c1e-fbf2-42c8-9a76-d732cfee3e7e",
                "name": "William Harris",
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
    "clz, test_data",
    [
        (
            CheckboxProperty,
            (
                {
                    'id': 'e2d6c7e6-dac5-43d3-8ba9-a29f31722c6b',
                    'name': 'Kevin Savage',
                    'type': PropertyType.CHECKBOX,
                    'checkbox': {},
                },
                {
                    'id': 'e2d6c7e6-dac5-43d3-8ba9-a29f31722c6b',
                    'name': 'Kevin Savage',
                    'type': PropertyType.CHECKBOX,
                    'checkbox': {},
                },
                {
                    "id": "e2d6c7e6-dac5-43d3-8ba9-a29f31722c6b",
                    "name": "Kevin Savage",
                    "type": "checkbox",
                    "checkbox": {},
                },
            ),
        ),
        (
            CreatedByProperty,
            (
                {
                    'id': '80ce2ea6-945d-45a2-9314-a2e178d3d636',
                    'name': 'Connie White',
                    'type': PropertyType.CREATED_BY,
                    'created_by': {},
                },
                {
                    'id': '80ce2ea6-945d-45a2-9314-a2e178d3d636',
                    'name': 'Connie White',
                    'type': PropertyType.CREATED_BY,
                    'created_by': {},
                },
                {
                    "id": "80ce2ea6-945d-45a2-9314-a2e178d3d636",
                    "name": "Connie White",
                    "type": "created_by",
                    "created_by": {},
                },
            ),
        ),
        (
            CreatedTimeProperty,
            (
                {
                    'id': 'a1d58c49-ce74-4a5f-9b21-e43c6078b060',
                    'name': 'Nathaniel Hanson',
                    'type': PropertyType.CREATED_TIME,
                    'created_time': {},
                },
                {
                    'id': 'a1d58c49-ce74-4a5f-9b21-e43c6078b060',
                    'name': 'Nathaniel Hanson',
                    'type': PropertyType.CREATED_TIME,
                    'created_time': {},
                },
                {
                    "id": "a1d58c49-ce74-4a5f-9b21-e43c6078b060",
                    "name": "Nathaniel Hanson",
                    "type": "created_time",
                    "created_time": {},
                },
            ),
        ),
        (
            DateProperty,
            (
                {
                    'id': '9fe139b3-9f4f-4c36-838c-27917369c808',
                    'name': 'Lauren Mills',
                    'type': PropertyType.DATE,
                    'date': {},
                },
                {
                    'id': '9fe139b3-9f4f-4c36-838c-27917369c808',
                    'name': 'Lauren Mills',
                    'type': PropertyType.DATE,
                    'date': {},
                },
                {
                    "id": "9fe139b3-9f4f-4c36-838c-27917369c808",
                    "name": "Lauren Mills",
                    "type": "date",
                    "date": {},
                },
            ),
        ),
        (
            EmailProperty,
            (
                {
                    'id': 'd1fc32da-3b99-4cd7-b84e-639a34d47e38',
                    'name': 'Andrew Jones',
                    'type': PropertyType.EMAIL,
                    'email': {},
                },
                {
                    'id': 'd1fc32da-3b99-4cd7-b84e-639a34d47e38',
                    'name': 'Andrew Jones',
                    'type': PropertyType.EMAIL,
                    'email': {},
                },
                {
                    "id": "d1fc32da-3b99-4cd7-b84e-639a34d47e38",
                    "name": "Andrew Jones",
                    "type": "email",
                    "email": {},
                },
            ),
        ),
        (
            FilesProperty,
            (
                {
                    'id': 'f268b03e-5064-4911-be43-735be77b9e1c',
                    'name': 'Sharon Smith',
                    'type': PropertyType.FILES,
                    'files': {},
                },
                {
                    'id': 'f268b03e-5064-4911-be43-735be77b9e1c',
                    'name': 'Sharon Smith',
                    'type': PropertyType.FILES,
                    'files': {},
                },
                {
                    "id": "f268b03e-5064-4911-be43-735be77b9e1c",
                    "name": "Sharon Smith",
                    "type": "files",
                    "files": {},
                },
            ),
        ),
        (
            FormulaProperty,
            (
                {
                    'id': '0ddda678-957e-48a9-bf8d-73c5b71b655d',
                    'name': 'Michael Davis',
                    'type': PropertyType.FORMULA,
                    'formula': NotionEquation(expression='sfiagPtGkBlMvFDRVYHk'),
                },
                {
                    'id': '0ddda678-957e-48a9-bf8d-73c5b71b655d',
                    'name': 'Michael Davis',
                    'type': PropertyType.FORMULA,
                    'formula': {'expression': 'sfiagPtGkBlMvFDRVYHk'},
                },
                {
                    "id": "0ddda678-957e-48a9-bf8d-73c5b71b655d",
                    "name": "Michael Davis",
                    "type": "formula",
                    "formula": {"expression": "sfiagPtGkBlMvFDRVYHk"},
                },
            ),
        ),
        (
            LastEditedByProperty,
            (
                {
                    'id': '07f531e2-9c5f-4418-b362-eceeb31e146a',
                    'name': 'Peter Love Jr.',
                    'type': PropertyType.LAST_EDITED_BY,
                    'last_edited_by': {},
                },
                {
                    'id': '07f531e2-9c5f-4418-b362-eceeb31e146a',
                    'name': 'Peter Love Jr.',
                    'type': PropertyType.LAST_EDITED_BY,
                    'last_edited_by': {},
                },
                {
                    "id": "07f531e2-9c5f-4418-b362-eceeb31e146a",
                    "name": "Peter Love Jr.",
                    "type": "last_edited_by",
                    "last_edited_by": {},
                },
            ),
        ),
        (
            LastEditedTimeProperty,
            (
                {
                    'id': 'b6fbd877-83e7-49a5-ab06-68a3f1e41e2b',
                    'name': 'Ellen Scott',
                    'type': PropertyType.LAST_EDITED_TIME,
                    'last_edited_time': {},
                },
                {
                    'id': 'b6fbd877-83e7-49a5-ab06-68a3f1e41e2b',
                    'name': 'Ellen Scott',
                    'type': PropertyType.LAST_EDITED_TIME,
                    'last_edited_time': {},
                },
                {
                    "id": "b6fbd877-83e7-49a5-ab06-68a3f1e41e2b",
                    "name": "Ellen Scott",
                    "type": "last_edited_time",
                    "last_edited_time": {},
                },
            ),
        ),
        (
            MultiSelectProperty,
            (
                {
                    'id': '94ce2a4d-5453-4246-a87b-e6a179b20af9',
                    'name': 'James Griffin',
                    'type': PropertyType.MULTI_SELECT,
                    'multi_select': SelectOptions(
                        options=[
                            BaseOption(
                                id='be1ba75b-e9c6-48fe-8124-1ad682c19883',
                                name='Steven Harvey',
                                color=Color.YELLOW,
                            ),
                            BaseOption(
                                id='d36596d7-16a9-4b4b-aa1d-1a87fb480ebf',
                                name='Robert Thomas',
                                color=Color.YELLOW,
                            ),
                        ]
                    ),
                },
                {
                    'id': '94ce2a4d-5453-4246-a87b-e6a179b20af9',
                    'name': 'James Griffin',
                    'type': PropertyType.MULTI_SELECT,
                    'multi_select': {
                        'options': [
                            {
                                'id': 'be1ba75b-e9c6-48fe-8124-1ad682c19883',
                                'name': 'Steven Harvey',
                                'color': Color.YELLOW,
                            },
                            {
                                'id': 'd36596d7-16a9-4b4b-aa1d-1a87fb480ebf',
                                'name': 'Robert Thomas',
                                'color': Color.YELLOW,
                            },
                        ]
                    },
                },
                {
                    "id": "94ce2a4d-5453-4246-a87b-e6a179b20af9",
                    "name": "James Griffin",
                    "type": "multi_select",
                    "multi_select": {
                        "options": [
                            {
                                "id": "be1ba75b-e9c6-48fe-8124-1ad682c19883",
                                "name": "Steven Harvey",
                                "color": "yellow",
                            },
                            {
                                "id": "d36596d7-16a9-4b4b-aa1d-1a87fb480ebf",
                                "name": "Robert Thomas",
                                "color": "yellow",
                            },
                        ]
                    },
                },
            ),
        ),
        (
            PeopleProperty,
            (
                {
                    'id': '0ee2063c-632e-4c48-ae12-3d8b78510dac',
                    'name': 'Emily Vargas',
                    'type': PropertyType.PEOPLE,
                    'people': {},
                },
                {
                    'id': '0ee2063c-632e-4c48-ae12-3d8b78510dac',
                    'name': 'Emily Vargas',
                    'type': PropertyType.PEOPLE,
                    'people': {},
                },
                {
                    "id": "0ee2063c-632e-4c48-ae12-3d8b78510dac",
                    "name": "Emily Vargas",
                    "type": "people",
                    "people": {},
                },
            ),
        ),
        (
            PhoneNumberProperty,
            (
                {
                    'id': '9164f1d4-828f-47ce-842b-19a8c42e909a',
                    'name': 'Ryan Cisneros',
                    'type': PropertyType.PHONE_NUMBER,
                    'phone_number': {},
                },
                {
                    'id': '9164f1d4-828f-47ce-842b-19a8c42e909a',
                    'name': 'Ryan Cisneros',
                    'type': PropertyType.PHONE_NUMBER,
                    'phone_number': {},
                },
                {
                    "id": "9164f1d4-828f-47ce-842b-19a8c42e909a",
                    "name": "Ryan Cisneros",
                    "type": "phone_number",
                    "phone_number": {},
                },
            ),
        ),
        (
            RelationProperty,
            (
                {
                    'id': 'cfa8aa75-c8a0-45ca-92e4-ec2b89cb9267',
                    'name': 'Joel Steele',
                    'type': PropertyType.RELATION,
                    'relation': DualRelation(
                        database_id=UUID('f9b716fd-243d-41d9-a925-3ba27d95c673'),
                        dual_property=SyncRelation(
                            synced_property_id=None,
                            synced_property_name='BzfrdohJhkdRvoTGcrno',
                        ),
                    ),
                },
                {
                    'id': 'cfa8aa75-c8a0-45ca-92e4-ec2b89cb9267',
                    'name': 'Joel Steele',
                    'type': PropertyType.RELATION,
                    'relation': {
                        'database_id': UUID('f9b716fd-243d-41d9-a925-3ba27d95c673'),
                        'dual_property': {
                            'synced_property_name': 'BzfrdohJhkdRvoTGcrno'
                        },
                    },
                },
                {
                    "id": "cfa8aa75-c8a0-45ca-92e4-ec2b89cb9267",
                    "name": "Joel Steele",
                    "type": "relation",
                    "relation": {
                        "database_id": "f9b716fd-243d-41d9-a925-3ba27d95c673",
                        "dual_property": {
                            "synced_property_name": "BzfrdohJhkdRvoTGcrno"
                        },
                    },
                },
            ),
        ),
        (
            RichTextProperty,
            (
                {
                    'id': 'c87c79c7-81d2-4734-8b81-b6f985bc13fa',
                    'name': 'William White',
                    'type': PropertyType.RICH_TEXT,
                    'rich_text': {},
                },
                {
                    'id': 'c87c79c7-81d2-4734-8b81-b6f985bc13fa',
                    'name': 'William White',
                    'type': PropertyType.RICH_TEXT,
                    'rich_text': {},
                },
                {
                    "id": "c87c79c7-81d2-4734-8b81-b6f985bc13fa",
                    "name": "William White",
                    "type": "rich_text",
                    "rich_text": {},
                },
            ),
        ),
        (
            RollupProperty,
            (
                {
                    'id': '6e96c3f0-b0ef-47b4-b266-f782c53be367',
                    'name': 'Donna Anthony',
                    'type': PropertyType.ROLLUP,
                    'rollup': Rollup(
                        relation_property_id='0c9bfd19-81fa-4466-b86f-b1f014c083a5',
                        rollup_property_id='b23901d2-ec27-4583-9b6c-ac0ea22307e8',
                        relation_property_name='Jackie Lawson MD',
                        rollup_property_name='Dustin Walker',
                        function=RollupFunction.EARLIEST_DATE,
                    ),
                },
                {
                    'id': '6e96c3f0-b0ef-47b4-b266-f782c53be367',
                    'name': 'Donna Anthony',
                    'type': PropertyType.ROLLUP,
                    'rollup': {
                        'relation_property_id': '0c9bfd19-81fa-4466-b86f-b1f014c083a5',
                        'rollup_property_id': 'b23901d2-ec27-4583-9b6c-ac0ea22307e8',
                        'relation_property_name': 'Jackie Lawson MD',
                        'rollup_property_name': 'Dustin Walker',
                        'function': RollupFunction.EARLIEST_DATE,
                    },
                },
                {
                    "id": "6e96c3f0-b0ef-47b4-b266-f782c53be367",
                    "name": "Donna Anthony",
                    "type": "rollup",
                    "rollup": {
                        "relation_property_id": "0c9bfd19-81fa-4466-b86f-b1f014c083a5",
                        "rollup_property_id": "b23901d2-ec27-4583-9b6c-ac0ea22307e8",
                        "relation_property_name": "Jackie Lawson MD",
                        "rollup_property_name": "Dustin Walker",
                        "function": "earliest_date",
                    },
                },
            ),
        ),
        (
            SelectProperty,
            (
                {
                    'id': '6b8f6d4c-e2a8-4262-9c96-63675fe3e2e1',
                    'name': 'Julie Gonzales',
                    'type': PropertyType.SELECT,
                    'select': SelectOptions(
                        options=[
                            BaseOption(
                                id='be1ba75b-e9c6-48fe-8124-1ad682c19883',
                                name='Steven Harvey',
                                color=Color.YELLOW,
                            ),
                            BaseOption(
                                id='d36596d7-16a9-4b4b-aa1d-1a87fb480ebf',
                                name='Robert Thomas',
                                color=Color.YELLOW,
                            ),
                        ]
                    ),
                },
                {
                    'id': '6b8f6d4c-e2a8-4262-9c96-63675fe3e2e1',
                    'name': 'Julie Gonzales',
                    'type': PropertyType.SELECT,
                    'select': {
                        'options': [
                            {
                                'id': 'be1ba75b-e9c6-48fe-8124-1ad682c19883',
                                'name': 'Steven Harvey',
                                'color': Color.YELLOW,
                            },
                            {
                                'id': 'd36596d7-16a9-4b4b-aa1d-1a87fb480ebf',
                                'name': 'Robert Thomas',
                                'color': Color.YELLOW,
                            },
                        ]
                    },
                },
                {
                    "id": "6b8f6d4c-e2a8-4262-9c96-63675fe3e2e1",
                    "name": "Julie Gonzales",
                    "type": "select",
                    "select": {
                        "options": [
                            {
                                "id": "be1ba75b-e9c6-48fe-8124-1ad682c19883",
                                "name": "Steven Harvey",
                                "color": "yellow",
                            },
                            {
                                "id": "d36596d7-16a9-4b4b-aa1d-1a87fb480ebf",
                                "name": "Robert Thomas",
                                "color": "yellow",
                            },
                        ]
                    },
                },
            ),
        ),
        (
            StatusProperty,
            (
                {
                    'id': 'c0cf62e2-97f5-4b7c-be28-ffdec4bb7975',
                    'name': 'Matthew Huber',
                    'type': PropertyType.STATUS,
                    'status': StatusOptions(
                        options=[
                            BaseOption(
                                id='007a7315-f15e-4369-a2d2-b30b47acfe76',
                                name='Emma Kent',
                                color=Color.YELLOW,
                            ),
                            BaseOption(
                                id='04a94bff-d91a-4a1b-ab32-ef96ad7fc7bd',
                                name='Natalie Yang',
                                color=Color.YELLOW,
                            ),
                        ]
                    ),
                    'groups': [
                        GroupOption(
                            option_ids=[UUID('441ca561-a349-485b-af44-2d8a34b64bd5')]
                        )
                    ],
                },
                {
                    'id': 'c0cf62e2-97f5-4b7c-be28-ffdec4bb7975',
                    'name': 'Matthew Huber',
                    'type': PropertyType.STATUS,
                    'status': {
                        'options': [
                            {
                                'id': '007a7315-f15e-4369-a2d2-b30b47acfe76',
                                'name': 'Emma Kent',
                                'color': Color.YELLOW,
                            },
                            {
                                'id': '04a94bff-d91a-4a1b-ab32-ef96ad7fc7bd',
                                'name': 'Natalie Yang',
                                'color': Color.YELLOW,
                            },
                        ]
                    },
                    'groups': [
                        {'option_ids': [UUID('441ca561-a349-485b-af44-2d8a34b64bd5')]}
                    ],
                },
                {
                    "id": "c0cf62e2-97f5-4b7c-be28-ffdec4bb7975",
                    "name": "Matthew Huber",
                    "type": "status",
                    "status": {
                        "options": [
                            {
                                "id": "007a7315-f15e-4369-a2d2-b30b47acfe76",
                                "name": "Emma Kent",
                                "color": "yellow",
                            },
                            {
                                "id": "04a94bff-d91a-4a1b-ab32-ef96ad7fc7bd",
                                "name": "Natalie Yang",
                                "color": "yellow",
                            },
                        ]
                    },
                    "groups": [
                        {"option_ids": ["441ca561-a349-485b-af44-2d8a34b64bd5"]}
                    ],
                },
            ),
        ),
        (
            TitleProperty,
            (
                {
                    'id': '750ae7d0-a7e0-478b-9d37-244ce4ea02e8',
                    'name': 'Walter Smith',
                    'type': PropertyType.TITLE,
                    'title': {},
                },
                {
                    'id': '750ae7d0-a7e0-478b-9d37-244ce4ea02e8',
                    'name': 'Walter Smith',
                    'type': PropertyType.TITLE,
                    'title': {},
                },
                {
                    "id": "750ae7d0-a7e0-478b-9d37-244ce4ea02e8",
                    "name": "Walter Smith",
                    "type": "title",
                    "title": {},
                },
            ),
        ),
        (
            UrlProperty,
            (
                {
                    'id': '00c5f734-b0d8-4b48-a383-5460cf5b9a1a',
                    'name': 'Ronald Bailey',
                    'type': PropertyType.URL,
                    'url': {},
                },
                {
                    'id': '00c5f734-b0d8-4b48-a383-5460cf5b9a1a',
                    'name': 'Ronald Bailey',
                    'type': PropertyType.URL,
                    'url': {},
                },
                {
                    "id": "00c5f734-b0d8-4b48-a383-5460cf5b9a1a",
                    "name": "Ronald Bailey",
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
