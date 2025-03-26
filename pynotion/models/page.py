from typing import Literal, Optional

from pydantic import Field, model_validator

from ._internal import BaseNotionModel, FrozenNotionModel
from .block import TxBlock
from .emoji import Emoji
from .file import File, ExternalFile
from .object import NotionObjectType, NotionObjectId
from .parent import Parent, ParentType
from .properties import RxPropertyValue, TxPropertyValue
from .types import NotionDatetime
from .user import UserRef


class RxPage(FrozenNotionModel):
    object: Literal[NotionObjectType.PAGE] = NotionObjectType.PAGE
    id: NotionObjectId
    created_time: Optional[NotionDatetime] = None
    created_by: Optional[UserRef] = None
    last_edited_time: Optional[NotionDatetime] = None
    last_edited_by: Optional[UserRef] = None
    archived: Optional[bool] = None
    in_trash: Optional[bool] = None
    icon: Optional[File | Emoji] = None
    cover: Optional[File] = None
    properties: Optional[dict[str, RxPropertyValue]] = None
    parent: Optional[Parent] = None
    url: Optional[str] = None
    public_url: Optional[str] = None


class TxPage(BaseNotionModel):
    parent: Parent
    properties: dict[str, TxPropertyValue] = Field(default_factory=dict)
    children: Optional[list[TxBlock]] = None
    icon: Optional[ExternalFile | Emoji] = None
    cover: Optional[File] = None

    @model_validator(mode="after")
    def _validate_properties(self):
        if self.parent.type == ParentType.PAGE_ID:
            allowed_keys = {"title"}
            actual_keys = set(self.properties.keys())

            if not actual_keys <= allowed_keys:
                extra_keys = actual_keys - allowed_keys
                raise ValueError(
                    f"When parent is PAGE_ID, only 'title' is allowed in properties. "
                    f"Found invalid keys: {extra_keys}"
                )
        return self
