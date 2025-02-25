from typing import TYPE_CHECKING

from .types import (
    ObjectId,
    ObjectType,
    Color,
    BackgroundColor,
    NotionLink,
    NotionEquation,
    NotionDate,
)

if TYPE_CHECKING:
    from .types import NotionBaseModel, NotionTypedModel

__all__ = [
    # types
    "ObjectId",
    "ObjectType",
    "Color",
    "BackgroundColor",
    "NotionLink",
    "NotionEquation",
    "NotionDate",
    "NotionBaseModel",
    "NotionTypedModel",
]
