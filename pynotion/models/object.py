from datetime import datetime
from enum import Enum
from typing import Annotated
from uuid import UUID

from pydantic import BeforeValidator

from ._internal import (
    validate_uuid4,
    validate_datetime,
    BaseNotionModel,
)

NotionObjectId = Annotated[str | int | bytes | UUID, BeforeValidator(validate_uuid4)]
CreatedTime = Annotated[str | datetime, BeforeValidator(validate_datetime)]
LastEditedTime = Annotated[str | datetime, BeforeValidator(validate_datetime)]


class NotionObjectType(str, Enum):
    """
    Defines main object types in Notion.

    Attributes:
        DATABASE: Database object type.
        PAGE: Page object type.
        BLOCK: Block object type.
        User: User object type.
        Comment: Comment object type.
    """

    DATABASE = "database"
    PAGE = "page"
    BLOCK = "block"
    User = "user"
    Comment = "comment"


class NotionObjectRef(BaseNotionModel):
    """Reference to a Notion object.

    Attributes:
        id: The ID of the object.
    """

    id: NotionObjectId


# class NormalNotionObjectModel(BaseNotionModel):
#     __no_instance__ = True
#
#     object: Literal[
#         NotionObjectType.DATABASE,
#         NotionObjectType.PAGE,
#         NotionObjectType.BLOCK,
#         NotionObjectType.Comment,
#     ] = Field(frozen=True)
#
#     id: Optional[NotionObjectId] = Field(default=None, frozen=True)
#     parent: Optional[Parent] = Field(default=None, frozen=True)
#     created_time: Optional[CreatedTime] = Field(default=None, frozen=True)
#     last_edited_time: Optional[LastEditedTime] = Field(default=None, frozen=True)
#     created_by: Optional["UserRef"] = Field(default=None, frozen=True)
#
#
# class FullNotionObjectModel(NormalNotionObjectModel):
#     __no_instance__ = True
#
#     object: Literal[
#         NotionObjectType.DATABASE,
#         NotionObjectType.PAGE,
#         NotionObjectType.BLOCK,
#     ] = Field(frozen=True)
#
#     last_edited_by: Optional["UserRef"] = Field(default=None, frozen=True)
#     archived: Optional[bool] = Field(default=None, frozen=True)
#     in_trash: Optional[bool] = Field(default=None, frozen=True)
