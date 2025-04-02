from functools import cached_property
from typing import TYPE_CHECKING, Union, Any, Self

from pynotion.client.config import NotionClientConfig

if TYPE_CHECKING:
    from pynotion.client.aio import NotionAsyncClient
    from pynotion.client.sync import NotionSyncClient

    from pynotion.endpoints.sync.user import UserSyncEndPoint
    from pynotion.endpoints.sync.page import PageSyncEndPoint
    from pynotion.endpoints.sync.block import BlockSyncEndPoint
    from pynotion.endpoints.sync.comment import CommentSyncEndPoint
    from pynotion.endpoints.sync.search import SearchSyncEndPoint
    from pynotion.endpoints.sync.database import DatabaseSyncEndPoint

    from pynotion.endpoints.aio.user import UserAsyncEndPoint
    from pynotion.endpoints.aio.page import PageAsyncEndPoint
    from pynotion.endpoints.aio.block import BlockAsyncEndPoint
    from pynotion.endpoints.aio.comment import CommentAsyncEndPoint
    from pynotion.endpoints.aio.search import SearchAsyncEndPoint
    from pynotion.endpoints.aio.database import DatabaseAsyncEndPoint


__all__ = ["PyNotion"]


class PyNotion:
    if TYPE_CHECKING:
        _config: "NotionClientConfig"
        _client: Union["NotionSyncClient", "NotionAsyncClient"]
        _async: bool

    def __init__(
        self,
        token: str,
        *,
        async_mode: bool = False,
        base_url: str = "https://api.notion.com/v1",
        version: str = "2022-06-28",
        timeout_ms: int = 60_000,
    ):
        self._config = NotionClientConfig(
            token=token, base_url=base_url, version=version, timeout_ms=timeout_ms
        )
        self._async = async_mode
        if self._async:
            from pynotion.client.aio import NotionAsyncClient

            self._client = NotionAsyncClient(self._config)
        else:
            from pynotion.client.sync import NotionSyncClient

            self._client = NotionSyncClient(self._config)

    def _get_endpoint(self, name: str):
        """
        Factory method to create endpoint instances based on name and mode.

        Args:
            name: The endpoint name (without 'EndPoint' suffix)

        Returns:
            An instance of the appropriate endpoint class
        """
        module_prefix = "pynotion.endpoints."
        module_suffix = f"{name.lower()}"
        class_prefix = name.capitalize()

        if self._async:
            module_path = f"{module_prefix}aio.{module_suffix}"
            class_name = f"{class_prefix}AsyncEndPoint"
        else:
            module_path = f"{module_prefix}sync.{module_suffix}"
            class_name = f"{class_prefix}SyncEndPoint"

        # Import the endpoint module dynamically
        module = __import__(module_path, fromlist=[class_name])
        endpoint_class = getattr(module, class_name)
        return endpoint_class(self._client)

    @cached_property
    def users(self) -> Union["UserAsyncEndPoint", "UserSyncEndPoint"]:
        """User endpoint for Notion API."""
        return self._get_endpoint("user")

    @cached_property
    def pages(self) -> Union["PageAsyncEndPoint", "PageSyncEndPoint"]:
        """Page endpoint for Notion API."""
        return self._get_endpoint("page")

    @cached_property
    def blocks(self) -> Union["BlockAsyncEndPoint", "BlockSyncEndPoint"]:
        """Block endpoint for Notion API."""
        return self._get_endpoint("block")

    @cached_property
    def comments(self) -> Union["CommentAsyncEndPoint", "CommentSyncEndPoint"]:
        """Comment endpoint for Notion API."""
        return self._get_endpoint("comment")

    @cached_property
    def search(self) -> Union["SearchAsyncEndPoint", "SearchSyncEndPoint"]:
        """Search endpoint for Notion API."""
        return self._get_endpoint("search")

    @cached_property
    def databases(self) -> Union["DatabaseAsyncEndPoint", "DatabaseSyncEndPoint"]:
        """Database endpoint for Notion API."""
        return self._get_endpoint("database")

    def close(self):
        """Close the synchronous client connection."""
        if hasattr(self._client, "close"):
            self._client.close()

    async def aclose(self) -> None:
        """Close the asynchronous client connection."""
        if hasattr(self._client, "aclose"):
            await self._client.aclose()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.aclose()
