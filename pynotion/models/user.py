from __future__ import annotations as _annotations

from enum import StrEnum
from typing import Optional, Union, TYPE_CHECKING, Annotated, Literal

from pydantic import Field, model_validator

from ._internal import (
    NotionBaseModel,
    NotionTypedModel,
    register_notion_type_enum,
    register_type_data,
)
from .types import (
    ObjectType,
    ObjectId,
    NotionEmail,
    NotionUrl,
)


# ---------------------- ENUMS ---------------------- #
@register_notion_type_enum
class UserType(StrEnum):
    """Defined user types in Notion.

    Attributes:
        PERSON: represents a user type for a person.
        BOT: represents a user type for a bot.

    References:
        https://developers.notion.com/reference/user#all-users
    """

    PERSON = "person"
    BOT = "bot"


@register_notion_type_enum
class BotOwnerType(StrEnum):
    """Defined bot owner types in Notion.

    Attributes:
        WORKSPACE: represents a bot owner type for a workspace.
        USER: represents a bot owner type for an individual user.

    References:
        https://developers.notion.com/reference/user#bots
    """

    WORKSPACE = "workspace"
    USER = "user"


# ---------------------- MODELS ---------------------- #
@register_type_data(UserType.PERSON)
class Person(NotionBaseModel):
    """Represents a person in Notion.

    Attributes:
        email: The email address of the person.

    References:
        https://developers.notion.com/reference/user#people
    """

    email: NotionEmail = Field(description="email address of the user")


class BotOwner(NotionTypedModel):
    """Represents a bot owner in Notion.

    Attributes:
        type: The type of the bot owner.
        type_data: The data related to this bot owner.

    References:
        https://developers.notion.com/reference/user#bots
    """

    type: BotOwnerType = Field(
        ..., description="Defines whether the bot owner is a 'workspace' or 'user'"
    )

    type_data: Optional[Literal[True]] = Field(
        default=None, description="Indicates if the bot belongs to a workspace"
    )

    register_type_data(BotOwnerType.WORKSPACE, Literal[True])


@register_type_data(UserType.BOT)
class Bot(NotionBaseModel):
    """Represents a bot in Notion.

    Attributes:
        owner: The owner of the bot.
        workspace_name: The name of the workspace if the bot belongs to a workspace.
    References:
        https://developers.notion.com/reference/user#bots
    """

    owner: BotOwner

    workspace_name: Optional[str] = Field(
        None, description="Workspace name if the bot belongs to a workspace"
    )

    @model_validator(mode="after")
    def validate_workspace_name(self):
        if self.owner.type == "workspace" and not self.workspace_name:
            raise ValueError(
                "workspace_name must be set when an owner. Type is 'workspace'."  # noqa
            )
        if self.owner.type == "user" and self.workspace_name is not None:
            raise ValueError(
                "workspace_name must be None when an owner. Type is 'user'."  # noqa
            )
        return self


class User(NotionTypedModel):
    """Represents a user in Notion.

    Attributes:
        object: Always 'user', ensuring consistency.
        id: Unique identifier for this user.
        type: Type of the user. Possible values are "person" and "bot".
        name: User's name, as displayed in Notion.
        avatar_url: Chosen avatar image.
        type_data: The user types specific data. Either a Person or a Bot.

    References:
        https://developers.notion.com/reference/user#all-users
    """

    object: ObjectType = Field(
        default=ObjectType.USER,
        description="Always 'user', ensuring consistency",
        frozen=True,
        init=False,
    )

    id: ObjectId = Field(..., description="Unique identifier for this user.")

    type: Optional[UserType] = Field(
        default=None,
        description='Type of the user. Possible values are "person" and "bot".',
    )

    name: Optional[str] = Field(
        default=None, description="User's name, as displayed in Notion."
    )

    avatar_url: Optional[NotionUrl] = Field(
        default=None, description="Chosen avatar image."
    )

    type_data: Optional[Union[Person, Bot]] = Field(
        default=None,
        description="The user types specific data. Either a Person or a Bot.",
    )

    if TYPE_CHECKING:
        type: Annotated[Optional[str, UserType], ...]

    @model_validator(mode="after")
    def validate_user_type(self):
        if self.type == "person" and not isinstance(self.type_data, Person):
            raise ValueError("A user of the type 'person' must have a 'person' field.")
        if self.type == "bot" and not isinstance(self.type_data, Bot):
            raise ValueError("A user of a type 'bot' must have a 'bot' field.")
        return self
