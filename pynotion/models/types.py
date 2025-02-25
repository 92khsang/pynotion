from __future__ import annotations as _annotations

import uuid
from datetime import datetime
from enum import StrEnum
from typing import TypeAlias, Optional
from zoneinfo import available_timezones

from pydantic import BaseModel, HttpUrl, field_validator, model_serializer


# ---------------------- BASE MODEL ---------------------- #
class NotionBaseModel(BaseModel):
    class Config:
        extra = "forbid"
        use_enum_values = True


class NotionTypedModel(NotionBaseModel):
    type: StrEnum
    obj: NotionBaseModel | StrEnum | str

    @model_serializer(mode="wrap")
    def serialize_model(self, nxt):
        data = nxt(self)
        obj_value = data.pop("obj", None)
        if obj_value is not None:
            data[self.type] = obj_value
        return data


# ---------------------- Aliases ---------------------- #
ObjectId: TypeAlias = uuid.UUID


# ---------------------- ENUMS ---------------------- #
class ObjectType(StrEnum):
    """Defines object types in Notion.

    Attributes:
        BLOCK: block object type.
        DATABASE: database object type.
        PAGE: page object type.
        USER: user object type.
    """

    BLOCK = "block"
    DATABASE = "database"
    PAGE = "page"
    USER = "user"


class Color(StrEnum):
    """Defines colors in Notion.

    Attributes:
        BLUE: blue color.
        BROWN: brown color.
        DEFAULT: default color.
        GRAY: gray color.
        GREEN: green color.
        ORANGE: orange color.
        PURPLE: purple color.
        PINK: pink color.
        RED: red color.
        YELLOW: yellow color.
    """

    BLUE = "blue"
    BROWN = "brown"
    DEFAULT = "default"
    GRAY = "gray"
    GREEN = "green"
    ORANGE = "orange"
    PURPLE = "purple"
    PINK = "pink"
    RED = "red"
    YELLOW = "yellow"


class BackgroundColor(StrEnum):
    """Defines background colors in Notion.

    Attributes:

        BLUE_BACKGROUND: blue background color.
        BROWN_BACKGROUND: brown background color.
        GRAY_BACKGROUND: gray background color.
        GREEN_BACKGROUND: green background color.
        ORANGE_BACKGROUND: orange background color.
        PURPLE_BACKGROUND: purple background color.
        PINK_BACKGROUND: pink background color.
        RED_BACKGROUND: red background color.
        YELLOW_BACKGROUND: yellow background color.
    """

    BLUE_BACKGROUND = "blue_background"
    BROWN_BACKGROUND = "brown_background"
    GRAY_BACKGROUND = "gray_background"
    GREEN_BACKGROUND = "green_background"
    ORANGE_BACKGROUND = "orange_background"
    PURPLE_BACKGROUND = "purple_background"
    PINK_BACKGROUND = "pink_background"
    RED_BACKGROUND = "red_background"
    YELLOW_BACKGROUND = "yellow_background"


# ---------------------- Objets ---------------------- #


class NotionLink(NotionBaseModel):
    """Represents a simple link in Notion.

    Attributes:
        url: The URL of the link.
    """

    url: HttpUrl


class NotionEquation(NotionBaseModel):
    """Represents a equation in Notion.

    Attributes:
        expression: Equation expression.
    """

    expression: str


class NotionDate(BaseModel):
    start: datetime
    end: Optional[datetime] = None
    time_zone: Optional[str] = None

    @field_validator("start", "end", mode="before")  # noqa
    @classmethod
    def parse_datetime(cls, v: Optional[str]) -> Optional[datetime]:
        """Parse ISO 8601 datetime string into Python datetime object while preserving timezone info."""
        if v is None:
            return None
        try:
            return datetime.fromisoformat(v.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError(f"Invalid ISO 8601 format: {v}")

    @field_validator("time_zone")  # noqa
    @classmethod
    def validate_timezone(cls, v: Optional[str]) -> Optional[str]:
        """Ensure the time_zone is a valid time zone."""
        if v is None:
            return None
        if v not in available_timezones():
            raise ValueError(f"Invalid IANA timezone: {v}")
        return v
