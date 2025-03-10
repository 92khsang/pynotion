from __future__ import annotations as _annotations

from enum import StrEnum
from typing import Literal, Union, TypeAlias, Annotated

from pydantic import Field, BeforeValidator

from ._internal import (
    BaseNotionModel,
    TypeObjectModel,
    validate_enum,
)
from .types import (
    NotionEquation,
    Color,
    BackgroundColor,
    NotionLink,
    NotionUrl,
    NotionDate,
    NotionUserRef,
    NotionObjectRef,
)


# ---------------------- ENUMS ---------------------- #
class RichTextType(StrEnum):
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


class MentionType(StrEnum):
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


class TemplateMentionType(StrEnum):
    """Defines template mention types in Notion.

    Attributes:
        TEMPLATE_MENTION_DATE: a template mention type is date.
        TEMPLATE_MENTION_USER: a template mention type is user.

    References:
        https://developers.notion.com/reference/rich-text#template-mention-type-object
    """

    TEMPLATE_MENTION_DATE = "template_mention_date"
    TEMPLATE_MENTION_USER = "template_mention_user"


# ---------------------- Annotations ---------------------- #
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

    bold: bool = Field(default=False)
    italic: bool = Field(default=False)
    strikethrough: bool = Field(default=False)
    underline: bool = Field(default=False)
    code: bool = Field(default=False)
    color: Annotated[
        Color | BackgroundColor | str,
        BeforeValidator(lambda v: validate_enum(v, (Color, BackgroundColor))),
    ] = Color.DEFAULT


# ---------------------- Text ---------------------- #
class Text(BaseNotionModel):
    """Represents a text type and optional link.

    Attributes:
        content: The text content
        link: The link object.

    References:
        https://developers.notion.com/reference/rich-text#text
    """

    content: Annotated[str, Field(max_length=2000)]

    link: (
        Annotated[
            str | NotionLink, BeforeValidator(lambda v: NotionLink(url=NotionUrl(v)))
        ]
        | None
    ) = None


# ---------------------- Equation ---------------------- #
Equation: TypeAlias = NotionEquation


# ---------------------- Mentions ---------------------- #
class MentionTemplate(TypeObjectModel):
    __type_object_map__ = {
        TemplateMentionType.TEMPLATE_MENTION_DATE: Literal["today", "now"],
        TemplateMentionType.TEMPLATE_MENTION_USER: Literal["me"],
    }

    type: Annotated[
        str | TemplateMentionType,
        BeforeValidator(lambda v: validate_enum(v, (TemplateMentionType,))),
    ]

    type_object: Literal["today", "now"] | Literal["me"]


MentionDatabase: TypeAlias = NotionObjectRef
MentionDate: TypeAlias = NotionDate
MentionPage: TypeAlias = NotionObjectRef
MentionUser: TypeAlias = NotionUserRef
MentionLinkPreview: TypeAlias = NotionLink


MentionObjects = Union[
    MentionDatabase,
    MentionDate,
    MentionLinkPreview,
    MentionPage,
    MentionTemplate,
    MentionUser,
]


class Mention(TypeObjectModel):
    __type_object_map__ = {
        MentionType.DATABASE: MentionDatabase,
        MentionType.DATE: MentionDate,
        MentionType.LINK_PREVIEW: MentionLinkPreview,
        MentionType.PAGE: MentionPage,
        MentionType.TEMPLATE_MENTION: MentionTemplate,
        MentionType.USER: MentionUser,
    }

    type: Annotated[
        str | MentionType,
        BeforeValidator(lambda v: validate_enum(v, (MentionType,))),
    ]

    type_object: MentionObjects


# ---------------------- RichText ---------------------- #
class RichText(TypeObjectModel):
    """Represents a rich text object.

    Attributes:
        type: The type of the rich text object.
        type_object: The data related to this particular rich text object.
        annotations: The information is used to style the rich text object.
        plain_text: The plain text without annotations.
        href: The URL of any link or Notion mentioned in this text, if any.

    References:
        https://developers.notion.com/reference/rich-text
    """

    __type_object_map__ = {
        RichTextType.TEXT: Text,
        RichTextType.EQUATION: Equation,
        RichTextType.MENTION: Mention,
    }

    type: Annotated[
        str | RichTextType,
        BeforeValidator(lambda v: validate_enum(v, (RichTextType,))),
        Field(frozen=True),
    ]

    type_object: Text | Equation | Mention

    annotations: Annotations = Field(default_factory=Annotations)

    read_only_plain_text: str | None = Field(default=None, frozen=True)

    read_only_href: NotionUrl | None = Field(default=None, frozen=True)

    @property
    def plain_text(self) -> str | None:
        return self.read_only_plain_text

    @property
    def href(self) -> NotionUrl | None:
        return self.read_only_href
