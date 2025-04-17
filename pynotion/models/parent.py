from enum import Enum
from typing import Literal, Annotated, TYPE_CHECKING, Union
from uuid import UUID

from pydantic import Field, BeforeValidator

from ._internal import BaseNotionModel
from ._internal.utils import discriminate_field

__all__ = [
    "BlockParent",
    "DatabaseParent",
    "NotionParent",
    "PARENT_CLASS_MAP",
    "PageParent",
    "ParentType",
    "WorkspaceParent",
]


class ParentType(str, Enum):
    """Defines the possible types of parents in Notion."""

    DATABASE_ID = "database_id"
    PAGE_ID = "page_id"
    BLOCK_ID = "block_id"
    WORKSPACE = "workspace"


class DatabaseParent(BaseNotionModel):
    """Represents a parent for a database.

    Attributes:
        type: Always "database_id".
        database_id: The ID of the database.
    """

    type: Literal[ParentType.DATABASE_ID] = ParentType.DATABASE_ID
    database_id: UUID


class PageParent(BaseNotionModel):
    """Represents a parent for a page.

    Attributes:
        type: Always "page_id".
        page_id: The ID of the page.
    """

    type: Literal[ParentType.PAGE_ID] = ParentType.PAGE_ID
    page_id: UUID


class BlockParent(BaseNotionModel):
    """Represents a parent for a block.

    Attributes:
        type: Always "block_id".
        block_id: The ID of the block.
    """

    type: Literal[ParentType.BLOCK_ID] = ParentType.BLOCK_ID
    block_id: UUID


class WorkspaceParent(BaseNotionModel):
    """Represents a parent for a workspace.

    Attributes:
        type: Always "workspace".
        workspace: Always True
    """

    type: Literal[ParentType.WORKSPACE] = ParentType.WORKSPACE
    workspace: Literal[True] = Field(default=True, frozen=True)


PARENT_CLASS_MAP = {
    ParentType.DATABASE_ID: "DatabaseParent",
    ParentType.PAGE_ID: "PageParent",
    ParentType.BLOCK_ID: "BlockParent",
    ParentType.WORKSPACE: "WorkspaceParent",
}

if not TYPE_CHECKING:
    NotionParent = Annotated[
        Union[tuple(PARENT_CLASS_MAP.values())],
        BeforeValidator(lambda v: discriminate_field(v, "type", PARENT_CLASS_MAP)),
    ]
else:
    NotionParent = Union[DatabaseParent, PageParent, BlockParent, WorkspaceParent]
