from uuid import uuid4

import pytest
from pydantic import ValidationError, BaseModel, UUID4

from pynotion.models.user import *
from tests.models.model_test_utils import (
    PydanticModelTester,
    DiscriminatedModelTester,
)


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
            WorkspaceBotOwner(),
            UserBotOwner(),
        ),
    ],
)
def test_bot_owner_model(sample_bot_owner_workspace, sample_bot_owner_user):
    """Test BotOwner model with both workspace and user types."""
    assert sample_bot_owner_workspace.type == BotOwnerType.WORKSPACE
    assert sample_bot_owner_workspace.workspace is True
    assert sample_bot_owner_user.type == BotOwnerType.USER


def test_notion_user_ref():
    with pytest.raises(
        ValueError, match=r"Input should be <NotionObjectType.USER: 'user'>"
    ):
        UserRef(object=NotionObjectType.PAGE, id=uuid4())

    valid_user_ref = UserRef(object="user", id=uuid4())
    assert valid_user_ref.object == "user"


@pytest.mark.parametrize(
    "sample_bot, expected_values",
    [
        (
            Bot(
                owner=WorkspaceBotOwner(),
                workspace_name="Test Workspace",
            ),
            ("workspace", "Test Workspace"),
        ),
        (
            Bot(
                owner=UserBotOwner(),
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
    owner_type: BotOwnerType, workspace_name: str | None, expected_error: str
):
    class TestModel(BaseModel):
        owner: BotOwner

    test_model = TestModel(**{"owner": {"type": owner_type.value}})

    with pytest.raises(ValidationError, match=expected_error):
        Bot(owner=test_model.owner, workspace_name=workspace_name)


@pytest.mark.parametrize(
    "clz, user_type, expected_error",
    [
        (
            PersonUser,
            UserType.PERSON,
            "Input should be a valid dictionary or instance of Person",
        ),
        (
            BotUser,
            UserType.BOT,
            "Input should be a valid dictionary or instance of Bot",
        ),
    ],
)
def test_user_model_without_data(clz, user_type: UserType, expected_error):
    """Test User model validation rules for type and type_object consistency."""
    with pytest.raises(ValidationError, match=expected_error):
        clz(
            object="user",
            id=str(uuid4()),
            type=user_type,
            name="Test User",
            avatar_url="https://example.com/avatar.png",
            **{user_type.value: None},
        )


@pytest.mark.parametrize(
    "annotated_clz, expected_clz, input_data",
    [
        (
            User,
            UserRef,
            {
                "object": "user",
                "id": str(uuid4()),
            },
        ),
        (
            User,
            PersonUser,
            {
                "object": "user",
                "id": str(uuid4()),
                "type": UserType.PERSON,
                "name": "Test User",
                "avatar_url": "https://example.com/avatar.png",
                "person": Person(email="user@example.com"),
            },
        ),
        (
            User,
            BotUser,
            {
                "object": "user",
                "id": str(uuid4()),
                "type": UserType.BOT,
                "name": "Test Bot",
                "avatar_url": "https://example.com/bot.png",
                "bot": Bot(
                    owner=WorkspaceBotOwner(),
                    workspace_name="Test Workspace",
                ),
            },
        ),
    ],
)
def test_discriminated_model(annotated_clz: type, expected_clz: type, input_data: dict):
    """Test valid User model instantiation with the type 'person' or 'bot'."""
    DiscriminatedModelTester(annotated_clz, expected_clz, **input_data).run_all_tests()


@pytest.mark.parametrize(
    "clz, input_dict, expected_dict, expected_json",
    [
        (
            Person,
            {"email": "user@example.com"},
            {"email": "user@example.com"},
            {"email": "user@example.com"},
        ),
        (
            WorkspaceBotOwner,
            {"type": "workspace", "workspace": True},
            {"type": BotOwnerType.WORKSPACE, "workspace": True},
            {"type": "workspace", "workspace": True},
        ),
        (
            UserBotOwner,
            {"type": "user"},
            {"type": BotOwnerType.USER},
            {"type": "user"},
        ),
        (
            Bot,
            {
                "owner": {"type": "workspace", "workspace": True},
                "workspace_name": "Notion Workspace",
            },
            {
                "owner": {"type": BotOwnerType.WORKSPACE, "workspace": True},
                "workspace_name": "Notion Workspace",
            },
            {
                "owner": {"type": "workspace", "workspace": True},
                "workspace_name": "Notion Workspace",
            },
        ),
        (
            UserRef,
            {
                "object": "user",
                "id": "d7db80bd-b3e3-4394-b134-a21b05412c7c",
            },
            {
                "object": "user",
                "id": UUID4("d7db80bd-b3e3-4394-b134-a21b05412c7c"),
            },
            {
                "object": "user",
                "id": "d7db80bd-b3e3-4394-b134-a21b05412c7c",
            },
        ),
        (
            PersonUser,
            {
                "object": "user",
                "id": "d7db80bd-b3e3-4394-b134-a21b05412c7c",
                "type": "person",
                "name": "Test User",
                "avatar_url": "https://example.com/avatar.png",
                "person": {"email": "user@example.com"},
            },
            {
                "object": "user",
                "id": UUID4("d7db80bd-b3e3-4394-b134-a21b05412c7c"),
                "type": UserType.PERSON,
                "name": "Test User",
                "avatar_url": "https://example.com/avatar.png",
                "person": {"email": "user@example.com"},
            },
            {
                "object": "user",
                "id": "d7db80bd-b3e3-4394-b134-a21b05412c7c",
                "type": "person",
                "name": "Test User",
                "avatar_url": "https://example.com/avatar.png",
                "person": {"email": "user@example.com"},
            },
        ),
        (
            BotUser,
            {
                "object": "user",
                "id": "923ef3ea-cff1-423a-a5af-a24cfcb08f7c",
                "type": "bot",
                "name": "Test Bot",
                "avatar_url": "https://example.com/bot.png",
                "bot": {
                    "owner": {"type": "workspace", "workspace": True},
                    "workspace_name": "Bot Workspace",
                },
            },
            {
                "object": "user",
                "id": UUID4("923ef3ea-cff1-423a-a5af-a24cfcb08f7c"),
                "type": UserType.BOT,
                "name": "Test Bot",
                "avatar_url": "https://example.com/bot.png",
                "bot": {
                    "owner": {"type": BotOwnerType.WORKSPACE, "workspace": True},
                    "workspace_name": "Bot Workspace",
                },
            },
            {
                "object": "user",
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
)
def test_models_serialization(
    clz: type[BaseModel], input_dict: dict, expected_dict: dict, expected_json: dict
):
    """Test serialization and deserialization of models in user.py."""
    PydanticModelTester(clz, (input_dict, expected_dict, expected_json)).run_all_tests()
