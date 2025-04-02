from typing import Literal, Optional, Annotated, TYPE_CHECKING, Union

from pydantic import Field, BeforeValidator

from pynotion.models.object import NotionObjectType, NotionObjectId
from ._internal import FrozenNotionModel, BaseNotionModel

if TYPE_CHECKING:
    from pynotion.models.parent import PageParent
    from pynotion.models.property.rx import Property
    from pynotion.models.property.tx import PropertySchema
    from pynotion.models.types import NotionDatetime
    from pynotion.models.user import UserRef
    from pynotion.models.rich_text.rx import RxRichText
    from pynotion.models.rich_text.tx import TxRichText

__all__ = ["RxDatabase", "CreateDatabase", "UpdateDatabase"]


class RxDatabase(FrozenNotionModel):
    """Represents a database in Notion.

    Attributes:
        id: The ID of the database.
        created_time: The date and time when the database was created.
        created_by: The user who created the database.
        last_edited_time: The date and time when the database was last edited.
        last_edited_by: The user who last edited the database.
        title: The title of the database.
        description: The description of the database.
        icon: The icon of the database.
        cover: The cover of the database.
        properties: The properties of the database.
        parent: The parent of the database.
        url: The URL of the database.
        archived: Whether the database is archived.
        in_trash: Whether the database is in the trash.
        is_inline: Whether the database is inline.
        public_url: The public URL of the database.
    """

    object: Literal[NotionObjectType.DATABASE] = NotionObjectType.DATABASE
    id: NotionObjectId
    created_time: Optional["NotionDatetime"] = None
    created_by: Optional["UserRef"] = None
    last_edited_time: Optional["NotionDatetime"] = None
    last_edited_by: Optional["UserRef"] = None
    title: Optional[list["RxRichText"]] = None
    description: Optional[list["RxRichText"]] = None
    icon: Union["None | NotionFile | NotionEmoji"] = None
    cover: Union["None | NotionFile"] = None
    properties: Optional[dict[str, "Property"]] = None
    parent: Optional["PageParent"] = None
    url: Optional[str] = Field(default=None, frozen=True)
    archived: Optional[bool] = None
    in_trash: Optional[bool] = None
    is_inline: Optional[bool] = None
    public_url: Optional[str] = None


class CreateDatabase(BaseNotionModel):
    """Model for creating a database.

    Attributes:
        parent: The parent of the database.
        title: The title of the database.
        properties: The properties of the database.
    """

    parent: Annotated[
        "str | PageParent",
        BeforeValidator(lambda v: PageParent(page_id=v) if isinstance(v, str) else v),
    ]
    title: Optional[list["TxRichText"]]
    properties: dict[str, "PropertySchema"]


class UpdateDatabase(BaseNotionModel):
    """Model for updating a database.

    Attributes:
        title: The title of the database.
        description: The description of the database.
        properties: The properties of the database.
    """

    title: Optional[list["TxRichText"]]
    description: Optional[list["TxRichText"]]
    properties: dict[str, Optional["PropertySchema"]]
