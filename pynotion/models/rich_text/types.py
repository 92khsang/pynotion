from enum import Enum

__all__ = [
    "RichTextType",
    "MentionType",
    "TemplateMentionType",
]


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
