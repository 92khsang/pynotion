from __future__ import annotations as _annotations

from enum import StrEnum
from typing import Optional, Literal, Union, TypeAlias, Annotated

from pydantic import Field, BeforeValidator

from ._internal import (
    NotionBaseModel,
    NotionTypedModel,
    register_notion_type_enum,
    register_type_data,
    validate_enum,
)
from .types import (
    NotionEquation,
    Color,
    BackgroundColor,
    NotionLink,
    NotionUrl,
    NotionDate,
    ObjectId,
)
from .user import User


# ---------------------- ENUMS ---------------------- #
@register_notion_type_enum
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


@register_notion_type_enum
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


@register_notion_type_enum
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
class Annotations(NotionBaseModel):
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
        Union[Color, BackgroundColor | str],
        BeforeValidator(lambda v: validate_enum(v, (Color, BackgroundColor))),
    ] = Color.DEFAULT


# ---------------------- Text ---------------------- #
@register_type_data(RichTextType.TEXT)
class Text(NotionBaseModel):
    """Represents a text type and optional link.

    Attributes:
        content: The text content
        link: The link object.

    References:
        https://developers.notion.com/reference/rich-text#text
    """

    content: Annotated[str, Field(max_length=2000, description="The text content.")]
    link: Annotated[
        Union[str, NotionLink, None],
        BeforeValidator(
            lambda v: NotionLink(url=NotionUrl(v)) if isinstance(v, str) else v
        ),
    ] = None


# ---------------------- Equation ---------------------- #
Equation: TypeAlias = NotionEquation
register_type_data(RichTextType.EQUATION, Equation)


# ---------------------- Mentions ---------------------- #
@register_type_data(MentionType.PAGE)
@register_type_data(MentionType.DATABASE)
class MentionObjectId(NotionBaseModel):
    """Wrapper class for ObjectId.

    Attributes:
        id: The ObjectId. It's a UUID format.

    """

    id: ObjectId


@register_type_data(MentionType.TEMPLATE_MENTION)
class TemplateMentionDate(NotionTypedModel):
    """Represents a template mention for a date.

    Attributes:
        type: The type of the mention.
        type_data: The data related to this particularly mentioned instance.

    References:
        https://developers.notion.com/reference/rich-text#template-mention-type-object
    """

    type: TemplateMentionType = Field(
        default=TemplateMentionType.TEMPLATE_MENTION_DATE, frozen=True, init=False
    )
    type_data: Literal["today", "now"]

    register_type_data(
        TemplateMentionType.TEMPLATE_MENTION_DATE, Literal["today", "now"]
    )


@register_type_data(MentionType.TEMPLATE_MENTION)
class TemplateMentionUser(NotionTypedModel):
    """Represents a template mention for a user.

    Attributes:
        type: The type of the mention.
        type_data: The data related to this particularly mentioned instance.

    References:
        https://developers.notion.com/reference/rich-text#template-mention-type-object
    """

    type: TemplateMentionType = Field(
        default=TemplateMentionType.TEMPLATE_MENTION_USER, frozen=True, init=False
    )
    type_data: Literal["me"] = Field(default="me", frozen=True, init=False)

    register_type_data(TemplateMentionType.TEMPLATE_MENTION_USER, Literal["me"])


@register_type_data(RichTextType.MENTION)
class MentionDatabase(NotionTypedModel):
    """Represents a database mention.

    Attributes:
        type: The type of the mention.
        type_data: The data related to this particularly mentioned instance.

    References:
        https://developers.notion.com/reference/rich-text#database-mention-type-object
    """

    type: MentionType = Field(default=MentionType.DATABASE, frozen=True, init=False)
    type_data: MentionObjectId


@register_type_data(RichTextType.MENTION)
class MentionDate(NotionTypedModel):
    """Represents a date mention.

    Attributes:
        type: The type of the mention.
        type_data: The data related to this particularly mentioned instance.

    References:
        https://developers.notion.com/reference/rich-text#date-mention-type-object
    """

    type: MentionType = Field(default=MentionType.DATE, frozen=True, init=False)
    type_data: NotionDate

    register_type_data(MentionType.DATE, NotionDate)


@register_type_data(RichTextType.MENTION)
class MentionLinkPreview(NotionTypedModel):
    """Represents a link preview mention.

    Attributes:
        type: The type of the mention.
        type_data: The data related to this particularly mentioned instance.

    References:
        https://developers.notion.com/reference/rich-text#link-preview-mention-type-object
    """

    type: MentionType = Field(default=MentionType.LINK_PREVIEW, frozen=True, init=False)
    type_data: Annotated[
        Union[str, NotionLink],
        BeforeValidator(
            lambda v: NotionLink(url=NotionUrl(v)) if isinstance(v, str) else v
        ),
    ]

    register_type_data(MentionType.LINK_PREVIEW, NotionLink)


@register_type_data(RichTextType.MENTION)
class MentionPage(NotionTypedModel):
    """Represents a page mention.

    Attributes:
        type: The type of the mention.
        type_data: The data related to this particularly mentioned instance.

    References:
        https://developers.notion.com/reference/rich-text#page-mention-type-object
    """

    type: MentionType = Field(default=MentionType.PAGE, frozen=True, init=False)
    type_data: MentionObjectId


@register_type_data(RichTextType.MENTION)
class MentionDateTemplate(NotionTypedModel):
    """Represents a template mention for a date.

    Attributes:
        type: The type of the mention.
        type_data: The data related to this particularly mentioned instance.

    References:
        https://developers.notion.com/reference/rich-text#template-mention-type-object
    """

    type: MentionType = Field(
        default=MentionType.TEMPLATE_MENTION, frozen=True, init=False
    )
    type_data: TemplateMentionDate


@register_type_data(RichTextType.MENTION)
class MentionUserTemplate(NotionTypedModel):
    """Represents a template mention for a user.

    Attributes:
        type: The type of the mention.
        type_data: The data related to this particularly mentioned instance.

    References:
        https://developers.notion.com/reference/rich-text#template-mention-type-object
    """

    type: MentionType = Field(
        default=MentionType.TEMPLATE_MENTION, frozen=True, init=False
    )
    type_data: TemplateMentionUser = Field(
        default_factory=TemplateMentionUser, frozen=True, init=False
    )


@register_type_data(RichTextType.MENTION)
class MentionUser(NotionTypedModel):
    """Represents a user mention.

    Attributes:
        type: The type of the mention.
        type_data: The data related to this particularly mentioned instance.

    References:
        https://developers.notion.com/reference/rich-text#user-mention-type-object
    """

    type: MentionType = Field(default=MentionType.USER, frozen=True, init=False)
    type_data: User

    register_type_data(MentionType.USER, User)


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
class RichText(NotionTypedModel):
    """Represents a rich text object.

    Attributes:
        type: The type of the rich text object.
        type_data: The data related to this particular rich text object.
        annotations: The information is used to style the rich text object.
        plain_text: The plain text without annotations.
        href: The URL of any link or Notion mentioned in this text, if any.

    References:
        https://developers.notion.com/reference/rich-text
    """

    type: RichTextType = Field(
        description='The type of this rich text object. Possible type values are: "text", "mention", "equation".'
    )

    type_data: Union[Text, Equation, Mention] = Field(
        description="An object containing type-specific configuration. Refer to the rich text type objects section below for details on type-specific values."
    )

    annotations: Annotations = Field(
        default_factory=Annotations,
        description="The information is used to style the rich text object. Refer to the annotation object section below for details.",
    )

    plain_text: str = Field(
        description="The plain text without annotations.",
        examples=["Some words "],
        max_length=2000,
    )

    href: Optional[NotionUrl] = Field(
        default=None,
        description="The URL of any link or Notion mentioned in this text, if any.",
        examples=["https://www.notion.so/Avocado-d093f1d200464ce78b36e58a3f0d8043"],
    )
