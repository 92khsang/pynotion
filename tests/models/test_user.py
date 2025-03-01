from typing import Optional
from uuid import uuid4

import pytest
from pydantic import ValidationError, BaseModel

from pynotion.models.types import ObjectId, NotionUrl, NotionEmail
from pynotion.models.user import UserType, BotOwnerType, Person, BotOwner, Bot, User
from tests.models.model_test_utils import PydanticModelTester


# ------------------ ENUM TESTS ------------------ #
@pytest.mark.parametrize(
    "user_type, expected_value",
    [
        (UserType.PERSON, "person"),
        (UserType.BOT, "bot"),
    ],
)
def test_user_type_enum(user_type, expected_value):
    """Test UserType enum values."""
    assert user_type.value == expected_value


@pytest.mark.parametrize(
    "bot_owner_type, expected_value",
    [
        (BotOwnerType.WORKSPACE, "workspace"),
        (BotOwnerType.USER, "user"),
    ],
)
def test_bot_owner_type_enum(bot_owner_type, expected_value):
    """Test BotOwnerType enum values."""
    assert bot_owner_type.value == expected_value


# ------------------ MODEL TESTS ------------------ #
@pytest.mark.parametrize(
    "sample_person",
    [
        Person(email="user@example.com"),
    ],
)
def test_person_model(sample_person):
    """Test Person model instantiation and validation."""
    assert sample_person.email == "user@example.com"


@pytest.mark.parametrize(
    "sample_bot_owner_workspace, sample_bot_owner_user",
    [
        (
            BotOwner(type=BotOwnerType.WORKSPACE, type_data=True),
            BotOwner(type=BotOwnerType.USER),
        ),
    ],
)
def test_bot_owner_model(sample_bot_owner_workspace, sample_bot_owner_user):
    """Test BotOwner model with both workspace and user types."""
    assert sample_bot_owner_workspace.type == BotOwnerType.WORKSPACE
    assert sample_bot_owner_workspace.type_data is True
    assert sample_bot_owner_user.type == BotOwnerType.USER
    assert sample_bot_owner_user.type_data is None


@pytest.mark.parametrize(
    "sample_bot, expected_values",
    [
        (
            Bot(
                owner=BotOwner(type=BotOwnerType.WORKSPACE, type_data=True),
                workspace_name="Test Workspace",
            ),
            ("workspace", "Test Workspace"),
        ),
        (
            Bot(
                owner=BotOwner(type=BotOwnerType.USER, type_data=None),
                workspace_name=None,
            ),
            ("user", None),
        ),
    ],
)
def test_bot_model_valid(sample_bot: Bot, expected_values: tuple):
    """Test valid Bot model instantiation."""
    assert sample_bot.owner.type == expected_values[0]
    assert sample_bot.workspace_name == expected_values[1]


@pytest.mark.parametrize(
    "owner_type, workspace_name, expected_error",
    [
        (
            BotOwnerType.WORKSPACE,
            None,
            "workspace_name must be set when an owner. Type is 'workspace'",
        ),
        (
            BotOwnerType.USER,
            "Invalid Workspace",
            "workspace_name must be None when an owner. Type is 'user'",
        ),
    ],
)
def test_bot_model_invalid_workspace_name(
    owner_type: BotOwnerType, workspace_name: Optional[str], expected_error: str
):
    """Test Bot model validation rules for workspace_name based on an owner type."""
    owner = BotOwner(
        type=owner_type,
        type_data=True if owner_type == BotOwnerType.WORKSPACE else None,
    )

    with pytest.raises(ValidationError, match=expected_error):
        Bot(owner=owner, workspace_name=workspace_name)


@pytest.mark.parametrize(
    "user_type, expected_error",
    [
        (
            UserType.PERSON,
            "A user of the type 'person' must have a 'person' field.",
        ),
        (UserType.BOT, "A user of a type 'bot' must have a 'bot' field."),
    ],
)
def test_user_model_without_data(user_type: UserType, expected_error):
    """Test User model validation rules for type and type_data consistency."""
    with pytest.raises(ValidationError, match=expected_error):
        User(
            id=ObjectId(str(uuid4())),
            type=user_type,
        )


@pytest.mark.parametrize(
    "object_id, user_type, name, avatar_url, type_data",
    [
        (
            ObjectId(str(uuid4())),
            UserType.PERSON,
            "Test User",
            "https://example.com/avatar.png",
            Person(email="user@example.com"),
        ),
        (
            ObjectId(str(uuid4())),
            UserType.BOT,
            "Test Bot",
            "https://example.com/bot.png",
            Bot(
                owner=BotOwner(type=BotOwnerType.WORKSPACE, type_data=True),
                workspace_name="Test Workspace",
            ),
        ),
        (
            ObjectId(str(uuid4())),
            None,
            None,
            None,
            None,
        ),
    ],
)
def test_user_model(object_id, user_type, name, avatar_url, type_data):
    """Test valid User model instantiation with the type 'person'."""
    user = User(
        id=object_id,
        type=user_type or None,
        name=name or None,
        avatar_url=avatar_url or None,
        type_data=type_data or None,
    )
    assert user.id == object_id
    assert user.type == user_type
    assert user.name == name
    assert user.avatar_url == avatar_url
    assert user.type_data == type_data
    assert isinstance(user.type_data, type(type_data))


@pytest.mark.parametrize(
    "clz, test_data",
    [
        (
            Person,
            [
                (
                    Person(email=NotionEmail("user@example.com")),
                    {"email": "user@example.com"},
                )
            ],
        ),
        (
            BotOwner,
            [
                (
                    BotOwner(type=BotOwnerType.WORKSPACE, type_data=True),
                    {"type": "workspace", "type_data": True},
                ),
                (
                    BotOwner(type=BotOwnerType.USER, type_data=None),
                    {"type": "user", "type_data": None},
                ),
            ],
        ),
        (
            Bot,
            [
                (
                    Bot(
                        owner=BotOwner(type=BotOwnerType.WORKSPACE, type_data=True),
                        workspace_name="Notion Workspace",
                    ),
                    {
                        "owner": {"type": "workspace", "type_data": True},
                        "workspace_name": "Notion Workspace",
                    },
                ),
            ],
        ),
        (
            User,
            [
                (
                    User(
                        id="d7db80bd-b3e3-4394-b134-a21b05412c7c",
                        type=UserType.PERSON,
                        name="Test User",
                        avatar_url=NotionUrl("https://example.com/avatar.png"),
                        type_data=Person(email="user@example.com"),
                    ),
                    {
                        "id": "d7db80bd-b3e3-4394-b134-a21b05412c7c",
                        "type": "person",
                        "name": "Test User",
                        "avatar_url": "https://example.com/avatar.png",
                        "person": {"email": "user@example.com"},
                    },
                ),
                (
                    User(
                        id=ObjectId("923ef3ea-cff1-423a-a5af-a24cfcb08f7c"),
                        type=UserType.BOT,
                        name="Test Bot",
                        avatar_url=NotionUrl("https://example.com/bot.png"),
                        type_data=Bot(
                            owner=BotOwner(type=BotOwnerType.WORKSPACE, type_data=True),
                            workspace_name="Bot Workspace",
                        ),
                    ),
                    {
                        "id": "923ef3ea-cff1-423a-a5af-a24cfcb08f7c",
                        "type": "bot",
                        "name": "Test Bot",
                        "avatar_url": "https://example.com/bot.png",
                        "bot": {
                            "owner": {"type": "workspace", "workspace": True},
                            "workspace_name": "Bot Workspace",
                        },
                    },
                ),
            ],
        ),
    ],
    ids=["Person", "BotOwner", "Bot", "User"],
)
def test_models_serialization(
    clz: type[BaseModel], test_data: list[tuple[BaseModel, dict]]
):
    """Test serialization and deserialization of models in user.py."""
    PydanticModelTester(clz, test_data).run_all_tests()
