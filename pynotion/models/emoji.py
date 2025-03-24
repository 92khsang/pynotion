from __future__ import annotations as _annotations

from enum import Enum
from typing import Literal, Annotated
from uuid import UUID

from pydantic import Field, ConfigDict, BeforeValidator

from ._internal import (
    BaseNotionModel,
    validate_uuid4,
    validate_url,
)


class EmojiType(str, Enum):
    """Defines the possible emoji types in Notion.

    Attributes:
        EMOJI: Standard Unicode emoji.
        CUSTOM_EMOJI: Custom emoji uploaded to Notion.
    """

    EMOJI = "emoji"
    CUSTOM_EMOJI = "custom_emoji"


class CustomEmojiObject(BaseNotionModel):
    """Represents a custom emoji in Notion.

    Custom emojis are uploaded images that can be used like regular emojis.

    Attributes:
        id: The unique identifier for the custom emoji.
        name: The display name of the custom emoji.
        url: The URL where the custom emoji image is hosted.

    References:
        https://developers.notion.com/reference/emoji-object#custom-emoji
    """

    model_config = ConfigDict(**BaseNotionModel.model_config, frozen=True)

    id: Annotated[str | int | bytes | UUID, BeforeValidator(validate_uuid4)]
    name: str
    url: Annotated[str, BeforeValidator(validate_url)]


class SingleEmoji(BaseNotionModel):
    """Represents a standard emoji in Notion.

    Attributes:
        type: The type of emoji.
        emoji: The standard Unicode emoji.
    """

    type: Literal[EmojiType.EMOJI] = Field(default=EmojiType.EMOJI, frozen=True)
    emoji: str


class CustomEmoji(BaseNotionModel):
    """Represents a custom emoji in Notion.

    Attributes:
        type: The type of emoji.
        custom_emoji: The custom emoji object.
    """

    type: Literal[EmojiType.CUSTOM_EMOJI] = Field(
        default=EmojiType.CUSTOM_EMOJI, frozen=True
    )
    custom_emoji: CustomEmojiObject


Emoji = Annotated[SingleEmoji | CustomEmoji, Field(discriminator="type")]
