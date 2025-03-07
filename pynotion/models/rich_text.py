from __future__ import annotations as _annotations

from enum import StrEnum
from typing import Literal, Union, TypeAlias, Annotated, get_args

from pydantic import Field, BeforeValidator, PrivateAttr

from ._internal import (
    BaseNotionModel,
    TypeObjectModel,
    validate_enum,
    FixedTypeObjectModel,
)
from .types import (
    NotionEquation,
    Color,
    BackgroundColor,
    NotionLink,
    NotionUrl,
    NotionDate,
    PartialUser,
    IdLinkObject,
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

    content: Annotated[str, Field(max_length=2000, description="The text content.")]
    link: (
        Annotated[
            str | NotionLink,
            BeforeValidator(
                lambda v: NotionLink(url=NotionUrl(v)) if isinstance(v, str) else v
            ),
        ]
        | None
    ) = None


# ---------------------- Equation ---------------------- #
Equation: TypeAlias = NotionEquation


# ---------------------- Mentions ---------------------- #
class TemplateMentionDate(FixedTypeObjectModel):
    """Represents a template mention for a date.

    Attributes:
        type: The type of the mention.
        type_object: The data related to this particularly mentioned instance.

    References:
        https://developers.notion.com/reference/rich-text#template-mention-type-object
    """

    __type_object_map__ = {
        TemplateMentionType.TEMPLATE_MENTION_DATE: Literal["today", "now"]
    }

    _type: TemplateMentionType = PrivateAttr(
        default=TemplateMentionType.TEMPLATE_MENTION_DATE
    )

    type_object: Literal["today", "now"]


class TemplateMentionUser(FixedTypeObjectModel):
    """Represents a template mention for a user.

    Attributes:
        type: The type of the mention.
        type_object: The data related to this particularly mentioned instance.

    References:
        https://developers.notion.com/reference/rich-text#template-mention-type-object
    """

    __type_object_map__ = {TemplateMentionType.TEMPLATE_MENTION_USER: Literal["me"]}

    _type: TemplateMentionType = PrivateAttr(
        default=TemplateMentionType.TEMPLATE_MENTION_USER
    )

    type_object: Literal["me"]


class MentionDatabase(FixedTypeObjectModel):
    """Represents a database mention.

    Attributes:
        type: The type of the mention.
        type_object: The data related to this particularly mentioned instance.

    References:
        https://developers.notion.com/reference/rich-text#database-mention-type-object
    """

    __type_object_map__ = {MentionType.DATABASE: IdLinkObject}

    _type: MentionType = PrivateAttr(default=MentionType.DATABASE)

    type_object: IdLinkObject


class MentionDate(FixedTypeObjectModel):
    """Represents a date mention.

    Attributes:
        type: The type of the mention.
        type_object: The data related to this particularly mentioned instance.

    References:
        https://developers.notion.com/reference/rich-text#date-mention-type-object
    """

    __type_object_map__ = {MentionType.DATE: NotionDate}

    _type: MentionType = PrivateAttr(default=MentionType.DATE)

    type_object: NotionDate


class MentionLinkPreview(FixedTypeObjectModel):
    """Represents a link preview mention.

    Attributes:
        type: The type of the mention.
        type_object: The data related to this particularly mentioned instance.

    References:
        https://developers.notion.com/reference/rich-text#link-preview-mention-type-object
    """

    __type_object_map__ = {MentionType.LINK_PREVIEW: NotionLink}

    _type: MentionType = PrivateAttr(default=MentionType.LINK_PREVIEW)

    type_object: Annotated[
        str | NotionLink,
        BeforeValidator(
            lambda v: NotionLink(url=NotionUrl(v)) if isinstance(v, str) else v
        ),
    ]


class MentionPage(FixedTypeObjectModel):
    """Represents a page mention.

    Attributes:
        type: The type of the mention.
        type_object: The data related to this particularly mentioned instance.

    References:
        https://developers.notion.com/reference/rich-text#page-mention-type-object
    """

    __type_object_map__ = {MentionType.PAGE: IdLinkObject}

    _type: MentionType = PrivateAttr(default=MentionType.PAGE)

    type_object: IdLinkObject


class MentionDateTemplate(FixedTypeObjectModel):
    """Represents a template mention for a date.

    Attributes:
        type: The type of the mention.
        type_object: The data related to this particularly mentioned instance.

    References:
        https://developers.notion.com/reference/rich-text#template-mention-type-object
    """

    __type_object_map__ = {MentionType.TEMPLATE_MENTION: TemplateMentionDate}

    _type: MentionType = PrivateAttr(default=MentionType.TEMPLATE_MENTION)

    type_object: TemplateMentionDate


class MentionUserTemplate(FixedTypeObjectModel):
    """Represents a template mention for a user.

    Attributes:
        type: The type of the mention.
        type_object: The data related to this particularly mentioned instance.

    References:
        https://developers.notion.com/reference/rich-text#template-mention-type-object
    """

    __type_object_map__ = {MentionType.TEMPLATE_MENTION: TemplateMentionUser}

    _type: MentionType = PrivateAttr(default=MentionType.TEMPLATE_MENTION)

    type_object: TemplateMentionUser = Field(frozen=True)


class MentionUser(FixedTypeObjectModel):
    """Represents a user mention.

    Attributes:
        type: The type of the mention.
        type_object: The data related to this particularly mentioned instance.

    References:
        https://developers.notion.com/reference/rich-text#user-mention-type-object
    """

    __type_object_map__ = {MentionType.USER: PartialUser}

    _type: MentionType = PrivateAttr(default=MentionType.USER)

    type_object: PartialUser


Mention = Union[
    MentionDatabase,
    MentionDate,
    MentionLinkPreview,
    MentionPage,
    MentionDateTemplate,
    MentionUserTemplate,
    MentionUser,
]


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
        RichTextType.MENTION: set(get_args(Mention)),
    }

    type: (
        Annotated[str, BeforeValidator(lambda v: validate_enum(v, (RichTextType,)))]
        | RichTextType
    ) = Field(frozen=True)

    type_object: Text | Equation | Mention = Field(
        description="An object containing type-specific configuration. Refer to the rich text type objects section below for details on type-specific values."
    )

    annotations: Annotations = Field(default_factory=Annotations)

    read_only_plain_text: str | None = Field(default=None, frozen=True)

    read_only_href: NotionUrl | None = Field(default=None, frozen=True)

    @property
    def plain_text(self) -> str | None:
        return self.read_only_plain_text

    @property
    def href(self) -> NotionUrl | None:
        return self.read_only_href
