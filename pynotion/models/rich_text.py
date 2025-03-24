from enum import Enum
from typing import Literal, Annotated, Optional

from pydantic import Field, BeforeValidator

from ._internal import (
    validate_enum,
    BaseNotionModel,
    validate_url,
    FrozenNotionModel,
)
from .object import NotionObjectRef
from .types import Color, BackgroundColor, NotionDate, NotionEquation, NotionUrlObject
from .user import User, UserRef


class RichTextType(str, Enum):
    """Rich text types in Notion."""

    TEXT = "text"
    EQUATION = "equation"
    MENTION = "mention"


class MentionType(str, Enum):
    """Mention types in Notion."""

    DATABASE = "database"
    DATE = "date"
    LINK_PREVIEW = "link_preview"
    PAGE = "page"
    TEMPLATE_MENTION = "template_mention"
    USER = "user"


class TemplateMentionType(str, Enum):
    """Defines template mention types in Notion."""

    TEMPLATE_MENTION_DATE = "template_mention_date"
    TEMPLATE_MENTION_USER = "template_mention_user"


class Annotations(BaseNotionModel):
    """
    Annotations for rich text.

    Attributes:
        bold: Whether the text is bold.
        italic: Whether the text is italic.
        strikethrough: Whether the text is strikethrough.
        underline: Whether the text is underlined.
        code: Whether the text is code.
        color: The color of the text.

    References:
        https://developers.notion.com/reference/rich-text#the-annotation-object
    """

    bold: bool = False
    italic: bool = False
    strikethrough: bool = False
    underline: bool = False
    code: bool = False
    color: Annotated[
        Color | BackgroundColor | str,
        BeforeValidator(lambda v: validate_enum(v, (Color, BackgroundColor))),
        Field(default=Color.DEFAULT),
    ]


class Text(BaseNotionModel):
    """Represents a rich text object.

    Attributes:
        content: The text content
        link: The link object.
    """

    content: Annotated[str, Field(max_length=2000)]
    link: Optional[NotionUrlObject] = None


class Equation(NotionEquation):
    """Represents an equation.

    Attributes:
        expression: The expression of the equation
    """

    pass


class DatabaseMention(BaseNotionModel):
    """Represents a database mention.

    Attributes:
        type: The type of the mention. Always "database".
        database: The ID of the database
    """

    type: Literal[MentionType.DATABASE] = Field(
        default=MentionType.DATABASE, frozen=True
    )
    database: NotionObjectRef


class DateMention(BaseNotionModel):
    """Represents a date mention.

    Attributes:
        type: The type of the mention. Always "date".
        date: The date
    """

    type: Literal[MentionType.DATE] = Field(default=MentionType.DATE, frozen=True)
    date: NotionDate


class LinkPreviewMention(BaseNotionModel):
    type: Literal[MentionType.LINK_PREVIEW] = Field(
        default=MentionType.LINK_PREVIEW, frozen=True
    )
    link_preview: NotionUrlObject


class PageMention(BaseNotionModel):
    type: Literal[MentionType.PAGE] = Field(default=MentionType.PAGE, frozen=True)
    page: NotionObjectRef


class TemplateMentionDate(BaseNotionModel):
    type: Literal[TemplateMentionType.TEMPLATE_MENTION_DATE] = Field(
        default=TemplateMentionType.TEMPLATE_MENTION_DATE,
        frozen=True,
    )
    template_mention_date: Literal["today", "now"]


class TemplateMentionUser(BaseNotionModel):
    type: Literal[TemplateMentionType.TEMPLATE_MENTION_USER] = Field(
        default=TemplateMentionType.TEMPLATE_MENTION_USER, frozen=True
    )
    template_mention_user: Literal["me"] = Field(default="me", frozen=True)


class TemplateMention(BaseNotionModel):
    type: Literal[MentionType.TEMPLATE_MENTION] = Field(
        default=MentionType.TEMPLATE_MENTION, frozen=True
    )
    template_mention: Annotated[
        TemplateMentionDate | TemplateMentionUser,
        Field(discriminator="type"),
    ]


class RxUserMention(BaseNotionModel):
    type: Literal[MentionType.USER] = Field(default=MentionType.USER, frozen=True)
    user: User


class TxUserMention(BaseNotionModel):
    type: Literal[MentionType.USER] = Field(default=MentionType.USER, frozen=True)
    user: UserRef


RxMention = Annotated[
    DatabaseMention
    | DateMention
    | LinkPreviewMention
    | PageMention
    | TemplateMention
    | RxUserMention,
    Field(discriminator="type"),
]

TxMention = Annotated[
    DatabaseMention
    | DateMention
    | LinkPreviewMention
    | PageMention
    | TemplateMention
    | TxUserMention,
    Field(discriminator="type"),
]


class _RxBaseRichText(FrozenNotionModel):
    """Represents a rich text object.

    Attributes:
        annotations: The information is used to style the rich text object.
        plain_text: The plain text without annotations.
        href: The URL of any link or Notion mentioned in this text, if any.

    References:
        https://developers.notion.com/reference/rich-text
    """

    annotations: Annotations
    plain_text: Optional[str]
    href: Optional[Annotated[str, BeforeValidator(validate_url)]]


class RxTextRichText(_RxBaseRichText):
    type: Literal[RichTextType.TEXT] = Field(default=RichTextType.TEXT)
    text: Text


class RxEquationRichText(_RxBaseRichText):
    type: Literal[RichTextType.EQUATION] = Field(default=RichTextType.EQUATION)
    equation: Equation


class RxMentionRichText(_RxBaseRichText):
    type: Literal[RichTextType.MENTION] = Field(default=RichTextType.MENTION)
    mention: RxMention


RxRichText = Annotated[
    RxTextRichText | RxEquationRichText | RxMentionRichText, Field(discriminator="type")
]


class _TxBaseRichText(BaseNotionModel):
    """Represents a rich text object.

    Attributes:
        annotations: The information is used to style the rich text object.

    References:
        https://developers.notion.com/reference/rich-text
    """

    annotations: Optional[Annotations] = None


class TxTextRichText(_TxBaseRichText):
    type: Literal[RichTextType.TEXT] = Field(default=RichTextType.TEXT)
    text: Text


class TxEquationRichText(_TxBaseRichText):
    type: Literal[RichTextType.EQUATION] = Field(default=RichTextType.EQUATION)
    equation: Equation


class TxMentionRichText(_TxBaseRichText):
    type: Literal[RichTextType.MENTION] = Field(default=RichTextType.MENTION)
    mention: TxMention


TxRichText = Annotated[
    TxTextRichText | TxEquationRichText | TxMentionRichText, Field(discriminator="type")
]
