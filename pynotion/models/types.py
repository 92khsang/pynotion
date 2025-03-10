from __future__ import annotations as _annotations

import uuid
from abc import ABC
from datetime import datetime
from enum import StrEnum
from typing import TypeAlias, Annotated, Any, Literal
from zoneinfo import ZoneInfo

from pydantic import (
    Field,
    BeforeValidator,
    EmailStr,
    model_validator,
    PrivateAttr,
    computed_field,
)
from pydantic_core import ArgsKwargs, PydanticUndefined

from ._internal import (
    validate_timezone,
    validate_datetime,
    validate_url,
    BaseNotionModel,
    TypeObjectModel,
    validate_enum,
    validate_uuid4,
    validate_enum_value,
)

NotionObjectId: TypeAlias = Annotated[
    str | int | bytes | uuid.UUID, BeforeValidator(validate_uuid4)
]

NotionDatetime: TypeAlias = Annotated[
    str | datetime, BeforeValidator(validate_datetime)
]

NotionEmail: TypeAlias = Annotated[str, Field(..., max_length=200), EmailStr]

NotionUrl: TypeAlias = Annotated[
    str, Field(..., max_length=2000), BeforeValidator(validate_url)
]


class ObjectType(StrEnum):
    """Defines object types in Notion.

    These types correspond to the primary object categories in the Notion API.
    The 'object' field in API responses will contain one of these values.

    Attributes:
        BLOCK: Block object type, representing content blocks like paragraphs or lists.
        DATABASE: Database object type, representing structured data collections.
        PAGE: Page object type, representing Notion pages.
        USER: User object type, representing Notion users.
        COMMENT: Comment object type, representing comments on pages.
    """

    BLOCK = "block"
    DATABASE = "database"
    PAGE = "page"
    USER = "user"
    COMMENT = "comment"


class Color(StrEnum):
    """Defines standard colors in Notion.

    These colors are used for text, backgrounds, and other UI elements.

    Attributes:
        BLUE: Blue color.
        BROWN: Brown color.
        DEFAULT: Default color (usually black or determined by theme).
        GRAY: Gray color.
        GREEN: Green color.
        ORANGE: Orange color.
        PURPLE: Purple color.
        PINK: Pink color.
        RED: Red color.
        YELLOW: Yellow color.
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

    These colors are specifically for block backgrounds and highlights.

    Attributes:
        BLUE_BACKGROUND: Blue background color.
        BROWN_BACKGROUND: Brown background color.
        GRAY_BACKGROUND: Gray background color.
        GREEN_BACKGROUND: Green background color.
        ORANGE_BACKGROUND: Orange background color.
        PURPLE_BACKGROUND: Purple background color.
        PINK_BACKGROUND: Pink background color.
        RED_BACKGROUND: Red background color.
        YELLOW_BACKGROUND: Yellow background color.
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


class ParentType(StrEnum):
    """Defines the possible types of parents in Notion.

    Each Notion object (except for the workspace itself) has a parent.
    This enum defines all possible parent types.

    Attributes:
        DATABASE_ID: Parent is a database. The type_object will contain the database ID.
        PAGE_ID: Parent is a page. The type_object will contain the page ID.
        BLOCK_ID: Parent is a block. The type_object will contain the block ID.
        WORKSPACE: Parent is a workspace. The type_object will be True.
    """

    DATABASE_ID = "database_id"
    PAGE_ID = "page_id"
    BLOCK_ID = "block_id"
    WORKSPACE = "workspace"


class FileType(StrEnum):
    """Defines the possible file types in Notion.

    Attributes:
        FILE: File hosted by Notion with an expiry time.
        EXTERNAL: File hosted externally (linked by URL).
    """

    FILE = "file"
    EXTERNAL = "external"


class EmojiType(StrEnum):
    """Defines the possible emoji types in Notion.

    Attributes:
        EMOJI: Standard Unicode emoji.
        CUSTOM_EMOJI: Custom emoji uploaded to Notion.
    """

    EMOJI = "emoji"
    CUSTOM_EMOJI = "custom_emoji"


class NotionLink(BaseNotionModel):
    """Represents a URL link in Notion.

    This model is used for wrapping URLs in Notion.

    Attributes:
        url: The URL of the link, validated to ensure it's properly formatted.
    """

    url: NotionUrl


class NotionHostedFile(NotionLink):
    """Represents a file hosted by Notion.

    Notion-hosted files have a URL that expires after a period of time.

    Attributes:
        url: The URL of the hosted file.
        expiry_time: The ISO 8601 datetime when the URL will expire.
    """

    expiry_time: NotionDatetime


class NotionExternalFile(NotionLink):
    """Represents an externally hosted file in Notion.

    Attributes:
        url: The URL of the externally hosted file.
    """

    pass


class NotionEquation(BaseNotionModel):
    """Represents a LaTeX equation in Notion.

    Equations are rendered using KaTeX in the Notion UI.

    Attributes:
        expression: LaTeX expression string for the equation.
    """

    expression: str


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
    end: NotionDatetime | None = Field(default=None)
    time_zone: str | None = Field(default=None)

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
        start: str | datetime,
        end: str | datetime | None,
        time_zone: str | None,
    ) -> tuple[str | datetime, str | datetime | None, str | None]:
        """
        Ensures that `start` and `end` datetimes conform to Notion's timezone constraints.

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
    def _pre_init(cls, values: Any) -> Any:
        """
        Pre-validates and transforms date inputs before model initialization.

        Args:
            values: Raw input values (dictionary or ArgsKwargs).

        Returns:
            Validated and transformed input values.

        Raises:
            ValueError: If datetime values fail validation.
        """
        if not isinstance(values, (ArgsKwargs, dict)):
            return values

        data = values.kwargs if isinstance(values, ArgsKwargs) else values

        # Validate and update datetime fields
        checked_start, checked_end, checked_tz = cls.validate_datetime_with_timezone(
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

        return values


class NotionParent(TypeObjectModel):
    """Represents a parent object in Notion.

    In Notion, most objects have a parent that represents their container.
    The parent can be a database, page, block, or the workspace itself.

    Attributes:
        type: The type of the parent object (database_id, page_id, block_id, or workspace).
        type_object: The data related to this particular parent type.
            For database_id, page_id, and block_id, this will be an NotionObjectId.
            For workspace, this will be a boolean (True).

    References:
        https://developers.notion.com/reference/parent-object
    """

    __type_object_map__ = {
        ParentType.DATABASE_ID: uuid.UUID,
        ParentType.PAGE_ID: uuid.UUID,
        ParentType.BLOCK_ID: uuid.UUID,
        ParentType.WORKSPACE: bool,
    }

    type: Annotated[
        str | ParentType,
        BeforeValidator(lambda v: validate_enum(v, (ParentType,))),
        Field(frozen=True),
    ]

    type_object: bool | NotionObjectId


class NotionFile(TypeObjectModel):
    """Represents a file in Notion.

    Files in Notion can be either hosted by Notion with an expiry time
    or external files linked by URL.

    Attributes:
        type: The type of the file (file or external).
        type_object: The data related to this particular file type.
            For 'file' type, this will be a NotionHostedFile.
            For 'external' type, this will be a NotionLink.

    References:
        https://developers.notion.com/reference/file-object
    """

    __type_object_map__ = {
        FileType.FILE: NotionHostedFile,
        FileType.EXTERNAL: NotionExternalFile,
    }

    type: Annotated[
        str | FileType,
        BeforeValidator(lambda v: validate_enum(v, (FileType,))),
        Field(frozen=True),
    ]

    type_object: NotionHostedFile | NotionExternalFile


class CustomEmoji(NotionLink):
    """Represents a custom emoji in Notion.

    Custom emojis are uploaded images that can be used like regular emojis.

    Attributes:
        id: The unique identifier for the custom emoji.
        name: The display name of the custom emoji.
        url: The URL where the custom emoji image is hosted.

    References:
        https://developers.notion.com/reference/emoji-object#custom-emoji
    """

    id: NotionObjectId = Field(frozen=True)

    name: str = Field(frozen=True)


class NotionEmoji(TypeObjectModel):
    """Represents an emoji in Notion.

    Notion supports both standard Unicode emojis and custom uploaded emojis.

    Attributes:
        type: The type of the emoji (emoji or custom_emoji).
        type_object: The data related to this particular emoji type.
            For 'emoji' type, this will be a string with the Unicode emoji.
            For 'custom_emoji' type, this will be a CustomEmoji object.

    References:
        https://developers.notion.com/reference/emoji-object
    """

    __type_object_map__ = {
        EmojiType.EMOJI: str,
        EmojiType.CUSTOM_EMOJI: CustomEmoji,
    }

    type: Annotated[
        str | EmojiType,
        BeforeValidator(lambda v: validate_enum(v, (EmojiType,))),
        Field(frozen=True),
    ]

    type_object: str | CustomEmoji


class NotionObjectRef(BaseNotionModel):
    """Represents a reference to a Notion object.

    Attributes:
        id: The unique identifier for the referenced object.

    """

    id: NotionObjectId = Field(frozen=True)


class NotionUserRef(NotionObjectRef):
    """
    Represents a minimal user reference when a full User object isn't needed.

    This is often used in created_by and last_edited_by fields.

    Attributes:
        id: Unique identifier for the user.
        object: Always 'user', confirming this is a user reference.
    """

    __serializable_private_attrs__ = {"_object": "object"}

    _object: ObjectType = PrivateAttr(default=ObjectType.USER)

    def __init__(self, *, object: ObjectType | None = None, **data: Any):  # noqa
        """
        Initialize a NotionUserRef.

        Args:
            object: Must be ObjectType.USER if provided.
            **data: Other user data, must include 'id'.

        Raises:
            ValueError: If object is provided but is not ObjectType.USER.
        """
        if object and object != ObjectType.USER:
            raise ValueError(f"Invalid object type: {object}")

        super().__init__(**data)

    @computed_field
    @property
    def object(self) -> ObjectType:
        """
        The object type, always 'user'.

        Returns:
            ObjectType.USER: The string "user".
        """
        return self._object


class NotionObject(BaseNotionModel, ABC):
    """
    Base class for primary Notion objects (pages, databases, blocks).

    This class provides the common fields and behavior shared by
    the main Notion object types.

    Attributes:
        object: The type of this object (database, page, or block).
        parent: The parent object that contains this object.
        id: Unique identifier for this object.
        created_time: ISO 8601 datetime when this object was created.
        last_edited_time: ISO 8601 datetime when this object was last edited.
        created_by: User who created this object.
        last_edited_by: User who last edited this object.
        archived: Whether this object is archived (moved to trash).
        in_trash: Whether this object is in the trash bin.
    """

    __serializable_private_attrs__ = {"_object": "object"}

    _object: Literal[ObjectType.DATABASE, ObjectType.PAGE, ObjectType.BLOCK]

    parent: NotionParent | None = Field(default=None)

    read_only_id: NotionObjectId | None = Field(default=None, frozen=True)

    read_only_created_time: NotionDatetime | None = Field(default=None, frozen=True)

    read_only_last_edited_time: NotionDatetime | None = Field(default=None, frozen=True)

    read_only_created_by: NotionUserRef | None = Field(default=None, frozen=True)

    read_only_last_edited_by: NotionUserRef | None = Field(default=None, frozen=True)

    read_only_archived: bool | None = Field(default=None, frozen=True)

    read_only_in_trash: bool | None = Field(default=None, frozen=True)

    @classmethod
    def _validate_object_exists(cls) -> None:
        private_attr = cls.__private_attributes__.get("_object")
        if private_attr.default is PydanticUndefined:
            raise ValueError("_object must have a default value")

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)
        cls._validate_object_exists()

    def __init__(self, /, **data: Any):
        obj = data.pop("object", None) or self.__private_attributes__["_object"].default

        if obj:
            obj = validate_enum_value(
                obj, {ObjectType.DATABASE, ObjectType.PAGE, ObjectType.BLOCK}
            )

        super().__init__(**data)
        object.__setattr__(self, "_object", obj)

    @property
    def id(self) -> NotionObjectId | None:
        """
        The unique identifier for this object.

        Returns:
            NotionObjectId: The UUID of this object.
        """
        return self.read_only_id

    @property
    def created_time(self) -> NotionDatetime | None:
        """
        The time when this object was created.

        Returns:
            NotionDatetime: ISO 8601 datetime.
        """
        return self.read_only_created_time

    @property
    def last_edited_time(self) -> NotionDatetime | None:
        """
        The time when this object was last edited.

        Returns:
            NotionDatetime: ISO 8601 datetime.
        """
        return self.read_only_last_edited_time

    @property
    def created_by(self) -> NotionUserRef | None:
        """
        The user who created this object.

        Returns:
            NotionUserRef: Basic info about the creator.
        """
        return self.read_only_created_by

    @property
    def last_edited_by(self) -> NotionUserRef | None:
        """
        The user who last edited this object.

        Returns:
            NotionUserRef: Basic info about the last editor.
        """
        return self.read_only_last_edited_by

    @property
    def archived(self) -> bool | None:
        """
        Whether this object is archived.

        Returns:
            bool: True if archived, False otherwise.
        """
        return self.read_only_archived

    @property
    def in_trash(self) -> bool | None:
        """
        Whether this object is in the trash bin.

        Returns:
            bool: True if in trash, False otherwise.
        """
        return self.read_only_in_trash

    @property
    def object(self) -> ObjectType:
        """
        The type of this object.

        Returns:
            ObjectType: The type (database, page, or block).
        """
        return self._object
