from typing import Optional, TYPE_CHECKING

from pynotion.client.aio import NotionAsyncClient
from pynotion.core.utils import dump_rx, dump_tx

if TYPE_CHECKING:
    from pynotion.models import (
        TxPagination,
        TimestampSort,
        ObjectFilter,
        PageOrDatabasePagination,
    )


class SearchAsyncEndPoint:
    def __init__(self, client: NotionAsyncClient):
        self._client = client

    async def search(
        self,
        query: Optional[str] = None,
        sort: Optional["TimestampSort"] = None,
        object_filter: Optional["ObjectFilter"] = None,
        pagination: Optional["TxPagination"] = None,
    ) -> "PageOrDatabasePagination":
        """Searches Notion pages and databases.

        Args:
            query (Optional[str], optional): The query string. Defaults to None.
            sort (Optional[TimestampSort], optional): The sort order. Defaults to None.
            object_filter (Optional[ObjectFilter], optional): The object filter. Defaults to None.
            pagination (Optional[TxPagination], optional): The pagination. Defaults to None.

        Returns:
            PageOrDatabasePagination: The search result.
        """
        body = {}

        if query:
            body["query"] = query
        if object_filter:
            body["filter"] = dump_tx(object_filter)
        if sort:
            body["sort"] = dump_tx(sort)
        if pagination:
            body.update(**dump_tx(pagination))

        data = await self._client.post("/search", body=body)
        return dump_rx("PageOrDatabasePagination", data)
