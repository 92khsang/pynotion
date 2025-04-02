from uuid import UUID

import pytest
from pydantic import BaseModel

from pynotion.models import *
from tests.models.model_test_utils import PydanticModelTester


@pytest.mark.parametrize(
    "clz, test_data",
    [
        (
            CheckboxPropertySchema,
            ({'checkbox': {}}, {'checkbox': {}}, {"checkbox": {}}),
        ),
        (
            CreatedByPropertySchema,
            ({'created_by': {}}, {'created_by': {}}, {"created_by": {}}),
        ),
        (
            CreatedTimePropertySchema,
            ({'created_time': {}}, {'created_time': {}}, {"created_time": {}}),
        ),
        (
            DatePropertySchema,
            ({'date': {}}, {'date': {}}, {"date": {}}),
        ),
        (
            EmailPropertySchema,
            ({'email': {}}, {'email': {}}, {"email": {}}),
        ),
        (
            FilesPropertySchema,
            ({'files': {}}, {'files': {}}, {"files": {}}),
        ),
        (
            FormulaPropertySchema,
            (
                {'formula': NotionEquation(expression='GOiShXcLdCSStyOrcXlv')},
                {'formula': {'expression': 'GOiShXcLdCSStyOrcXlv'}},
                {"formula": {"expression": "GOiShXcLdCSStyOrcXlv"}},
            ),
        ),
        (
            LastEditedByPropertySchema,
            ({'last_edited_by': {}}, {'last_edited_by': {}}, {"last_edited_by": {}}),
        ),
        (
            LastEditedTimePropertySchema,
            (
                {'last_edited_time': {}},
                {'last_edited_time': {}},
                {"last_edited_time": {}},
            ),
        ),
        (
            MultiSelectPropertySchema,
            (
                {
                    'multi_select': SelectOptionsSchema(
                        options=[
                            BaseOptionSchema(name='Michael Collins', color=Color.PINK)
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
            NumberPropertySchema,
            (
                {'number': NumberSchema(format=NumberFormat.NEW_ZEALAND_DOLLAR)},
                {'number': {'format': NumberFormat.NEW_ZEALAND_DOLLAR}},
                {"number": {"format": "new_zealand_dollar"}},
            ),
        ),
        (
            PeoplePropertySchema,
            ({'people': {}}, {'people': {}}, {"people": {}}),
        ),
        (
            PhoneNumberPropertySchema,
            ({'phone_number': {}}, {'phone_number': {}}, {"phone_number": {}}),
        ),
        (
            RelationPropertySchema,
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
            RichTextPropertySchema,
            ({'rich_text': {}}, {'rich_text': {}}, {"rich_text": {}}),
        ),
        (
            RollupPropertySchema,
            (
                {
                    'rollup': RollupSchema(
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
            SelectPropertySchema,
            (
                {
                    'select': SelectOptionsSchema(
                        options=[
                            BaseOptionSchema(name='Michael Collins', color=Color.PINK)
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
            TitlePropertySchema,
            ({'title': {}}, {'title': {}}, {"title": {}}),
        ),
        (
            UrlPropertySchema,
            ({'url': {}}, {'url': {}}, {"url": {}}),
        ),
    ],
)
def test_tx_property_schema_models_serialization(
    clz: type[BaseModel], test_data: tuple[dict, dict, dict]
):
    PydanticModelTester(clz, test_data).run_all_tests()
