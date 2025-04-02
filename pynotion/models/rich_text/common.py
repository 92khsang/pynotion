from typing import Annotated, Optional, Literal, TYPE_CHECKING, Any

from pydantic import Field, BeforeValidator

from pynotion.models.rich_text.types import MentionType, TemplateMentionType
from .._internal import BaseNotionModel, validate_enum
from .._internal.utils import discriminate_field

if TYPE_CHECKING:
    from pynotion.models.object import NotionObjectIdWrapper
    from pynotion.models.types import (
        Color,
        BackgroundColor,
        NotionDate,
        NotionUrlWrapper,
    )


__all__ = [
    "Annotations",
    "Text",
    "Equation",
    "DatabaseMention",
    "DateMention",
    "LinkPreviewMention",
    "PageMention",
    "TemplateMentionDate",
    "TemplateMentionUser",
    "TemplateMention",
    "TEMPLATE_MENTION_CLASS_MAP",
]


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
        "Color | BackgroundColor | str",
        BeforeValidator(lambda v: validate_enum(v, (Color, BackgroundColor))),
    ] = "default"


class Text(BaseNotionModel):
    """Represents a rich text object.

    Attributes:
        content: The text content
        link: The link object.
    """

    content: Annotated[str, Field(max_length=2000)]
    link: Optional["NotionUrlWrapper"] = None


class Equation(BaseNotionModel):
    """Represents an equation.

    Attributes:
        expression: The expression of the equation
    """

    expression: str


class DatabaseMention(BaseNotionModel):
    """Represents a database mention.

    Attributes:
        type: The type of the mention. Always "database".
        database: The ID of the database
    """

    type: Literal[MentionType.DATABASE] = Field(
        default=MentionType.DATABASE, frozen=True
    )
    database: "NotionObjectIdWrapper"


class DateMention(BaseNotionModel):
    """Represents a date mention.

    Attributes:
        type: The type of the mention. Always "date".
        date: The date
    """

    type: Literal[MentionType.DATE] = Field(default=MentionType.DATE, frozen=True)
    date: "NotionDate"


class LinkPreviewMention(BaseNotionModel):
    """Represents a link preview mention.

    Attributes:
        type: The type of the mention. Always "link_preview".
        link_preview: The URL of the link
    """

    type: Literal[MentionType.LINK_PREVIEW] = Field(
        default=MentionType.LINK_PREVIEW, frozen=True
    )
    link_preview: "NotionUrlWrapper"


class PageMention(BaseNotionModel):
    """Represents a page mention.

    Attributes:
        type: The type of the mention. Always "page".
        page: The ID of the page.
    """

    type: Literal[MentionType.PAGE] = Field(default=MentionType.PAGE, frozen=True)
    page: "NotionObjectIdWrapper"


class TemplateMentionDate(BaseNotionModel):
    """Represents a template mention date.

    Attributes:
        type: The type of the mention. Always "template_mention_date".
        template_mention_date: Always "today" or "now"
    """

    type: Literal[TemplateMentionType.TEMPLATE_MENTION_DATE] = Field(
        default=TemplateMentionType.TEMPLATE_MENTION_DATE,
        frozen=True,
    )
    template_mention_date: Literal["today", "now"]


class TemplateMentionUser(BaseNotionModel):
    """Represents a template mention user.

    Attributes:
        type: The type of the mention. Always "template_mention_user".
        template_mention_user: Always "me"
    """

    type: Literal[TemplateMentionType.TEMPLATE_MENTION_USER] = Field(
        default=TemplateMentionType.TEMPLATE_MENTION_USER, frozen=True
    )
    template_mention_user: Literal["me"] = Field(default="me", frozen=True)


TEMPLATE_MENTION_CLASS_MAP = {
    TemplateMentionType.TEMPLATE_MENTION_DATE: "TemplateMentionDate",
    TemplateMentionType.TEMPLATE_MENTION_USER: "TemplateMentionUser",
}


class TemplateMention(BaseNotionModel):
    """Represents a template mention.

    Attributes:
        type: The type of the mention. Always "template_mention".
        template_mention: The template mention
    """

    type: Literal[MentionType.TEMPLATE_MENTION] = Field(
        default=MentionType.TEMPLATE_MENTION, frozen=True
    )
    template_mention: Annotated[
        Any,
        BeforeValidator(
            lambda v: discriminate_field(v, "type", TEMPLATE_MENTION_CLASS_MAP)
        ),
    ]
