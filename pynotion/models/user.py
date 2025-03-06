from __future__ import annotations as _annotations

from enum import StrEnum
from typing import Optional, Union, Literal, Any, Annotated

from pydantic import Field, model_validator, PrivateAttr, BeforeValidator

from ._internal import (
    BaseNotionModel,
    TypeObjectModel,
    validate_enum_value,
    validate_enum,
    ReadOnlyTypeObjectModel,
    validate_uuid4,
)
from .types import (
    NotionEmail,
    NotionUrl,
    ObjectType,
    ObjectId,
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
class Person(BaseNotionModel):
    """Represents a person in Notion.

    Attributes:
        email: The email address of the person.

    References:
        https://developers.notion.com/reference/user#people
    """

    email: NotionEmail = Field(description="email address of the user")


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
        Union[str, BotOwnerType],
        BeforeValidator(lambda v: validate_enum(v, (BotOwnerType,))),
        Field(frozen=True),
    ]

    type_object: Union[None, Literal[True]] = Field(
        default=None, description="Indicates if the bot belongs to a workspace"
    )


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

    workspace_name: Optional[str] = Field(
        None, description="Workspace name if the bot belongs to a workspace"
    )

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


class User(ReadOnlyTypeObjectModel):
    """Represents a user in Notion.

    Attributes:
        object: Always 'user', ensuring consistency.
        id: Unique identifier for this user.
        type: The type of the user (person or bot).
        name: The name of the user.
        url: The URL of the user's avatar.
        type_object: The data related to this user, either Person or Bot.

    References:
        https://developers.notion.com/reference/user#all-users
    """

    __serializable_private_attrs__ = {"_object": "object"}

    __type_object_map__ = {
        UserType.PERSON: Person,
        UserType.BOT: Bot,
    }

    _object: ObjectType = PrivateAttr(default=ObjectType.USER)

    read_only_id: Annotated[
        Union[None, ObjectId],
        BeforeValidator(lambda v: validate_uuid4(v) if v else v),
        Field(frozen=True),
    ] = None

    read_only_type: Annotated[
        Union[None, str, UserType],
        BeforeValidator(lambda v: validate_enum(v, (UserType,)) if v else v),
        Field(frozen=True),
    ] = None

    read_only_name: Optional[str] = Field(default=None, frozen=True)

    read_only_avatar_url: Optional[NotionUrl] = Field(default=None, frozen=True)

    read_only_type_object: Annotated[Union[None, Person, Bot], Field(frozen=True)] = (
        None
    )

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

    def __init__(self, **data: Any):
        """Initialize a User instance.

        Args:
            **data: Dictionary of attribute values to initialize the User with.
                May include 'object' which should be ObjectType.USER.

        Raises:
            ValueError: If 'object' is provided but not ObjectType.USER.
        """
        obj = data.pop("object", None) or ObjectType.USER
        obj = validate_enum_value(obj, {ObjectType.USER})

        super().__init__(**data)
        object.__setattr__(self, "_object", obj)

    @property
    def object(self) -> ObjectType:
        """The object type, always 'user'.

        Returns:
            ObjectType: Always ObjectType.USER.
        """
        return self._object

    @property
    def id(self) -> ObjectId:
        """The unique identifier for this user.

        Returns:
            ObjectId: The user's ID.
        """
        return self.read_only_id

    @property
    def name(self) -> Optional[str]:
        """The user's name.

        Returns:
            str: The user's name, or None if not available.
        """
        return self.read_only_name

    @property
    def avatar_url(self) -> Optional[NotionUrl]:
        """The URL of the user's avatar image.

        Returns:
            NotionUrl: The URL to the user's avatar, or None if not available.
        """
        return self.read_only_avatar_url

    @property
    def type(self) -> Union[UserType, None]:
        """The type of user (person or bot).

        Returns:
            UserType: The type of the user.
        """
        return self.read_only_type

    @property
    def type_object(self) -> Union[Person, Bot, None]:
        """The type-specific object for this user.

        Returns:
            Person or Bot: Additional data specific to this user type.
        """
        return self.read_only_type_object
