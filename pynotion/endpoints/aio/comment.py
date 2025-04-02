from typing import Optional, Union, TYPE_CHECKING

from pydantic import UUID4

from pynotion.client.aio import NotionAsyncClient
from pynotion.core.utils import dump_rx, dump_tx

if TYPE_CHECKING:
    from pynotion.models import (
        TxPagination,
        RxComment,
        CommentPagination,
        TxCommentWithParent,
        TxCommentWithDiscussionId,
    )


class CommentAsyncEndPoint:
    def __init__(self, client: NotionAsyncClient):
        self._client = client

    async def create_comment(
        self, comment: Union["TxCommentWithDiscussionId", "TxCommentWithParent"]
    ) -> "RxComment":
        """
        Creates a new comment on a block.

        Args:
            comment: The comment to be created. It must contain either a `parent` or
                a `discussion_id`.

        Returns:
            The newly created comment.
        """
        body = dump_tx(comment)
        data = await self._client.post("/comments", body=body)
        return dump_rx("RxComment", data)

    async def retrieve_comments(
        self, block_id: UUID4, pagination: Optional["TxPagination"]
    ) -> "CommentPagination":
        """
        Retrieves comments for a specified block.

        Args:
            block_id (UUID4): The unique identifier of the block.
            pagination (Optional[TxPagination]): Pagination parameters for the request.

        Returns:
            CommentPagination: Paginated list of comments for the specified block.
        """
        params = {"block_id": block_id, **(dump_tx(pagination) or {})}
        data = await self._client.get(f"/comments", params=params)
        return dump_rx("CommentPagination", data)
