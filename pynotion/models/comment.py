from typing import Literal, Optional

from pydantic import Field

from ._internal import FrozenNotionModel, BaseNotionModel
from .object import NotionObjectType, NotionObjectId
from .parent import PageParent
from .rich_text import RxRichText, TxRichText
from .types import NotionDatetime
from .user import UserRef


class RxComment(FrozenNotionModel):
    object: Literal[NotionObjectType.COMMENT] = NotionObjectType.COMMENT
    id: NotionObjectId
    parent: PageParent
    discussion_id: NotionObjectId
    created_time: NotionDatetime
    created_by: UserRef
    last_edited_time: Optional[NotionDatetime] = None
    rich_text: list[RxRichText] = Field(default_factory=list)


class TxCommentWithDiscussionId(BaseNotionModel):
    discussion_id: NotionObjectId
    rich_text: list[TxRichText] = Field(default_factory=list)


class TxCommentWithParent(BaseNotionModel):
    parent: PageParent
    rich_text: list[TxRichText] = Field(default_factory=list)


TxComment = TxCommentWithDiscussionId | TxCommentWithParent
