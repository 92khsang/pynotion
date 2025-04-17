from __future__ import annotations as _annotations

from enum import Enum
from typing import Literal, Annotated, Union, TYPE_CHECKING
from uuid import UUID

from pydantic import Field, ConfigDict, BeforeValidator

from ._internal import BaseNotionModel, validate_url
from ._internal.utils import discriminate_field

__all__ = [
    "EmojiType",
    "CustomEmojiObject",
    "SingleEmoji",
    "CustomEmoji",
    "NotionEmoji",
    "EMOJI_CLASS_MAP",
]


class EmojiType(str, Enum):
    """Defines the possible emoji types in Notion."""

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

    id: UUID
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


EMOJI_CLASS_MAP = {
    EmojiType.EMOJI: "SingleEmoji",
    EmojiType.CUSTOM_EMOJI: "CustomEmoji",
}


if not TYPE_CHECKING:
    NotionEmoji = Annotated[
        Union[tuple(EMOJI_CLASS_MAP.values())],
        BeforeValidator(lambda v: discriminate_field(v, "type", EMOJI_CLASS_MAP)),
    ]
else:
    NotionEmoji = Union[SingleEmoji, CustomEmoji]
