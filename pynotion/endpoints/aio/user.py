from typing import Optional, TYPE_CHECKING

from pydantic import UUID4

from pynotion.client.aio import NotionAsyncClient
from pynotion.core.utils import dump_rx, dump_tx
from pynotion.models.user import USER_CLASS_MAP

if TYPE_CHECKING:
    from pynotion.models import (
        UserPagination,
        NotionUser,
        BotUser,
        TxPagination,
    )


class UserAsyncEndPoint:
    def __init__(self, client: NotionAsyncClient):
        self._client = client

    async def list_all_users(
        self, pagination: Optional["TxPagination"] = None
    ) -> "UserPagination":
        """
        List all users.

        Args:
            pagination (TxPagination, optional): Pagination properties.

        Returns:
            UserPagination: Pagination of users.
        """
        params = dump_tx(pagination)
        data = await self._client.get("/users", params=params)
        return dump_rx("UserPagination", data)

    async def retrieve_user(self, user_id: UUID4) -> "NotionUser":
        """
        Retrieve a user.

        Args:
            user_id (UUID4): The ID of the user to retrieve.

        Returns:
            NotionUser: The retrieved user.
        """
        data = await self._client.get(f"/users/{user_id}")

        type_value = data.get("type", None)
        if type_value not in USER_CLASS_MAP:
            raise ValueError(f"Invalid type: {type_value}")

        return dump_rx(USER_CLASS_MAP[type_value], data)

    async def retrieve_your_token_bot_user(self) -> "BotUser":
        """
        Retrieve the bot user associated with the API token.

        Returns:
            BotUser: The bot user associated with the API token.
        """
        data = await self._client.get("/users/me")
        return dump_rx("BotUser", data)
