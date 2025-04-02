from typing import Optional, Annotated, TYPE_CHECKING

from pydantic import BeforeValidator

from pynotion.models.object import NotionObjectId
from .._internal import BaseNotionModel, validate_enum

if TYPE_CHECKING:
    from pynotion.models.types import Color, BackgroundColor

__all__ = [
    "SyncedFrom",
    "DuplicateSynced",
    "TableOfContents",
    "model_synced_discriminator",
]


class SyncedFrom(BaseNotionModel):
    """Represents the type of the synced from the object.

    Attributes:
        block_id: An identifier for the original synced_block.
    """

    block_id: NotionObjectId


class DuplicateSynced(BaseNotionModel):
    """Represents a duplicated synced block.

    Attributes:
        synced_from: The type of the synced from object.
        children: Always None
    """

    synced_from: SyncedFrom
    children: None = None


def model_synced_discriminator(v):

    from .._internal.utils import get_value_for_discriminator

    synced_from_value = get_value_for_discriminator(v, "synced_from")

    if synced_from_value is not None:
        return "duplicated"
    else:
        return "original"


class TableOfContents(BaseNotionModel):
    """Represents the content of a table.

    Attributes:
        color: The color of the table.
    """

    color: Optional[
        Annotated[
            "str | Color | BackgroundColor",
            BeforeValidator(lambda v: validate_enum(v, (Color, BackgroundColor))),
        ]
    ]
