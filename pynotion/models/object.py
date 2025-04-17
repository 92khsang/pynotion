from enum import Enum
from uuid import UUID

from ._internal import BaseNotionModel

__all__ = ["NotionObjectType", "NotionObjectIdWrapper"]


class NotionObjectType(str, Enum):
    """Defines main object types in Notion."""

    DATABASE = "database"
    PAGE = "page"
    BLOCK = "block"
    USER = "user"
    COMMENT = "comment"


class NotionObjectIdWrapper(BaseNotionModel):
    """Reference to a Notion object.

    Attributes:
        id: The ID of the object.
    """

    id: UUID
