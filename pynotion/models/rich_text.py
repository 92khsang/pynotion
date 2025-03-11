from __future__ import annotations as _annotations

from abc import ABC
from enum import StrEnum
from typing import Literal, Union, TypeAlias, Annotated, Any

from pydantic import Field, BeforeValidator, field_validator, model_validator

from ._internal import (
    BaseNotionModel,
    TypeObjectModel,
    validate_enum,
)
from .types import (
    Color,
    BackgroundColor,
    NotionDate as _NotionDate,
    NotionLink as _NotionLink,
    NotionUrl as _NotionUrl,
    NotionUserRef as _NotionUserRef,
    NotionObjectRef as _NotionObjectRef,
    NotionEquation as _NotionEquation,
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

    link: str | _NotionLink | None = Field(default=None)

    @field_validator("link", mode="before")
    def validate_link(cls, v):
        if v is None or isinstance(v, _NotionLink):
            return v
        return _NotionLink(url=_NotionUrl(v))


# ---------------------- Equation ---------------------- #
Equation: TypeAlias = _NotionEquation


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


MentionDatabase: TypeAlias = _NotionObjectRef
MentionDate: TypeAlias = _NotionDate
MentionPage: TypeAlias = _NotionObjectRef
MentionUser: TypeAlias = _NotionUserRef
MentionLinkPreview: TypeAlias = _NotionLink

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
RichTextHref: TypeAlias = _NotionUrl


class BaseRichText(TypeObjectModel, ABC):
    """Base class for rich text objects.

    Attributes:
        type: The type of the rich text object.
        type_object: The data related to this particular rich text object.

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

    @model_validator(mode="before")
    @classmethod
    def validate_abstract_clz(cls, values: Any) -> Any:
        if cls == BaseRichText:
            raise TypeError("Cannot instantiate abstract class BaseRichText")

        return values


class TxRichText(BaseRichText):
    """Represents a rich text object.

    Attributes:
        type: The type of the rich text object.
        type_object: The data related to this particular rich text object.
        annotations: The information is used to style the rich text object.

    References:
        https://developers.notion.com/reference/rich-text
    """

    annotations: Annotations = Field(default_factory=Annotations)


class RxRichText(BaseRichText):
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

    type_object: Text | Equation | Mention = Field(frozen=True)
    annotations: Annotations = Field(frozen=True)
    plain_text: str | None = Field(frozen=True)
    href: RichTextHref | None = Field(frozen=True)


RichText: TypeAlias = TxRichText | RxRichText
