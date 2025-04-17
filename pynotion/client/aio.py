from typing import Optional

import httpx

from pynotion.core.response import handle_response, handle_http_error
from .base import BaseClient
from .config import NotionClientConfig


class NotionAsyncClient(BaseClient):
    def __init__(self, config: NotionClientConfig):
        super().__init__(config)
        self._client = httpx.AsyncClient(
            headers=self.build_headers(),
            timeout=httpx.Timeout(config.timeout_ms / 1000),
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self._client.aclose()

    async def get(self, path: str, params: Optional[dict] = None) -> dict:
        return await self._request("GET", path, params=params)

    async def post(self, path: str, body: dict) -> dict:
        return await self._request("POST", path, json=body)

    async def patch(self, path: str, body: dict) -> dict:
        return await self._request("PATCH", path, json=body)

    async def delete(self, path: str, params: Optional[dict] = None) -> dict:
        return await self._request("DELETE", path, params=params)

    async def _request(self, method: str, path: str, **kwargs) -> Optional[dict]:
        try:
            response = await self._client.request(
                method, self.build_url(path), **kwargs
            )
            return handle_response(response)
        except Exception as e:
            raise handle_http_error(e)
