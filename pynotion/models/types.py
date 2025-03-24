from __future__ import annotations as _annotations

from datetime import datetime
from enum import Enum
from typing import Annotated, Optional, Any
from zoneinfo import ZoneInfo

from pydantic import BeforeValidator, Field, model_validator

from ._internal import (
    validate_timezone,
    validate_datetime,
    BaseNotionModel,
    validate_url,
    validate_empty_dict,
)

NotionEmptyDict = Annotated[
    dict, BeforeValidator(validate_empty_dict), Field(default_factory=dict)
]


class Color(str, Enum):
    """Defines standard colors in Notion."""

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


class BackgroundColor(str, Enum):
    """Defines background colors in Notion."""

    BLUE_BACKGROUND = "blue_background"
    BROWN_BACKGROUND = "brown_background"
    GRAY_BACKGROUND = "gray_background"
    GREEN_BACKGROUND = "green_background"
    ORANGE_BACKGROUND = "orange_background"
    PURPLE_BACKGROUND = "purple_background"
    PINK_BACKGROUND = "pink_background"
    RED_BACKGROUND = "red_background"
    YELLOW_BACKGROUND = "yellow_background"


class NotionEquation(BaseNotionModel):
    """Represents an equation in Notion.

    Attributes:
        expression: The expression of the equation.
    """

    expression: str


class NotionUrlObject(BaseNotionModel):
    """Represents a URL object in Notion.

    Attributes:
        url: The URL of the object.
    """

    url: Annotated[str, BeforeValidator(validate_url)]


NotionDatetime = Annotated[str | datetime, BeforeValidator(validate_datetime)]


class NotionDate(BaseNotionModel):
    """Represents a date or datetime in Notion.

    Notion dates can represent a single point in time or a range with start and end times.
    They can optionally include timezone information.

    Attributes:
        start: The start datetime in ISO 8601 format.
        end: The end datetime in ISO 8601 format (optional).
        time_zone: The IANA timezone identifier (optional).

    Notes:
        - `start` and `end` must be in ISO 8601 format.
        - If `time_zone` is provided, `start` and `end` must not contain UTC offsets.
        - If `time_zone` is None, `start` and `end` can contain UTC offsets.
    """

    start: NotionDatetime
    end: Optional[NotionDatetime] = None
    time_zone: Optional[Annotated[str, BeforeValidator(validate_timezone)]] = Field(
        default=None
    )

    @classmethod
    def _validate_single_datetime(
        cls, dt: str | datetime, time_zone: str | None, dt_name: str
    ) -> str | datetime:
        """
        Validate and process a single datetime value according to Notion's datetime rules.

        Args:
            dt: Datetime value to validate (string in ISO 8601 format or datetime object).
            time_zone: IANA timezone identifier to validate against, if provided.
            dt_name: Name of the datetime field for error messages.

        Returns:
            The validated and potentially timezone-adjusted datetime.

        Raises:
            ValueError: If the datetime format is invalid or conflicts with timezone rules.
        """

        def has_utc_offset(dt_str: str) -> bool:
            """Check if the ISO string has a UTC offset (Z, + or - notation)."""
            dt_time_format = dt_str.split("T")[1] or ""
            utc_offset_chars = ["Z", "+", "-"]
            return any(char in dt_time_format for char in utc_offset_chars)

        # If timezone is provided, enforce timezone rules
        if time_zone:
            validate_timezone(time_zone)

            # For string inputs
            if isinstance(dt, str):
                if has_utc_offset(dt):
                    raise ValueError(
                        f"`{dt_name}` should not have a UTC offset when `time_zone` is provided: {dt}"
                    )

                dt_obj = datetime.fromisoformat(dt)

                # Localize the datetime
                return dt_obj.replace(tzinfo=ZoneInfo(time_zone)).isoformat()

        return dt

    @classmethod
    def validate_datetime_with_timezone(
        cls,
        start: str | datetime,
        end: str | datetime | None,
        time_zone: str | None,
    ) -> tuple[str | datetime, str | datetime | None, str | None]:
        """
        Ensures that `start` and `end` datetime conform to Notion's timezone constraints.

        Args:
            start: Start datetime value (string in ISO 8601 format or datetime object).
            end: End datetime value (string in ISO 8601 format, datetime object, or None).
            time_zone: IANA timezone identifier, if provided.

        Returns:
            Tuple of (validated start datetime, validated end datetime, validated timezone).

        Raises:
            ValueError: If any values fail validation according to Notion's datetime rules.
        """
        # Validate start datetime
        validated_start = cls._validate_single_datetime(start, time_zone, "start")

        # Validate end datetime if provided
        validated_end = (
            cls._validate_single_datetime(end, time_zone, "end") if end else None
        )

        return validated_start, validated_end, time_zone

    @model_validator(mode="before")
    @classmethod
    def _pre_init(cls, input_values: Any) -> Any:
        """
        Pre-validates and transforms date inputs before model initialization.

        Args:
            input_values: Raw input values (dictionary or ArgsKwargs).

        Returns:
            Validated and transformed input values.

        Raises:
            ValueError: If datetime values fail validation.
        """
        values = input_values.copy()
        data = dict(values) if isinstance(values, dict) else values.kwargs

        if data:

            def extract_value(key: str) -> Any:
                return (
                    data.get(key, None)
                    if isinstance(data, dict)
                    else getattr(data, key, None)
                )

            # Validate and update datetime fields
            checked_start, checked_end, checked_tz = (
                cls.validate_datetime_with_timezone(
                    extract_value("start"),
                    extract_value("end"),
                    extract_value("time_zone"),
                )
            )

            # Update data with validated values
            data.update(
                {
                    "start": checked_start,
                    **({"end": checked_end} if checked_end is not None else {}),
                    **({"time_zone": checked_tz} if checked_tz is not None else {}),
                }
            )

        return values
