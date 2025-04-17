from typing import Annotated, Optional, Literal, TYPE_CHECKING, Union

from pydantic import Field, BeforeValidator

from pynotion.models.rich_text.types import MentionType, RichTextType
from .._internal import BaseNotionModel, FrozenNotionModel, validate_url
from .._internal.utils import discriminate_field

if TYPE_CHECKING:
    from pynotion.models import (
        NotionUser,
        Annotations,
        Text,
        Equation,
    )


__all__ = [
    "RxMention",
    "RxTextRichText",
    "RxEquationRichText",
    "RxMentionRichText",
    "RxUserMention",
    "RxRichText",
    "RX_MENTION_CLASS_MAP",
    "RX_RICH_TEXT_CLASS_MAP",
]


class RxUserMention(BaseNotionModel):
    """Represents a user mention.

    Attributes:
        type: The type of the mention. Always "user".
        user: The user
    """

    type: Literal[MentionType.USER] = Field(default=MentionType.USER, frozen=True)
    user: "NotionUser"


RX_MENTION_CLASS_MAP = {
    MentionType.DATE: "DateMention",
    MentionType.DATABASE: "DatabaseMention",
    MentionType.LINK_PREVIEW: "LinkPreviewMention",
    MentionType.PAGE: "PageMention",
    MentionType.TEMPLATE_MENTION: "TemplateMention",
    MentionType.USER: "RxUserMention",
}

RxMention = Annotated[
    Union[tuple(RX_MENTION_CLASS_MAP.values())],
    BeforeValidator(lambda v: discriminate_field(v, "type", RX_MENTION_CLASS_MAP)),
]


class _RxBaseRichText(FrozenNotionModel):
    annotations: "Annotations"
    plain_text: Optional[str]
    href: Optional[Annotated[str, BeforeValidator(validate_url)]]


class RxTextRichText(_RxBaseRichText):
    """Represents a text rich text object.

    Attributes:
        annotations: The information is used to style the rich text object.
        plain_text: The plain text without annotations.
        href: The URL of any link or Notion mentioned in this text, if any.
        type: The type of the rich text object. Always "text".
        text: The text content

    References:
        https://developers.notion.com/reference/rich-text
    """

    type: Literal[RichTextType.TEXT] = Field(default=RichTextType.TEXT)
    text: "Text"


class RxEquationRichText(_RxBaseRichText):
    """Represents an equation rich text object.

    Attributes:
        annotations: The information is used to style the rich text object.
        plain_text: The plain text without annotations.
        href: The URL of any link or Notion mentioned in this text, if any.
        type: The type of the rich text object. Always "equation".
        equation: The equation content
    """

    type: Literal[RichTextType.EQUATION] = Field(default=RichTextType.EQUATION)
    equation: "Equation"


class RxMentionRichText(_RxBaseRichText):
    """Represents a mention rich text object.

    Attributes:
        annotations: The information is used to style the rich text object.
        plain_text: The plain text without annotations.
        href: The URL of any link or Notion mentioned in this text, if any.
        type: The type of the rich text object. Always "mention".
        mention: The mention content
    """

    type: Literal[RichTextType.MENTION] = Field(default=RichTextType.MENTION)
    mention: "RxMention"


RX_RICH_TEXT_CLASS_MAP = {
    RichTextType.TEXT: "RxTextRichText",
    RichTextType.EQUATION: "RxEquationRichText",
    RichTextType.MENTION: "RxMentionRichText",
}

if not TYPE_CHECKING:
    RxRichText = Annotated[
        Union[tuple(RX_RICH_TEXT_CLASS_MAP.values())],
        BeforeValidator(
            lambda v: discriminate_field(v, "type", RX_RICH_TEXT_CLASS_MAP)
        ),
    ]
else:
    RxRichText = Union[RxTextRichText, RxEquationRichText, RxMentionRichText]
