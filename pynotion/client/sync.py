from typing import Optional

import httpx

from pynotion.core.response import handle_response, handle_http_error
from .base import BaseClient
from .config import NotionClientConfig


class NotionSyncClient(BaseClient):
    def __init__(self, config: NotionClientConfig):
        super().__init__(config)
        self._client = httpx.Client(
            headers=self.build_headers(),
            timeout=httpx.Timeout(config.timeout_ms / 1000),
        )

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._client.close()

    def get(self, path: str, params: Optional[dict] = None) -> dict:
        return self._request("GET", path, params=params)

    def post(self, path: str, body: dict) -> dict:
        return self._request("POST", path, json=body)

    def patch(self, path: str, body: dict) -> dict:
        return self._request("PATCH", path, json=body)

    def delete(self, path: str, params: Optional[dict] = None) -> dict:
        return self._request("DELETE", path, params=params)

    def _request(self, method: str, path: str, **kwargs) -> Optional[dict]:
        try:
            response = self._client.request(method, self.build_url(path), **kwargs)
            return handle_response(response)
        except Exception as e:
            raise handle_http_error(e)
