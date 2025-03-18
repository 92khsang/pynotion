from enum import Enum
from typing import Literal, Annotated, Optional

from pydantic import Field, BeforeValidator

from ._internal import (
    validate_enum,
    BaseNotionModel,
    validate_url,
)
from .object import NotionObjectRef
from .types import Color, BackgroundColor, NotionDate, NotionEquation, NotionUrlObject
from .user import User


class RichTextType(str, Enum):
    """Defines rich text types in Notion.

    Attributes:
        TEXT: Text rich text type.
        EQUATION: equation rich text type.
        MENTION: mention a rich text type.

    References:
        https://developers.notion.com/reference/rich-text
    """

    TEXT = "text"
    EQUATION = "equation"
    MENTION = "mention"


class MentionType(str, Enum):
    """Defines mention types in Notion.

    Attributes:
        DATABASE: database mention type.
        DATE: date mention type.
        LINK_PREVIEW: link preview mentions type.
        PAGE: page a mention type.
        TEMPLATE_MENTION: template mention type.
        USER: user mention type.

    References:
        https://developers.notion.com/reference/rich-text#mention
    """

    DATABASE = "database"
    DATE = "date"
    LINK_PREVIEW = "link_preview"
    PAGE = "page"
    TEMPLATE_MENTION = "template_mention"
    USER = "user"


class TemplateMentionType(str, Enum):
    """Defines template mention types in Notion.

    Attributes:
        TEMPLATE_MENTION_DATE: a template mention type is date.
        TEMPLATE_MENTION_USER: a template mention type is user.

    References:
        https://developers.notion.com/reference/rich-text#template-mention-type-object
    """

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

    bold: Optional[bool] = Field(default=None)
    italic: Optional[bool] = Field(default=None)
    strikethrough: Optional[bool] = Field(default=None)
    underline: Optional[bool] = Field(default=None)
    code: Optional[bool] = Field(default=None)
    color: Optional[
        Annotated[
            Color | BackgroundColor | str,
            BeforeValidator(lambda v: validate_enum(v, (Color, BackgroundColor))),
        ]
    ] = Field(default=None)


class Text(BaseNotionModel):
    """Represents a rich text object.

    Attributes:
        content: The text content
        link: The link object.
    """

    content: Annotated[str, Field(max_length=2000)]
    link: Optional[NotionUrlObject] = Field(default=None)


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


class UserMention(BaseNotionModel):
    type: Literal[MentionType.USER] = Field(default=MentionType.USER, frozen=True)
    user: User


Mention = Annotated[
    DatabaseMention
    | DateMention
    | LinkPreviewMention
    | PageMention
    | TemplateMention
    | UserMention,
    Field(discriminator="type"),
]


class _BaseRichText(BaseNotionModel):
    """Represents a rich text object.

    Attributes:
        annotations: The information is used to style the rich text object.
        plain_text: The plain text without annotations.
        href: The URL of any link or Notion mentioned in this text, if any.

    References:
        https://developers.notion.com/reference/rich-text
    """

    annotations: Optional[Annotations] = Field(default=None)
    plain_text: Optional[str] = Field(default=None)
    href: Optional[Annotated[str, BeforeValidator(validate_url)]] = Field(default=None)


class TextRichText(_BaseRichText):
    type: Literal[RichTextType.TEXT] = Field(default=RichTextType.TEXT)
    text: Text


class EquationRichText(_BaseRichText):
    type: Literal[RichTextType.EQUATION] = Field(default=RichTextType.EQUATION)
    equation: Equation


class MentionRichText(_BaseRichText):
    type: Literal[RichTextType.MENTION] = Field(default=RichTextType.MENTION)
    mention: Mention


RichText = Annotated[
    TextRichText | EquationRichText | MentionRichText, Field(discriminator="type")
]
