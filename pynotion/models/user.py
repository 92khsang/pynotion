from enum import Enum
from typing import Literal, Annotated, Optional

from pydantic import (
    Field,
    model_validator,
    Discriminator,
    Tag,
    BeforeValidator,
)

from ._internal import (
    BaseNotionModel,
    validate_url,
    validate_email,
)
from .object import (
    NotionObjectType,
    NotionObjectId,
)


class UserType(str, Enum):
    """Defined user types in Notion.

    Attributes:
        PERSON: represents a user type for a person.
        BOT: represents a user type for a bot.

    References:
        https://developers.notion.com/reference/user#all-users
    """

    PERSON = "person"
    BOT = "bot"


class BotOwnerType(str, Enum):
    """Defined bot owner types in Notion.

    Attributes:
        WORKSPACE: represents a bot owner type for a workspace.
        USER: represents a bot owner type for an individual user.

    References:
        https://developers.notion.com/reference/user#bots
    """

    WORKSPACE = "workspace"
    USER = "user"


class WorkspaceBotOwner(BaseNotionModel):
    type: Literal[BotOwnerType.WORKSPACE] = Field(
        default=BotOwnerType.WORKSPACE, frozen=True
    )
    workspace: Literal[True] = Field(default=True, frozen=True)


class UserBotOwner(BaseNotionModel):
    type: Literal[BotOwnerType.USER] = Field(default=BotOwnerType.USER, frozen=True)


BotOwner = Annotated[
    WorkspaceBotOwner | UserBotOwner,
    Field(discriminator="type"),
]


class Person(BaseNotionModel):
    """Represents a person in Notion.

    Attributes:
        email: The email address of the person.

    References:
        https://developers.notion.com/reference/user#people
    """

    email: Annotated[str, BeforeValidator(validate_email)]


class Bot(BaseNotionModel):
    """Represents a bot in Notion.

    Attributes:
        owner: The owner of the bot.
        workspace_name: The name of the workspace if the bot belongs to a workspace.

    References:
        https://developers.notion.com/reference/user#bots
    """

    owner: Optional[BotOwner] = None

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
    Represents a minimal user reference when a full User object isn't needed.

    This is often used in created_by and last_edited_by fields.

    Attributes:
        id: Unique identifier for the user.
        object: Always 'user', confirming this is a user reference.
    """

    object: Literal[NotionObjectType.USER] = Field(
        default=NotionObjectType.USER, frozen=True
    )
    id: NotionObjectId = Field(frozen=True)


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
    person: Person


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
    bot: Bot


def model_user_discriminator(v):
    from ._internal.utils import get_value_for_discriminator

    type_value = get_value_for_discriminator(v, "type")

    match type_value:
        case None:
            return "ref"
        case UserType.PERSON:
            return "person"
        case UserType.BOT:
            return "bot"

    raise ValueError(f"Unknown user type: {v}")


User = Annotated[
    (
        Annotated[UserRef, Tag("ref")]
        | Annotated[PersonUser, Tag("person")]
        | Annotated[BotUser, Tag("bot")]
    ),
    Discriminator(model_user_discriminator),
]
