from enum import Enum
from typing import Literal, Annotated

from pydantic import Field

from ._internal import BaseNotionModel
from .object import NotionObjectId


class ParentType(str, Enum):
    """Defines the possible types of parents in Notion.

    Each Notion object (except for the workspace itself) has a parent.
    This enum defines all possible parent types.

    Attributes:
        DATABASE_ID: Parent is a database. The type_object will contain the database ID.
        PAGE_ID: Parent is a page. The type_object will contain the page ID.
        BLOCK_ID: Parent is a block. The type_object will contain the block ID.
        WORKSPACE: Parent is a workspace. The type_object will be True.
    """

    DATABASE_ID = "database_id"
    PAGE_ID = "page_id"
    BLOCK_ID = "block_id"
    WORKSPACE = "workspace"


class DatabaseParent(BaseNotionModel):
    """Represents a parent for a database.

    Attributes:
        database_id: The ID of the database.
    """

    type: Literal[ParentType.DATABASE_ID] = Field(
        default=ParentType.DATABASE_ID, frozen=True
    )
    database_id: NotionObjectId


class PageParent(BaseNotionModel):
    """Represents a parent for a page.

    Attributes:
        page_id: The ID of the page.
    """

    type: Literal[ParentType.PAGE_ID] = Field(default=ParentType.PAGE_ID, frozen=True)
    page_id: NotionObjectId


class BlockParent(BaseNotionModel):
    """Represents a parent for a block.

    Attributes:
        block_id: The ID of the block.
    """

    type: Literal[ParentType.BLOCK_ID] = Field(default=ParentType.BLOCK_ID, frozen=True)
    block_id: NotionObjectId


class WorkspaceParent(BaseNotionModel):
    """Represents a parent for a workspace.

    Attributes:
        workspace: Always True
    """

    type: Literal[ParentType.WORKSPACE] = Field(
        default=ParentType.WORKSPACE, frozen=True
    )
    workspace: Literal[True] = Field(default=True, frozen=True)


Parent = Annotated[
    DatabaseParent | PageParent | BlockParent | WorkspaceParent,
    Field(discriminator="type"),
]
