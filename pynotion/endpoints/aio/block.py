from typing import Optional, TYPE_CHECKING

from pydantic import UUID4

from pynotion.client.aio import NotionAsyncClient
from pynotion.core.utils import dump_rx, dump_tx
from pynotion.models.block.rx import RX_BLOCK_CLASS_MAP

if TYPE_CHECKING:
    from pynotion.models import TxBlock, RxBlock, BlockPagination, TxPagination


class BlockAsyncEndPoint:
    def __init__(self, client: NotionAsyncClient):
        self._client = client

    @staticmethod
    def _dump_rx_block(data: dict) -> "RxBlock":
        type_value = data.get("type")
        if type_value not in RX_BLOCK_CLASS_MAP:
            raise ValueError(f"Invalid type: {type_value}")
        return dump_rx(RX_BLOCK_CLASS_MAP[type_value], data)

    async def append_block_children(
        self,
        parent_id: UUID4,
        children: list["TxBlock"],
        after: Optional[UUID4] = None,
    ) -> "BlockPagination":
        """
        Appends a new block to a page or database.

        Args:
            parent_id: The ID of the parent page or database.
            children: A list of blocks to append.
            after: The ID of the block after which to insert the new blocks.

        Returns:
            A `BlockPagination` object containing the IDs of the new blocks.
        """
        body = {"children": [dump_tx(child) for child in children]}
        if after:
            body["after"] = str(after)

        url = f"/blocks/{parent_id}/children"
        data = await self._client.patch(url, body=body)
        return dump_rx("BlockPagination", data)

    async def retrieve_block(self, block_id: UUID4) -> "RxBlock":
        """
        Retrieves a block by its ID.

        Args:
            block_id (UUID4): The ID of the block to retrieve.

        Returns:
            RxBlock: The block object associated with the given ID.
        """
        data = await self._client.get(f"/blocks/{block_id}")
        return self._dump_rx_block(data)

    async def retrieve_block_children(
        self, block_id: UUID4, pagination: Optional["TxPagination"] = None
    ) -> "BlockPagination":
        """
        Retrieves a list of blocks from a page or database.

        Args:
            block_id (UUID4): The ID of the page or database.
            pagination (TxPagination): The pagination parameters.

        Returns:
            BlockPagination: The pagination object containing the IDs of the blocks.
        """
        params = dump_tx(pagination)
        data = await self._client.get(f"/blocks/{block_id}/children", params=params)
        return dump_rx("BlockPagination", data)

    async def update_block(self, block_id: UUID4, block: "TxBlock") -> "RxBlock":
        """
        Updates a block by its ID.

        Args:
            block_id (UUID4): The ID of the block to update.
            block (TxBlock): The block object with updated properties.

        Returns:
            RxBlock: The updated block object associated with the given ID.

        Raises:
            ValueError: If the block object contains children.
        """

        if getattr(block, "children", None):
            raise ValueError("Cannot update children by update_block")

        body = dump_tx(block)
        data = await self._client.patch(f"/blocks/{block_id}", body=body)
        return self._dump_rx_block(data)

    async def delete_block(self, block_id: UUID4) -> "RxBlock":
        """
        Deletes a block by its ID.

        Args:
            block_id (UUID4): The ID of the block to delete.

        Returns:
            RxBlock: The deleted block object associated with the given ID.
        """
        data = await self._client.delete(f"/blocks/{block_id}")
        return self._dump_rx_block(data)

    async def restore_block(self, block_id: UUID4) -> "RxBlock":
        """
        Restores a block by its ID.

        Args:
            block_id (UUID4): The ID of the block to restore.

        Returns:
            RxBlock: The restored block object associated with the given ID.
        """
        body = {"archived": False}
        data = await self._client.patch(f"/blocks/{block_id}", body=body)
        return self._dump_rx_block(data)
