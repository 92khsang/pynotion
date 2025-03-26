from typing import Literal, Optional, Annotated

from pydantic import Field, BeforeValidator

from ._internal import FrozenNotionModel, BaseNotionModel
from .emoji import Emoji
from .file import File
from .object import NotionObjectType, NotionObjectId
from .parent import PageParent
from .properties import Property, TxPropertySchema
from .rich_text import RxRichText, TxRichText
from .types import NotionDatetime
from .user import UserRef


class RxDatabase(FrozenNotionModel):
    object: Literal[NotionObjectType.DATABASE] = NotionObjectType.DATABASE
    id: NotionObjectId
    created_time: Optional[NotionDatetime] = None
    created_by: Optional[UserRef] = None
    last_edited_time: Optional[NotionDatetime] = None
    last_edited_by: Optional[UserRef] = None
    title: Optional[list[RxRichText]] = None
    description: Optional[list[RxRichText]] = None
    icon: Optional[File | Emoji] = None
    cover: Optional[File] = None
    properties: Optional[dict[str, Property]] = None
    parent: Optional[PageParent] = None
    url: Optional[str] = Field(default=None, frozen=True)
    archived: Optional[bool] = None
    in_trash: Optional[bool] = None
    is_inline: Optional[bool] = None
    public_url: Optional[str] = None


class CreateDatabase(BaseNotionModel):
    parent: Annotated[
        str | PageParent,
        BeforeValidator(lambda v: PageParent(page_id=v) if isinstance(v, str) else v),
    ]
    title: Optional[list[TxRichText]]
    properties: dict[str, TxPropertySchema]


class UpdateDatabase(BaseNotionModel):
    title: Optional[list[TxRichText]]
    description: Optional[list[TxRichText]]
    properties: dict[str, TxPropertySchema]


TxDatabase = CreateDatabase | UpdateDatabase
