from typing import Literal, Optional, TYPE_CHECKING

from pydantic import Field

from pynotion.models.object import NotionObjectType
from ._internal import FrozenNotionModel, BaseNotionModel

if TYPE_CHECKING:
    from pynotion.models import (
        PageParent,
        NotionParent,
        RxRichText,
        TxRichText,
        NotionDatetime,
        UserRef,
    )

__all__ = ["RxComment", "TxCommentWithParent", "TxCommentWithDiscussionId"]


class RxComment(FrozenNotionModel):
    """Represents a comment in Notion.

    Attributes:
        object: Always "comment".
        id: Unique identifier for the comment.
        parent: Parent page of the comment.
        discussion_id: Unique identifier for the discussion of the comment.
        created_time: ISO 8601 datetime when the comment was created.
        created_by: NotionUser who created the comment.
        last_edited_time: ISO 8601 datetime when the comment was last edited.
        rich_text: Rich text content of the comment.
    """

    object: Literal[NotionObjectType.COMMENT] = NotionObjectType.COMMENT
    id: UUID
    parent: "NotionParent"
    discussion_id: UUID
    created_time: "NotionDatetime"
    created_by: "UserRef"
    last_edited_time: Optional["NotionDatetime"] = None
    rich_text: list["RxRichText"] = Field(default_factory=list)


class TxCommentWithDiscussionId(BaseNotionModel):
    """Represents a comment for creating a new comment.

    Attributes:
        discussion_id: Unique identifier for the discussion of the comment.
        rich_text: Rich text content of the comment.
    """

    discussion_id: UUID
    rich_text: list["TxRichText"] = Field(default_factory=list)


class TxCommentWithParent(BaseNotionModel):
    """Represents a comment for creating a new comment.

    Attributes:
        parent: Parent page of the comment.
        rich_text: Rich text content of the comment.
    """

    parent: "PageParent"
    rich_text: list["TxRichText"] = Field(default_factory=list)
