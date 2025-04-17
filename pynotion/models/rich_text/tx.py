from typing import Annotated, Optional, Literal, TYPE_CHECKING, Union

from pydantic import Field, BeforeValidator

from pynotion.models.rich_text.types import MentionType, RichTextType
from .._internal import BaseNotionModel
from .._internal.utils import discriminate_field

if TYPE_CHECKING:
    from pynotion.models.user import UserRef
    from pynotion.models.rich_text.common import (
        Annotations,
        Text,
        Equation,
    )


__all__ = [
    "TxTextRichText",
    "TxEquationRichText",
    "TxMentionRichText",
    "TxUserMention",
    "TxMention",
    "TxRichText",
    "TX_MENTION_CLASS_MAP",
    "TX_RICH_TEXT_CLASS_MAP",
]


class TxUserMention(BaseNotionModel):
    """Represents a user mention.

    Attributes:
        type: The type of the mention. Always "user".
        user: The user reference
    """

    type: Literal[MentionType.USER] = Field(default=MentionType.USER, frozen=True)
    user: "UserRef"


TX_MENTION_CLASS_MAP = {
    MentionType.DATE: "DateMention",
    MentionType.DATABASE: "DatabaseMention",
    MentionType.LINK_PREVIEW: "LinkPreviewMention",
    MentionType.PAGE: "PageMention",
    MentionType.TEMPLATE_MENTION: "TemplateMention",
    MentionType.USER: "TxUserMention",
}

TxMention = Annotated[
    Union[tuple(TX_MENTION_CLASS_MAP.values())],
    BeforeValidator(lambda v: discriminate_field(v, "type", TX_MENTION_CLASS_MAP)),
]


class _TxBaseRichText(BaseNotionModel):
    """Represents a rich text object.

    Attributes:
        annotations: The information is used to style the rich text object.

    References:
        https://developers.notion.com/reference/rich-text
    """

    annotations: Optional["Annotations"] = None


class TxTextRichText(_TxBaseRichText):
    """Represents a text rich text object.

    Attributes:
        annotations: The information is used to style the rich text object.
        type: The type of the rich text object. Always "text".
        text: The text content
    """

    type: Literal[RichTextType.TEXT] = Field(default=RichTextType.TEXT)
    text: "Text"


class TxEquationRichText(_TxBaseRichText):
    """Represents an equation rich text object.

    Attributes:
        annotations: The information is used to style the rich text object.
        type: The type of the rich text object. Always "equation".
        equation: The equation content
    """

    type: Literal[RichTextType.EQUATION] = Field(default=RichTextType.EQUATION)
    equation: "Equation"


class TxMentionRichText(_TxBaseRichText):
    """Represents a mention rich text object.

    Attributes:
        annotations: The information is used to style the rich text object.
        type: The type of the rich text object. Always "mention".
        mention: The mention content
    """

    type: Literal[RichTextType.MENTION] = Field(default=RichTextType.MENTION)
    mention: TxMention


TX_RICH_TEXT_CLASS_MAP = {
    RichTextType.TEXT: "TxTextRichText",
    RichTextType.EQUATION: "TxEquationRichText",
    RichTextType.MENTION: "TxMentionRichText",
}

if not TYPE_CHECKING:
    TxRichText = Annotated[
        Union[tuple(TX_RICH_TEXT_CLASS_MAP.values())],
        BeforeValidator(
            lambda v: discriminate_field(v, "type", TX_RICH_TEXT_CLASS_MAP)
        ),
    ]
else:
    TxRichText = Union[TxTextRichText, TxEquationRichText, TxMentionRichText]
