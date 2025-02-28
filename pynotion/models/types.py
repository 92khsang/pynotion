from __future__ import annotations as _annotations

from datetime import datetime
from enum import StrEnum
from typing import TypeAlias, Annotated, Optional, Union
from zoneinfo import ZoneInfo

from pydantic import (
    Field,
    BeforeValidator,
    UUID4,
    EmailStr,
)

from ._internal import (
    validate_timezone,
    validate_datetime,
    validate_url,
    NotionBaseModel,
)

ObjectId: TypeAlias = UUID4
NotionDatetime: TypeAlias = Annotated[
    datetime | str, BeforeValidator(validate_datetime)
]
NotionEmail: TypeAlias = Annotated[str, EmailStr]
NotionUrl: TypeAlias = Annotated[str, BeforeValidator(validate_url)]


class ObjectType(StrEnum):
    """Defines object types in Notion.

    Attributes:
        BLOCK: block object type.
        DATABASE: database object type.
        PAGE: page object type.
        USER: user object type.
        COMMENT: comment object type.
    """

    BLOCK = "block"
    DATABASE = "database"
    PAGE = "page"
    USER = "user"
    COMMENT = "comment"


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


class NotionLink(NotionBaseModel):
    """Represents a simple link in Notion.

    Attributes:
        url: The URL of the link.
    """

    url: NotionUrl = Field(description="The URL of the link")


class NotionEquation(NotionBaseModel):
    """Represents a equation in Notion.

    Attributes:
        expression: Equation expression.
    """

    expression: str


class NotionDate(NotionBaseModel):
    """Represents a date in Notion.

    Attributes:
        start: The start datetime in ISO 8601 format.
        end: The end datetime in ISO 8601 format (optional).
        time_zone: The timezone of the date (optional).

    Notes:
        - `start` and `end` must be in ISO 8601 format.
        - If `time_zone` is provided, `start` and `end` must not contain UTC offsets.
        - If `time_zone` is None, `start` and `end` can contain UTC offsets.
    """

    start: NotionDatetime = Field(description="The start datetime of the date.")
    end: Optional[NotionDatetime] = Field(
        default=None, description="The end datetime of the date."
    )
    time_zone: Optional[str] = Field(
        default=None, description="The timezone of the date."
    )

    @classmethod
    def _validate_single_datetime(
        cls, dt: Union[str, datetime], time_zone: Optional[str], dt_name: str
    ) -> Union[str, datetime]:
        """
        Validate and process a single datetime value.

        Args:
            dt: Datetime to validate
            time_zone: Timezone to validate against
            dt_name: Name of the datetime field (for error messages)

        Returns:
            Validated and potentially timezone-adjusted datetime
        """

        def has_utc_offset(dt_str: str) -> bool:
            """Check if the ISO string has a UTC offset."""
            return "Z" in dt_str or "+" in dt_str

        # Validate input type
        if not isinstance(dt, (str, datetime)):
            raise ValueError(
                f"`{dt_name}` should be a datetime or a string in ISO 8601 format: {dt}"
            )

        # If timezone is provided, enforce timezone rules
        if time_zone:
            validate_timezone(time_zone)

            # For string inputs
            if isinstance(dt, str):
                if has_utc_offset(dt):
                    raise ValueError(
                        f"`{dt_name}` should not have a UTC offset when `time_zone` is provided: {dt}"
                    )

                try:
                    dt_obj = datetime.fromisoformat(dt)
                except ValueError:
                    raise ValueError(f"Invalid ISO 8601 format: {dt}")

                # Localize the datetime
                return dt_obj.replace(tzinfo=ZoneInfo(time_zone)).isoformat()

            # For datetime inputs
            if dt.tzinfo and dt.tzinfo != ZoneInfo(time_zone):
                raise ValueError(f"`{dt_name}` should be in {time_zone} timezone: {dt}")

        return dt

    @classmethod
    def validate_datetime_with_timezone(
        cls,
        start: Union[str, datetime],
        end: Union[str, datetime, None],
        time_zone: Optional[str],
    ) -> tuple[Union[str, datetime], Union[str, datetime, None], Optional[str]]:
        """
        Ensures that `start` and `end` conform to timezone constraints.
        """
        # Validate start datetime
        validated_start = cls._validate_single_datetime(start, time_zone, "start")

        # Validate end datetime if provided
        validated_end = (
            cls._validate_single_datetime(end, time_zone, "end") if end else None
        )

        return validated_start, validated_end, time_zone

    def __init__(self, **data):
        # Validate and update datetime fields
        checked_start, checked_end, checked_tz = self.validate_datetime_with_timezone(
            data.get("start"), data.get("end"), data.get("time_zone")
        )

        # Update data with validated values
        data.update(
            {
                "start": checked_start,
                **({"end": checked_end} if checked_end is not None else {}),
                **({"time_zone": checked_tz} if checked_tz is not None else {}),
            }
        )

        super().__init__(**data)
