from typing import Literal, Optional, TYPE_CHECKING, Union
from uuid import UUID

from pydantic import Field, model_validator

from pynotion.models.object import NotionObjectType
from ._internal import BaseNotionModel, FrozenNotionModel

if TYPE_CHECKING:
    from pynotion.models import (
        NotionDatetime,
        NotionEmoji,
        NotionFile,
        NotionParent,
        RxPropertyValue,
        TxBlock,
        TxPropertyValue,
        UserRef,
    )


__all__ = ["RxPage", "TxPage"]


class RxPage(FrozenNotionModel):
    """Represents a Notion page.

    Attributes:
        object: The type of the object. Always "page".
        id: The ID of the page.
        created_time: The creation time of the page.
        created_by: The user who created the page.
        last_edited_time: The last time the page was edited.
        last_edited_by: The user who last edited the page.
        archived: Whether the page is archived.
        in_trash: Whether the page is in the trash.
        icon: The icon of the page.
        cover: The cover of the page.
        properties: The properties of the page.
        parent: The parent of the page.
        url: The URL of the page.
        public_url: The public URL of the page.
    """

    object: Literal[NotionObjectType.PAGE] = NotionObjectType.PAGE
    id: UUID
    created_time: Optional["NotionDatetime"] = None
    created_by: Optional["UserRef"] = None
    last_edited_time: Optional["NotionDatetime"] = None
    last_edited_by: Optional["UserRef"] = None
    archived: Optional[bool] = None
    in_trash: Optional[bool] = None
    icon: Optional[Union["NotionFile", "NotionEmoji"]] = None
    cover: Optional["NotionFile"] = None
    properties: Optional[dict[str, "RxPropertyValue"]] = None
    parent: Optional["NotionParent"] = None
    url: Optional[str] = None
    public_url: Optional[str] = None


class TxPage(BaseNotionModel):
    """Model for creating or updating a page in Notion.

    Attributes:
        parent: The parent of the page.
        properties: The properties of the page.
        children: The children of the page.
        icon: The icon of the page.
        cover: The cover of the page.
    """

    parent: "NotionParent"
    properties: dict[str, "TxPropertyValue"] = Field(default_factory=dict)
    children: Optional[list["TxBlock"]] = None
    icon: Optional[Union["NotionFile", "NotionEmoji"]] = None
    cover: Optional["NotionFile"] = None

    @model_validator(mode="after")
    def _validate_properties(self):
        if self.parent.type.value == "page_id":
            allowed_keys = {"title"}
            actual_keys = set(self.properties.keys())

            if not actual_keys <= allowed_keys:
                extra_keys = actual_keys - allowed_keys
                raise ValueError(
                    f"When parent is PAGE_ID, only 'title' is allowed in properties. "
                    f"Found invalid keys: {extra_keys}"
                )
        return self
