from __future__ import annotations as _annotations

from enum import StrEnum
from typing import Literal, Annotated, TypeAlias

from pydantic import Field, model_validator, BeforeValidator

from ._internal import (
    BaseNotionModel,
    TypeObjectModel,
    validate_enum,
)
from .types import (
    NotionEmail as _NotionEmail,
    NotionUrl as _NotionUrl,
    NotionObjectId as _NotionObjectId,
)


# ---------------------- ENUMS ---------------------- #
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
UserId: TypeAlias = _NotionObjectId
PersonEmail: TypeAlias = _NotionEmail
AvatarUrl: TypeAlias = _NotionUrl


class Person(BaseNotionModel):
    """Represents a person in Notion.

    Attributes:
        email: The email address of the person.

    References:
        https://developers.notion.com/reference/user#people
    """

    email: PersonEmail


class BotOwner(TypeObjectModel):
    """Represents a bot owner in Notion.

    Attributes:
        type: The type of the bot owner (workspace or user).
        type_object: The data related to this bot owner. True for workspace,
            None for user.

    References:
        https://developers.notion.com/reference/user#bots
    """

    __type_object_map__ = {
        BotOwnerType.WORKSPACE: Literal[True],
        BotOwnerType.USER: None,
    }

    type: Annotated[
        str | BotOwnerType,
        BeforeValidator(lambda v: validate_enum(v, (BotOwnerType,))),
        Field(frozen=True),
    ]

    type_object: Literal[True] | None = Field(default=None, frozen=True)


class Bot(BaseNotionModel):
    """Represents a bot in Notion.

    Attributes:
        owner: The owner of the bot.
        workspace_name: The name of the workspace if the bot belongs to a workspace.
            Required when owner type is workspace, must be None when owner type is user.

    References:
        https://developers.notion.com/reference/user#bots
    """

    owner: BotOwner

    workspace_name: str | None = Field(default=None)

    @model_validator(mode="after")
    def validate_workspace_name(self):
        """Validates workspace_name based on owner type.

        Raises:
            ValueError: If workspace_name is missing for workspace owner
                or present for user owner.

        Returns:
            Bot: The validated Bot instance.
        """
        if self.owner.type == "workspace" and not self.workspace_name:
            raise ValueError(
                "workspace_name must be set when an owner. Type is 'workspace'."  # noqa
            )
        if self.owner.type == "user" and self.workspace_name is not None:
            raise ValueError(
                "workspace_name must be None when an owner. Type is 'user'."  # noqa
            )
        return self


class User(TypeObjectModel):
    """Represents a user in Notion.

    Attributes:
        object: Always 'user', ensuring consistency.
        id: Unique identifier for this user.
        type: The type of the user (person or bot).
        name: The name of the user.
        avatar_url: The URL of the user's avatar.
        type_object: The data related to this user, either Person or Bot.

    References:
        https://developers.notion.com/reference/user#all-users
    """

    __type_object_map__ = {
        UserType.PERSON: Person,
        UserType.BOT: Bot,
    }

    object: Literal["user"] = Field(frozen=True)

    id: UserId = Field(frozen=True)

    type: (
        Annotated[
            str | UserType, BeforeValidator(lambda v: validate_enum(v, (UserType,)))
        ]
        | None
    ) = Field(frozen=True)

    name: str | None = Field(frozen=True)

    avatar_url: AvatarUrl | None = Field(frozen=True)

    type_object: Person | Bot | None = Field(frozen=True)

    @model_validator(mode="after")
    def validate_user_type(self):
        """Validates that type_object matches the specified user type.

        Raises:
            ValueError: If the type_object doesn't match the expected type.

        Returns:
            User: The validated User instance.
        """
        if self.type == "person" and not isinstance(self.type_object, Person):
            raise ValueError("A user of the type 'person' must have a 'person' field.")
        if self.type == "bot" and not isinstance(self.type_object, Bot):
            raise ValueError("A user of a type 'bot' must have a 'bot' field.")
        return self


User: TypeAlias = User
