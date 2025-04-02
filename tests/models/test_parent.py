from uuid import uuid4, UUID

import pytest
from pydantic import ValidationError

from pynotion.models import (
    DatabaseParent,
    ParentType,
    PageParent,
    BlockParent,
    WorkspaceParent,
)
from tests.models.model_test_utils import PydanticModelTester


@pytest.mark.parametrize(
    "clz, parent_type, type_object, should_raise",
    [
        (DatabaseParent, ParentType.DATABASE_ID, uuid4(), False),
        (PageParent, ParentType.PAGE_ID, uuid4(), False),
        (BlockParent, ParentType.BLOCK_ID, uuid4(), False),
        (WorkspaceParent, ParentType.WORKSPACE, True, False),
        (WorkspaceParent, ParentType.WORKSPACE, False, True),
        (WorkspaceParent, ParentType.WORKSPACE, uuid4(), True),
        (PageParent, ParentType.PAGE_ID, "invalid-id", True),  # Invalid UUID
    ],
)
def test_notion_parent(clz, parent_type, type_object, should_raise):
    if should_raise:
        with pytest.raises(ValidationError):
            clz(type=parent_type, **{parent_type: type_object})

    else:
        parent = clz(type=parent_type, **{parent_type: type_object})
        assert parent.type == parent_type
        assert getattr(parent, parent_type) == type_object


@pytest.mark.parametrize(
    "model_class, test_data",
    [
        (
            DatabaseParent,
            (
                {
                    "type": "database_id",
                    "database_id": "f4de14e1-0cff-4497-835f-29d6d04d62c1",
                },
                {
                    "type": ParentType.DATABASE_ID,
                    "database_id": UUID("f4de14e1-0cff-4497-835f-29d6d04d62c1"),
                },
                {
                    "type": "database_id",
                    "database_id": "f4de14e1-0cff-4497-835f-29d6d04d62c1",
                },
            ),
        ),
        (
            PageParent,
            (
                {
                    "type": "page_id",
                    "page_id": "f4de14e1-0cff-4497-835f-29d6d04d62c1",
                },
                {
                    "type": ParentType.PAGE_ID,
                    "page_id": UUID("f4de14e1-0cff-4497-835f-29d6d04d62c1"),
                },
                {"type": "page_id", "page_id": "f4de14e1-0cff-4497-835f-29d6d04d62c1"},
            ),
        ),
        (
            BlockParent,
            (
                {
                    "type": "block_id",
                    "block_id": "f4de14e1-0cff-4497-835f-29d6d04d62c1",
                },
                {
                    "type": ParentType.BLOCK_ID,
                    "block_id": UUID("f4de14e1-0cff-4497-835f-29d6d04d62c1"),
                },
                {
                    "type": "block_id",
                    "block_id": "f4de14e1-0cff-4497-835f-29d6d04d62c1",
                },
            ),
        ),
        (
            WorkspaceParent,
            (
                {
                    "type": "workspace",
                    "workspace": True,
                },
                {
                    "type": ParentType.WORKSPACE,
                    "workspace": True,
                },
                {"type": "workspace", "workspace": True},
            ),
        ),
    ],
)
def test_pydantic_models(model_class, test_data):
    tester = PydanticModelTester(model_class, test_data)
    tester.run_all_tests()
