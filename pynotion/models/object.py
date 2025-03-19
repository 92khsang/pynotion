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
        USER: User object type.
        COMMENT: Comment object type.
    """

    DATABASE = "database"
    PAGE = "page"
    BLOCK = "block"
    USER = "user"
    COMMENT = "comment"


class NotionObjectRef(BaseNotionModel):
    """Reference to a Notion object.

    Attributes:
        id: The ID of the object.
    """

    id: NotionObjectId
