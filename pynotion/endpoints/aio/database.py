from typing import Optional, TYPE_CHECKING

from pydantic import UUID4

from pynotion.client.aio import NotionAsyncClient
from pynotion.core.utils import dump_rx, dump_tx

if TYPE_CHECKING:
    from pynotion.models import (
        CreateDatabase,
        UpdateDatabase,
        PropertyFilter,
        NotionSort,
        PageOrDatabasePagination,
        TxPagination,
        RxDatabase,
    )


class DatabaseAsyncEndPoint:
    def __init__(self, client: NotionAsyncClient):
        self._client = client

    async def create_database(self, create_db_model: "CreateDatabase") -> "RxDatabase":
        """
        Creates a new database.

        Args:
            create_db_model: The model containing the database create details.

        Returns:
            RxDatabase: An object containing the created database information.
        """
        body = dump_tx(create_db_model)
        data = await self._client.post("/databases", body=body)
        return dump_rx("RxDatabase", data)

    async def query_databases(
        self,
        database_id: UUID4,
        property_filter: Optional["PropertyFilter"] = None,
        sort: Optional[list["NotionSort"]] = None,
        pagination: Optional["TxPagination"] = None,
    ) -> "PageOrDatabasePagination":
        """
        Queries the database with given filters and sorts.

        Args:
            database_id: The id of the database to query.
            property_filter: A list of filters to apply to the query.
            sort: A list of sorts to apply to the query.
            pagination: A pagination object to control the results.

        Returns:
            A PageOrDatabasePagination object containing the results of the query.
        """
        body = {}

        if property_filter:
            body["filter"] = dump_tx(property_filter)
        if sort:
            body["sorts"] = [dump_tx(s) for s in sort]
        if pagination:
            body.update(dump_tx(pagination))

        data = await self._client.post(f"/databases/{database_id}/query", body=body)
        return dump_rx("PageOrDatabasePagination", data)

    async def retrieve_database(self, database_id: UUID4) -> "RxDatabase":
        """
        Retrieves a database by its id.

        Args:
            database_id: The id of the database to retrieve.

        Returns:
            A RxDatabase object containing the database.
        """
        data = await self._client.get(f"/databases/{database_id}")
        return dump_rx("RxDatabase", data)

    async def update_database(
        self, database_id: UUID4, update_db_model: "UpdateDatabase"
    ) -> "RxDatabase":
        """
        Updates a database with the provided model.

        Args:
            database_id (UUID4): The ID of the database to update.
            update_db_model (UpdateDatabase): The model containing the update details.

        Returns:
            RxDatabase: An object containing the updated database information.
        """
        body = dump_tx(update_db_model)
        data = await self._client.patch(f"/databases/{database_id}", body=body)
        return dump_rx("RxDatabase", data)
