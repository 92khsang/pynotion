from enum import Enum
from typing import Literal, Annotated, Optional, Union, TYPE_CHECKING
from uuid import UUID

from pydantic import (
    Field,
    model_validator,
    BeforeValidator,
)

from pynotion.models.object import NotionObjectType
from ._internal import (
    BaseNotionModel,
    validate_url,
    validate_email,
)
from ._internal.utils import discriminate_field

__all__ = [
    "UserType",
    "BotOwnerType",
    "WorkspaceBotOwner",
    "UserBotOwner",
    "Bot",
    "Person",
    "PersonUser",
    "BotUser",
    "UserRef",
    "BotOwner",
    "NotionUser",
    "BOT_OWNER_CLASS_MAP",
    "USER_CLASS_MAP",
]


class UserType(str, Enum):
    """Defined user types in Notion."""

    PERSON = "person"
    BOT = "bot"


class BotOwnerType(str, Enum):
    """Defined bot owner types in Notion."""

    WORKSPACE = "workspace"
    USER = "user"


class WorkspaceBotOwner(BaseNotionModel):
    """Represents a bot owner for a workspace in Notion.

    Attributes:
        type: Always "workspace".
        workspace: Always True
    """

    type: Literal[BotOwnerType.WORKSPACE] = Field(
        default=BotOwnerType.WORKSPACE, frozen=True
    )
    workspace: Literal[True] = Field(default=True, frozen=True)


class UserBotOwner(BaseNotionModel):
    """Represents a bot owner for a user in Notion.

    Attributes:
        type: Always "user".
    """

    type: Literal[BotOwnerType.USER] = Field(default=BotOwnerType.USER, frozen=True)


BOT_OWNER_CLASS_MAP: dict[str, str] = {
    BotOwnerType.WORKSPACE: "WorkspaceBotOwner",
    BotOwnerType.USER: "UserBotOwner",
}


BotOwner = Annotated[
    Union[tuple(BOT_OWNER_CLASS_MAP.values())],
    BeforeValidator(lambda v: discriminate_field(v, "type", BOT_OWNER_CLASS_MAP)),
]


class Person(BaseNotionModel):
    """Represents a person in Notion.

    Attributes:
        email: The email address of the person.
    """

    email: Annotated[str, BeforeValidator(validate_email)]


class Bot(BaseNotionModel):
    """Represents a bot in Notion.

    Attributes:
        owner: The owner of the bot.
        workspace_name: The name of the workspace if the bot belongs to a workspace.
    """

    owner: Union[None, BotOwner] = None
    workspace_name: Optional[str] = None

    @model_validator(mode="after")
    def validate_workspace_name(self):
        """Validates workspace_name based on an owner type.

        Raises:
            ValueError: If workspace_name is missing for a workspace owner
                or present for a user owner.

        Returns:
            Bot: The validated Bot instance.
        """
        if self.owner is None:
            return self

        if self.owner.type == "workspace" and not self.workspace_name:
            raise ValueError(
                "workspace_name must be set when an owner. Type is 'workspace'."  # noqa
            )
        if self.owner.type == "user" and self.workspace_name is not None:
            raise ValueError(
                "workspace_name must be None when an owner. Type is 'user'."  # noqa
            )
        return self


class UserRef(BaseNotionModel):
    """
    Represents a minimal user reference when a full NotionUser object isn't needed.

    This is often used in created_by and last_edited_by fields.

    Attributes:
        id: Unique identifier for the user.
        object: Always 'user', confirming this is a user reference.
    """

    object: Literal[NotionObjectType.USER] = Field(
        default=NotionObjectType.USER, frozen=True
    )
    id: UUID


class _BaseUser(UserRef):
    name: Optional[str] = None
    avatar_url: Optional[Annotated[str, BeforeValidator(validate_url)]] = Field(
        default=None
    )


class PersonUser(_BaseUser):
    """Represents a person user in Notion.

    Attributes:
        object: Always 'user', confirming this is a person user.
        id: Unique identifier for the person user.
        type: Always 'person', confirming this is a person user.
        person: The person associated with the person user.
        name: The name of the person.
        avatar_url: The URL of the avatar image of the person.
    """

    type: Literal[UserType.PERSON] = Field(default=UserType.PERSON)
    person: "Person"


class BotUser(_BaseUser):
    """Represents a bot user in Notion.

    Attributes:
        object: Always 'user', confirming this is a bot user.
        id: Unique identifier for the bot user.
        type: Always 'bot', confirming this is a bot user.
        bot: The bot associated with the bot user.
        name: The name of the bot.
        avatar_url: The URL of the avatar image of the bot.
    """

    type: Literal[UserType.BOT] = Field(default=UserType.BOT)
    bot: "Bot"


USER_CLASS_MAP: dict[Optional[str], str] = {
    UserType.PERSON: "PersonUser",
    UserType.BOT: "BotUser",
    None: "UserRef",
}

if not TYPE_CHECKING:
    NotionUser = Annotated[
        Union[tuple(USER_CLASS_MAP.values())],
        BeforeValidator(lambda v: discriminate_field(v, "type", USER_CLASS_MAP)),
    ]
else:
    NotionUser = Union[PersonUser, BotUser, UserRef]
